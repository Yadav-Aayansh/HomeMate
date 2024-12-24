# HomeMate/server/app/custom.py

from datetime import datetime
import os
import pytz
import re
from flask import request, current_app
from flask_jwt_extended import get_jwt
import random

def IndianZone():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

# Creating Decorator for Checking Role 
def role_required(role):  #sending the role # fn is desirable function for user
    def wrapper(fn):    # decorator function
        def extra_checks(*args, **kwargs):   # extra_checks is adding extra stuff in fn
            decoded_data = get_jwt()    # Dict Form
            if decoded_data.get('role') != role:
                return {'message': 'Access Denied!'}, 403
            good_to_go = fn(*args, **kwargs)
            return good_to_go
        return extra_checks
    return wrapper


# Allowed file extensions
ALLOWED_PHOTOS = {'png', 'jpg', 'jpeg'}
ALLOWED_DOCS = {'pdf'}

def allowed_file(filename, allowed_filetype):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_filetype

def upload_photo(user_id, old, new):
    if new and allowed_file(new.filename, ALLOWED_PHOTOS):
        if old != 'servicer.png':
            old_dir = f"app/static/profile/photos/{old}"
            os.remove(old_dir)
        new_photo = f"{user_id}-{random.randint(0,70)}.jpg"
        file_path = os.path.join('app/static/profile/photos/', new_photo)
        new.save(file_path)
        return new_photo
    

def upload_identity(user_id, old, new):
    if new and allowed_file(new.filename, ALLOWED_DOCS):
        if old:
            old_dir = f"app/static/profile/identity/{old}"
            os.remove(old_dir)
        new_doc = f"{user_id}-{random.randint(0,70)}.pdf"
        file_path = os.path.join('app/static/profile/identity/', new_doc)
        new.save(file_path)
        return new_doc



  
