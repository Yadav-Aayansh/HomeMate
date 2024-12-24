# HomeMate/server/app/api/signup.py

from flask_restful import Resource
from flask import request
from ..models import Review
from .. import db
from ..custom import role_required
from flask_jwt_extended import jwt_required

class ReviewApi(Resource):
    @jwt_required()
    def get(self, service_request_id):
        try:
            review = Review.query.filter_by(service_request_id=service_request_id).first()
            if review:
                return {'rating': str(review.rating), 'review_text': review.review_text}, 200
            return {}, 200
        except:
            return {'message' : "Something went wrong!"}, 500
    
    @jwt_required()
    @role_required('Customer')
    def put(self, service_request_id):
        data = request.json
        rating = data.get('rating')
        review_text = data.get('review_text')
        try: 
            exist = Review.query.filter_by(service_request_id=service_request_id).first()
            if exist:
                exist.rating = rating
                exist.review_text = review_text 
            else:
                new_review = Review(service_request_id=service_request_id, rating=rating, review_text=review_text)
                db.session.add(new_review)
            
            db.session.commit()
            return {'message': 'Review added!'}, 200
        except Exception as e:
            return {'message': f'Something went wrong!{e}'}, 500