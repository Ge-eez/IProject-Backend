from datetime import datetime
from flaskapp import db, login_manager
import csv
from flask_restful import fields, marshal_with
from flask_login import UserMixin
from flask import session
from safrs import SAFRSBase, SAFRSAPI

@login_manager.user_loader
def load_user(user_id):
    sess = session
    # print(sess)
    # if(sess.get('account_type')):
    #     print(sess['account_type'])
    #     return Account.query.get(int(user_id))
    print("session from models", sess)
    if sess.get('account_type') == 'admin':
        return Admin.query.get(int(user_id))
    elif sess.get('account_type') == 'company':
        return Company.query.get(int(user_id))
    elif sess.get('account_type') == 'student':
        return Student.query.get(int(user_id))
    elif sess.get('account_type') == 'teacher':
        return Teacher.query.get(int(user_id))
    else:
        return Account.query.get(int(user_id))
    # else:
    #     return Account.query.get(int(user_id))

class Company(SAFRSBase, db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    location = db.Column(db.String(80), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    projects = db.relationship('Project', backref='project', lazy=True)

    def __repr__(self):
        return f"Company('{self.name}, {self.location}')"
    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Institution(SAFRSBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    location = db.Column(db.String(80), nullable=False)
    teachers = db.relationship('Teacher', backref='teacher', lazy=True)
    students = db.relationship('Student', backref='learns', lazy=True)

    def __repr__(self):
        return f"Institution ('{self.name}')"
    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Student(SAFRSBase, db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    batch = db.Column(db.Integer, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    student_id = db.Column(db.String, nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
    
    works = db.relationship('Work', backref='developer', lazy=True)
    
    def __repr__(self):
        return f"Student ('{self.name}, {self.student_id}')"
    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Admin(SAFRSBase, db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    
    def __repr__(self):
        return f"Admin ('{self.name}')"
    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Account(SAFRSBase, db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"Account ('{self.role}, {self.role_id}')"
    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Teacher(SAFRSBase, db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)

    works = db.relationship('Work', backref='overviews', lazy=True)
    
    def __repr__(self):
        return f"Lecturer ('{self.name}, {self.institution_id}')"
    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Project(SAFRSBase, db.Model):

    __table_args__ = (
        db.UniqueConstraint('title', 'company_id', name='unique_project'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(180), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    price = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    deadline = db.Column(db.DateTime)
    technologies = db.Column(db.PickleType, nullable=False)
    
    works = db.relationship('Work', backref='done', lazy=True)    

    def __repr__(self):
        return f"Project ('{self.title}, {self.company_id}')"
    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Work(SAFRSBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teachers_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    projects_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, unique=True)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)

    
    ratings = db.relationship('Rating', backref='rates', lazy=True)

    payments = db.relationship('Payment', backref='pays', lazy=True)

    def __repr__(self):
        return f"Project ('{self.student_id}, {self.project_id}')"
    
    def as_dict(self):
            return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Rating(SAFRSBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False, unique=True)
    teacher_review = db.Column(db.String(200))
    company_review = db.Column(db.String(200))
    
    def __repr__(self):
        return f"Project ('{self.student_id}, {self.project_id}')"

    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class Payment(SAFRSBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Integer, nullable=False)
    
    
    def __repr__(self):
        return f"Payment ('{self.work_id}, {self.price}')"

    def as_dict(self):
           return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

def main():
    global db

    f = open("institutions.csv") 
    reader = csv.reader(f) 
    next(reader, None)

    for name, location in reader:
        record = Institution(**{
            'name': name,
            'location': location
        })
        db.session.add(record)
    db.session.commit()

payment_fields = {
    'price': fields.Integer,
    'date': fields.DateTime,
    'id': fields.Integer,
    'work_id': fields.Integer
}
rating_fields = {
    'teacher_review': fields.String,
    'company_review': fields.String,
    'id': fields.Integer,
    'work_id': fields.Integer
}
work_fields = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'teachers_id': fields.Integer,
    'projects_id': fields.Integer,
    'start_date': fields.DateTime,
    'deadline': fields.DateTime,
    'finished': fields.Boolean,
    'ratings': fields.Nested(rating_fields),
    'pays': fields.Nested(payment_fields)
}
project_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Integer,
    'technologies': fields.String,
    'company_id': fields.Integer,
    'deadline': fields.DateTime,
    'active': fields.Boolean,
    'works': fields.Nested(work_fields)
}
teacher_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'institution_id': fields.Integer,
    'verified': fields.Boolean,
    'works': fields.Nested(work_fields)
}
student_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'batch': fields.Integer,
    'student_id': fields.String,
    'institution_id': fields.Integer,
    'verified': fields.Boolean,
    'works': fields.Nested(work_fields)
}
company_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'location': fields.String,
    'verified': fields.Boolean,
    'projects': fields.Nested(project_fields)
}
account_fields = {
    'role': fields.String,
    'email': fields.String,
    'id': fields.Integer,
    'role_id': fields.Integer,
    'password': fields.String
}
institution_fields = {
    'location': fields.String,
    'name': fields.String,
    'id': fields.Integer,
    'teachers': fields.Nested(teacher_fields),
    'students': fields.Nested(student_fields)
}