import os
from flask_bcrypt import Bcrypt
from flask import Blueprint, session, request, jsonify, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flaskapp import db, bcrypt
from flask_login import login_user, current_user

from flask_jwt import JWT
import jwt

from flaskapp.models import *

bp = Blueprint('project', __name__, url_prefix='/project')

