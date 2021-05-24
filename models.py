from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


# class Companies():
#     __tablename__ = "companies"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(80), nullable=False, unique=True)
#     location = db.Column(db.String(80), nullable=False)
#     verified = db.Column(db.Boolean, nullable=False)
#     password = db.Column(db.String(80), nullable=False)

# class Students():
#     __tablename__ = "students"
#     id = db.Column(db.Integer, primary_key=True)
#     name VARCHAR NOT NULL,
#     email VARCHAR NOT NULL unique,
#     batch SMALLINT NOT NULL CHECK (batch BETWEEN 1 and 6),
#     institutions_id INTEGER REFERENCES institutions,
#     student_identification VARCHAR NOT NULL,
#     password VARCHAR NOT NULL

# class Teachers():
#     __tablename__ = "teachers"
#     id = db.Column(db.Integer, primary_key=True)
#     name VARCHAR NOT NULL,
#     email VARCHAR NOT NULL unique,
#     batch SMALLINT NOT NULL CHECK (batch BETWEEN 1 and 6),
#     institutions_id INTEGER REFERENCES institutions,
#     student_identification VARCHAR NOT NULL,
#     password VARCHAR NOT NULL

# class Institutions():
#     __tablename__ = "institutions"
#     id = db.Column(db.Integer, primary_key=True)
#     name VARCHAR NOT NULL,
#     email VARCHAR NOT NULL unique,
#     batch SMALLINT NOT NULL CHECK (batch BETWEEN 1 and 6),
#     institutions_id INTEGER REFERENCES institutions,
#     student_identification VARCHAR NOT NULL,
#     password VARCHAR NOT NULL

# class Projects(db.Model):
#     __tablename__ = "projects"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(80), nullable=False, unique=True)
#     location = db.Column(db.String(80), nullable=False)
#     verified = db.Column(db.Boolean(80), nullable=False)
#     password = db.Column(db.String(80), nullable=False)

# class Works():
#     __tablename__ = "works"
#     id = db.Column(db.Integer, primary_key=True)
#     name VARCHAR NOT NULL,
#     email VARCHAR NOT NULL unique,
#     batch SMALLINT NOT NULL CHECK (batch BETWEEN 1 and 6),
#     institutions_id INTEGER REFERENCES institutions,
#     student_identification VARCHAR NOT NULL,
#     password VARCHAR NOT NULL

# class Ratings():
#     __tablename__ = "ratings"
#     id = db.Column(db.Integer, primary_key=True)
#     name VARCHAR NOT NULL,
#     email VARCHAR NOT NULL unique,
#     batch SMALLINT NOT NULL CHECK (batch BETWEEN 1 and 6),
#     institutions_id INTEGER REFERENCES institutions,
#     student_identification VARCHAR NOT NULL,
#     password VARCHAR NOT NULL

          