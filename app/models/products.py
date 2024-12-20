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
        # Calculate reviews data
        valid_reviews = [review for review in self.reviews if not review.is_deleted]

        # Calculate average rating and total reviews
        average_rating = (
            round(sum(review.rating for review in valid_reviews) / len(valid_reviews), 1)
            if valid_reviews
            else None
        )

        # Format reviews
        formatted_reviews = [
            {
                "user_name": review.user.name,  # Fetch user name
                "review": review.review,
                "rating": review.rating,
                "created_at": review.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for review in valid_reviews
        ]

        # Build the product dictionary
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "product_name": self.product_name,
            "price": f"{self.price:.2f}",  # Ensure price is formatted as a string with 2 decimal places
            "discount": round(self.discount, 1) if self.discount else None,
            "product_desc": self.product_desc,
            "stock": self.stock,
            "min_stock": self.min_stock,
            "category_id": self.category_id,
            "category_name": self.category.category_name if self.category else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
            "eco_point": self.eco_point,
            "image_url": self.image_url,
            "recycle_material": self.recycle_material_percentage,
            "reviews": {
                "average_rating": average_rating,
                "total_reviews": len(valid_reviews),
                "reviews": formatted_reviews,  # List of individual reviews
            },
        }