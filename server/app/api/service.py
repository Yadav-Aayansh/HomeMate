# HomeMate/server/app/api/service.py

from flask import request
from flask_restful import Resource
from ..models import Service, User
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from ..custom import role_required
from .. import db

class ServiceApi(Resource):    
    def get(self):
        verify_jwt_in_request(optional=True)
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(username=current_user).first()
        except Exception:
            pass
        
        data = request.args
        if user:
            if user.role == 'Admin':
                category = data.get('category')
                if category:
                    result = Service.query.filter_by(category=category).all()
                    if result:
                        services = [
                            {
                                'service_id': service.service_id,
                                'name': service.name,
                                'base_price': str(service.base_price),
                                'time_required': service.time_required,
                                'description': service.description,
                                'category': service.category,
                                'created_at': service.created_at.isoformat(),
                                'updated_at': service.updated_at.isoformat()
                            }
                            for service in result
                        ]
                    return services, 200
                result = Service.query.with_entities(Service.category).distinct().all()
                categories = [category[0] for category in result]
                return {'Service Categories': categories}, 200
        service_type = data.get('service_type')
        if service_type:
            service_type_exist = Service.query.filter_by(name=service_type).first()
            if service_type_exist:
                response = {'Service ID': service_type_exist.service_id,
                            'Service Category': service_type_exist.category,
                            'Service Fee': str(service_type_exist.base_price),
                            'Service Time Required': service_type_exist.time_required,
                            'Service Description': service_type_exist.description}
                return response, 200
            return {'message': 'Service does not exist!'}, 400
        category = data.get('category')
        if category:
            result = Service.query.filter_by(category=category).with_entities(Service.name).all()
            if result:
                services = [service[0] for service in result]
                return {'Services': services}, 200
            return {'message': 'Category does not exist!'}, 400
        # Distinct = Unique Values Only,
        result = Service.query.with_entities(Service.category).distinct().all()
        categories = [category[0] for category in result]
        return {'Service Categories': categories}, 200
        

    @jwt_required()
    @role_required('Admin')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        base_price = data.get('base_price')
        time_required = data.get('time_required')
        description = data.get('description')
        category = data.get('category')

        if name is None:
            return {'message' : 'Service Name is required!'}, 400
        
        if base_price is None:
            return {'message' : 'Base Price is required!'}, 400
        
        if time_required is None:
            return {'message' : 'Service Required-Time is required!'}, 400
        
        if description is None:
            return {'message' : 'Description is required!'}, 400
        
        if category is None:
            return {'message' : 'Category is required!'}, 400
        
        try:
            exist = Service.query.filter_by(name=name).first()
            if exist:
                return {'message': 'Service already exist!'}, 409
            
            new_service = Service(name=name, base_price=base_price, time_required=time_required, description=description, category=category)
            db.session.add(new_service)
            db.session.commit()
            return {'message': 'Service added successfully!'}, 200
        
        except:
            return {'message': 'Something went wrong!'}, 500
        

    @jwt_required()
    @role_required('Admin')
    def put(self, service_id):
        data = request.get_json()
        name = data.get('name')
        base_price = data.get('base_price')
        time_required = data.get('time_required')
        description = data.get('description')
        category = data.get('category')

        if name is None:
            return {'message': 'Service Name is required!'}, 400

        if base_price is None:
            return {'message': 'Base Price is required!'}, 400

        if time_required is None:
            return {'message': 'Service Required-Time is required!'}, 400

        if description is None:
            return {'message': 'Description is required!'}, 400

        if category is None:
            return {'message': 'Category is required!'}, 400

        try:
            service = Service.query.get(service_id)
            if not service:
                return {'message': 'Service not found!'}, 404

            service.name = name
            service.base_price = base_price
            service.time_required = time_required
            service.description = description
            service.category = category

            db.session.commit()
            return {'message': 'Service updated successfully!'}, 200

        except:
            return {'message': 'Something went wrong!'}, 500
        

    @jwt_required()
    @role_required('Admin')
    def delete(self, service_id):
        try:
            service = Service.query.get(service_id)
            if not service:
                return {'message': 'Service not found!'}, 404

            db.session.delete(service)
            db.session.commit()
            return {'message': 'Service deleted successfully!'}, 200

        except:
            return {'message': 'Something went wrong!'}, 500