# HomeMate/server/app/models/customer.py

from .. import db
from ..custom import IndianZone

class Customer(db.Model):
    __tablename__ = 'customers'
    # Columns
    customer_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(120))
    pincode = db.Column(db.String(6), nullable=False)
    profile_picture = db.Column(db.String(50), default='customer.svg')
    is_ban = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, default=IndianZone(), onupdate=IndianZone())

    # Relationships
    user = db.relationship('User', back_populates='customer', uselist=False)
    service_requests = db.relationship('ServiceRequest', back_populates='customer', cascade='all, delete-orphan')