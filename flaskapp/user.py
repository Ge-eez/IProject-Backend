from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, pagination
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *

from flaskapp.models import *

class UserAPI(Resource):
        
    @token_required
    def get(self, id=None):
        message = ""
        if(id):
            user = Account.query.filter_by(id=id)
            if(user):
                return pagination.paginate(user, account_fields)
            else:
                message = "User not found"
        else:
                users = Account.query.all()
                if(users):
                    return pagination.paginate(users, account_fields)
                else:
                    message = "Users not available"
                
        
        return abort(400, {'message': message})

    def delete(self, id):
        message = ""
        if(is_admin(request)):
            try:
                acc = Account.query.filter_by(id=id)
                account = acc.first()
                if(account):
                    if(account.role == 'company'):
                        user = Company.query.filter_by(id=account.role_id)
                    elif(account.role == 'student'):
                        user = Student.query.filter_by(id=account.role_id)
                    elif(account.role == 'teacher'):
                        user = Teacher.query.filter_by(id=account.role_id)
                    user.delete()
                    acc.delete()
                    db.session.commit()  
                    return "Account deleted"
                else:
                    message = "Account not found"
            except Exception as e:
                message = "Account not deleted "+ str(e)

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})

class UserVerificationAPI(Resource):
        
    def put(self, id):
        message = ""
        if(is_admin(request)):
            try:
                account = Account.query.filter_by(id=id).first()
                if(account):
                    if(account.role == 'company'):
                        user = Company.query.filter_by(id=account.role_id).first()
                    elif(account.role == 'student'):
                        user = Student.query.filter_by(id=account.role_id).first()
                    elif(account.role == 'teacher'):
                        user = Teacher.query.filter_by(id=account.role_id).first()
                    if(user.verified == True):
                        message = "User already verified"
                    else:
                        user.verified = True
                        db.session.commit()  
                        return "Account verified"
                else:
                    message = "Account not found"
            except Exception as e:
                message = "Account not verified "+ str(e)

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})

class StudentAPI(Resource):
        
    @token_required_student
    def get(self, id=None):
        message = ""
        if(id):
            user = Student.query.filter_by(id=id)
            if(user):
                return pagination.paginate(user, student_fields)
            else:
                message = "Student not found"
        else:
            users = Student.query.all()
            if(users):
                return pagination.paginate(users, student_fields)
            else:
                message = "Students not available"
            
        
        return abort(400, {'message': message})

    @token_required
    def delete(self, id):
        message = ""
        try:
            user = Student.query.filter_by(id=id)
            student = user.first()
            if(student):
                account = Account.query.filter_by(role_id=student.id, role='student')

                user.delete()
                account.delete()
                db.session.commit()  
                return "Account deleted"
            else:
                message = "Account not found"
        except Exception as e:
            message = "Account not deleted "+ str(e)
        
        return abort(400, {'message': message})

class TeacherAPI(Resource):
        
    @token_required_teacher
    def get(self, id=None):
        message = ""
        if(id):
            user = Teacher.query.filter_by(id=id)
            if(user):
                return pagination.paginate(user, teacher_fields)
            else:
                message = "Teacher not found"
        else:
                users = Teacher.query.all()
                if(users):
                    return pagination.paginate(users, teacher_fields)
                else:
                    message = "Teachers not available"
                
        
        return abort(400, {'message': message})

    @token_required
    def delete(self, id):
        message = ""
        try:
            user = Teacher.query.filter_by(id=id)
            teacher = user.first()
            if(teacher):
                account = Account.query.filter_by(role_id=teacher.id, role='teacher')

                user.delete()
                account.delete()
                db.session.commit()  
                return "Account deleted"
            else:
                message = "Account not found"
        except Exception as e:
            message = "Account not deleted "+ str(e)
        
        return abort(400, {'message': message})

class CompanyAPI(Resource):
        
    @token_required_company
    def get(self, id=None):
        message = ""
        if(id):
            user = Company.query.filter_by(id=id)
            if(user):
                return pagination.paginate(user, company_fields)
            else:
                message = "Company not found"
        else:
            users = Company.query.all()
            if(users):
                return pagination.paginate(users, company_fields)
            else:
                message = "Companies not available"
            

        
        return abort(400, {'message': message})

    @token_required
    def delete(self, id):
        message = ""
        try:
            user = Company.query.filter_by(id=id)
            company = user.first()
            if(company):
                account = Account.query.filter_by(role_id=company.id, role='company')

                user.delete()
                account.delete()
                db.session.commit()  
                return "Account deleted"
            else:
                message = "Account not found"
        except Exception as e:
            message = "Account not deleted "+ str(e)

        
        return abort(400, {'message': message})
