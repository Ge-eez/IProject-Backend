from flask_bcrypt import Bcrypt
from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, bcrypt, app
from flask_login import login_user, current_user, logout_user
from flaskapp.routes import *
import jwt
from datetime import datetime
from datetime import timedelta

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
    if(logged_in(current_user)):
        return jsonify({'message': "Already logged in"})
    data = request.form  
    message = ""
    try:
        if(data.get('name') and data.get('institution_id')and data.get('batch') and data.get('student_id') and data.get('email') and data.get('password')):
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_student = Student(name=data['name'], 
                            email=data['email'], 
                            batch=data['batch'],
                            student_id=data['student_id'],
                            institution_id=data['institution_id']) 
            db.session.add(new_student)  
            db.session.commit()   

            account = add_to_account(data['email'], hashed_password, "student", new_student.id)
            if(not account):
                raise Exception("Account not created")

            message = "Account created"
        else:
            raise Exception("Form is missing")
    
    except Exception as e:
        message = str(e)

    return jsonify({'message': message})

@bp.route('/register_teacher', methods=['POST'])
def signup_teacher():  
    if(logged_in(current_user)):
        return jsonify({'message': "Already logged in"})
    data = request.form  
    message = ""
    try:
        if(data.get('name') and data.get('institution_id') and data.get('email') and data.get('password')):
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_teacher = Teacher(name=data['name'], 
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
    if(logged_in(current_user)):
        return jsonify({'message': "Already logged in"})
    data = request.form  
    message = ""
    try:
        if(data.get('name') and data.get('location') and data.get('email') and data.get('password')):
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_company = Company(name=data['name'], 
                            location=data['location'],
                            email=data['email']) 
            print("1")
            db.session.add(new_company)  
            print("2")
            db.session.commit() 
            print("3")
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
    if(logged_in(current_user)):
        return jsonify({'message': "Already logged in"})
    data = request.form  
    result = {}
    try:
        if(bool(data.get('email') and data.get('password'))):
            user = Account.query.filter_by(email=data['email']).first()
            if(user and bcrypt.check_password_hash(user.password, data['password'])):
                if(user.role == 'company'):
                    active = Company.query.get(user.role_id)
                    result['role'] = 'companies'
                elif(user.role == 'student'):
                    active = Student.query.get(user.role_id)
                    result['role'] = 'students'
                elif(user.role == 'teacher'):
                    active = Teacher.query.get(user.role_id)
                    result['role'] = 'teachers'
                elif(user.role == 'admin'):
                    active = Admin.query.get(user.role_id)
                    result['role'] = 'Admin'

                session["account_type"] = user.role
                print("session from auth", session)
                login_user(active, remember=True)
                result['message'] = "Logged in"
                result['user_id'] = current_user.id

                

                result["token"] = jwt.encode({'id' : user.id, 'user': active.as_dict(), 'role': user.role, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256").decode("utf-8") 
                
            else:
                return abort(404, {'message': "Invalid login"})
        else:
            raise Exception("Form is missing")
    
    except Exception as e:
        result['message'] = str(e)

    return jsonify(result)

@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session["account_type"] = ''
    return jsonify({'message': "Logged out successfully"})  

    