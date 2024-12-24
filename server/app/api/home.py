# HomeMate/server/app/api/home.py

from flask_restful import Resource
from flask import Response

HomePage = """
<h1>Hello From api.homemate.com</h1>
<h3>127.0.3.1 -- api.homemate.com</h3>
<h3>Https + SSL Certified</h3>
"""

class HomeApi(Resource):
    def get(self):
        return Response(HomePage, mimetype='text/html')
