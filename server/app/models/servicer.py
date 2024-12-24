# HomeMate/server/app/models/servicer.py

from .. import db
from ..custom import IndianZone

class ServiceProfessional(db.Model):
    __tablename__ = 'service_professionals'
    # Columns
    service_professional_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(255))
    service_type = db.Column(db.String(30), nullable=False)
    experience = db.Column(db.Numeric(3,1), nullable=False)
    profile_picture = db.Column(db.String(50), nullable=False, default='servicer.png')
    earning = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    work_done = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Numeric(3,2), nullable=False, default=0)
    identity_proof =  db.Column(db.String(50))
    profile_verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_at = db.Column(db.DateTime)
    fee = db.Column(db.Numeric(10,2))
    availability = db.Column(db.String(20), nullable=False)
    is_ban = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=IndianZone(), onupdate=IndianZone())

    # Relationships
    user = db.relationship('User', back_populates='service_professional', uselist=False)
    serviceable_pincodes = db.relationship('ServiceablePincode', back_populates='service_professional', cascade='all, delete-orphan')
    service_requests = db.relationship('ServiceRequest', back_populates='service_professional', cascade='all, delete-orphan')