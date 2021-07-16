import os
import math
from sanic.response import json, text, html

def hello_world():
    return {"hello": "world","halo":"dunia"}


def loadMain():
    fileName = os.path.join(os.path.dirname(__file__), 'main.html')
    try:
        f = open(fileName, "r")
        htmlText = f.read()
        f.close()
    except:
        return html("We are sorry,there was an error ..., %s is not found"%fileName)
    return html(htmlText)


# def search(request):
#     """
#
#     """
#     if 'q' in request.args:
#
