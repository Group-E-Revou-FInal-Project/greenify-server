import json
from flask import request
from flask_jwt_extended import get_jwt_identity
from app.services.user_services import UserService
from app.middlewares.auth_middleware import token_required
from app.constants.response_status import Response
from app.utils.validators import UpdateProfile

class ProfileController:
    @staticmethod
    @token_required
    def get_profile_data():
        user_id = json.loads(get_jwt_identity())['user_id']
        response = UserService.get_user_profile(user_id)
        
        if response is None:
            return Response.error(message='User not found', code=400)
        
        return Response.success(data=response, message='Success get profile data', code=200)
    
    @staticmethod
    @token_required
    def update_profile():
        data = request.get_json()
        
        try:
            validate_update = UpdateProfile.model_validate(data)
        except ValueError as e:
            return Response.error(f"{str(e)}", 400)
        
        user_id = json.loads(get_jwt_identity())['user_id']
        
        response = UserService.update_profile(user_id, validate_update.model_dump(exclude_none=True))
        
        if response is None:
            return Response.error(message='User not found', code=400)
        
        return Response.success(data=response, message='Success update profile data', code=200)