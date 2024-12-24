# HomeMate/server/app/models/admin.py

from .. import db

class Admin(db.Model):
    __tablename__ = 'admins'
    # Columns
    admin_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='admin', uselist=False)