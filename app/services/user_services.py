from datetime import datetime, timezone
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.temp_users import TempUser
from app.models.users import User, Role

class UserService:
    @staticmethod
    def temp_users(data):
        temp = TempUser(email=data['email'],
                        otp_code=data['otp_code'])
        temp.set_expiration(1) # 1 minute
        
        try:
            db.session.add(temp)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return None
        
        return temp.to_dict()
        
    @staticmethod
    def otp_validation(data):
        check_otp = TempUser.query.filter_by(email=data['email'], otp_code=data['otp_code']).first() 
        check_email = User.query.filter_by(email=data['email']).first()
        
        if check_email is not None:
            return 'Email already registered'
        
        if  check_otp.expires_at > datetime.now():
            return 'OTP code has expired'
        
        if check_otp is None:
            return 'Invalid OTP code'
        
        check_otp.verified = True
        
        db.session.add(check_otp)
        db.session.commit()
        
        return 'OTP code verified'
    
    @staticmethod
    def otp_refresh(data):
        new_otp = TempUser.query.filter_by(email=data['email']).first()
        
        new_otp.otp_code = data["otp_code"]
        new_otp.expires_at = datetime.now(timezone.utc)

        db.session.add(new_otp)
        db.session.commit()
        
        return new_otp.to_dict()
        
    @staticmethod
    def register_user(data):
        verified_email = TempUser.query.filter_by(email=data['email'], verified=True).first()
        email_record = TempUser.query.filter_by(email=data['email']).first()
        role = Role.query.filter_by(rolename=data['role']).first()
        
        if role is None:
            return 'Role not found'
        
        if verified_email is None:
            return 'Email not verified'
        
        new_user = User(name=data['name'], 
                    email=data['email'], 
                    dateofbirth=data['dateofbirth'], 
                    gender=data['gender'])
        
        new_user.set_password(data['password'])
        new_user.roles.append(role)
        
        try:
            db.session.delete(email_record)
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict()
        except IntegrityError:
            db.session.rollback()
            return "Email already exists"
    
    @staticmethod
    def create_role(data):
        new_role = Role(rolename=data['rolename'])
        
        try:
            db.session.add(new_role)
            db.session.commit()
            return new_role.to_dict()
        except IntegrityError:
            db.session.rollback()
            return "Role already exists"
    @staticmethod
    def get_user_profile(data):
        user = User.query.filter_by(id=data["id"], email=data['email']).first()
    
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()