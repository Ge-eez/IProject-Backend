import os
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from flask_migrate import Migrate
from flask_rest_paginate import Pagination
from safrs import SAFRSBase, SAFRSAPI

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'f604efb78b05fc462348c8f5f4cf82c7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["DEBUG"] = True

dbUrl = os.getenv("DATABASE_URL")
if(dbUrl[8] == ":"):
    dbUrl = dbUrl[0:8] + "ql" + dbUrl[8:len(dbUrl)]
app.config['SQLALCHEMY_DATABASE_URI'] = dbUrl 

bcrypt = Bcrypt(app)
Session(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
api = Api(app)
migrate = Migrate(app, db)
pagination = Pagination(app, db)


from flaskapp.models import *
def create_api(app, HOST="localhost", PORT=5000, API_PREFIX="/swagger"):
    api = SAFRSAPI(app, host=HOST, port=PORT, prefix=API_PREFIX)
    api.expose_object(Account)
    api.expose_object(Admin)
    api.expose_object(Institution)
    api.expose_object(Company)
    api.expose_object(Student)
    api.expose_object(Teacher)
    api.expose_object(Project)
    api.expose_object(Work)
    api.expose_object(Rating)
    print("Created API: http://{}:{}{}".format(HOST, PORT, API_PREFIX))


from flaskapp import routes, auth, project, user, institution, work, rating, index

app.register_blueprint(auth.bp)

api.add_resource(index.IndexAPI, '/', '/<int:id>')

api.add_resource(institution.InstitutionAPI, '/institutions/', '/institutions/<int:id>')

api.add_resource(project.ProjectAPI, '/projects/', '/projects/<int:id>')

api.add_resource(user.UserAPI, '/users/', '/users/<int:id>')
api.add_resource(user.UserVerificationAPI, '/users/verify/<int:id>')
api.add_resource(user.StudentAPI, '/students/', '/students/<int:id>')
api.add_resource(user.TeacherAPI, '/teachers/', '/teachers/<int:id>')
api.add_resource(user.CompanyAPI, '/companies/', '/companies/<int:id>')

api.add_resource(work.WorkAPI, '/works/', '/works/<int:id>')
api.add_resource(work.FinishWorkAPI, '/work/end/<int:id>')

api.add_resource(rating.RateAPI, '/rates/', '/rates/<int:id>')


create_api(app)