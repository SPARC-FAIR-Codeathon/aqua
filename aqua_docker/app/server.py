"""
This is the main file of Sanic Server. All accesses initially will be directed
to this file.
"""

from sanic import Sanic

SANIC_PREFIX = "SANIC_"

app = Sanic(name='AQUA')

# import helper
from .utils.helper import getSuggestions, getSearch, loadMain, getAutoComplete

@app.route("/")
async def root(request):
    return loadMain()

@app.route("/search")
async def search(request):
    return getSearch(request)

@app.route("/suggestions")
async def suggestions(request):
    """
    Get suggestions from SciGraph
    Parameters:
        - query: is a string query
        - limit: the maximum returned number
    Examples:
        - http://130.216.216.55/suggestions?query=rat&limit=10
    """
    return getSuggestions(request)

@app.route("/autocomplete")
async def autocomplete(request):
    """
    Get autocomplete from SciGraph
    Parameters:
        - query: is a string query
        - limit: the maximum returned number
        - verbose:
            - yes -> will return results as returned by SciGraph
            - no -> will return autocomplete as a list
    Examples:
        - http://130.216.216.55/autocomplete?query=rat&limit=10
        - http://130.216.216.55/autocomplete?query=rat&limit=10&verbose=true
    """
    return getAutoComplete(request)

app.static('/cache', './cache', '/static', './static')  # while in docker files from static will be served by ngnix
if __name__ == "__main__":
    import os
    for k, v in os.environ.items():
        if k.startswith(SANIC_PREFIX):
            _, config_key = k.split(SANIC_PREFIX, 1)
            app.config[config_key] = v
    app.run(host="0.0.0.0", port=8000, debug=True)
