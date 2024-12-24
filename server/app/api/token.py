# HomeMate/server/app/api/token.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required

class TokenApi(Resource):
    @jwt_required()
    def get(self):
        token = request.cookies.get('access_token_cookie')
        response = {'message': 'Token verified!', 'token': token}
        return response, 200
        

        



