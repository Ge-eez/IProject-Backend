from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, app
from flask_login import current_user
from flask_restful import Resource


from flaskapp.models import *

def logged_in(current_user):
    return current_user.is_authenticated
def logged_out(current_user):
    return not(current_user.is_authenticated)
def is_admin(current_user):
    return (logged_in(current_user) and session['account_type'] == 'admin')
def is_student(current_user):
    return (logged_in(current_user) and session['account_type'] == 'student')
def is_teacher(current_user):
    return (logged_in(current_user) and session['account_type'] == 'teacher')
def is_company(current_user):
    return (logged_in(current_user) and session['account_type'] == 'company')

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'error': error.description['message']})