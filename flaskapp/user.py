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

class UserAPI(Resource):
        
    def get(self, id=None):
        message = ""
        if(current_user.is_authenticated  and session['account_type'] == 'admin' ):
            if(id):
                user = Account.query.filter_by(id=id).first()
                if(user):
                    return user.as_dict()
                else:
                    message = "User not found"
            else:
                users = Account.query.all()
                if(users):
                    my_dict = dict() 
                    for index,value in enumerate(users):
                        my_dict[index] = value.as_dict()
                    return my_dict
                else:
                    message = "Users not available"
                

        else:
            message = "Access Denied"
        
        abort(400, {'message': message})


    def put(self, id):
        pass

    def delete(self, id):
        message = ""
        if(current_user.is_authenticated  and session['account_type'] == 'admin' ):
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
        
        abort(400, {'message': message})
