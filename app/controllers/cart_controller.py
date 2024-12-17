import json
from flask import request
from flask_jwt_extended import get_jwt_identity
from app.services.cart_services import CartService
from app.utils.validators import Cart
from app.constants.response_status import Response
from app.utils.functions.handle_field_error import handle_field_error


class CartController:
    
    @staticmethod
    def add_to_cart():
        data = request.get_json()
        data['user_id'] = json.loads(get_jwt_identity())['user_id']
        
        try:
            validate_cart = Cart.model_validate(data)
        except ValueError as e:
            message = handle_field_error(e)
            return Response.error(message=message, code=400)
        
        response = CartService.add_to_cart(validate_cart.model_dump(exclude_none=True))
        
        if 'error' in response:
            return Response.error(message=response['error'], code=400)
        
        return Response.success(data=response, message='Success add to cart', code=201)
    
    @staticmethod
    def decrease_cart():
        data = request.get_json()
        data['user_id'] = json.loads(get_jwt_identity())['user_id']
        
        try:
            validate_cart = Cart.model_validate(data)
        except ValueError as e:
            message = handle_field_error(e)
            return Response.error(message=message, code=400)
        
        response = CartService.decrease_cart(validate_cart.model_dump(exclude_none=True))
        
        if response is None:
            return Response.success(data=response, message='Success remove item from cart', code=200)
        
        if 'error' in response:
            return Response.error(message=response['error'], code=400)
        
        
        return Response.success(data=response, message='Success decrease cart', code=200)
    
    @staticmethod
    def get_carts():
        user_id = json.loads(get_jwt_identity())['user_id']
        response = CartService.get_carts(user_id)
        
        if response == []:
            return Response.success(data=response, message='Cart is empty', code=200)
        
        
        return Response.success(data=response, message='Success get carts', code=200)
    
    @staticmethod
    def update_cart_quantity():
        data = request.get_json()
        data['user_id'] = json.loads(get_jwt_identity())['user_id']
        
        try:
            validate_cart = Cart.model_validate(data)
        except ValueError as e:
            message = handle_field_error(e)
            return Response.error(message=message, code=400)
        
        response = CartService.update_cart_quantity(validate_cart.model_dump(exclude_none=True))
        
        if response is None:
            return Response.success(data=response, message='Success remove item from cart', code=200)
        
        if 'error' in response:
            return Response.error(message=response['error'], code=400)
        
        
        return Response.success(data=response, message='Success update cart quantity', code=200)