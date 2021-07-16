from sanic import Sanic

SANIC_PREFIX = "SANIC_"

app = Sanic(name='Biosimulation_Model_IR')


#import helper
from .utils.helper import *

@app.route("/")
async def root(request):
    return loadMain()

@app.route("/search")
async def root(request):
   return search(request,tester)

app.static('/cache', './cache', '/static', './static')  # while in docker files from static will be served by ngnix
if __name__ == "__main__":
    for k, v in os.environ.items():
        if k.startswith(SANIC_PREFIX):
            _, config_key = k.split(SANIC_PREFIX, 1)
            app.config[config_key] = v
    app.run(host="0.0.0.0", port=8000, debug=True)
