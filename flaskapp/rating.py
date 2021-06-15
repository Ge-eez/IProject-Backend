from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, pagination
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *


from flaskapp.models import *

class RateAPI(Resource):
        
    def get(self, id=None):
        message = ""
        if(logged_in(current_user)):
            if(id):
                rate = Rating.query.filter_by(id=id)
                rating = rate.first()
                if(rating):
                    if(is_student(current_user) and not(rating.rates.student_id == current_user.id)) or (is_teacher(current_user) and not(rating.rates.teachers_id == current_user.id)):
                        return abort(400, {'message': "Access denied"}) 
                    return pagination.paginate(rate, rating_fields)
                else:
                    message = "Rating not found"
            else:
                if(is_student(current_user)):
                    ratings = Rating.query.join(Work, Work.student_id == current_user.id)
                elif(is_teacher(current_user)):
                    ratings = Rating.query.join(Work, Work.teachers_id == current_user.id)
                else:
                    ratings = Rating.query.all()
                if(ratings):
                    return pagination.paginate(ratings, rating_fields)
                else:
                    message = "Ratings not available"

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})

    def post(self):
        message = ""
        if(is_teacher(current_user) or is_company(current_user)):
            data = request.form
            if(data and data.get('work_id')  
                and data.get('review')):
                
                try:
                    rating = Rating.query.filter_by(work_id=data['work_id']).first()
                    work = Work.query.filter_by(id=data['work_id']).first()
                    if(rating  and is_company(current_user)):
                        if(work.done.company_id == current_user.id):
                            if(rating.company_review):
                                message = "Already reviewed"
                            else:
                                rating.company_review = data['review']
                                db.session.commit() 
                                return "Reviewed successfully" 
                        else:
                            return abort(400, {'message': "Access denied"})     
                    elif(rating and is_teacher(current_user) ):
                        if(work.teachers_id == current_user.id):
                            if(rating.teacher_review):
                                message = "Already reviewed"
                            else:
                                rating.teacher_review = data['review']
                                db.session.commit() 
                                return "Reviewed successfully" 
                        else:
                            return abort(400, {'message': "Access denied"})     
                    elif(is_company(current_user)):
                        if(work.done.company_id == current_user.id):
                            new_rating = Rating(work_id=data['work_id'], 
                                company_review=data['review']) 
                            db.session.add(new_rating) 
                            db.session.commit() 
                            return "Reviewed successfully" 
                        else:
                            return abort(400, {'message': "Access denied"})  
                    elif(is_teacher(current_user)):
                        if(work.teachers_id == current_user.id):
                            new_rating = Rating(work_id=data['work_id'], 
                                teacher_review=data['review']) 
                            db.session.add(new_rating) 
                            db.session.commit() 
                            return "Reviewed successfully" 
                        else:
                            return abort(400, {'message': "Access denied"})  
                    
                except:
                    message = "Work not created"
            else: 
                message += "Form is missing"

        else:
            message = "Access Denied"
        
        return abort(400, {'message': message})

