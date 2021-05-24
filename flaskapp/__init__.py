import os
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'f604efb78b05fc462348c8f5f4cf82c7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

dbUrl = os.getenv("DATABASE_URL")
if(dbUrl[8] == ":"):
    dbUrl = dbUrl[0:8] + "ql" + dbUrl[8:len(dbUrl)]
app.config['SQLALCHEMY_DATABASE_URI'] = dbUrl 

bcrypt = Bcrypt(app)
Session(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from flaskapp import routes

from flaskapp import auth
from flaskapp import project

app.register_blueprint(auth.bp)
app.register_blueprint(project.bp)