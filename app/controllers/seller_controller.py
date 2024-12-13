import json
from email_validator import validate_email, EmailNotValidError
from flask import request
from flask_jwt_extended import get_jwt_identity
from app.constants.response_status import Response
from app.services.sellers_services import SellerService
from app.utils.validators import CreateSeller
from pydantic import ValidationError


class SellerController:
    @staticmethod
    def create_seller():
        data = request.get_json()
        user_id = json.loads(get_jwt_identity())['user_id']
        data['user_id'] = user_id
        
        try:
            validate_seller = CreateSeller.model_validate(data)
        except ValidationError as e:
            return Response.error(f"{str(e)}", 400)
            
        response = SellerService.create_seller(validate_seller.model_dump())
        
        if response is None:
            return Response.error(message="You already have a store", code=400)
        
        return response
    
    @staticmethod
    def update_seller():
        data = request.get_json()    
        user_id = json.loads(get_jwt_identity())['user_id']
        data['user_id'] = user_id
        
        try:
            validate_seller = CreateSeller.model_validate(data)
        except ValidationError as e:
            return Response.error(f"{str(e)}", 400)
            
        response = SellerService.update_seller(validate_seller.model_dump())
        
        if response is None:
            return Response.error(message="You don't have a store", code=400)
        
        
    @staticmethod
    def seller_management(seller_id, action=False):
        response = SellerService.deactivate_seller(seller_id,action)
        if response is None:
            return Response.error(message="You don't have a store", code=400)
        
        return response
         