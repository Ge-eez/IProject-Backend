from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, app
from flask_login import current_user
import jwt
from flask_restful import Resource


from flaskapp.models import *

def token_required_student(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return {'message': 'Token is missing'}, 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                
            currentUser = Account.query.filter_by(id=data['id']).first()
            print(currentUser.role)
        except:
            return {'message': 'Token is invalid'}, 401

        if currentUser.role != "student":
            return {'message' : 'You are not authorized'}
            
        return f(*args, **kwargs)

    return decorated

def token_required_teacher(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return {'message': 'Token is missing'}, 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                
            currentUser = Account.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'Token is invalid'}, 401

        if currentUser.role != "teacher":
            return {'message' : 'You are not authorized'}
            
        return f(*args, **kwargs)

    return decorated

def token_required_company(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return {'message': 'Token is missing'}, 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                
            currentUser = Account.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'Token is invalid'}, 401

        if currentUser.role != "company":
            return {'message' : 'You are not authorized'}
            
        return f(*args, **kwargs)

    return decorated

def token_required_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return {'message': 'Token is missing'}, 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                
            currentUser = Account.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'Token is invalid'}, 401

        if currentUser.role != "admin":
            return {'message' : 'You are not authorized'}
            
        return f(*args, **kwargs)

    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return {'message': 'Token is missing'}, 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                
            currentUser = Account.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'Token is invalid'}, 401

            
        return f(*args, **kwargs)

    return decorated

def logged_in(current_user):
    return current_user.is_authenticated
def logged_out(current_user):
    return not(current_user.is_authenticated)

def is_admin(session):
    return (session['account_type'] == 'admin')
def is_student(session):
    return (session['account_type'] == 'student')
def is_teacher(session):
    return (session['account_type'] == 'teacher')
def is_company(session):
    return (session['account_type'] == 'company')

def get_current_user(request):
    token = None
    if 'X-Access-Token' in request.headers:
        token = request.headers['X-Access-Token']
    if not token:
        return {'message': 'Token is missing'}, 403

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        print(data)
            
        return data['user']
    except:
        return 0

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'error': error.description['message']})