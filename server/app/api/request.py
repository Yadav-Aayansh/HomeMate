# HomeMate/server/app/api/request.py

from flask import request
from flask_restful import Resource
from ..models import ServiceRequest, User
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from ..custom import role_required, IndianZone
from .. import db


class ServiceRequestApi(Resource):
    @jwt_required()
    def get(self, service_request_id=None):
        token = request.cookies.get('access_token_cookie')
        filter = request.args.get('filter', 'Requested')
        decoded_token = decode_token(token)
        current_user = get_jwt_identity()
        if decoded_token.get('role') == 'Customer':
            try:
                if service_request_id:
                    service_request = ServiceRequest.query.get_or_404(service_request_id)
                    return {
                        'service_request_id': service_request.service_request_id,
                        'service_id': service_request.service_id,
                        'customer_id': service_request.customer_id,
                        'service_professional_id': service_request.service_professional_id,
                        'request_date': service_request.request_date.isoformat(),
                        'completion_date': service_request.completion_date.isoformat() if service_request.completion_date else None,
                        'status': service_request.status,
                        'remarks': service_request.remarks,
                        'priority': service_request.priority,
                        'address': service_request.address,
                        'pincode': service_request.pincode,
                        'payment_status': service_request.payment_status,
                        'cancellation_reason': service_request.cancellation_reason,
                        'updated_at': service_request.updated_at.isoformat()
                    }, 200
            
                is_user = User.query.filter_by(username=current_user).first()
                service_requests = [req for req in is_user.customer.service_requests if req.status == filter]
                response = [
                    {'service_request_id': service_request.service_request_id,
                    'service': service_request.service.name,
                    'service_professional': service_request.service_professional.name,
                    'request_date': service_request.request_date.isoformat(),
                    'completion_date': service_request.completion_date.isoformat() if service_request.completion_date else None,
                    'status': service_request.status,
                    'remarks': service_request.remarks,
                    'priority': service_request.priority,
                    'address': service_request.address,
                    'pincode': service_request.pincode,
                    'review': len(service_request.review),
                    'payment_status': service_request.payment_status,
                    'cancellation_reason': service_request.cancellation_reason,
                    'updated_at': service_request.updated_at.isoformat()}
                    for service_request in service_requests
                ]
                return response, 200
            except Exception as e:
                return {'message': 'Something went wrong!{e}'}, 500
            
        elif decoded_token.get('role') == 'Professional':
            try:
                if service_request_id:
                    service_request = ServiceRequest.query.get_or_404(service_request_id)
                    return {
                        'service_request_id': service_request.service_request_id,
                        'service_id': service_request.service_id,
                        'customer_id': service_request.customer_id,
                        'service_professional_id': service_request.service_professional_id,
                        'request_date': service_request.request_date.isoformat(),
                        'completion_date': service_request.completion_date.isoformat() if service_request.completion_date else None,
                        'status': service_request.status,
                        'remarks': service_request.remarks,
                        'priority': service_request.priority,
                        'address': service_request.address,
                        'pincode': service_request.pincode,
                        'payment_status': service_request.payment_status,
                        'cancellation_reason': service_request.cancellation_reason,
                        'updated_at': service_request.updated_at.isoformat()
                    }, 200
            
                is_user = User.query.filter_by(username=current_user).first()
                service_requests = [req for req in is_user.service_professional.service_requests if req.status == filter]
                response = [
                    {'service_request_id': service_request.service_request_id,
                    'service': service_request.service.name,
                    'customer': service_request.customer.name,
                    'request_date': service_request.request_date.isoformat(),
                    'completion_date': service_request.completion_date.isoformat() if service_request.completion_date else None,
                    'status': service_request.status,
                    'remarks': service_request.remarks,
                    'priority': service_request.priority,
                    'address': service_request.address,
                    'pincode': service_request.pincode,
                    'payment_status': service_request.payment_status,
                    'cancellation_reason': service_request.cancellation_reason,
                    'updated_at': service_request.updated_at.isoformat()}
                    for service_request in service_requests
                ]
                return response, 200
            except Exception as e:
                return {'message': 'Something went wrong!'}, 500

        elif decoded_token.get('role') == 'Admin':
            try:
                if service_request_id:
                    service_request = ServiceRequest.query.get_or_404(service_request_id)
                    return {
                        'service_request_id': service_request.service_request_id,
                        'service_id': service_request.service_id,
                        'customer_id': service_request.customer_id,
                        'service_professional_id': service_request.service_professional_id,
                        'request_date': service_request.request_date.isoformat(),
                        'completion_date': service_request.completion_date.isoformat() if service_request.completion_date else None,
                        'status': service_request.status,
                        'remarks': service_request.remarks,
                        'priority': service_request.priority,
                        'address': service_request.address,
                        'pincode': service_request.pincode,
                        'payment_status': service_request.payment_status,
                        'cancellation_reason': service_request.cancellation_reason,
                        'updated_at': service_request.updated_at.isoformat()
                    }, 200
            
                service_requests = ServiceRequest.query.filter_by(status=filter)
                response = [
                    {'service_request_id': service_request.service_request_id,
                    'service': service_request.service.name,
                    'customer': service_request.customer.name,
                    'service_professional': service_request.service_professional.name,
                    'request_date': service_request.request_date.isoformat(),
                    'completion_date': service_request.completion_date.isoformat() if service_request.completion_date else None,
                    'status': service_request.status,
                    'remarks': service_request.remarks,
                    'priority': service_request.priority,
                    'address': service_request.address,
                    'pincode': service_request.pincode,
                    'payment_status': service_request.payment_status,
                    'cancellation_reason': service_request.cancellation_reason,
                    'updated_at': service_request.updated_at.isoformat()}
                    for service_request in service_requests
                ]
                return response, 200
            except Exception as e:
                return {'message': 'Something went wrong!'}, 500
            
        else:
            return {'message': 'Illegal request!'}, 400

        

    def post(self):
        data = request.get_json()
        service_id = data.get('service_id')
        customer_id = data.get('customer_id')
        service_professional_id = data.get('service_professional_id')
        address = data.get('address')
        pincode = data.get('pincode')

        if service_id is None:
            return {'message': 'Service ID is required!'}, 400
        if customer_id is None:
            return {'message': 'Customer ID is required!'}, 400
        if service_professional_id is None:
            return {'message': 'Service Professional ID is required!'}, 400
        if address is None:
            return {'message': 'Address is required!'}, 400
        if pincode is None:
            return {'message': 'Pincode is required!'}, 400

        remarks = data.get('remarks')
        priority = data.get('priority', 'Medium')

        service_request = ServiceRequest(
            service_id=service_id,
            customer_id=customer_id,
            service_professional_id=service_professional_id,
            address=address,
            pincode=pincode,
            remarks=remarks,
            priority=priority
        )
        db.session.add(service_request)
        db.session.commit()

        return {"message": "Service request created successfully"}, 201

    @jwt_required()
    def put(self, service_request_id):
        service_request = ServiceRequest.query.get_or_404(service_request_id)
        token = request.cookies.get('access_token_cookie')
        decoded_token = decode_token(token)
        current_user = get_jwt_identity()
        data = request.get_json()
        if decoded_token.get('role') == 'Customer':
            try:
                customer = User.query.filter_by(username=current_user).first().customer
                if service_request.customer_id != customer.customer_id:
                    return {'message': 'Illegal request!'}, 400
                
                if 'status' in data:
                    if data['status'] == 'Cancelled':
                        service_request.status = data['status']
                        service_request.cancellation_reason = data.get('cancellation_reason')
                        db.session.commit()
                        return {"message": "Service request cancelled!"}, 200
                if 'priority' in data:
                    service_request.priority = data['priority']
                if 'address' in data:
                    if data['address'] == '':
                        return {'message': 'Address is required!'}, 400
                    service_request.address = data['address']
                if 'pincode' in data:
                    if data['pincode'] == '':
                        return {'message': 'Pincode is required!'}, 400
                    service_request.pincode = data['pincode']
                if 'remarks' in data:
                    service_request.remarks = data['remarks']

                db.session.commit()
                return {"message": "Service request updated successfully"}, 200
            except:
                pass

        elif decoded_token.get('role') == 'Professional':
            try:
                professional = User.query.filter_by(username=current_user).first().service_professional
                if service_request.service_professional_id != professional.service_professional_id:
                    return {'message': 'Illegal request!'}, 400
                
                if 'status' in data:
                    if data['status'] == 'Completed':
                        now = IndianZone()
                        service_request.completion_date = now
                    service_request.status = data['status']
                  
                db.session.commit()
                return {"message": "Service request updated successfully"}, 200  
            except Exception as e:
                return {'message': f'Something went wrong!{e}'}, 500
        
        else:
            return {'message': 'Illegal request!'}, 400
    
    @jwt_required()
    @role_required('Admin')
    def delete(self, service_request_id):
        try:
            request = ServiceRequest.query.get(service_request_id)
            db.session.delete(request)
            db.session.commit()
            return {"message": "Service request deleted successfully"}, 200  
        except Exception as e:
            return {'message': f'Something went wrong!{e}'}, 500


        
        
        # if 'completion_date' in data:
        #     service_request.completion_date = datetime.fromisoformat(data['completion_date'])
        
        # if 'remarks' in data:
        #     service_request.remarks = data['remarks']
        


        # if 'payment_status' in data:
        #     service_request.payment_status = data['payment_status']

        # db.session.commit()
        
        # return {"message": "Service request updated successfully"}, 200