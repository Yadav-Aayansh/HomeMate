# HomeMate/server/app/api/logout.py

from flask_restful import Resource
from flask_jwt_extended import unset_access_cookies
from flask import make_response

class LogoutApi(Resource):
    def get(self):
        response = make_response({"message": "Logged out successfully!"})
        unset_access_cookies(response)
        return response