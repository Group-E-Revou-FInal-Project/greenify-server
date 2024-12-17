import json
from flask import request
from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from app.constants.response_status import Response
from app.services.product_services import ProductService 
from app.utils.validators import AddCategory, Product, UpdateProduct
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
        user_id = json.loads(get_jwt_identity())['user_id']
        
        try:
            validate_product = Product.model_validate(data)
        except ValidationError as e:
            missing_fields = handle_field_error(e)
            return Response.error(message=missing_fields, code=400)
        
        response = ProductService.add_product(user_id, validate_product.model_dump())
        
        if response is None:
            return Response.error(message='Oops, something went wrong', code=400)
        
        return response
    
    @staticmethod
    def update_product(product_id):
        data = request.get_json()
        user_id = json.loads(get_jwt_identity())['user_id']
        
        try:
            validate_product = UpdateProduct.model_validate(data)
        except ValidationError as e:
            missing_fields = handle_field_error(e)
            return Response.error(message=missing_fields, code=400)
        
        response = ProductService.update_product(user_id, product_id, validate_product.model_dump(exclude_none=True))
        
        if "error" in response:
            return Response.error(message=response["error"], code=400)
        
        return Response.success(data=response, message="Success update product", code=200)
    
    @staticmethod
    def get_product_by_id(product_id):
        response = ProductService.get_product_by_id(product_id)
        if response is None:
            return Response.error("Product not found", 404)
        return Response.success(data=response, message="Success get data product", code=200)
    
    @staticmethod
    def delete_product(product_id):
        response = ProductService.delete_product(product_id)
        if response is None:
            return Response.error("Product not found", 404)
        return Response.success(data=response, message="Success delete product", code=200)
    
    @staticmethod
    def restore_product(product_id):
        response = ProductService.restore_product(product_id)
        if response is None:
            return Response.error("Product not found", 404)
        return Response.success(data=response, message="Success restore product", code=200)
    
    @staticmethod
    def get_all_products():
        response = ProductService.get_all_products()
        if response is None:
            Response.error(message='Products not found', code=400)
        return Response.success(data=response, message="Success get data product", code=200)
    
    @staticmethod
    def get_products():
        try:
            if not request.args:
                response = ProductService.get_all_products()
                return Response.success(data=response, message="Success get data product", code=200)
            
            # Extract query parameters
            category = request.args.get('category')
            min_price = request.args.get('min_price')
            max_price = request.args.get('max_price')
            has_discount = request.args.get('has_discount') 
            page = int(request.args.get('page'))
            per_page = int(request.args.get('per_page', 20))
            sort_order = request.args.get('sort_order', default='asc')
            has_discount = has_discount.lower() == 'true' if has_discount is not None else None

            response = ProductService.get_products_by_filters(
                category=category,
                min_price=min_price,
                max_price=max_price,
                has_discount=has_discount,
                page=page,
                per_page=per_page,
                sort_order=sort_order
            )

            return Response.success(data=response, message="Success get data product", code=200)

        except ValueError:
            # Handle invalid inputs for pagination or filters
            return Response.error(message="Invalid parameters", code=400)
        except Exception as e:
            # General error handling
            return Response.error(message=f"Oops, something went wrong: {str(e)}", code=500)

    
    @staticmethod
    def landing_product():
        data = request.get_json()
        
        try:
            validate_product = Product.model_validate(data)
        except ValidationError as e:
            missing_fields = handle_field_error(e)
            return Response.error(message=missing_fields, code=400)
        
        response = ProductService.add_product(validate_product.model_dump())
        
        if response is None:
            return Response.error(message='Oops, something went wrong', code=400)
        
        return response
    
    @staticmethod
    def recommendation_product():
        user_id = json.loads(get_jwt_identity())['user_id']
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        recommendations = ProductService.get_recommendations(user_id, page, per_page)
        return Response.success(data=recommendations, message="Success get data recommendation", code=200)
