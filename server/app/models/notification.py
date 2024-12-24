# HomeMate/server/app/models/notification.py

from .. import db
from ..custom import IndianZone

class Notification(db.Model):
    __tablename__ = "notifications"
    # Columns
    notification_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=IndianZone())

    # Relationships
    user = db.relationship("User", back_populates="notifications")