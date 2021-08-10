"""
Yuda Munarko
26 July 2021
"""

from .notifyme_utils import add_new_single_entry
import os
import requests
from sanic.response import json, html

# loading api_key from environment
api_key = os.getenv('ES_API_KEY', None)


def loadMain():
    """
    Loading main page of the web server.
    """
    fileName = os.path.join(os.path.dirname(__file__), 'main.html')
    try:
        f = open(fileName, "r")
        htmlText = f.read()
        f.close()
    except:
        return html("We are sorry,there was an error ..., %s is not found" % fileName)
    return html(htmlText)


def __find(element, JSON):
    """
    To find the content in elasticsearch's hits based on path in element.
    Arguments:
        - element: a path to the content, e.g. _source.item.keywords.keyword
        - JSON: a dictionary as a result of elasticsearch query
    """
    try:
        paths = element.split(".")
        data = JSON
        for count, p in enumerate(paths):
            if isinstance(data[p], dict):
                data = data[p]
            elif isinstance(data[p], list):
                data = [__find(element[element.find(p)+len(p)+1:], lst)
                        for lst in data[p]]
                break
            elif len(paths)-1 == count:
                return data[p]
        if [] in data:
            data.remove([])
        return data
    except:
        return []


def getSearch(request):
    """
    To search datasets based on query
        - see search(request) in server.py
    """
    # initialise query run
    summary = {}
    url = 'https://scicrunch.org/api/1/elastic/SPARC_PortalDatasets_pr/_search?api_key='+api_key
    size = '200'
    includes = ["item.keywords.keyword",
                "item.name",
                "item.readme.description",
                "item.description",
                "pennsieve.firstPublishedAt.timestamp",
                "pennsieve.updatedAt.timestamp",
                "pennsieve.banner.uri",
                "pennsieve.identifier",
                "contributors.last.name",
                "contributors.first.name",
                "item.statistics.samples.count",
                "item.statistics.subjects.count",
                "anatomy.organ.name",
                "organisms.primary.species.originalName",
                "item.published.boolean",
                "item.techniques.keyword",
                ]
    query = {
        "size": size,
        "from": 0,
        "_source": {
            "includes": includes
        },
        "highlight": {
            "fields": {
                "item.name": {},
                "item.description": {},
                "item.readme.description": {},
            }
        },
    }
    if 'query' in request.args:
        # get argument values
        q = request.args['query'][0]
        force = 'no' if 'force' not in request.args else request.args['force'][0]
        match = 'no' if 'match' not in request.args else request.args['match'][0]
        summary['force'] = force
        summary['match'] = match
        summary['query'] = q
        summary['executed'] = q
        summary['suggestions'] = __getSuggestions(q, 10)
        query['query'] = {"query_string": {"query": q}}
        if force != 'yes' and len(summary['suggestions']) > 0:
            query['query']['query_string']['query'] = summary['suggestions'][0]
            summary['executed'] = summary['suggestions'][0]
        if match == 'yes':
            query['query']['query_string']['query'] = '\"' + \
                query['query']['query_string']['query'] + '\"'

    response = requests.post(url, json=query)
    summary['total'] = response.json()['hits']['total']
    summary['filters'] = {'keywords': {}, 'authors': {},
                          'status': {'public': [], 'embargoed': []}}
    summary['sorts'] = {'ranking': [], 'date': []}
    summary['hits'] = {}
    dates, srtDates, names, srtNames = [], [], [], []
    for hit in response.json()['hits']['hits']:
        idx = __find('_source.pennsieve.identifier', hit)
        if idx == []:
            idx = 'dummy_' + str(len(summary['hits']))  # embargo and none

        # extract filters
        ## extract from keywords
        for keyword in __find('_source.item.keywords.keyword', hit):
            if keyword not in summary['filters']['keywords']:
                summary['filters']['keywords'][keyword] = []
            summary['filters']['keywords'][keyword] += [idx]
        ## extract from contributors
        firsts = __find('_source.contributors.first.name', hit)
        lasts = __find('_source.contributors.last.name', hit)
        for name in [first+' '+last for first, last in (zip(firsts, lasts))]:
            if name not in summary['filters']['authors']:
                summary['filters']['authors'][name] = []
            summary['filters']['authors'][name] += [idx]
        ## extract status (public|embargoed)
        if idx.startswith('dummy'):
            summary['filters']['status']['embargoed'] += [idx]
        else:
            summary['filters']['status']['public'] += [idx]

        # extract sorting based on ranking
        summary['sorts']['ranking'] += [idx]
        # extract sorting based on dates
        dates += [str(__find('_source.pennsieve.firstPublishedAt.timestamp', hit))]
        srtDates += [str(idx)]
        names += [str(__find('_source.item.name', hit))]
        srtNames += [str(idx)]
        # set hit
        ht = {'url': 'https://sparc.science/datasets/'+idx,
              'banner': __find('_source.pennsieve.banner.uri', hit),
              '_id': hit['_id'],
              '_score': hit['_score'],
              'firstPublishedAt': __find('_source.pennsieve.firstPublishedAt.timestamp', hit),
              'updatedAt': __find('_source.pennsieve.updatedAt.timestamp', hit),
              'name': __find('_source.item.name', hit),
              'description': __find('_source.item.description', hit),
              'readme': __find('_source.item.readme.description', hit),
              'samples': __find('_source.item.statistics.samples.count', hit),
              'subjects': __find('_source.item.statistics.subjects.count', hit),
              'anatomy': __find('_source.anatomy.organ.name', hit),
              'organisms': __find('_source.organisms.primary.species.originalName', hit),
              'publication': __find('_source.item.published.boolean', hit),
              'techniques': __find('_source.item.techniques.keyword', hit),
              }
        if 'highlight' in hit:
            ht['highlight'] = {}
            for type, value in hit['highlight'].items():
                ht['highlight'][type.split('.')[1]] = value
        summary['hits'][idx] = ht

    # sort based on dates and titles
    if len(dates) > 0:  # when there are results
        dates, srtDates = zip(*sorted(zip(dates, srtDates), reverse=True))
        names, srtNames = zip(*sorted(zip(names, srtNames)))
    summary['sorts']['date'] = list(srtDates)
    summary['sorts']['name'] = list(srtNames)
    return json(summary)


