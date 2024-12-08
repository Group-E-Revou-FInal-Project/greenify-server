from datetime import datetime, timezone
from math import ceil
import random
from flask import Response, jsonify
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.products import Product
from app.models.categories import Category
from app.models.sellers import Seller
from app.models.users import User
from app.models.wishlist import Wishlist


class ProductService:
    @staticmethod
    def add_category(data):
        new_category = Category(category_name=data['category_name'])
        
        try:
            db.session.add(new_category)
            db.session.commit()
            return new_category.to_dict()
        except IntegrityError:
            db.session.rollback()
            return None
        
    @staticmethod
    def add_product(data):
        new_product = Product(seller_id=data['seller_id'], 
                              product_name=data['product_name'], 
                              price=data['price'], 
                              product_desc=data['product_desc'], 
                              stock=data['stock'], 
                              min_stock=data['min_stock'], 
                              category_id=data['category_id'],
                              eco_point=data['eco_point'],
                              recycle_material_percentage=data['recycle_material_percentage'])
        
        try:
            db.session.add(new_product)
            db.session.commit()
            return new_product.to_dict()
        except IntegrityError:
            db.session.rollback()
            return None
        
    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return [category.to_dict() for category in categories]
    
    @staticmethod
    def get_all_products():
        products = Product.query.all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_product_by_id(id):
        product = Product.query.filter_by(id=id).first()
        return product.to_dict()
    
    @staticmethod
    def get_filter_product(filter, value):
        products = Product.query.filter_by(**{filter: value}).all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_recommendations(user_id, page, per_page):
        # Get the user
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        seller = Seller.query.filter_by(user_id=user_id).first()
        seller_id = seller.id if seller else None

        interest_ids = [category.id for category in user.interests]

        wishlisted_products = db.session.query(Wishlist.product_id).filter_by(user_id=user_id).subquery()

        recommendations_query = Product.query

        if interest_ids:
            recommendations_query = recommendations_query.filter(Product.category_id.in_(interest_ids))

        if seller_id:
            recommendations_query = recommendations_query.filter(Product.seller_id != seller_id)

       
        recommendations_query = recommendations_query.filter(Product.id.in_(wishlisted_products))

     
        new_arrivals = Product.query.filter(Product.seller_id != seller_id).order_by(Product.id.desc()).limit(20).all()
        random_products = Product.query.filter(Product.seller_id != seller_id).order_by(func.random()).limit(20).all()

        # Paginate the recommendations query
        recommendations_paginated = recommendations_query.paginate(page=page, per_page=per_page, error_out=False)

        combined_recommendations = recommendations_paginated.items + new_arrivals + random_products
        unique_recommendations = {product.id: product for product in combined_recommendations}.values()

        # Calculate pagination details
        total_items = len(unique_recommendations)
        total_pages = ceil(total_items / per_page)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_recommendations = list(unique_recommendations)[start_index:end_index]

        # Return paginated response
        return {
            "page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages,
            "data": [
                {
                    "id": p.id,
                    "name": p.product_name,
                    "price": float(p.price),
                    "discount": float(p.discount) if p.discount else None,
                    "category": p.category.category_name,
                    "image_url": p.image_url,
                    "eco_point": p.eco_point,
                    "recycle_material_percentage": p.recycle_material_percentage,
                }
                for p in paginated_recommendations
            ]
        }
    
    
