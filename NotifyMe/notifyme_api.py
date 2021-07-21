from flask import Flask,json
from flask_restplus import Api, Resource, reqparse
from Notifyme_utils import add_new_single_entry
import requests
import logging

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('email', help='registrant email')
parser.add_argument('keywords', help='searck keywords')

@api.route('/aqua/notifyme')
class Retrieve_search(Resource):
    @api.doc(parser=parser)
    def get(self):        
        args = parser.parse_args()
        email = args['email']
        keywords = args['keywords']
        add_new_single_entry(email,keywords)
        return 'registrant successfully added'
           
if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    app.run(host='localhost', port=5432)