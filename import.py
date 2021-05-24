import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def create_student_table():
    global db
    create_student_table = """
    CREATE TABLE students (
          id SERIAL PRIMARY KEY,
          name VARCHAR NOT NULL,
          email VARCHAR NOT NULL unique,
          batch SMALLINT NOT NULL CHECK (batch BETWEEN 1 and 6),
          institutions_id INTEGER REFERENCES institutions,
          student_identification VARCHAR NOT NULL,
          password VARCHAR NOT NULL
      )
    """
    db.execute(create_student_table)
    db.commit()

def create_teacher_table():
    global db
    create_user_table = """
    CREATE TABLE teachers (
          id SERIAL PRIMARY KEY,
          name VARCHAR NOT NULL,
          email VARCHAR NOT NULL unique,
          institutions_id INTEGER REFERENCES institutions,
          password VARCHAR NOT NULL,
          verified BOOLEAN  NOT NULL DEFAULT 'f'
      )
    """
    db.execute(create_user_table)
    db.commit()

def create_work_table():
    global db
    create_user_table = """
    CREATE TABLE works (
          id SERIAL PRIMARY KEY,
          students_id INTEGER REFERENCES students,
          teachers_id INTEGER REFERENCES teachers,
          projects_id INTEGER REFERENCES projects,
          start_date DATE NOT NULL DEFAULT CURRENT_DATE,
          deadline DATE NOT NULL,
          finished BOOLEAN NOT NULL  DEFAULT 'f'
      )
    """
    db.execute(create_user_table)
    db.commit()

def create_institution_table():
    global db
    create_institution_table = """
    CREATE TABLE institutions (
          id SERIAL PRIMARY KEY,
          name VARCHAR NOT NULL,
          location VARCHAR NOT NULL
      )
    """
    db.execute(create_institution_table)
    db.commit()

def create_company_table():
    global db
    create_company_table = """
    CREATE TABLE companies (
          id SERIAL PRIMARY KEY,
          name VARCHAR NOT NULL,
          email VARCHAR NOT NULL unique,
          location VARCHAR NOT NULL,
          verified BOOLEAN  NOT NULL DEFAULT 'f',
          password VARCHAR NOT NULL
      )
    """
    db.execute(create_company_table)
    db.commit()

def create_project_table():
    global db
    create_project_table = """
    CREATE TABLE projects (
          id SERIAL PRIMARY KEY,
          companies_id INTEGER REFERENCES companies,
          title VARCHAR NOT NULL,
          description VARCHAR NOT NULL unique,
          technologies TEXT [],
          price_range NUMERIC NOT NULL,
          active BOOLEAN NOT NULL  DEFAULT 't',
          deadline DATE NOT NULL
      )
    """
    db.execute(create_project_table)
    db.commit()

def create_rating_table():
    global db
    create_book_table = """
    CREATE TABLE ratings (
          id SERIAL PRIMARY KEY,
          works_id INTEGER REFERENCES works,
          teachers_review TEXT,
          companies_review TEXT
      )
    """
    db.execute(create_book_table)
    db.commit()

def main():
    global db

    f = open("institutions.csv") 
    reader = csv.reader(f) 
    next(reader, None)

    for name, location, in reader:
        db.execute("INSERT INTO institutions (name, location) VALUES (:name, :location)", 
                  {"name": name, 
                   "location": location})

    db.commit()

if __name__ == '__main__':
    # create_company_table()
    # create_institution_table()
    # create_student_table()
    # create_teacher_table()
    # create_project_table()
    # create_work_table()
    # create_rating_table()
    main()