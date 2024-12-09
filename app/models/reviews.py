from datetime import datetime, timezone
from app.configs.connector import db

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Relationships
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    
    @db.validates('rating')
    def validate_rating(self, key, value):
        if value < 0 or value > 5:
            raise ValueError('Rating must be between 0 and 5')
        return value
    
    @db.validates('review')
    def validate_review(self, key, value):
        if len(value) > 2500:
            raise ValueError('Review has a maximum of 2500 characters')
        return value
    
    def soft_delete(self):
        self.is_deleted = True
        
    def restore(self):
        self.is_deleted = False

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'review': self.review,  
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_delted': self.is_deleted
        }