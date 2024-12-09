from datetime import datetime, timezone
from app.configs.connector import db

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)          
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True, default=None, onupdate=datetime.now(timezone.utc))
    
    user = db.relationship('User', backref=db.backref('carts', lazy=True))
    product = db.relationship('Product', backref=db.backref('carts', lazy=True))
    
    @db.validates('quantity')
    def validate_quantity(self, key, value):
        if value <= 0:
            db.session.delete(self)
            db.session.commit()
            raise ValueError("Quantity must be greater than 0")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'total_price': self.product.price * self.quantity,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }