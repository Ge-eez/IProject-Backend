import os
from flask_bcrypt import Bcrypt
from flask import Blueprint, session, request, jsonify, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flaskapp import db, bcrypt
from flask_login import login_user, current_user, logout_user

from flask_jwt import JWT
import jwt

from flaskapp.models import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

def add_to_account(email, hashed_password, role, role_id):
    data = request.form  
    success = True
    try:
        new_user = Account(password=hashed_password, 
                            email=email, 
                            role=role,
                            role_id=role_id) 
        db.session.add(new_user)  
        db.session.commit()   
    
    except Exception as e:
        print(e)
        success = False

    return success

@bp.route('/register_student', methods=['POST'])
def signup_student():  
    if(current_user.is_authenticated):
        return jsonify({'message': "Already logged in"})
    data = request.form  
    message = ""
    try:
        if(data):
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_student = Student(name=data['name'], 
                            password=hashed_password, 
                            email=data['email'], 
                            batch=data['batch'],
                            student_id=data['student_id'],
                            institution_id=data['institution_id']) 
            db.session.add(new_student)  
            db.session.commit()   

            account = add_to_account(data['email'], hashed_password, "student", new_student.id)
            if( not account):
                raise Exception("Account not created")

            message = "Account created"
        else:
            raise Exception("Form is missing")
    
    except Exception as e:
        message = str(e)

    return jsonify({'message': message})

@bp.route('/register_teacher', methods=['POST'])
def signup_teacher():  
    if(current_user.is_authenticated):
        return jsonify({'message': "Already logged in"})
    data = request.form  
    message = ""
    try:
        if(data):
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_teacher = Teacher(name=data['name'], 
                            password=hashed_password, 
                            email=data['email'], 
                            institution_id=data['institution_id']) 
            db.session.add(new_teacher)  
            db.session.commit()   

            account = add_to_account(data['email'], hashed_password, "teacher", new_teacher.id)
            if( not account):
                raise Exception("Account not created")
                
            message = "Account created"
        else:
            raise Exception("Form is missing")
    
    except Exception as e:
        message = str(e)

    return jsonify({'message': message})

@bp.route('/register_company', methods=['POST'])
def signup_company():  
    if(current_user.is_authenticated):
        return jsonify({'message': "Already logged in"})
    data = request.form  
    message = ""
    try:
        if(data):
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_company = Company(name=data['name'], 
                            password=hashed_password, 
                            location=data['location'],
                            email=data['email']) 
            db.session.add(new_company)  
            db.session.commit()   

            account = add_to_account(data['email'], hashed_password, "company", new_company.id)
            if( not account):
                raise Exception("Account not created")
                
            message = "Account created"
        else:
            raise Exception("Form is missing")
    
    except Exception as e:
        message = str(e)

    return jsonify({'message': message})

@bp.route('/login', methods=['POST'])
def login():
    if(current_user.is_authenticated):
        return jsonify({'message': "Already logged in"})
    data = request.form  
    result = {}
    try:
        if(data):
            user = Account.query.filter_by(email=data['email']).first()
            if(user and bcrypt.check_password_hash(user.password, data['password'])):
                if(user.role == 'company'):
                    active = Company.query.get(user.role_id)
                elif(user.role == 'student'):
                    active = Student.query.get(user.role_id)
                if(user.role == 'teacher'):
                    active = Teacher.query.get(user.role_id)
                login_user(active, remember=False)
                result['message'] = "Logged in"
                result['user_id'] = current_user.id
            else:
                result['message'] = "Invalid login"
        else:
            raise Exception("Form is missing")
    
    except Exception as e:
        result['message'] = str(e)

    return jsonify(result)

@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': "Logged out successfully"})
    