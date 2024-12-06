from email_validator import validate_email, EmailNotValidError
from flask import request
from app.constants.response_status import Response
from app.services.sellers_services import SellerService


class SellerController:
    @staticmethod
    def create_seller():
        data = request.get_json()
        
        response = SellerService.create_seller(data)
        
        if response is None:
            return Response.error(message="You already have a store", code=400)
        
        return response
         