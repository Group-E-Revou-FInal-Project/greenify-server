from datetime import datetime, timezone
from app.configs.connector import db

class Seller(db.Model):
    __tablename__ = 'seller_profile'

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    store_name        = db.Column(db.String, unique=True, nullable=False)
    store_description = db.Column(db.String, nullable=True)
    store_logo        = db.Column(db.String, nullable=True)
    address           = db.Column(db.String, nullable=True)
    phone_number      = db.Column(db.String, nullable=False)
    created_at        = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at        = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))

    # Relationship
    user = db.relationship('User', backref=db.backref('seller_profile', lazy=True))
    products_list = db.relationship('Product', backref=db.backref('seller_profile', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'store_name': self.store_name,
            'store_description': self.store_description,
            'store_logo': self.store_logo,
            'address': self.address,
            'phone_number': self.phone_number,
            'created_at': self.created_at,
            'updated_by': self.updated_at
        }