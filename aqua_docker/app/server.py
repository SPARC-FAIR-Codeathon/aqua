"""
Yuda Munarko
26 july 2021

This is the main file of Sanic Server. All accesses initially will be directed
to this file.
"""

from sanic import Sanic
# from sanic_cors import CORS

SANIC_PREFIX = "SANIC_"

app = Sanic(name='AQUA')
# CORS(app)

# import helper methods
from .utils.helper import getSuggestions, getSearch, loadMain, \
    getAutoComplete, getAutoComplete_sc, getNotifyMe

@app.route("/")
async def root(request):
    return loadMain()

@app.route("/search")
async def search(request):
    """
    GET datasets based on the provided query
    Parameters:
        -   query (optional): is a query terms.
        -   force (optional): to force the server to execute a refined query or not.
            -   yes : execute the refined query.
            -   no (default): execute the original query.
        -   match : to signal the server to identify datasets with full query phrase or not.
            -   yes : return datasets having the query phrase.
            -   no (default): return dataset having at least one term of the query phrase.
    Example:
        - http://130.216.216.55/search?query=rattis%20norvegicu&match=yes
    Return:
        - a dictionary about returned datasets (see API documentation)
    """
    return getSearch(request)

@app.route("/suggestions")
async def suggestions(request):
    """
    GET autocorrection from symspellpy pipeline and suggestions from SciGraph
    Parameters:
        - query: is a string query
        - limit: the maximum returned number
    Examples:
        - http://130.216.216.55/suggestions?query=rat&limit=10
    Return:
        - a list of suggestions
    """
    return getSuggestions(request)

@app.route("/autocomplete")
async def autocomplete(request):
    """
    GET autocomplete from fast-autocomplete
    Parameters:
        - query: is a string query
        - limit: the maximum returned number
    Examples:
        - http://130.216.216.55/autocomplete?query=rat&limit=10
        - http://130.216.216.55/autocomplete?query=rat&limit=10&verbose=true
    Return:
        - a list of autocomplete"""
    return getAutoComplete(request)

@app.route("/autocomplete_sc")
async def getAutoComplete_sc(request):
    """
    GET autocomplete from SciGraph
    Parameters:
        - query: is a string query
        - limit: the maximum returned number
    Examples:
        - http://130.216.216.55/autocomplete_sc?query=rat&limit=10
        - http://130.216.216.55/autocomplete_sc?query=rat&limit=10&verbose=true
    Return:
        - a list of autocomplete
    """
    return getAutoComplete_sc(request)

@app.route("/notifyme", methods=["POST"])
async def notifyMe(request):
    """
    POST email and keywords to get notification for new datasets.
    Parameters:
        - email: the registered email
        - keywords: the topic keywords to match to new datasets
    Example:
        - curl -d “email=test@test.ac.nz&keywords=otonom”
    Return:
        - json {'success':'true|false'}
    """
    return getNotifyMe(request)

app.static('/cache', './cache', '/static', './static')
if __name__ == "__main__":
    import os
    for k, v in os.environ.items():
        if k.startswith(SANIC_PREFIX):
            _, config_key = k.split(SANIC_PREFIX, 1)
            app.config[config_key] = v
    app.run(host="0.0.0.0", port=8000, debug=True)
