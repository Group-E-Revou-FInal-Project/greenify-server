from datetime import datetime, timezone
from app.configs.connector import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # Relationship
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'order_id': self.order_id,
            'quantity': self.quantity,
            'total_price': self.product.price * self.product.discount / 100 * self.quantity if self.product.discount else self.product.price * self.quantity, 
            'created_at': self.created_at,
        }