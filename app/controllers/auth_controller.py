import datetime
import json
import pyotp  # For 2FA
from flask import jsonify, request
from app.configs.connector import db
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity, 
    jwt_required
)
from app.services.user_services import UserService
from app.constants.response_status import Response
from flask_mail import Message
from app import mail
from werkzeug.security import generate_password_hash, check_password_hash

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
            identity=json.dumps({'user_id': user.id, 'role': user.roles[0].rolename}),
            expires_delta=datetime.timedelta(hours=1)
        )
        refresh_token = create_refresh_token(identity=json.dumps({'user_id': user.id}))

        if user.two_factor_secret:
            return Response.success(
                data={
                    'message': '2FA enabled, please verify the OTP',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                message="2FA required.",
                code=200
            )

        return Response.success(
            data={
                'message': 'Logged in successfully',
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            message="Logged in successfully.",
            code=200
        )

    @staticmethod
    def verify_2fa():
        data = request.get_json()
        user_id = get_jwt_identity()['user_id']
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
        user_id = get_jwt_identity()['user_id']
        user = UserService.get_user_by_id(user_id)
        user.two_factor_verified = False
        db.session.commit()

        return Response.success(
            data={"message": "Logged out successfully"},
            message="Logged out.",
            code=200
        )

    @staticmethod
    def enable_2fa():
        user_id = get_jwt_identity()['user_id']
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
            msg = Message(
                subject="Enable 2FA for Your Account",
                recipients=[user.email],
                body=f"Revou Bank Authenticator\n\n"
                    f"OTP Code: {current_otp}\n"
                    f"Provisioning URL: {otp_provisioning_url}"
            )
            mail.send(msg)

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



