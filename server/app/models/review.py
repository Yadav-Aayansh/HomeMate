# HomeMate/server/app/models/review.py

from .. import db
from ..custom import IndianZone

class Review(db.Model):
    __tablename__ = 'reviews'
    # Columns
    review_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.service_request_id'), nullable=False)
    rating = db.Column(db.Numeric(3,2), nullable=False)
    review_text = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=IndianZone())

    # Relationships
    service_request = db.relationship('ServiceRequest', back_populates='review', uselist=False)