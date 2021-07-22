import os
import requests
from sanic.response import json, text, html

api_key = os.getenv('ES_API_KEY', None)

def loadMain():
    fileName = os.path.join(os.path.dirname(__file__), 'main.html')
    try:
        f = open(fileName, "r")
        htmlText = f.read()
        f.close()
    except:
        return html("We are sorry,there was an error ..., %s is not found"%fileName)
    return html(htmlText)

def find(element, JSON):
    try:
        paths = element.split(".")
        data = JSON
        for count, p in enumerate(paths):
            if isinstance(data[p], dict):
                data = data[p]
            elif isinstance(data[p], list):
                data = [find(element[element.find(p)+len(p)+1:], lst) for lst in data[p]]
                break
            elif len(paths)-1 == count:
                return data[p]
        return data
    except:
        return []

def getSearch(request):
    """
    Searching function: an interface to elasticsearch
    """
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
        "_source":{
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
            query['query']['query_string']['query'] = '\"' + query['query']['query_string']['query'] +'\"'

    response = requests.post(url, json=query)
    summary['total'] = response.json()['hits']['total']
    summary['filters'] = {'keywords':{}, 'authors':{}}
    summary['sorts'] = {'ranking':[],'date':[]}
    summary['hits'] = {}
    dates, srtDates, names, srtNames = [], [], [], []
    for hit in response.json()['hits']['hits']:
        idx = find('_source.pennsieve.identifier', hit)
        if idx == []:
            idx = 'dummy_' + str(len(summary['hits'])) # embargo and none

        # extract filters
        ## extract from keywords
        for keyword in find('_source.item.keywords.keyword', hit):
            if keyword not in summary['filters']['keywords']:
                summary['filters']['keywords'][keyword] = []
            summary['filters']['keywords'][keyword] += [idx]
        ## extract from contributors
        firsts = find('_source.contributors.first.name', hit)
        lasts = find('_source.contributors.last.name', hit)
        for name in [first+' '+last for first, last in (zip(firsts,lasts))]:
            if name not in summary['filters']['authors']:
                summary['filters']['authors'][name] = []
            summary['filters']['authors'][name] += [idx]

        # extract sorting based on ranking
        summary['sorts']['ranking'] += [idx]
        # extract sorting based on dates
        dates += [str(find('_source.pennsieve.firstPublishedAt.timestamp', hit))]
        srtDates += [str(idx)]
        names += [str(find('_source.item.name', hit))]
        srtNames += [str(idx)]
        # set hit
        ht = {'url': 'https://sparc.science/datasets/'+idx,
              'banner': find('_source.pennsieve.banner.uri', hit),
              '_id': hit['_id'],
              '_score': hit['_score'],
              'firstPublishedAt': find('_source.pennsieve.firstPublishedAt.timestamp', hit),
              'updatedAt': find('_source.pennsieve.updatedAt.timestamp', hit),
              'name': find('_source.item.name', hit),
              'description': find('_source.item.description', hit),
              'readme': find('_source.item.readme.description', hit),
              'samples': find('_source.item.statistics.samples.count', hit),
              'subjects': find('_source.item.statistics.subjects.count', hit),
              'anatomy': find('_source.anatomy.organ.name', hit),
              'organisms': find('_source.organisms.primary.species.originalName', hit),
              'publication': find('_source.item.published.boolean', hit),
              'techniques': find('_source.item.techniques.keyword', hit),
              'embargoed': 'true' if idx.startswith('dummy') else 'false',
               }
        if 'highlight' in hit:
            ht['highlight'] = {}
            for type, value in hit['highlight'].items():
                ht['highlight'][type.split('.')[1]] = value
        summary['hits'][idx] = ht

    # sort based on dates and titles
    if len(dates) > 0: # when there are results
        dates, srtDates = zip(*sorted(zip(dates, srtDates),reverse=True))
        names, srtNames = zip(*sorted(zip(names, srtNames)))
    summary['sorts']['date'] = list(srtDates)
    summary['sorts']['name'] = list(srtNames)
    return json(summary)

def getSuggestions(request):
    """
    get suggestions function
    """
    if 'query' not in request.args: return json({})
    query = request.args['query'][0]
    limit = request.args['limit'] if 'limit' in request.args else '10'
    return json(__getSuggestions(query, limit))

def __getSuggestions(query, limit):
    # check possible correction
    correction = __getCorrection(query)
    url = 'https://scicrunch.org/api/1/scigraph/vocabulary/suggestions/'+query
    params = {'api_key':api_key,'limit':limit}
    rsp = requests.get(url, params=params)
    return [correction] + rsp.json()

def getAutoComplete(request):
    """
    get autocomplete function
    """
    if 'query' not in request.args: return json({})
    query = request.args['query'][0]
    limit = request.args['limit'] if 'limit' in request.args else '10'
    verbose = 'no' if 'verbose' not in request.args else request.args['verbose'][0]
    return json(__getAutoComplete(query, limit, verbose))

def __getAutoComplete(query, limit, verbose):
    url = 'https://scicrunch.org/api/1/scigraph/vocabulary/autocomplete/'+query
    params = {'api_key':api_key,'limit':limit,'searchSynonyms':'true','searchAbbreviations':'false','searchAcronyms':'false','includeDeprecated':'false'}
    rsp = requests.get(url, params=params)
    if verbose == 'yes': return rsp.json()
    completions = []
    for completion in rsp.json():
        cmp = completion['completion'].lower()
        if cmp not in completions:
            completions += [cmp]
        for cmp in completion['concept']['labels']:
            if cmp.lower() not in completions:
                completions += [cmp.lower()]
        for cmp in completion['concept']['synonyms']:
            if cmp.lower() not in completions:
                completions += [cmp.lower()]
        for cmp in completion['concept']['abbreviations']:
            if cmp.lower() not in completions:
                completions += [cmp.lower()]
    return completions

def loadSpellChecker():
    from symspellpy import SymSpell, Verbosity
    max_edit_distance_dictionary = 4
    prefix_length = 10
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    sym_spell.load_pickle('/usr/src/app/resources/_spell_model')
    return sym_spell

sym_spell = loadSpellChecker()

def __getCorrection(query):
    max_edit_distance_lookup = 4
    result = sym_spell.word_segmentation(query)
    return result.corrected_string
