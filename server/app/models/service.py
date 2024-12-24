# HomeMate/server/app/models/service.py

from .. import db
from ..custom import IndianZone

class Service(db.Model):
    __tablename__ = 'services'
    # Columns
    service_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    base_price = db.Column(db.Numeric(10,2), nullable=False)
    time_required = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime, default=IndianZone())
    updated_at = db.Column(db.DateTime, default=IndianZone(), onupdate=IndianZone())

    # Relationships
    service_requests = db.relationship('ServiceRequest', back_populates='service', cascade='all, delete-orphan')