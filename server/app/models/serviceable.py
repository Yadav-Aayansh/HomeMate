# HomeMate/server/app/models/serviceable.py

from .. import db

class ServiceablePincode(db.Model):
    __tablename__ = 'serviceable_pincodes'
    # Coulmns
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    service_professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.service_professional_id'), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)

    # Relationships
    service_professional = db.relationship('ServiceProfessional', back_populates='serviceable_pincodes')