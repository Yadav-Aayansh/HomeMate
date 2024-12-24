# HomeMate/server/app/api/login.py

from flask_restful import Resource
from flask import request, make_response, render_template
from ..models.user import User
from ..models.oauth import OAuth
from ..custom import is_valid_email
from .. import db
from flask_jwt_extended import create_access_token, set_access_cookies, decode_token
import time
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_DOMAIN = os.getenv('BACKEND_DOMAIN')
FRONTEND_URL = os.getenv('FRONTEND_URL')

class LoginApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_mail = data.get('user_mail').lower()
            password = data.get('password')
            oauth_user = data.get('oauth_user')
            if oauth_user:
                platform = data.get('platform')
                unique_id = data.get('unique_id')
                user = User.query.filter_by(email=user_mail).first()
                if user:
                    if self.ban_checker(user):
                        return {'message': 'Your Account is banned!'}, 400
                    oauth_user = OAuth.query.filter_by(user_id=user.user_id).first()
                    if not oauth_user:
                        platform = data.get('platform')
                        unique_id = data.get('unique_id')
                        if platform not in ["Google", "Facebook", "Microsoft"]:
                            return {'message': 'Unknown user identity!'}, 400
                        if unique_id is None:
                            return {'message': f'{platform} ID is required!'}, 400
                        
                        oauth_user = OAuth(user_id=user.user_id, platform=platform, unique_id=unique_id)
                        db.session.add(oauth_user)
                        db.session.commit()
                    if oauth_user.platform == platform and oauth_user.unique_id == unique_id:
                        addon = {'role': user.role, 'email': user_mail}
                        if user.role == 'Customer':
                            addon['pincode'] = user.customer.pincode
                        token = create_access_token(identity=user.username, additional_claims=addon)
                        response = make_response({'message': 'Logged in successfully!'})
                        set_access_cookies(response, token)
                        return response
                return {'message': 'Account does not exist!'}, 404
            else:
                user_exist_username = User.query.filter_by(username=user_mail).first()
                user_exist_mail = User.query.filter_by(email=user_mail).first()
                if user_exist_username:
                    if self.ban_checker(user_exist_username):
                        return {'message': 'Your Account is banned!'}, 400
                    if user_exist_username.check_password(password):
                        addon = {'role': user_exist_username.role, 'email': user_exist_username.email }
                        if user_exist_username.role == 'Customer':
                            addon['pincode'] = user_exist_username.customer.pincode
                        token = create_access_token(identity=user_mail, additional_claims=addon)
                        response = make_response({'message': 'Logged in successfully!'})
                        set_access_cookies(response, token)
                        return response
                    return {'message': 'Invalid username or password'}, 401            
                elif user_exist_mail:
                    if self.ban_checker(user_exist_mail):
                        return {'message': 'Your Account is banned!'}, 400
                    if user_exist_mail.check_password(password):
                        addon = {'role': user_exist_mail.role, 'email': user_mail }
                        if user_exist_mail.role == 'Customer':
                            addon['pincode'] = user_exist_mail.customer.pincode
                        token = create_access_token(identity=user_exist_mail.username, additional_claims=addon)
                        response = make_response({'message': 'Logged in successfully!'})
                        set_access_cookies(response, token)
                        return response
                    return {'message': 'Invalid username or password'}, 401
                else:
                    return {'message': 'Account does not exist!'}, 404
            
        except Exception as e:
            return {'message': f'Something went wrong!'}
        
    def ban_checker(self, user):
        if user.role == 'Customer':
            if user.customer.is_ban:
                return True
        elif user.role == 'Professional':
            if user.service_professional.is_ban:
                return True
        return False
        

class ResetPasswordApi(Resource):
    def get(self):
        from ..tasks.template import send_email
        email = request.args.get('email')
        if email is None:
            return {'message': 'Email is required to reset the password!'}, 400
        
        if not is_valid_email(email):
            return {'message': 'Email address is invalid!'}, 400
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))
                link = f"{FRONTEND_URL}/reset-password?token={token}"
                body = render_template('reset.html', link=link)
                subject = "Reset Your Password"
                send_email(email, subject, body, is_html=True)
            return {'message': 'If an account associated with this email address exists, a password reset link will be dispatched to this address.'}, 200
        except Exception as e:
            return {'message': f'Something went wrong!'}, 500
        

    def post(self):
        data = request.get_json()
        token = data.get('token')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password is None:
            return {'message': 'Password is required!'}, 400
        if confirm_password is None:
            return {'message': 'Confirm Password is required!'}, 400
        
        if password and confirm_password:
            if len(password) < 8 or len(confirm_password) < 8:
                return {'message': 'Password must be at least 8 characters!'}, 400
            if password != confirm_password:
                return {'message': 'Password and Confirm Password must be same!'}, 400

        if token is None:
            return {'message': 'Unauthorized attempt!'}, 400
        
        try:
            decoded_token = decode_token(token)
            exp_time = decoded_token['exp']
            current_time = int(time.time())
            if current_time > exp_time :
                return {'message': 'Reset Link expired!'}, 400
            
            email = decoded_token['sub']
            user = User.query.filter_by(email=email).first()
            if not user:
                return {'message': 'Unauthorized attempt!'}, 400
            
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'Password updated successfully!'}, 200
            
        except:
            return {'message': 'Unauthorized attempt!'}, 400

            

