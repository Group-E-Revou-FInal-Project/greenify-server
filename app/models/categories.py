from datetime import datetime, timezone
from app.configs.connector import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id            = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, unique=True, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at    = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    is_deleted    = db.Column(db.Boolean, default=False)
    
    #Realationship
    products  = db.relationship('Product', backref='categories', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }