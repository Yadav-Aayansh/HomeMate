# HomeMate/server/app/models/request.py

from .. import db
from ..custom import IndianZone

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    # Columns
    service_request_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    service_professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.service_professional_id'), nullable=False)
    request_date = db.Column(db.DateTime, default=IndianZone())
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default='Requested')
    remarks = db.Column(db.String(120))
    priority = db.Column(db.String(10), default='Medium')
    address = db.Column(db.String(120), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    payment_status = db.Column(db.Boolean, nullable=False, default=False)
    cancellation_reason = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=IndianZone(), onupdate=IndianZone())

    # Relationships
    service = db.relationship('Service', back_populates='service_requests')
    customer = db.relationship('Customer', back_populates='service_requests')
    service_professional = db.relationship('ServiceProfessional', back_populates='service_requests')
    review = db.relationship('Review', back_populates='service_request', cascade='all, delete-orphan')
