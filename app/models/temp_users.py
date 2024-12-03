from datetime import datetime, timedelta
from app.configs.connector import db

class TempUser(db.Model):
    __tablename__ = 'temp_users'
    
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(255), unique=False, nullable=False)
    otp_code    = db.Column(db.String(255), unique=True, nullable=False)
    expires_at  = db.Column(db.DateTime, nullable=False)

    def set_expiration(self, duration_in_minutes: int):
        self.expires_at = datetime.now() + timedelta(minutes=duration_in_minutes)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'otp_code': self.otp_code,
        }      