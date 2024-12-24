# HomeMate/server/app/api/oauth.py

from flask_restful import Resource
import os
from dotenv import load_dotenv
from flask import request, redirect, make_response
import requests
from ..models import Customer, ServiceProfessional
import urllib.parse

load_dotenv()

class GoogleAuthSignupApi(Resource):
    def get(self):
        token_generator_url = 'https://oauth2.googleapis.com/token'
        user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        FRONTEND_URL = os.getenv('FRONTEND_URL')
        BACKEND_URL = os.getenv('BACKEND_URL')

        data = {
            'code': request.args.get('code'),
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': f'{BACKEND_URL}/api/signup/google-oauth',
            'grant_type': 'authorization_code'
        }

        token_response = requests.post(token_generator_url, data=data)
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        state = request.args.get('state')
        role = state.split('=')[1]

        if role == 'Customer':
            rows = Customer.query.count()
            username = f'customer{rows+1}'
        else:
            rows = ServiceProfessional.query.count()
            username = f'professional{rows+1}'

        name = urllib.parse.unquote(user_info['name'])
        query = f'role={role}&username={username}&email={user_info['email']}&name={name}&platform=Google&unique_id={user_info['sub']}'
        return redirect(f'{FRONTEND_URL}/signup/additional-info?{query}')
    

class GoogleAuthLoginApi(Resource):
    def get(self):
        token_generator_url = 'https://oauth2.googleapis.com/token'
        user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        FRONTEND_URL = os.getenv('FRONTEND_URL')
        BACKEND_URL = os.getenv('BACKEND_URL')

        data = {
            'code': request.args.get('code'),
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': f'{BACKEND_URL}/api/login/google-oauth',
            'grant_type': 'authorization_code'
        }

        try:
            token_response = requests.post(token_generator_url, data=data)
            token_json = token_response.json()
            access_token = token_json.get('access_token')

            headers = {'Authorization': f'Bearer {access_token}'}
            user_info_response = requests.get(user_info_url, headers=headers)
            user_info = user_info_response.json()

            credentials = f'oauth_user=True&user_mail={user_info['email']}&platform=Google&unique_id={user_info['sub']}'
            return redirect(f'{FRONTEND_URL}/login?{credentials}')
        
        except Exception:
            error = 'Something went wrong!'
            return redirect(f'{FRONTEND_URL}/login?error={error}')
        

class FacebookAuthSignupApi(Resource):
    def get(self):
        token_generator_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
        user_info_url = 'https://graph.facebook.com/v12.0/me'
        FRONTEND_URL = os.getenv('FRONTEND_URL')
        BACKEND_URL = os.getenv('BACKEND_URL')

        data = {
            'code': request.args.get('code'),
            'client_id': os.getenv('FACEBOOK_CLIENT_ID'),
            'client_secret': os.getenv('FACEBOOK_CLIENT_SECRET'),
            'redirect_uri': f'{BACKEND_URL}/api/signup/facebook-oauth',
        }

        token_response = requests.get(token_generator_url, params=data)
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        params = {'fields': 'id,name,email', 'access_token': access_token}
        user_info_response = requests.get(user_info_url, params=params)
        user_info = user_info_response.json()

        state = request.args.get('state')
        role = state.split('=')[1]

        if role == 'Customer':
            rows = Customer.query.count()
            username = f'customer{rows+1}'
        else:
            rows = ServiceProfessional.query.count()
            username = f'professional{rows+1}'

        name = urllib.parse.unquote(user_info['name'])
        query = f'role={role}&username={username}&email={user_info["email"]}&name={name}&platform=Facebook&unique_id={user_info["id"]}'
        return redirect(f'{FRONTEND_URL}/signup/additional-info?{query}')


class FacebookAuthLoginApi(Resource):
    def get(self):
        token_generator_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
        user_info_url = 'https://graph.facebook.com/v12.0/me'
        FRONTEND_URL = os.getenv('FRONTEND_URL')
        BACKEND_URL = os.getenv('BACKEND_URL')

        data = {
            'code': request.args.get('code'),
            'client_id': os.getenv('FACEBOOK_CLIENT_ID'),
            'client_secret': os.getenv('FACEBOOK_CLIENT_SECRET'),
            'redirect_uri': f'{BACKEND_URL}/api/login/facebook-oauth',
        }

        try:
            token_response = requests.get(token_generator_url, params=data)
            token_json = token_response.json()
            access_token = token_json.get('access_token')

            params = {'fields': 'id,email', 'access_token': access_token}
            user_info_response = requests.get(user_info_url, params=params)
            user_info = user_info_response.json()

            credentials = f'oauth_user=True&user_mail={user_info["email"]}&platform=Facebook&unique_id={user_info["id"]}'
            return redirect(f'{FRONTEND_URL}/login?{credentials}')
        
        except Exception:
            error = 'Something went wrong!'
            return redirect(f'{FRONTEND_URL}/login?error={error}')

            