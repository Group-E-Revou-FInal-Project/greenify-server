# user_controller.py
from email_validator import validate_email, EmailNotValidError
from flask import Response, jsonify, request
from app.services.user_services import UserService
from app.utils.validators.temp_email import OTPCode
from app.utils.functions.generate_otp import generate_random_otp
from flask_mail import Mail, Message
from app import mail
class UserController:
    
    @staticmethod
    def temp_users():
        data = request.get_json()
        try:
            valid = validate_email(data['email'])  
            email = valid.email
        except EmailNotValidError as e:
            return jsonify({"Invalid email": f"{str(e)}"}), 400
        
        otp_code = generate_random_otp()
        data["otp_code"] = otp_code
            
        try:
            msg = Message(
                subject="Verication OTP Code Greenify",
                recipients=[email],
                body=f"Greenify OTP code for email validation: {otp_code}, expires in 1 minute"
            )
            mail.send(msg)
        except Exception as e:
            return jsonify({"error": f"{str(e)}"}), 400
        
        response = UserService.temp_users(data)
        
        return response
    
    @staticmethod
    def check_otp():
        data = request.get_json()
        try:
            validate_otp = OTPCode.model_validate(data)
        except ValueError as e:
            return jsonify({"error": f"{str(e)}"}), 400
        
        response = UserService.check_otp(validate_otp.model_dump())
        return response
    def get_all_users():
        return 200

        

        
        
