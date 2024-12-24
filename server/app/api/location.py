# HomeMate/server/app/api/location.py

from flask_restful import Resource
from flask import request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class AutoCompleteApi(Resource):
    def get(self):
        query = request.args.get('q')
        if not query:
            return {"message": "Query parameter is required"}, 400
        
        API_KEY = os.getenv('LOCATION_API_KEY')
        url = 'https://autocomplete.search.hereapi.com/v1/autocomplete'
        
        params = {
            'q': query,
            'apiKey': API_KEY,
            'in': 'countryCode:IND'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            items = response.json().get('items')
            address_list = {'result': [{'address': item['address']['label'], 'pincode': item['address']['postalCode']}
                for item in items]}
            return address_list, 200
        else:
            return {"error": response.json()}, response.status_code
        

class PincodeToCityApi(Resource):
    def get(self):
        query = request.args.get('q')
        if not query:
            return {"message": "Query parameter is required"}, 400
        
        API_KEY = os.getenv('LOCATION_API_KEY')
        url = 'https://autocomplete.search.hereapi.com/v1/autocomplete'
        
        params = {
            'q': query,
            'apiKey': API_KEY,
            'in': 'countryCode:IND',
            'types': 'postalCode'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            items = response.json().get('items')
            city_list = {'result': [{'city': item['address']['city']}
                for item in items]}
            return city_list, 200
        else:
            return {"error": response.json()}, response.status_code