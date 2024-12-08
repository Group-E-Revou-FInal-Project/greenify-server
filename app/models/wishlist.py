
from datetime import datetime, timezone
from app.configs.connector import db

# Wishlist Model
class Wishlist(db.Model):
    __tablename__ = "wishlist"

    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))

    product = db.relationship("Product", backref="wishlists")
    user = db.relationship("User", backref="wishlists")
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }