from flask import json, request
from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from app.constants.response_status import Response
from app.services.wishlist_services import WishlistService
from app.utils.validators import AddWishlist

class WishlistController:
    @staticmethod
    def add_to_wishlist():
        data = request.get_json()
        user_id = json.loads(get_jwt_identity())['user_id']
        
        # Validate the request data
        try:
            validate_wishlist = AddWishlist.model_validate(data)
        except ValidationError as e:
            return Response.error(f"{str(e)}", 400)

        # Call the service method to handle the logic
        response = WishlistService.add_to_wishlist(user_id, validate_wishlist.model_dump())

        # Handle errors returned from the service
        if isinstance(response, dict) and response.get("error"):
            return Response.error(message=response["error"], code=500)

        # Return success response (always success if it's already in the wishlist or newly added)
        return Response.success(
            data=response.get("wishlist"),
            message=response.get("message", "Added to wishlist successfully."),
            code=200
        )
    
    @staticmethod
    def get_user_wishlist():
        user_id = json.loads(get_jwt_identity())['user_id']
        wishlist = WishlistService.get_user_wishlist(user_id)
        return Response.success(data=wishlist, message="Fetched wishlist successfully", code=200)
    
    @staticmethod
    def remove_from_wishlist():
        data = request.get_json()
        user_id = json.loads(get_jwt_identity())['user_id']
        product_id = data.get('product_id')
        
        if not product_id:
            return Response.error(message="Product ID is required", code=400)
        
        success = WishlistService.remove_from_wishlist(user_id, product_id)
        
        if not success:
            return Response.error(message='Failed to remove from wishlist', code=400)
        
        return Response.success(message='Removed from wishlist successfully', code=200)
    
    @staticmethod
    def clear_wishlist():
        user_id = json.loads(get_jwt_identity())['user_id']
        success = WishlistService.clear_wishlist(user_id)
        
        if not success:
            return Response.error(message='Failed to clear wishlist', code=400)
        
        return Response.success(message='Wishlist cleared successfully', code=200)
