# HomeMate/server/app/models/oauth.py

from .. import db
from ..custom import IndianZone

class OAuth(db.Model):
    __tablename__ = 'oauth'
    # Columns
    oauth_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    platform = db.Column(db.String(10), nullable=False)
    unique_id = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=IndianZone())

    # Relationships
    user = db.relationship('User', back_populates='oauth')

    