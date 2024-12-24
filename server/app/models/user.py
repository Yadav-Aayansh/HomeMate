# HomeMate/server/app/models/user.py

from .. import db
from ..custom import IndianZone
from werkzeug.security import generate_password_hash, check_password_hash
from .admin import Admin
from .customer import Customer
from .servicer import ServiceProfessional

class User(db.Model):
    __tablename__ = 'users'
    # Columns
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(25), nullable=False)
    oauth_user = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, default=IndianZone())
    created_at = db.Column(db.DateTime, default=IndianZone())
    updated_at = db.Column(db.DateTime, default=IndianZone(), onupdate=IndianZone())

    # Relationships
    admin = db.relationship('Admin', back_populates='user', uselist=False, cascade='all, delete-orphan')
    customer = db.relationship('Customer', back_populates='user', uselist=False, cascade='all, delete-orphan')
    service_professional = db.relationship('ServiceProfessional', back_populates='user', uselist=False, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', back_populates='user', cascade='all, delete-orphan')
    oauth = db.relationship('OAuth', back_populates='user', cascade='all, delete-orphan')

    # Methods
    def set_password(self, password=None):
        if password != None and password != '':
            self.password = generate_password_hash(str(password))

    def check_password(self, password):
        if self.password:
            return check_password_hash(self.password, password)
        return False
    
    def additional_commit(self, data):
        if self.role == 'Admin':
            new_admin = Admin(user_id=self.user_id)
            db.session.add(new_admin)
        elif self.role == 'Customer':
            name = data.get('name')
            address = data.get('address')
            pincode = data.get('pincode')
            if name is None:
                return {'message': "Customer's Name is missing!"}, 400 
            if pincode is None:
                return {'message': "Customer's Pincode is missing!"}, 400
            if address is None:
                return {'message': "Customer's Address is missing!"}, 400
            new_customer = Customer(user_id=self.user_id, name=name, address=address, pincode=pincode)
            db.session.add(new_customer)
        elif self.role == 'Professional':
            name = data.get('name')
            service_type = data.get('service_type')
            experience = data.get('experience')
            availability = data.get('availability')
            if name is None:
                return {'message': "Service Professional's Name is missing!"}, 400
            if service_type is None:
                return {'message': "Service Professional's Service Type is missing!"}, 400
            if experience is None:
                return {'message': "Service Professional's Experience is missing!"}, 400
            if availability is None:
                return {'message': "Service Professional's Availability is missing!"}, 400
            
            new_professional = ServiceProfessional(user_id=self.user_id, name=name, service_type=service_type, experience=experience, availability=availability)
            db.session.add(new_professional)
    