def getSuggestions(request):
    """
    To get query suggestion from scigraph
        - see suggestions(request) in server.py
    """
    if 'query' not in request.args:
        return json({})
    query = request.args['query'][0]
    limit = request.args['limit'] if 'limit' in request.args else '10'
    return json(__getSuggestions(query, limit))


def __getSuggestions(query, limit):
    """
    To get suggestions as a list data type.
    """
    # get possible correction
    correction = __getCorrection(query)
    # get suggestion from SciGraph
    url = 'https://scicrunch.org/api/1/scigraph/vocabulary/suggestions/'+query
    params = {'api_key': api_key, 'limit': limit}
    rsp = requests.get(url, params=params)
    # return the correction and suggestions
    return [correction] + rsp.json()


def getAutoComplete_sc(request):
    """
    To get autocomplete from SciGraph
        - see autocomplete_sc(request) in server.py
    """
    if 'query' not in request.args:
        return json({})
    query = request.args['query'][0]
    limit = request.args['limit'][0] if 'limit' in request.args else '10'
    verbose = 'no' if 'verbose' not in request.args else request.args['verbose'][0]
    return json(__getAutoComplete_sc(query, limit, verbose))


def __getAutoComplete_sc(query, limit, verbose):
    """
    To get autocomplete as a list data type.
    """
    url = 'https://scicrunch.org/api/1/scigraph/vocabulary/autocomplete/'+query
    params = {'api_key': api_key, 'limit': limit, 'searchSynonyms': 'true',
              'searchAbbreviations': 'false', 'searchAcronyms': 'false',
              'includeDeprecated': 'false'}
    rsp = requests.get(url, params=params)
    if verbose == 'yes':
        return rsp.json()
    completions = []
    for completion in rsp.json():
        cmp = completion['completion'].lower()
        if cmp not in completions:
            completions += [cmp]
    return completions


def __loadWordsCompletion():
    """
    Loading autocomplete n-gram model to fast_autocomplete
    """
    from fast_autocomplete import autocomplete_factory
    content_files = {
        'words': {
            'filepath': "/usr/src/app/resources/words_autocomplete1.json",
            'compress': True
        }
    }
    return autocomplete_factory(content_files=content_files)


# get fast_autocomplete pipeline
autocomplete = __loadWordsCompletion()


def getAutoComplete(request):
    """
    To get autocomplete from fast_autocomplete
        - see autocomplete(request) in server.py
    """
    if 'query' not in request.args:
        return json([])
    query = request.args['query'][0]
    limit = int(request.args['limit'][0]) if 'limit' in request.args else 10
    completions = autocomplete.search(word=query, max_cost=3, size=limit)
    return json([' '.join(completion) for completion in completions])


def __loadSpellChecker():
    """
    Loading spelling checker n-gram model to symspellpy
    """
    from symspellpy import SymSpell, Verbosity
    max_edit_distance_dictionary = 4
    prefix_length = 10
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    sym_spell.load_pickle('/usr/src/app/resources/_spell_model')
    return sym_spell


# get symspellpy pipeline
sym_spell = __loadSpellChecker()


def __getCorrection(query):
    """
    To get autocorrection as a string.
    """
    result = sym_spell.word_segmentation(query)
    return result.corrected_string


#importing add_new_single_entry for NotifyMe purpose


def getNotifyMe(request):
    """
    To set email and keywords to get notification for new datasets
        - see notifyMe(request) in server.py
    """
    try:
        email = request.form['email'][0]
        keywords = request.form['keywords'][0]
        add_new_single_entry(email, keywords)
        return json({'success': 'true'})
    except:
        return json({'success': 'false'})
