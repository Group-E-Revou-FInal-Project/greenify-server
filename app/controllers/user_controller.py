# user_controller.py
from email_validator import validate_email, EmailNotValidError
from flask import request
from app.constants.response_status import Response
from app.services.user_services import UserService
from app.utils.validators import OTPCode, RegisterUser, Role
from app.utils.functions.generate_otp import generate_random_otp
from flask_mail import Mail, Message
from app import mail
class UserController:
    
    @staticmethod
    def email_validaton():
        data = request.get_json()
        try:
            valid = validate_email(data['email'])  
            email = valid.email
        except EmailNotValidError as e:
            return Response.error(f"{str(e)}", 400)
        
        otp_code = generate_random_otp()
        data["otp_code"] = otp_code
        
        response = UserService.temp_users(data)
        
        if response is None:
            return Response.error(message="Email already exist", code=400)
            
        try:
            msg = Message(
                subject="Verication OTP Code Greenify",
                recipients=[email],
                body=f"Greenify OTP code for email validation: {otp_code}, expires in 1 minute"
            )
            mail.send(msg)
        except Exception as e:
            return Response.error(f"{str(e)}", 400)
    
        
        return response
    
    @staticmethod
    def otp_validation():
        data = request.get_json()
        try:
            validate_otp = OTPCode.model_validate(data)
        except ValueError as e:
            return Response.error(f"{str(e)}", 400)
        
        response = UserService.otp_validation(validate_otp.model_dump())
        
        if response != 'OTP code verified':
            return Response.error(message=response, code=400)
        
        return Response.success(message=response, code=200)
    
    @staticmethod
    def otp_refresh():
        data = request.get_json()
        
        try:
            valid = validate_email(data['email'])  
            email = valid.email
        except EmailNotValidError as e:
            return Response.error(f"{str(e)}", 400)
        
        new_otp = generate_random_otp()
        
        data["otp_code"] = new_otp
        
        response = UserService.otp_refresh(data)
        
        try:
            msg = Message(
                subject="Verication OTP Code Greenify",
                recipients=[email],
                body=f"Greenify OTP code for email validation: {new_otp}, expires in 1 minute"
            )
            mail.send(msg)
        except Exception as e:
            return Response.error(f"{str(e)}", 400)
        
        return Response.success(data=response, message="Success refresh otp code", code=200)
    
    @staticmethod
    def register_user():
        data = request.get_json()
        
        try:
            validate_user = RegisterUser.model_validate(data)
        except ValueError as e:
            return Response.error(f"{str(e)}", 400)
        
        response = UserService.register_user(validate_user.model_dump())
        
        if response == "Role not found":
            return Response.error(message=response, code=400)
        
        if response == "Email not verified":
            return Response.error(message=response, code=400)
        
        if response == "Email already exists":
            return Response.error(message=response, code=400)
        
        return Response.success(data=response, message="register success", code=200)
    
    @staticmethod
    def add_role():
        data = request.get_json()
        
        try:
            validate_role = Role.model_validate(data)
        except ValueError as e:
            return Response.error(f"{str(e)}", 400)
        
        response = UserService.create_role(validate_role.model_dump())
        
        if response == "Role already exists":
            return Response.error(message=response, code=400)
        
        return Response.success(data=response, message="Success add role", code=200)
    
    def get_all_users():
        return 200

        

        
        
