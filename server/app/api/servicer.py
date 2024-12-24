# HomeMate/server/app/api/servicer.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required, decode_token
from flask import request
from ..models import ServiceProfessional, ServiceablePincode
from .. import db, cache
from ..custom import role_required

class ServicerApi(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self, servicer_id=None):
        if servicer_id:
            service_professional = ServiceProfessional.query.get(servicer_id)
            if not service_professional:
                return {'message': 'Service Professional not found!'}
            
            return {
                'service_professional_id': service_professional.service_professional_id,
                'name': service_professional.name,
                'description': service_professional.description,
                'experience': float(service_professional.experience),
                'profile_picture': service_professional.profile_picture,
                'work_done': service_professional.work_done,
                'rating': float(service_professional.rating),
                'fee': str(service_professional.fee) if service_professional.fee else None,
                'availability': service_professional.availability
            }, 200


        limit = 10
        offset = request.args.get('offset', 0)
        pincode = request.args.get('pincode')
        service_type = request.args.get('service_type')
        experience = request.args.get('experience', 0)
        fee_min = request.args.get('fee_min', 0)
        fee_max = request.args.get('fee_max', 99999999.99)
        sort_by = request.args.get('sort_by', '')
        availability = request.args.get('availability')
        profile_verified = request.args.get('profile_verified')
        is_ban = request.args.get('is_ban')

        token = request.cookies.get('access_token_cookie')
        decoded_token = decode_token(token)
        if decoded_token.get('role') == 'Admin':
            query = ServiceProfessional.query
            if profile_verified:
                query = query.filter_by(profile_verified=(profile_verified == 'True'))
            if is_ban:
                query = query.filter_by(is_ban=(is_ban == 'True'))
            if pincode:
                query = query.filter(ServiceProfessional.serviceable_pincodes.any(ServiceablePincode.pincode.ilike(f"%{pincode}%")))
            if service_type:
                query = query.filter(ServiceProfessional.service_type.ilike(f"%{service_type}%"))
            if experience:
                query = query.filter(ServiceProfessional.experience>=experience)
            if fee_min:
                query = query.filter(ServiceProfessional.fee>=fee_min)
            if fee_max:
                query = query.filter(ServiceProfessional.fee<=fee_max)
            if availability:
                query = query.filter_by(availability=availability)
            

            if sort_by and sort_by != 'feeHigh':
                query = query.order_by(getattr(ServiceProfessional, sort_by).desc())
            else:
                query = query.order_by(ServiceProfessional.fee)

            total_professionals = query.count()
            professionals = query.offset(offset).limit(limit).all()

            professionals_list = [{
                'service_professional_id': professional.service_professional_id,
                'name': professional.name,
                'description': professional.description,
                'experience': float(professional.experience),
                'profile_picture': professional.profile_picture,
                'work_done': professional.work_done,
                'rating': float(professional.rating),
                'fee': str(professional.fee) if professional.fee else None,
                'availability': professional.availability,
                'identity_proof': professional.identity_proof,
                'profile_verified': professional.profile_verified,
                'is_ban': professional.is_ban
            } for professional in professionals]

            has_more = total_professionals > (offset+limit)

            return {"has_more": has_more, "professionals": professionals_list}, 200
        
        else:
            query = ServiceProfessional.query.filter_by(profile_verified=True, is_ban=False)
            if pincode:
                query = query.filter(ServiceProfessional.serviceable_pincodes.any(ServiceablePincode.pincode.ilike(f"%{pincode}%")))
            if service_type:
                query = query.filter(ServiceProfessional.service_type.ilike(f"%{service_type}%"))
            if experience:
                query = query.filter(ServiceProfessional.experience>=experience)
            if fee_min:
                query = query.filter(ServiceProfessional.fee>=fee_min)
            if fee_max:
                query = query.filter(ServiceProfessional.fee<=fee_max)
            if availability:
                query = query.filter_by(availability=availability)

            if sort_by and sort_by != 'feeHigh':
                query = query.order_by(getattr(ServiceProfessional, sort_by).desc())
            else:
                query = query.order_by(ServiceProfessional.fee)

            total_professionals = query.count()
            professionals = query.offset(offset).limit(limit).all()

            professionals_list = [{
                'service_professional_id': professional.service_professional_id,
                'name': professional.name,
                'description': professional.description,
                'experience': float(professional.experience),
                'profile_picture': professional.profile_picture,
                'work_done': professional.work_done,
                'rating': float(professional.rating),
                'fee': str(professional.fee) if professional.fee else None,
                'availability': professional.availability
            } for professional in professionals]

            has_more = total_professionals > (offset+limit)

            return {"has_more": has_more, "professionals": professionals_list}, 200
        
    @jwt_required()
    @role_required('Admin')
    def put(self, servicer_id):
        cache.clear()
        ban_unban = request.args.get('account')
        verify_unverify = request.args.get('verification')
        try:
            professional = ServiceProfessional.query.get(servicer_id)
            if ban_unban:
                professional.is_ban = not professional.is_ban
            elif verify_unverify:
                professional.profile_verified = not professional.profile_verified
            db.session.commit()
            return {'message': 'Action applied successfully!'}, 200
        except Exception as e:
            return {'message': f'Something went wrong!{e}'}, 500



            