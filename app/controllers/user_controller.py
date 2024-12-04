# user_controller.py
from app.services.user_services import UserService
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from email_validator import validate_email, EmailNotValidError
class UserController:
    
    @staticmethod
    def get_all_users():
        users = UserService.get_all_users()
        return 200, [user.to_dict() for user in users]