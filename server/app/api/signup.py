# HomeMate/server/app/api/signup.py

from flask_restful import Resource
from flask import request
from ..models import User, OAuth
from .. import db
from ..custom import is_valid_email, is_valid_username

class SignupApi(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')

        if email is None:
            return {'message': 'Email address is required!'}, 400
        
        email = data.get('email').lower()
        if not is_valid_email(email):
            return {'message': 'Email address is invalid!'}, 400

        email_checker = bool(User.query.filter_by(email=email).first())
        if email_checker:
            return {'message': 'Email address is already in use!'}, 400
        
        if username is None:
            return {'message': 'Username is required!'}, 400
        
        username = data.get('username').lower()
        if not is_valid_username(username):
            return {'message': 'Username is invalid!'}, 400
        
        username_checker = bool(User.query.filter_by(username=username).first())
        if username_checker:
            return {'message': 'Username already taken!'}, 400
        
        role = data.get('role')
        if role not in ['Admin', 'Customer', 'Professional']:
            return {'message': 'Invalid role!'}, 400
        
        oauth_user = data.get('oauth_user')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if oauth_user:
            platform = data.get('platform')
            unique_id = data.get('unique_id')
            if platform not in ["Google", "Facebook", "Microsoft"]:
                return {'message': 'Unknown user identity!'}, 400
            if unique_id is None:
                return {'message': f'{platform} ID is required!'}, 400
                    
        if not oauth_user and password is None:
            return {'message': 'Password is required!'}, 400

        if password and not confirm_password:
            return {'message': 'Confirm Password is required!'}, 400
        
        if not password and confirm_password:
            return {'message': 'Password is required!'}, 400
        
        if password and confirm_password:
            if len(password) < 8 or len(confirm_password) < 8:
                return {'message': 'Password must be at least 8 characters!'}, 400
            if password != confirm_password:
                return {'message': 'Password and Confirm Password must be same!'}, 400
        
        try:
            new_user = User(email=email, username=username, role=role, oauth_user=oauth_user)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush()
            if oauth_user:
                exist_oauth = OAuth.query.filter_by(unique_id=unique_id).first()
                if exist_oauth:
                    return {'message': 'User already exist!'}, 400
                try:
                    new_oauth = OAuth(user_id=new_user.user_id, platform=platform, unique_id=unique_id)
                    db.session.add(new_oauth)
                    db.session.flush()
                except Exception as e:
                    db.session.rollback()
                    return {'message' : f'An error occurred str{e}'}, 500
            response = new_user.additional_commit(data)
            if response:
                db.session.rollback()
                return response
            db.session.commit()
            return {'message' : 'Signup successful!'}, 200

        except Exception as e:
            return {'message' : f'An error occurred str{e}'}, 500

