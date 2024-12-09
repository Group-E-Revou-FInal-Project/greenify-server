from flask import json, request
from flask_jwt_extended import get_jwt_identity
from app.constants.response_status import Response
from app.services.UserInterestService import UserInterestService
from app.utils.validators import user_interest

class UserInterestController:
    # CREATE
    @staticmethod
    def add_interest():
        data = request.get_json()
        try:
            validate_interest = user_interest.model_validate(data)
        except ValueError as e:
            return Response.error(f"{str(e)}", 400)
        response = UserInterestService.add_user_interest(validate_interest.model_dump())
    
        if "error" in response:
                return {"message": response}, 400
            
        return {"message": "Interest added successfully", "data": response}, 200

    @staticmethod
    def get_interests():
        user_id = json.loads(get_jwt_identity())['user_id']
        interests = UserInterestService.get_user_interests(user_id)
        if "error" in interests:
                return {"message": interests}, 400
            
        return {"interests": interests}, 200
    
    @staticmethod
    def update_interests():
        data = request.get_json()
        user_id = json.loads(get_jwt_identity())['user_id']
        
        response = UserInterestService.update_interests(user_id, data)
        
        if 'error' in response:
            return Response.error(message=response['error'], code=400)
        
        return Response.success(data=response, message='Success update profile data', code=200)
    
    @staticmethod
    def remove_interest():
        data = request.get_json()
        user_id = json.loads(get_jwt_identity())['user_id']
        data['user_id'] = user_id
        try:
            validate_interest = user_interest.model_validate(data)
        except ValueError as e:
            return Response.error(f"{str(e)}", 400)
        response = UserInterestService.remove_user_interest(validate_interest.model_dump())
        if "error" in response:
                return {"message": response}, 400

        return {"message": "Interest removed successfully", "data": ''}, 200

