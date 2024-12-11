from sqlalchemy import Enum
from app.configs.connector import db
from datetime import datetime, timezone
from app.constants.enums import TransactionStatus
from app.utils.functions.calculate_total_prices import calculate_total_prices

class TransactionHistory(db.Model):
    __tablename__ = 'transactions_history'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profile.id'), nullable=False)
    price = db.Column(db.Numeric(16, 2), nullable=True)
    eco_point = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    voucher_id = db.Column(db.Integer, db.ForeignKey('voucher.id'), nullable=True)
    discount = db.Column(db.Float, nullable=True)
    status = db.Column(Enum(TransactionStatus), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    
    # Relationship
    user = db.relationship('User', backref=db.backref('transactions_history', lazy=True))
    seller = db.relationship('Seller', backref=db.backref('transactions_history', lazy=True))
    voucher = db.relationship('Voucher', backref=db.backref('transactions_history', lazy=True))
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'user_id': self.user_id,
            'seller_id': self.seller_id,
            'price': self.price,
            'eco_point': self.eco_point,
            'quantity': self.quantity,
            'voucher_id': self.voucher_id,
            'discount': self.discount,
            'total_price': calculate_total_prices(self.price, self.quantity, self.discount, self.voucher.discount_percentage),
            'status': self.status.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }