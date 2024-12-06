# user_controller.py
from email_validator import validate_email, EmailNotValidError
from flask import request
from app.constants.response_status import Response
from app.services.product_services import ProductService    


class ProductController:
    
    @staticmethod
    def add_category():
        data = request.get_json()
        response = ProductService.add_category(data)
        
        if response is None:
            return Response.error(message='Already exists', code=400)
        
        return response
    
    @staticmethod
    def add_product():
        data = request.get_json()
        response = ProductService.add_product(data)
        
        if response == "Ops, something went wrong":
            return Response.error(message=response, code=400)
        
        return response