from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, pagination
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *


from flaskapp.models import *

class InstitutionAPI(Resource):
        
    @token_required_student
    def get(self, id=None):
        message = ""
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
                
        
        return abort(400, {'message': message})
