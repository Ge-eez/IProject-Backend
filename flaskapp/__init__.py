import os
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from flask_migrate import Migrate

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


from flaskapp import routes, auth, project, user, institution, work

app.register_blueprint(auth.bp)
api.add_resource(project.ProjectAPI, '/projects/', '/projects/<int:id>')
api.add_resource(user.UserAPI, '/users/', '/users/<int:id>')
api.add_resource(institution.InstitutionAPI, '/institutions/', '/institutions/<int:id>')
api.add_resource(user.UserVerificationAPI, '/users/verify/<int:id>')
api.add_resource(user.StudentAPI, '/students/', '/students/<int:id>')
api.add_resource(user.TeacherAPI, '/teachers/', '/teachers/<int:id>')
api.add_resource(user.CompanyAPI, '/companies/', '/companies/<int:id>')