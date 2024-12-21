from datetime import datetime, timedelta
import json

from pydantic import ValidationError
from sqlalchemy import extract, func, text
from app.constants.enums import TransactionStatus
from app.models.products import Product
from app.models.reviews import Review
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
            seller = Seller.query.filter(Seller.user_id == user_id).first()
            if not seller:
                return Response.error(
                    message="You are not authorized to access seller metrics.",
                    code=403,
                )

            # Query 1: Total selling
            total_selling = (
                db.session.query(func.sum(TransactionHistory.price))
                .filter(TransactionHistory.seller_id == seller.id)
                .scalar()
                or 0
            )

            # Query 2: Total buyers
            total_buyers = (
                db.session.query(TransactionHistory.user_id)
                .filter(TransactionHistory.seller_id == seller.id)
                .distinct()
                .count()
            )

            # Query 3: Pending sales with Enum to Text cast
            pending_sales = (
                db.session.query(func.count(TransactionHistory.id))
                .filter(
                    TransactionHistory.seller_id == seller.id,
                    text("transactions_history.status::TEXT = 'Pending'")  # Cast Enum to Text
                )
                .scalar()
            )

            # Placeholder for total rating
            total_rating_query = (
                db.session.query(func.avg(Review.rating))
                .join(Product, Review.product_id == Product.id)
                .filter(Product.seller_id == seller.id, Review.is_deleted == False)
            )
            total_rating = total_rating_query.scalar() or 0  # Default to 0 if no reviews

            # Construct metrics
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
            
    @staticmethod
    def get_sales_data():
        try:
            user_id = json.loads(get_jwt_identity())['user_id']

            # Check if the user has a seller profile
            seller = Seller.query.filter(Seller.user_id == user_id).first()
            if not seller:
                return Response.error(
                    message="You are not authorized to access seller metrics.",
                    code=403
                )

            # Retrieve the filter from query parameters
            filter_by = request.args.get('filter', 'month')  # Default to "month"
            query = db.session.query(
                func.sum(TransactionHistory.price).label("total_sales")
            )
            labels, data = [], []

            if filter_by == 'day':
                # Group by day
                query = query.add_columns(func.date(TransactionHistory.created_at).label("grouped_date"))
                query = query.filter(TransactionHistory.created_at >= datetime.now() - timedelta(days=7))
                query = query.group_by(func.date(TransactionHistory.created_at))
                results = query.filter(TransactionHistory.seller_id == seller.id).all()
                labels = [(datetime.now() - timedelta(days=i)).strftime("%a") for i in range(7)][::-1]
                data = [next((r.total_sales for r in results if r.grouped_date.strftime("%a") == day), 0) for day in labels]

            elif filter_by == 'month':
                # Group by month
                query = query.add_columns(
                    extract('month', TransactionHistory.created_at).label("grouped_month"),
                    extract('year', TransactionHistory.created_at).label("grouped_year")
                )
                query = query.filter(extract('year', TransactionHistory.created_at) == datetime.now().year)
                query = query.group_by(
                    extract('month', TransactionHistory.created_at),
                    extract('year', TransactionHistory.created_at)
                )
                results = query.filter(TransactionHistory.seller_id == seller.id).all()
                labels = ["Jan", "Feb", "Mar", "Apr", "May"]
                data = [next((r.total_sales for r in results if int(r.grouped_month) == i + 1), 0) for i in range(5)]

            elif filter_by == 'year':
                # Group by year
                query = query.add_columns(extract('year', TransactionHistory.created_at).label("grouped_year"))
                query = query.group_by(extract('year', TransactionHistory.created_at))
                results = query.filter(TransactionHistory.seller_id == seller.id).all()
                labels = [str(datetime.now().year - i) for i in range(5)][::-1]
                data = [next((r.total_sales for r in results if int(r.grouped_year) == int(year)), 0) for year in labels]

            else:
                return Response.error(
                    message="Invalid filter. Valid options are 'day', 'month', 'year'.",
                    code=400
                )

            metrics = {
                "labels": labels,
                "data": data
            }

            return Response.success(
                data=metrics,
                message="Sales data fetched successfully.",
                code=200
            )

        except Exception as e:
            return Response.error(
                message=f"An error occurred while fetching sales data: {str(e)}",
                code=500
            )



                
            
    