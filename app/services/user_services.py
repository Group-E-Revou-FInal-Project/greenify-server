from datetime import datetime, timezone
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.temp_users import TempUser
from app.models.users import User
from werkzeug.security import check_password_hash
from app.models.users import User, Role
from app.models.categories import Category

class UserService:
    @staticmethod
    def temp_users(data, verified=None): 
        if verified is None: verified = False
        temp = TempUser(email=data['email'],
                        otp_code=data['otp_code'])
        temp.set_expiration(1) # 1 minute
        temp.verified = verified
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
            
        if check_otp is None:
            return 'Invalid OTP code'
        
        if  check_otp.expires_at > datetime.now():
            return 'OTP code has expired'
        
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
    def get_user_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def register_user(data):
        verified_email = TempUser.query.filter_by(email=data['email'], verified=True).first()
        email_record = TempUser.query.filter_by(email=data['email']).first()
        role = Role.query.filter_by(rolename=data['role']).first()
        
        if verified_email is None:
            return 'Email not verified'

        if role is None:
            return 'Role not found'

        if not isinstance(data.get('interests'), list) or len(data['interests']) != 3:
            return 'You must provide exactly 3 interests'
        
        interests = []
        for interest_name in data['interests']:
            interest = Category.query.filter_by(category_name=interest_name).first()
            interests.append(interest)
        
        
        new_user = User(name=data['name'], 
                    email=data['email'], 
                    dateofbirth=data['dateofbirth'], 
                    gender=data['gender'])
        
        new_user.set_password(data['password'])
        new_user.roles.append(role)
        new_user.interests.extend(interests)
        
        try:
            db.session.delete(email_record)
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict()
        except IntegrityError:
            db.session.rollback()
            return "Email already exists"
        
    @staticmethod
    def get_user_data(data):
        user = User.query.filter_by(id=data['id']).first()
        return user.to_dict()
    
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
    def get_user_profile(user_id):
        user = User.query.filter_by(id=user_id).first()
        
        return user.to_dict()
    
    @staticmethod
    def update_profile(user_id, data):
        user = User.query.filter_by(id=user_id).first()
        
        if user is None:
            return None
        
        user.name = data.get('name', user.name)
        user.dateofbirth = data.get('dateofbirth', user.dateofbirth)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.gender = data.get('gender', user.gender)
        
        db.session.add(user)
        db.session.commit()
        
        return user.to_dict()
    
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def temp_user_forgot_password(email):
        return TempUser.query.filter_by(email=email, verified=True).first()
    
    @staticmethod
    def otp_validation_reset(data):
        check_otp = TempUser.query.filter_by(email=data['email'], otp_code=data['otp_code']).first() 
        check_email = User.query.filter_by(email=data['email']).first()
        
        if check_email is None:
            return 'Email not registered'
         
        if check_otp is None:
            return 'Invalid OTP code'
        
        if check_otp.expires_at > datetime.now():
            return 'OTP code has expired'
        
        check_otp.verified = True
        try:
            db.session.add(check_otp)
            db.session.commit()        
        except IntegrityError:
            db.session.rollback()
            return 'ERROR otp code request does not exist'
        return 'OTP code verified'
    
    @staticmethod
    def reset_password(data):
        validate_otp = {
            "email": data['email'],
            "otp_code": data['otp_code'],
        }
        email_record = TempUser.query.filter_by(email=data['email']).first()
        response = UserService.otp_validation_reset(validate_otp)
        if response != 'OTP code verified':
            return {"error": response}

        user = UserService.get_user_by_email(data['email'])
        if not user:
            return {"error": "User not found"}
        try:
            user.set_password(data['password'])
            db.session.delete(email_record)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return {"error": f"Failed to delete temporary email record: {str(error)}"}
        return {"success": "Password reset successfully"}

    @staticmethod
    def change_password(data):
        user = UserService.get_user_by_email(data['email'])
        if not user:
            return {"error": "User not found"}

        if not check_password_hash(user.password_hash, data['previous_password']):
            return {"error": "Invalid previous password"}

        if data['previous_password'] == data['new_password']:
            return {"error": "New password cannot be the same as the previous password"}

        user.set_password(data['new_password'])

        try:
            db.session.commit()
            return {"success": "Password changed successfully"}
        except Exception as error:
            db.session.rollback()
            return {"error": f"Failed to change password: {str(error)}"}
