from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *


from flaskapp.models import *

class WorkAPI(Resource):
        
    def get(self, id=None):
        message = ""
        if(logged_in(current_user)):
            if(id):
                if(is_company(current_user)):
                    project = Project.query.filter_by(id=id, company_id=current_user.id).first()
                elif(is_student(current_user)):
                    project = Project.query.filter_by(id=id, company_id=current_user.id).first()
                elif(is_teacher(current_user)):
                    project = Project.query.filter_by(id=id, company_id=current_user.id).first()
                else:
                    project = Project.query.filter_by(id=id).first()
                if(project):
                    return project.as_dict()
                else:
                    message = "Project not found"
            else:
                if(is_company(current_user)):
                    project = Project.query.filter_by(company_id=current_user.id)
                else:
                    projects = Project.query.all()
                if(projects):
                    my_dict = dict() 
                    for index,value in enumerate(projects):
                        my_dict[index] = value.as_dict()
                    return my_dict
                else:
                    message = "Projects not available"

        else:
            message = "Access Denied"
        
        abort(400, {'message': message})


    def put(self, id):
        message = ""
        if(is_company(current_user) or is_admin(current_user)):
            try:
                if(is_company(current_user)):
                    project = Project.query.filter_by(id=id, company_id=current_user.id)
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
        
        abort(400, {'message': message})


    def post(self):
        message = ""
        if(is_student(current_user)):
            data = request.form
            if(data and data.get('projects_id')  
                and data.get('teachers_id')  
                and data.get('deadline') ):
                
                try:
                    new_work = Work(projects_id=data['projects_id'], 
                        teachers_id=data['teachers_id'], 
                        deadline=data['deadline'],
                        student_id=current_user.id) 
                    db.session.add(new_work)  
                    db.session.commit()  
                    return "Work created"
                except:
                    message = "Work not created"
            else: 
                message += "Form is missing"

        else:
            message = "Access Denied"
        
        abort(400, {'message': message})

    def delete(self, id):
        message = ""
        if(is_company(current_user) or is_admin(current_user)):
            try:
                if(is_company(current_user)):
                    project = Project.query.filter_by(id=id, company_id=current_user.id)
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
        
        abort(400, {'message': message})
