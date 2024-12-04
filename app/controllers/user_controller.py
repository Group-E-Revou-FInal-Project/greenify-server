# user_controller.py
from email_validator import validate_email, EmailNotValidError
from flask import request
from app.constants.response_status import Response
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
            return Response.error(f"{str(e)}", 400)
        
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
            return Response.error(f"{str(e)}", 400)
        
        response = UserService.temp_users(data)
        
        return response
    
    @staticmethod
    def check_otp():
        data = request.get_json()
        try:
            validate_otp = OTPCode.model_validate(data)
        except ValueError as e:
            return Response.error(f"{str(e)}", 400)
        
        response = UserService.check_otp(validate_otp.model_dump())
        
        if response == "OTP code has expired" or response is None:
            return Response.error(message=response, code=400)
        
        return Response.success(message=response, code=200)
    
    @staticmethod
    def register_user():
        data = request.get_json()
        response = UserService.register_user(data)
        
        if response == "Email not verified":
            return Response.error(message=response, code=400)
        
        if response == "Email already exists":
            return Response.error(message=response, code=400)
        
        return Response.success(data=response, message="register success", code=200)
    
    def get_all_users():
        return 200

        

        
        
