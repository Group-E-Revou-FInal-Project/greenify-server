from datetime import datetime, timezone
from app.configs.connector import db

class Product(db.Model):
    __tablename__ = 'products'

    id                          = db.Column(db.Integer, primary_key=True)
    seller_id                   = db.Column(db.Integer, db.ForeignKey('seller_profile.id'), nullable=False)
    product_name                = db.Column(db.String, nullable=False)
    price                       = db.Column(db.Numeric, nullable=False)
    product_desc                = db.Column(db.String, nullable=True)
    stock                       = db.Column(db.Integer, nullable=False)
    min_stock                   = db.Column(db.Integer, nullable=False)
    category_id                 = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    eco_point                   = db.Column(db.Integer, nullable=True)
    recycle_material_percentage = db.Column(db.Integer, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    is_deleted = db.Column(db.Boolean, default=False)

    # Relationship
    seller = db.relationship('Seller', backref=db.backref('products', lazy=True))
    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'seller_id': self.seller_id,
            'product_name': self.product_name,
            'price': self.price,
            'product_desc': self.product_desc,
            'stok': self.stok,
            'min_stok': self.min_stok,
            'category_id': self.category_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'eco_point': self.eco_point,
            'recycle_material': self.recycle_material
        }