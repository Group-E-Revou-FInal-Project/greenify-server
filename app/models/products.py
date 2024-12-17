from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import CheckConstraint
from app.configs.connector import db

class Product(db.Model):
    __tablename__ = 'products'

    id                          = db.Column(db.Integer, primary_key=True)
    seller_id                   = db.Column(db.Integer, db.ForeignKey('seller_profile.id'), nullable=False)
    product_name                = db.Column(db.String, nullable=False)
    price                       = db.Column(db.Numeric(16, 2), nullable=False)
    discount                    = db.Column(db.Float, nullable=True)   
    product_desc                = db.Column(db.String, nullable=True)
    stock                       = db.Column(db.Integer, nullable=False)
    min_stock                   = db.Column(db.Integer, nullable=False)
    is_out_of_stock             = db.Column(db.Boolean, default=False, nullable=False)
    category_id                 = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    eco_point                   = db.Column(db.Integer, nullable=True)
    recycle_material_percentage = db.Column(db.Integer, nullable=True)
    image_url                   = db.Column(db.String, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('discount >= 0 AND discount <= 100', name='check_discount_range'),
    )
    
    def soft_delete(self):
        self.is_deleted = True
        
    def restore(self):
        self.is_deleted = False

    # Relationship
    seller_profile = db.relationship('Seller', uselist=False, backref=db.backref('products', lazy=True))
    category = db.relationship('Category', uselist=False, backref=db.backref('product', uselist=False, lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'seller_id': self.seller_id,
            'product_name': self.product_name,
            'price': round(self.price * Decimal(1 - self.discount / 100), 2) if self.discount else self.price,
            'discount': self.discount,
            'product_desc': self.product_desc,
            'stok': self.stock,
            'min_stok': self.min_stock,
            'category_id': self.category_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'eco_point': self.eco_point,
            'recycle_material': self.recycle_material_percentage,
            'reviews': [review.to_dict() for review in self.reviews if not review.is_deleted]
        }