# HomeMate/server/app/api/home.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from ..custom import role_required
from ..models import Customer
from .. import db, cache

class CustomerApi(Resource):
    @jwt_required()
    @role_required('Admin')
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        limit = 10
        offset = request.args.get('offset', 0)

        is_ban = request.args.get('is_ban')
        name = request.args.get('name')
        query = Customer.query
        if is_ban:
            query = query.filter_by(is_ban=(is_ban == 'True'))
        if name:
            query = query.filter(Customer.name.ilike(f"%{name}%"))
        
        total_customers = query.count()
        customers = query.offset(offset).limit(limit).all()

        customers_list = [{
                'customer_id': customer.customer_id,
                'name': customer.name,
                'address': customer.address,
                'pincode': customer.pincode,
                'requests': len(customer.service_requests),
                'username': customer.user.username,
                'email': customer.user.email,
                'is_ban': customer.is_ban
        } for customer in customers]

        has_more = total_customers > (offset+limit)

        return {"has_more": has_more, "customers": customers_list}, 200
    
    @jwt_required()
    @role_required('Admin')
    def put(self, customer_id):
        cache.clear()
        try:
            customer = Customer.query.get(customer_id)
            customer.is_ban = not customer.is_ban
            db.session.commit()
            return {'message': 'Action applied successfully!'}, 200
        except Exception as e:
            return {'message': f'Something went wrong!'}, 500