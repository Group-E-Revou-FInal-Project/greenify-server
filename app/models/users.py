from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.configs.connector import db
from sqlalchemy import Enum as SqlEnum
from app.constants.gender_enums import gender_enum

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), unique=False, nullable=False)
    email       = db.Column(db.String(255), unique=True, nullable=False)
    dateofbirth = db.Column(db.DateTime, nullable=False)
    gender      = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active    = db.Column(db.Boolean, default=True)
    oauth_id     = db.Column(db.String(255), nullable=True)
    oauth_provider = db.Column(db.String(255), nullable=True)
    two_factor_secret = db.Column(db.String(255), nullable=True)  
    two_factor_verified = db.Column(db.Boolean, default=False)  
    
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy=True))

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'dateofbirth': self.dateofbirth.isoformat(),
            'gender': self.gender,
            'phone_number': self.phone_number,
            'is_active': self.is_active,
            'created_at' : self.created_at.isoformat(),
            'updated_at' : self.updated_at.isoformat(),
            'roles': [role.to_dict() for role in self.roles],
        }
        
    
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'rolename': self.rolename
        }
        
        
    
