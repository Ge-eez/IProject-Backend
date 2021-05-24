import os
from flask_bcrypt import Bcrypt
from flask import Blueprint, session, render_template, url_for, flash, redirect, request, jsonify, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flaskapp import app, db, bcrypt

from flask_jwt import JWT
import jwt

from flaskapp.models import *

## Helpers
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config[SECRET_KEY])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if ("logged_in" not in session) or (session["logged_in"] == False):
            next = request.url
            return redirect(url_for("login", next=next))
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if ("logged_in" in session) and (session["logged_in"] == True):
            session.clear()
            session["logged_in"] = False
        return f(*args, **kwargs)
    return decorated_function




@app.route('/login_teacher', methods=['GET', 'POST'])
@logout_required
def login_teacher():
    return "Hehe"
    

