from datetime import datetime, timezone
from app.configs.connector import db

class UserAddress(db.Model):
    __tablename__ = 'users_address'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)   
    city = db.Column(db.String(255), nullable=False)      
    postal_code = db.Column(db.Integer, nullable=False)   
    province = db.Column(db.String(255), nullable=False)  
    phone_number = db.Column(db.String(20), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationship
    user = db.relationship("User", backref="addresses")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name_address": self.name,
            "address": self.address,
            "city": self.city,
            "postal_code": self.postal_code,
            "province": self.province,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }
