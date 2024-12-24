# HomeMate/server/app/api/payment.py

from flask_restful import Resource
from flask import request
import os
from dotenv import load_dotenv
import razorpay
from flask_jwt_extended import jwt_required
from ..custom import role_required
from ..models import ServiceRequest
from .. import db

load_dotenv()
razorpay_client = razorpay.Client(auth=(os.getenv('RAZORPAY_CLIENT_ID'), os.getenv('RAZORPAY_ACCESS_KEY')))

class PaymentApi(Resource):
    def get(self):
        service_request_id = request.args.get('service_request_id')
        if service_request_id:
            service_request = ServiceRequest.query.get_or_404(service_request_id)
            fee = service_request.service_professional.fee
            time_required = service_request.service.time_required
            format = time_required.split(' ')[1]
            time_required = time_required.split(' ')[0]
            if format == 'hours':
                total = float(fee) * float(time_required)
            if format == 'minutes':
                total = float(fee) * (float(time_required) / 60)

            additional = {'fee': str(fee), 'time_required': f'{time_required} {format}', 'total': str(total)}
            amount = total * 100
            currency = 'INR'
            order_data = {
                'amount': amount,
                'currency': currency,
                'payment_capture': '1'
            }
            order = razorpay_client.order.create(data=order_data)
            return {'order': order, 'additional': additional}, 200
        
        return {'message': 'Service Request ID is required!'}, 400
    
    @jwt_required()
    @role_required('Customer')    
    def post(self):
        data = request.json
        required_fields = ['service_request_id', 'payment_id', 'order_id', 'signature']
        for field in required_fields:
            if not data.get(field):
                return f"{field} is required!", 400
        try:
            service_request_id = data['service_request_id']
            payment_id = data['payment_id']
            order_id = data['order_id']
            signature = data['signature']

            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            razorpay_client.utility.verify_payment_signature(params_dict)

            payment = razorpay_client.payment.fetch(payment_id)
            if payment['status'] == 'captured':
                service_request = ServiceRequest.query.get_or_404(service_request_id)
                service_request.payment_status = True
                db.session.commit()

                return {'message': 'Payment successful!'}, 200
            else:
                return {'message': 'Payment not successful.'}, 400

        except:
            return {'message': 'Something went wrong!'}, 500