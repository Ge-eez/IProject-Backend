from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, pagination
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *


from flaskapp.models import *

class WorkAPI(Resource):
        
    @token_required
    def get(self, id=None):
        message = ""
        if(id):
            if(is_company(current_user)):
                work = Work.query.filter_by(id=id, company_id=current_user.id)
            elif(is_student(current_user)):
                work = Work.query.filter_by(id=id, student_id=current_user.id)
            elif(is_teacher(current_user)):
                work = Work.query.filter_by(id=id, teachers_id=current_user.id)
            else:
                work = Work.query.filter_by(id=id)
            if(work.first()):
                return pagination.paginate(works, work_fields)
            else:
                message = "Work not found"
        else:
                if(is_company(current_user)):
                    works = Work.query.join(Project, Work.projects_id==Project.id).filter(Project.company_id==current_user.id)
                elif(is_student(current_user)):
                    works = Work.query.filter_by(student_id=current_user.id)
                elif(is_teacher(current_user)):
                    works = Work.query.filter_by(teachers_id=current_user.id)
                else:
                    works = Work.query.all()
                if(works):
                    return pagination.paginate(works, work_fields)
                else:
                    message = "Works not available"

        
        return abort(400, {'message': message})


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
        
        return abort(400, {'message': message})


    def post(self):
        message = ""
        if(is_student(current_user)):
            data = request.form
            if(data and data.get('projects_id')  
                and data.get('teachers_id')  
                and data.get('deadline') ):
                
                try:
                    project = Project.query.filter_by(id=data['projects_id']).first()
                    teacher = Teacher.query.filter_by(id=data['teachers_id']).first()
                    if(project and teacher):
                        new_work = Work(projects_id=data['projects_id'], 
                            teachers_id=data['teachers_id'], 
                            deadline=data['deadline'],
                            student_id=current_user.id) 
                        db.session.add(new_work)  
                        db.session.commit()  
                        return "Work created"
                    else:
                        message = "Project or Teacher doesn't exist"
                except:
                    message = "Work not created"
            else: 
                message += "Form is missing"

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})

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
        
        return abort(400, {'message': message})

class FinishWorkAPI(Resource):
    
    def put(self, id):
        message = ""
        if(is_student(current_user)):
            try:
                work = Work.query.filter_by(id=id, student_id=current_user.id).first()
                if(work):
                    if(work.finished == True):
                        message = "Work already finished"
                    else:
                        work.finished = True
                        db.session.commit()  
                        return "Work finished"
                else:
                    message = "Work not found"
            except Exception as e:
                message = "Work not finished "+ str(e)

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})

