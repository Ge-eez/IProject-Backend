from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, pagination
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *

from flaskapp.models import *

class IndexAPI(Resource):
        
    def get(self, id=None):
        message = ''' We're working on the documentation. Thank you for your patience.
                    These are the routes that we got. 
                    /institutions/, /institutions/<int:id>, /projects/, /projects/<int:id>, /users/, /users/<int:id>, /users/verify/<int:id>, /students/, /students/<int:id>, /teachers/, /teachers/<int:id>, /companies/, /companies/<int:id>, /works/, /works/<int:id>, /work/end/<int:id>, /rates/, /rates/<int:id>,
                    '''
        return message

    def delete(self, id=None):
        return "LOL what are you trying"
    def post(self, id=None):
        return "LOL what are you trying"
    def put(self, id=None):
        return "LOL what are you trying"

