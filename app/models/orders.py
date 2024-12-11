from datetime import datetime, timezone
from app.configs.connector import db
from app.constants.enums import OrderStatus
from sqlalchemy import Enum

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Numeric(16, 2), nullable=True)
    total_eco_point = db.Column(db.Integer, nullable=True)
    status = db.Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    
    # Relaitonship
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'user_id': self.user_id,
            'total_price': self.total_price,
            'total_eco_point': self.total_eco_point,
            'status': self.status.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }