from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, pagination
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *


from flaskapp.models import *

class ProjectAPI(Resource):
        
    @token_required
    def get(self, id=None):
        message = ""
        if(id):
            if(is_company(session)):
                project = Project.query.filter_by(id=id, company_id=get_current_user(request)['id'])
            else:
                project = Project.query.filter_by(id=id)
            if(project):
                return pagination.paginate(project, project_fields)
            else:
                message = "Project not found"
        else:
            if(is_company(session)):
                projects = Project.query.filter_by(company_id=get_current_user(request)['id'])
            else:
                projects = Project.query.all()

            if(projects):
                return pagination.paginate(projects, project_fields)
            else:
                message = "Projects not available"

       
        
        return abort(400, {'message': message})


    def put(self, id):
        message = ""
        if(is_company(session) or is_admin(session)):
            try:
                if(is_company(session)):
                    project = Project.query.filter_by(id=id, company_id=get_current_user(request)['id'])
                else:
                    project = Project.query.filter_by(id=id)
                if(project):
                    project.update()
                    db.session.commit()  
                    return "Project updated"
                else:
                    message = "Project not found"
            except Exception as e:
                message = "Project not updated" + str(e)

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})


    def post(self):
        message = ""
        if(is_company(session)):
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
                        company_id=get_current_user(request)['id']) 
                    db.session.add(new_project)  
                    db.session.commit()  
                    return "Project created"
                except:
                    message = "Project not created"
            else: 
                message += "Form is missing"

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})

    def delete(self, id):
        message = ""
        if(is_company(session) or is_admin(session)):
            try:
                if(is_company(session)):
                    project = Project.query.filter_by(id=id, company_id=get_current_user(request)['id'])
                else:
                    project = Project.query.filter_by(id=id)
                if(project):
                    project.delete()
                    db.session.commit()  
                    return "Project deleted"
                else:
                    message = "Project not found"
            except Exception as e:
                message = "Project not deleted" + str(e)

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})

