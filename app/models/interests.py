from datetime import datetime, timezone
from app.configs.connector import db

class Interest(db.Model):
    __tablename__ = 'interests'

    id          = db.Column(db.Integer, primary_key=True)
    interest    = db.Column(db.String(255), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    created_at  = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at  = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    
    # #Relationship
    category = db.relationship('Category', backref=db.backref('interests', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'interest': self.interest,
            'category_id': self.category_id
        }