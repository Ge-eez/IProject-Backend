import os
from flask_bcrypt import Bcrypt
from flask import Blueprint, session, request, jsonify, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flaskapp import db, bcrypt, api
from flask_login import login_user, current_user
from flask_restful import Resource

from flask_jwt import JWT
import jwt

from flaskapp.models import *

class ProjectAPI(Resource):
        
    def get(self, id=None):
        message = ""
        if(current_user.is_authenticated):
            if(id):
                project = Project.query.filter_by(id=id).first()
                return project.as_dict()
            else:
                projects = Project.query.all()
                my_dict = dict() 
                for index,value in enumerate(projects):
                    my_dict[index] = value.as_dict()
                return my_dict

        else:
            message = "Login first"
        
        abort(400, {'message': message})


    def put(self, id):
        pass

    def post(self):
        message = ""
        if(current_user.is_authenticated):
            if(session['account_type'] == 'company'):
                data = request.form
                if(data and data.get('title')  
                    and data.get('description')  
                    and data.get('price') 
                    and data.get('deadline') 
                    and data.get('technologies')):
                    
                    technologies = (data['technologies']).split(',')
                    try:
                        new_project = Project(title=data['title'], 
                            description=data['description'], 
                            price=data['price'], 
                            deadline=data['deadline'],
                            technologies=technologies,
                            company_id=current_user.id) 
                        db.session.add(new_project)  
                        db.session.commit()  
                        return "Project created"
                    except:
                        raise Exception("Project not created")
                else: 
                    message += "Form is missing"
            else: 
                message += "No access"

        else:
            message = "Login first"
        
        abort(400, {'message': message})

    def delete(self, id):
        message = ""
        if(current_user.is_authenticated):
            if(session['account_type'] == 'company' or session['account_type'] == 'admin' ):
                try:
                    Project.query.filter_by(id=id).delete()
                    db.session.commit()  
                    return "Project deleted"
                except:
                    raise Exception("Project not deleted")

            else: 
                message += "No access"

        else:
            message = "Login first"
        
        abort(400, {'message': message})

