from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.temp_users import TempUser
from app.models.users import User
from werkzeug.security import check_password_hash

class UserService:
    @staticmethod
    def temp_users(data):
        temp = TempUser(email=data['email'],
                        otp_code=data['otp_code'])
        temp.set_expiration(1) # 1 minute
        
        try:
            db.session.add(temp)
            db.session.commit()
            return jsonify({"success": f"sent email to {data['email']}"}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Email already exists"}), 400
        
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def reset_password(data):
        validate_otp = {
            "email": data['email'],
            "otp_code": data['otp_code'],
        }

        response = UserService.otp_validation(validate_otp)
        if response != 'OTP code verified':
            return {"error": response}

        user = UserService.get_user_by_email(data['email'])
        if not user:
            return {"error": "User not found"}

        user.set_password(data['password'])

        db.session.commit()
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


        
# def success(data=None, message="Operation successful.", code=200):
# def error(message="An error occurred.", code=400):
