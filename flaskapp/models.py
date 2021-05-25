from datetime import datetime
from flaskapp import db, login_manager
import csv
from flask_login import UserMixin
from flask import session

@login_manager.user_loader
def load_user(user_id):
    if session['account_type'] == 'admin':
        return Admin.query.get(int(user_id))
    elif session['account_type'] == 'company':
        return Company.query.get(int(user_id))
    elif session['account_type'] == 'student':
        return Student.query.get(int(user_id))
    elif session['account_type'] == 'teacher':
        return Teacher.query.get(int(user_id))
    else:
        return Account.query.get(int(user_id))

class Company(db.Model, UserMixin):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    location = db.Column(db.String(80), nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(60), nullable=False)
    projects = db.relationship('Project', backref='project', lazy=True)

    def __repr__(self):
        return f"Company('{self.name}, {self.location}')"

class Institution(db.Model):
    __tablename__ = "institution"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    location = db.Column(db.String(80), nullable=False)
    teachers = db.relationship('Teacher', backref='teacher', lazy=True)
    students = db.relationship('Student', backref='learns', lazy=True)

    def __repr__(self):
        return f"Institution ('{self.name}')"

class Student(db.Model, UserMixin):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    batch = db.Column(db.Integer, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    student_id = db.Column(db.String, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
    
    works = db.relationship('Work', backref='developer', lazy=True)
    
    def __repr__(self):
        return f"Student ('{self.name}, {self.student_id}')"

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"Admin ('{self.name}, {self.institution_id}')"

class Account(db.Model, UserMixin):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"Account ('{self.role}, {self.role_id}')"


class Teacher(db.Model, UserMixin):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(60), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)

    works = db.relationship('Work', backref='overviews', lazy=True)
    
    def __repr__(self):
        return f"Lecturer ('{self.name}, {self.institution_id}')"


class Project(db.Model):

    __tablename__ = "project"
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


class Work(db.Model):
    __tablename__ = "work"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teachers_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    projects_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)

    
    ratings = db.relationship('Rating', backref='rates', lazy=True)

    def __repr__(self):
        return f"Project ('{self.student_id}, {self.project_id}')"

class Rating(db.Model):
    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    teacher_review = db.Column(db.String(200), nullable=False)
    company_review = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f"Project ('{self.student_id}, {self.project_id}')"

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