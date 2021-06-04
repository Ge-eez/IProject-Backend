from flask import Blueprint, session, request, jsonify, abort
from functools import wraps
from flaskapp import db, api, pagination
from flask_login import current_user
from flask_restful import Resource
from flaskapp.routes import *


from flaskapp.models import *

class PaymentAPI(Resource):
        
    def get(self, id=None):
        message = ""
        if(logged_in(current_user)):
            if(id):
                pay = Payment.query.filter_by(id=id)
                payment = rate.first()
                if(payment):
                    if(is_student(current_user) and not(payment.pays.student_id == current_user.id)):
                        abort(400, {'message': "Access denied"}) 
                    return pagination.paginate(pay, payment_fields)
                else:
                    message = "Payment not found"
            else:
                if(is_student(current_user)):
                    payments = Payment.query.join(Work, Work.student_id == current_user.id)
                else:
                    payments = Rating.query.all()
                if(payments):
                    return pagination.paginate(payments, payment_fields)
                else:
                    message = "Payments not available"

        else:
            message = "Access Denied"
        
        abort(400, {'message': message})

    def post(self):
        message = ""
        if(is_company(current_user)):
            data = request.form
            if(data and data.get('work_id')  
                and data.get('price')):
                
                try:
                    work = Work.query.filter_by(id=data['work_id']).first()
                    if(work.done.company_id == current_user.id):
                        new_payment = Payment(work_id=data['work_id'], 
                            price=data['price']) 
                        db.session.add(new_payment) 
                        db.session.commit() 
                        return "Paid successfully" 
                    else:
                        abort(400, {'message': "Access denied"})  
                    
                except:
                    message = "Payment not created"
            else: 
                message += "Form is missing"

        else:
            message = "Access Denied"
        
        abort(400, {'message': message})
