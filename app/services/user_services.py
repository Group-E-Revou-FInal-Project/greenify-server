from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.temp_users import TempUser
from app.models.users import User

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
    def check_otp(data):
        check_otp = TempUser.query.filter_by(email=data['email'], otp_code=data['otp_code']).first() 
        
        if check_otp is None:
            return jsonify({"error": "Invalid OTP"}), 400
        
        return jsonify({"success": "OTP verified"}), 200
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
        
# def success(data=None, message="Operation successful.", code=200):
# def error(message="An error occurred.", code=400):
