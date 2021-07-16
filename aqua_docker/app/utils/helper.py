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
    Searching function
    """
    return json({})

def getSuggestions(request):
    """
    get suggestions function
    """
    if 'query' not in request.args:
        return json({})
    query = request.args['query'][0]
    url = 'https://scicrunch.org/api/1/scigraph/vocabulary/suggestions/'+query
    limit = request.args['limit'] if 'limit' in request.args else 10
    params = {'api_key':api_key,'limit':limit}
    rsp = requests.get(url, params=params)
    return json(rsp.json())

def getAutoComplete(request):
    """
    get autocomplete function
    """
    if 'query' not in request.args:
        return json({})
    query = request.args['query'][0]
    url = 'https://scicrunch.org/api/1/scigraph/vocabulary/autocomplete/'+query
    limit = request.args['limit'] if 'limit' in request.args else 10
    params = {'api_key':api_key,'limit':limit,'searchSynonyms':'true','searchAbbreviations':'false','searchAcronyms':'false','includeDeprecated':'false'}
    rsp = requests.get(url, params=params)
    if 'verbose' in request.args:
        if request.args['verbose']:
            return json(rsp.json())
    completions = [];
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
    return json(completions)
