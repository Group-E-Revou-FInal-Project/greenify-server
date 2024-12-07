from flask import request
from pydantic import ValidationError
from app.constants.response_status import Response
from app.services.product_services import ProductService 
from app.utils.validators import AddCategory, AddProduct, UpdateProduct
from app.utils.functions.handle_field_error import handle_field_error   

class ProductController:
    
    @staticmethod
    def add_category():
        data = request.get_json()
        
        try:
            validate_category = AddCategory.model_validate(data)
        except ValidationError as e:
            missing_fields = handle_field_error(e)
            return Response.error(message=missing_fields, code=400)
        
        response = ProductService.add_category(validate_category.model_dump())
        
        if response is None:
            return Response.error(message='Already exists', code=400)
        
        return response
    
    @staticmethod
    def add_product():
        data = request.get_json()
        
        try:
            validate_product = AddProduct.model_validate(data)
        except ValidationError as e:
            missing_fields = handle_field_error(e)
            return Response.error(message=missing_fields, code=400)
        
        response = ProductService.add_product(validate_product.model_dump())
        
        if response is None:
            return Response.error(message='Oops, something went wrong', code=400)
        
        return response
    
    @staticmethod
    def update_product(id):
        data = request.get_json()
        
        try:
            validate_product = UpdateProduct.model_validate(data)
        except ValidationError as e:
            missing_fields = handle_field_error(e)
            return Response.error(message=missing_fields, code=400)
        
        response = ProductService.update_product(id, validate_product.model_dump(exclude_none=True))
        
        if response is None:
            return Response.error(message='Oops, something went wrong', code=400)
        
        return response