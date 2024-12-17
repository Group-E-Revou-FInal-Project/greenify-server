import json
from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from app.services.review_services import ReviewService
from flask import request
from app.utils.validators import Review
from app.utils.functions.handle_field_error import handle_field_error
from app.constants.response_status import Response


class ReviewController:
    
    @staticmethod
    def add_review():
        data = request.get_json()
        data['user_id'] = json.loads(get_jwt_identity())['user_id']
        
        try:
            validated_data = Review.model_validate(data)
        except ValidationError as e:
            print(f'error: {e}')
            message = handle_field_error(e)
            return Response.error(message=message, code=400)

        response = ReviewService.add_review(validated_data.model_dump(exclude_none=True))
        if "error" in response:
            return Response.error(message=response["error"], code=400)

        return Response.success(data=response, message="Review added successfully", code=201)
    
    @staticmethod
    def get_reviews():
        user_id = json.loads(get_jwt_identity())['user_id']
        response = ReviewService.get_reviews(user_id)
        return Response.success(data=response, message="Review fetched successfully", code=200)
    
    @staticmethod
    def get_good_reviews():
        response = ReviewService.get_good_reviews()
        return Response.success(data=response, message="Good reviews fetched successfully", code=200)
    
    @staticmethod
    def delete_review(review_id):
        data = request.get_json()
        data['user_id'] = json.loads(get_jwt_identity())['user_id']
        data['id'] = review_id
        
        try:
            validate_data = Review.model_validate(data)
        except ValidationError as e:
            print(f'error: {e}')
            message = handle_field_error(e)
            return Response.error(message=message, code=400)
        
        response = ReviewService.delete_review(validate_data.model_dump(exclude_none=True))
        
        if response is None:
            return Response.error(message='Review not found', code=400)
        
        return Response.success(data=response, message='Reviews deleted successfully', code=200)
    
    @staticmethod
    def get_all_seller_reviews(seller_id):
        response = ReviewService.get_reviews_by_seller(seller_id)
        return Response.success(data=response, message="Seller reviews fetched successfully", code=200)