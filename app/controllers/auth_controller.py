import datetime
import json
from pydantic import ValidationError
import pyotp  # For 2FA
from flask import jsonify, make_response, request
from app.configs.connector import db
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity, 
    jwt_required
)
from app.models.users import User
from app.services.user_services import UserService
from app.constants.response_status import Response
from flask_mail import Message
from app import mail
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError

from app.utils.functions.generate_otp import generate_random_otp
from app.utils.functions.send_emails import send_email
from app.utils.validators import changePassword

class AuthController:
    # def success(data=None, message="Operation successful.", code=200):
    # def error(message="An error occurred.", code=400):    
    @staticmethod
    def login():
        data = request.get_json()

        if 'email' not in data or not data['email']:
            return Response.error("Email is required", 400)

        if 'password' not in data or not data['password']:
            return Response.error("Password is required", 400)

        user = UserService.get_user_by_email(data['email'])
        if not user:
            return Response.error("Account does not exist", 401)

        if not check_password_hash(user.password_hash, data['password']):
            return Response.error("Invalid password", 401)

        access_token = create_access_token(
            identity=json.dumps({'user_id': user.id, 'role': user.roles[0].rolename,'email': user.email}),
            expires_delta=datetime.timedelta(hours=1)
        )
        refresh_token = create_refresh_token(identity=json.dumps({'user_id': user.id}))
        
        response = make_response(jsonify({
        "message": "Logged in successfully.",
        "data": {
            "access_token": access_token,  
            "refresh_token": refresh_token 
        },
        "code": 200
        }))
        response.set_cookie(
            "access_token", 
            access_token, 
            httponly=True, 
            secure=True, 
            samesite='Strict'
        )
        response.set_cookie(
            "refresh_token", 
            refresh_token, 
            httponly=True, 
            secure=True, 
            samesite='Strict'
        )

        return response

    @staticmethod
    def verify_2fa():
        data = request.get_json()
        user_id = json.loads(get_jwt_identity())['user_id']
        user = UserService.get_user_by_id(user_id)

        if not user.two_factor_secret:
            return Response.error("2FA not enabled for this user", 400)

        provided_otp = data.get('otp_code', None)
        totp = pyotp.TOTP(user.two_factor_secret)

        if totp.verify(provided_otp, valid_window=1):
            user.two_factor_verified = True
            db.session.commit()
            return Response.success(
                data={"message": "2FA verified successfully"},
                message="2FA verified.",
                code=200
            )

        return Response.error("Invalid 2FA code", 400)

    @staticmethod
    def logout():
        try:
            user_id = json.loads(get_jwt_identity())['user_id']
            if user_id is None:
                return Response.error("User ID is null", 400)

            user = UserService.get_user_by_id(user_id)
            if user is None:
                return Response.error("User not found", 404)

            user.two_factor_secret = None
            db.session.commit()

            return Response.success(
                data={"message": "Logged out successfully"},
                message="Logged out.",
                code=200
            )
        except Exception as e:
            db.session.rollback()
            return Response.error(str(e), 500)

    @staticmethod
    def enable_2fa():
        user_id = json.loads(get_jwt_identity())['user_id']
        user = UserService.get_user_by_id(user_id)

        secret = pyotp.random_base32()
        user.two_factor_secret = secret
        db.session.commit()

        otp_provisioning_url = pyotp.totp.TOTP(secret).provisioning_uri(
            user.email, issuer_name="Revou Bank"
        )
        totp = pyotp.TOTP(secret)
        current_otp = totp.now()

        try:
            user_email = user.email  # Use the validated email
            recipient_name = user.name if user.name else "Pengguna"
            subject = "Greenify Enable 2FA for Your Account"
            header = "Grennify"
            content = f"""
            <p>Hai, {recipient_name}!</p>
            <p>Gunakan kode OTP di bawah ini untuk dapat melakukan verifikasi 2FA pada akun Anda:</p>
            <h3 style="color: #32a852; text-align: center;">{current_otp}</h3>
            <p>OTP hanya berlaku selama 1 menit:</p>
            """
            send_email(user_email, header, content, subject)
        
            return Response.success(
                data={"message": "2FA enabled and setup email sent"},
                message="2FA enabled.",
                code=200
            )
        except Exception as e:
            return Response.error(f"Error sending email: {str(e)}", 500)

    @staticmethod
    @jwt_required(refresh=True)
    def refresh_token():
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return Response.success(
            data={"access_token": new_access_token},
            message="Token refreshed.",
            code=200
        )
        
    def forgot_password():
        data = request.get_json()
        if 'email' not in data or not data['email']:
            return Response.error("Email is required", 400)

        try:
            valid = validate_email(data['email'])
            email = valid.email
        except EmailNotValidError as e:
            return Response.error(f"Invalid email: {str(e)}", 400)

        if not email:
            return Response.error("Email is required", 400)
        
        
        email_validate = UserService.get_user_by_email(email)
        if not email_validate:
            return Response.error("User not found", code=404)
        
        otp_code = generate_random_otp()
        data["otp_code"] = otp_code

        
        validateUser = UserService.temp_user_forgot_password(email)
        if validateUser:
            try:
                db.session.delete(validateUser)
                db.session.commit()
            except Exception as error:
                db.session.rollback()
                return {"error": f"Failed to delete temporary email record: {str(error)}"}
            
        response = UserService.temp_users(data,True)
        if response is not None:
            user_email = email  # Use the validated email
            recipient_name = email_validate.name if email_validate.name else "Pengguna"
            subject = "Greenify reset password verification code"
            header = "Grennify"
            content = f"""
            <p>Hai, {recipient_name}!</p>
            <p>Gunakan kode OTP di bawah ini untuk dapat melakukan reset password pada akun Anda:</p>
            <h3 style="color: #32a852; text-align: center;">{otp_code}</h3>
            <p>OTP hanya berlaku selama 1 menit:</p>
            """
            response = send_email(user_email, header, content, subject)
            if response is not None and 'error' in response:
                return Response.error(response['error'], 400)
            
        

        return Response.success("Reset password verification code has been sent", 200)
    
    def forgot_change_password():
        data = request.get_json()

        if 'email' not in data or not data['email']:
            return Response.error("Email is required", 400)

        if 'otp_code' not in data or not data['otp_code']:
            return Response.error("OTP code is required", 400)

        if 'password' not in data or not data['password']:
            return Response.error("Password is required", 400)


        try:
            validate_changePassword = changePassword.model_validate(data)
        except ValidationError as e:
            return Response.error(f"{str(e)}", 400)
        
        reset_response = UserService.reset_password(validate_changePassword.model_dump())

        if "error" in reset_response:
            return Response.error(reset_response["error"], 400)

        return Response.success(
            data={"message": reset_response["success"]},
            message="Password reset successfully.",
            code=200
        )
    
    def change_password():
        data = request.get_json()
        user_email = json.loads(get_jwt_identity())['email']
        data['email'] = user_email
        if 'otp_code' not in data or not data['otp_code']:
            return Response.error("OTP code is required", 400)

        if 'password' not in data or not data['password']:
            return Response.error("Password is required", 400)
        
        response = UserService.change_password(data)
        if "error" in response:
            return Response.error(response["error"], 400)
        
        return Response.success(
                data={"message": response["success"]},
                message="Changed password.",
                code=200
            )
        
        

