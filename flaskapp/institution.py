from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, pagination
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *


from flaskapp.models import *

class InstitutionAPI(Resource):
        
    def get(self, id=None):
        message = ""
        if(logged_in(current_user)):
            if(id):
                institution = Institution.query.filter_by(id=id)
                if(institution):
                    return pagination.paginate(institution, institution_fields)
                else:
                    message = "Institution not found"
            else:
                institutions = Institution.query.all()
                if(institutions):
                    return pagination.paginate(institutions, institution_fields)
                else:
                    message = "Institutions not available"
                

        else:
            message = "Access Denied"
        
        abort(400, {'message': message})
