import os
from flask_bcrypt import Bcrypt
from flask import session, render_template, url_for, flash, redirect, request, jsonify, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flaskapp import app

from flaskapp.models import *


# Models



## Helpers
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
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/register_company', methods=['GET', 'POST'])
@logout_required
def register_company():
    return "Hehe"


