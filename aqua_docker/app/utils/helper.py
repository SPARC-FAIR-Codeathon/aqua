import os
import requests
from sanic.response import json, text, html

api_key = '6u6izfSzCHTqVvphJ28lUbAtX0nXGhrd'
def loadMain():
    fileName = os.path.join(os.path.dirname(__file__), 'main.html')
    try:
        f = open(fileName, "r")
        htmlText = f.read()
        f.close()
    except:
        return html("We are sorry,there was an error ..., %s is not found"%fileName)
    return html(htmlText)

def getSearch(request):
    """
    Searching function: an interface to elasticsearch
    """
    summary = {}
    url = 'https://scicrunch.org/api/1/elastic/SPARC_PortalDatasets_pr/_search?api_key='+api_key
    size = '200'
    query = {
        "size": size,
        "from": 0,
        "_source":{
            "includes":["item.keywords","item.name",
                        "item.readme",
                        "item.description",
                        "pennsieve.versionPublishedAt",
                        "pennsieve.banner",
                        "pennsieve.identifier",
                        "contributors.last",
                        "contributors.first"],
        },
    }
    if 'query' in request.args:
        q = request.args['query'][0]
        force = 'no' if 'force' not in request.args else request.args['force'][0]
        if 'query' in request.args:
            query['query'] = {"query_string": {"query": q}}
            summary['query'] = q
            summary['executed'] = q
            summary['force'] = force
            summary['suggestions'] = __getSuggestions(q, 10)
            if force != 'yes':
                autocomplete = __getAutoComplete(request.args['query'][0], 1, 'no')
                if q.lower() not in autocomplete:
                    if len(summary['suggestions']) > 0:
                        query['query'] = {"query_string": {"query": summary['suggestions'][0]}}
                        summary['executed'] = summary['suggestions'][0]
        # if 'query' in request.args:
        #     query['query'] = {"query_string": {"query": q}}

    response = requests.post(url, json=query)
    summary['total'] = response.json()['hits']['total']
    summary['filters'] = {'keywords':{}, 'authors':{}}
    summary['sorts'] = {'ranking':[],'date':[]}
    summary['hits'] = {}
    dates, srtDates = [], []
    for hit in response.json()['hits']['hits']:
        try:
            idx = hit['_source']['pennsieve']['identifier']
            # extract filters
            ## extract from keywords
            for key in hit['_source']['item']['keywords']:
                if key['keyword'] in summary['filters']['keywords']:
                    summary['filters']['keywords'][key['keyword']] += [idx]
                else:
                    summary['filters']['keywords'][key['keyword']] = [idx]
            ## extract from contributors
            for key in hit['_source']['contributors']:
                name = key['first']['name'] + ' ' + key['last']['name']
                if name in summary['filters']['authors']:
                    summary['filters']['authors'][name] += [idx]
                else:
                    summary['filters']['authors'][name] = [idx]
            # extract sorting based on ranking
            summary['sorts']['ranking'] += [idx]
            # extract sorting based on dates
            dates += [hit['_source']['pennsieve']['versionPublishedAt']['timestamp']]
            srtDates += [idx]
            # set hit
            ht = {'url': 'https://sparc.science/datasets/'+idx,
                  'banner': hit['_source']['pennsieve']['banner']['uri'],
                  '_id': hit['_id'],
                  '_score': hit['_score'],
                  'date': hit['_source']['pennsieve']['versionPublishedAt']['timestamp'],
                  'name': hit['_source']['item']['name'],
                  'description': hit['_source']['item']['description'],
                  'readme': hit['_source']['item']['readme'],
                   }
            summary['hits'][idx] = ht
        except:
            pass

    # sort based on dates
    if len(dates) > 0: # when there are results
        dates, srtDates = zip(*sorted(zip(dates, srtDates),reverse=True))
    summary['sorts']['date'] = list(srtDates)
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
    url = 'https://scicrunch.org/api/1/scigraph/vocabulary/suggestions/'+query
    params = {'api_key':api_key,'limit':limit}
    rsp = requests.get(url, params=params)
    return rsp.json()

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
    if verbose == 'yes': return json(rsp.json())
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
