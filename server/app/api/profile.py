# HomeMate/server/app/api/profile.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, decode_token, get_jwt_identity
from ..models import User, ServiceablePincode
from ..custom import is_valid_email, is_valid_username, upload_photo, upload_identity
from .. import db
import os

class ProfileApi(Resource):
    @jwt_required()
    def get(self):
        token = request.cookies.get('access_token_cookie')
        decoded_token = decode_token(token)
        if decoded_token.get('role') == 'Customer':
            current_user = get_jwt_identity()
            try:
                is_user = User.query.filter_by(username=current_user).first()
                if is_user:
                    details = {
                        'username': current_user,
                        'customer_id': is_user.customer.customer_id,
                        'email': is_user.email,
                        'name': is_user.customer.name,
                        'profile_picture': is_user.customer.profile_picture,
                        'address': is_user.customer.address,
                        'pincode': is_user.customer.pincode
                    }
                    
                    return details, 200
                return {'message': 'User not found!'}, 400
            except:
                return {'message': 'Something went wrong!'}, 500
            
        elif decoded_token.get('role') == 'Professional':
            current_user = get_jwt_identity()
            try:
                is_user = User.query.filter_by(username=current_user).first()
                if is_user:
                    details = {
                        'username': current_user,
                        'email': is_user.email,
                        'name': is_user.service_professional.name,
                        'fee': str(is_user.service_professional.fee),
                        'rating': float(is_user.service_professional.rating),
                        'profile_verified': is_user.service_professional.profile_verified,
                        'description': is_user.service_professional.description,
                        'identity_proof': is_user.service_professional.identity_proof,
                        'service_type': is_user.service_professional.service_type,
                        'experience': str(is_user.service_professional.experience),
                        'profile_picture': is_user.service_professional.profile_picture,
                        'availability': is_user.service_professional.availability,
                        'serviceable_pincodes': [row.pincode for row in is_user.service_professional.serviceable_pincodes]
                    }
                    
                    return details, 200
                return {'message': 'User not found!'}, 400
            except:
                return {'message': 'Something went wrong!'}, 500
            
        else:
            return {'message': 'Illegal request!'}, 400
        
    @jwt_required()
    def put(self):
        token = request.cookies.get('access_token_cookie')
        decoded_token = decode_token(token)
        if decoded_token.get('role') == 'Professional':
            current_user = get_jwt_identity()
            try:
                is_user = User.query.filter_by(username=current_user).first()
                if is_user:
                    data = request.form
                    username = data.get('username')
                    email = data.get('email')

                    if email is None:
                        return {'message': 'Email address is required!'}, 400
                    
                    email = data.get('email').lower()
                    if not is_valid_email(email):
                        return {'message': 'Email address is invalid!'}, 400

                    email_checker = User.query.filter_by(email=email).first()
                    if email_checker.user_id != is_user.user_id:
                        return {'message': 'Email address is already in use!'}, 400
                    
                    if username is None:
                        return {'message': 'Username is required!'}, 400
                    
                    username = data.get('username').lower()
                    if not is_valid_username(username):
                        return {'message': 'Username is invalid!'}, 400
                    
                    username_checker = User.query.filter_by(username=username).first()
                    if username_checker.user_id != is_user.user_id:
                        return {'message': 'Username already taken!'}, 400
                    
                    name = data.get('name')
                    if name is None:
                        return {'message': 'Name is required!'}, 400
                    
                    availability = data.get('availability')
                    if availability is None:
                        return {'message': 'Availability is required!'}, 400
                    
                    service_type = data.get('service_type')
                    if service_type is None:
                        return {'message': 'Service Type is required!'}, 400
                    
                    fee = data.get('fee')
                    if fee is None:
                        return {'message': 'Service Fee is required!'}, 400
                    
                    experience = data.get('experience')
                    if experience is None:
                        return {'message': 'Experience is required!'}, 400
                    
                    description = data.get('description')
                    if description is not None and len(description) > 255:
                        return {'message': 'Description should not be more than 255 characters!'}, 400
                    
                    
                    files = request.files
                    change_picture = files.get('change_picture')
                    if change_picture:
                        old = is_user.service_professional.profile_picture
                        filename = upload_photo(is_user.user_id, old, change_picture)
                        is_user.service_professional.profile_picture = filename

                    identity_proof = files.get('identity_proof')
                    if identity_proof:
                        old = is_user.service_professional.identity_proof
                        filename = upload_identity(is_user.user_id, old, identity_proof)
                        is_user.service_professional.identity_proof = filename

                    serviceable_pincodes = data.get('serviceable_pincodes')
                    db.session.query(ServiceablePincode).filter_by(service_professional_id=is_user.service_professional.service_professional_id).delete(synchronize_session=False)
                    if serviceable_pincodes != "":
                        pincodes = serviceable_pincodes.split(',')
                        for pincode in pincodes:
                            new_serviceable_pincode = ServiceablePincode(pincode=pincode, service_professional_id=is_user.service_professional.service_professional_id)
                            db.session.add(new_serviceable_pincode)
                    
                    
                    is_user.email = email
                    is_user.username = username
                    is_user.service_professional.name = name
                    is_user.service_professional.description = description
                    is_user.service_professional.service_type = service_type
                    is_user.service_professional.experience = experience
                    is_user.service_professional.fee = fee
                    is_user.service_professional.availability = availability

                    db.session.commit()
                    
                    return {'message': 'Profile updated successfully!'}, 200
                return {'message': 'User not found!'}, 400
            except Exception as e:
                return {'message': f'Something went wrong!{e}'}, 500
            
        else:
            return {'message': 'Illegal request!'}, 400
        

    @jwt_required()
    def delete(self):
        token = request.cookies.get('access_token_cookie')
        decoded_token = decode_token(token)
        if decoded_token.get('role') == 'Professional':
            current_user = get_jwt_identity()
            try:
                is_user = User.query.filter_by(username=current_user).first()
                picture = is_user.service_professional.profile_picture
                if is_user and picture != 'servicer.png':
                    old_dir = f"app/static/profile/photos/{picture}"
                    os.remove(old_dir)
                    is_user.service_professional.profile_picture = 'servicer.png'
                    db.session.commit()

                    return {'message': 'Profile picture deleted successfully!'}, 200
                return {'message': 'User not found!'}, 400
            except:
                return {'message': 'Something went wrong!'}, 500
            
        else:
            return {'message': 'Illegal request!'}, 400




        



