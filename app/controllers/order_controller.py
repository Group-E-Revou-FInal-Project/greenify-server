import json

from pydantic import ValidationError
from app.models.transactions_history import TransactionHistory
from app.utils.validators.invoince_validate import validate_invoice_number
from app.utils.validators import OrderPayment
from flask import request
from app.constants.response_status import Response
from flask_jwt_extended import get_jwt_identity
from app.models.sellers import Seller
from app.services.order_services import OrderService
from app.utils.functions.handle_field_error import handle_field_error
from app.configs.connector import db

class OrderController:
    
    @staticmethod
    def get_all_order():
        user_id = json.loads(get_jwt_identity())['user_id']
        response = OrderService.get_order(user_id)
        return Response.success(data=response, message="Orders fetched successfully", code=200)
    
    @staticmethod
    def create_order():
        user_id = json.loads(get_jwt_identity())['user_id']
        response = OrderService.create_order(user_id)
        return Response.success(data=response, message="Order created successfully", code=201)
    
    @staticmethod
    def get_order_by_id(order_id):
        user_id = json.loads(get_jwt_identity())['user_id']
        
        response = OrderService.get_order_by_id(order_id, user_id)
        
        if 'error' in response:
            return Response.error(message=response['error'], code=404)
        
        return Response.success(data=response, message="Order fetched successfully", code=200)
    
    @staticmethod
    def get_order_items(order_id):
        user_id = json.loads(get_jwt_identity())['user_id']
        
        response = OrderService.get_order_items(order_id, user_id)
        
        if 'error' in response:
            return Response.error(message=response['error'], code=404)
        
        return Response.success(data=response, message="Order fetched successfully", code=200)
    
    @staticmethod
    def payment_order():
        data = request.get_json()
        data['user_id'] = json.loads(get_jwt_identity())['user_id']
        
        try:
            validate_payment = OrderPayment.model_validate(data)
        except ValidationError as e:
            message = handle_field_error(e)
            return Response.error(message=message, code=400)
        except ValueError as e:
            return Response.error(f"{str(e)}", 400)
        
        response = OrderService.payment_order(validate_payment.model_dump(exclude_none=True))
        
        if response is None:
            return Response.error(message="Order not found", code=404)
            
        return Response.success(data=response, message="Order payment successfully", code=200)
    
    @staticmethod
    def cancel_order():
        invoice_number = request.get_json()['invoice_number']
        user_id = json.loads(get_jwt_identity())['user_id']
        
        response = OrderService.cancel_order(invoice_number, user_id)
        
        if response is None:
            return Response.error(message="Order not found", code=404)
            
        return Response.success(data=response, message="Order canceled successfully", code=200)
    
    @staticmethod
    def get_user_transaction_history():
        user_id = json.loads(get_jwt_identity())['user_id']
        response = OrderService.get_user_transaction_history(user_id)
        return Response.success(data=response, message="Transaction history fetched successfully", code=200)
    
    def get_seller_transaction_history():
        user_id = json.loads(get_jwt_identity())['user_id']

        # Validate if the user has a seller profile
        seller = Seller.query.filter_by(user_id=user_id).first()
        if not seller:
            return {"error": "You are not authorized to access seller transactions."}, 403
        response = OrderService.get_seller_transaction_history(seller.id)
        
        return Response.success(data=response, message="Transaction history fetched successfully", code=200)
    
    @staticmethod
    def get_seller_metrics():
        try:
            user_id = json.loads(get_jwt_identity())['user_id']

            # Check if the user has a seller profile
            seller = Seller.query.filter_by(user_id=user_id).first()
            if not seller:
                return Response.error(
                    message="You are not authorized to access seller metrics.",
                    code=403,
                )

            # Fetch metrics
            total_selling = db.session.query(db.func.sum(TransactionHistory.price)).filter_by(seller_id=seller.id).scalar() or 0
            total_buyers = db.session.query(TransactionHistory.user_id).filter_by(seller_id=seller.id).distinct().count()
            pending_sales = db.session.query(TransactionHistory).filter_by(seller_id=seller.id, status="Pending").count()
            total_rating = 4.5  # Placeholder for ratings logic if available

            metrics = {
                "total_selling": total_selling,
                "total_buyers": total_buyers,
                "total_rating": total_rating,
                "pending_sales": pending_sales,
            }

            return Response.success(
                data=metrics,
                message="Metrics fetched successfully.",
                code=200,
            )
        except Exception as e:
            return Response.error(
                message=f"An error occurred while fetching metrics: {str(e)}",
                code=500,
            )
            
            
    