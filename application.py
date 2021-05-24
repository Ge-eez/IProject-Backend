import os
from flask import Flask, session, render_template, url_for, flash, redirect, request, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
from flask_bcrypt import Bcrypt


app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'f604efb78b05fc462348c8f5f4cf82c7'
bcrypt = Bcrypt(app)
Session(app)

# Set up database
dbUrl = os.getenv("DATABASE_URL")
if(dbUrl[8] == ":"):
    dbUrl = dbUrl[0:8] + "ql" + dbUrl[8:len(dbUrl)]
engine = create_engine(dbUrl)
db = scoped_session(sessionmaker(bind=engine))

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

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found lol"

@app.route('/register_company', methods=['GET', 'POST'])
@logout_required
def register_company():
    return "Hehe"

@app.route('/institution', methods=['GET', 'POST'])
def register_institution():
    result = {"success": ""}
    name = request.form.get('name')
    location = request.form.get('location')
    try:
        if name and location:
            db.execute("INSERT INTO institutions (name, location) VALUES (:name, :location)",
                                   {"name": request.form['name'], 
                                   "location": request.form['location']})
            db.commit()
            result['success'] = True
        else: 
            raise Exception("Name or Location missing")
    except Exception as e:
        result['success'] = False
        result['message'] = str(e)
    return jsonify(result)


@app.route('/register_student', methods=['GET', 'POST'])
@logout_required
def register_student():
    return Companies.query.all()

@app.route('/register_teacher', methods=['GET', 'POST'])
@logout_required
def register_teacher():
    return Companies.query.all()

@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    return "Hello"


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    session["logged_in"] = False

    # Redirect user to login index
    return redirect(url_for("home"))

