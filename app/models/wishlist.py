
from datetime import datetime, timezone
from app.configs.connector import db

# Wishlist Model
class Wishlist(db.Model):
    __tablename__ = "wishlist"

    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
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
            'product': {
                'id': self.product.id,
                'name': self.product.product_name,
                'price': float(self.product.price),  # Convert Decimal to float for JSON serialization
                'discount': self.product.discount,
                'final_price': float(self.product.price) * (1 - (float(self.product.discount) / 100)) if self.product.discount else float(self.product.price),
                'description': self.product.product_desc,
                'stock': self.product.stock,
                'is_out_of_stock': self.product.is_out_of_stock,
                'eco_point': self.product.eco_point,
                'recycle_material_percentage': self.product.recycle_material_percentage,
                'image_url': self.product.image_url,
                'category_id': self.product.category_id,
                'created_at': self.product.created_at,
                'updated_at': self.product.updated_at,
                'is_deleted': self.product.is_deleted,
            } if self.product else None,  # Include product details only if linked product exists
        }