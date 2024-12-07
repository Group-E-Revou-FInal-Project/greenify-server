from datetime import datetime, timezone
from math import ceil
import random
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.products import Product
from app.models.categories import Category
from app.models.users import User


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
    def update_product(user_id, product_id, data):
        product = Product.query.filter_by(id=product_id).first()
        user_check = User.query.filter_by(id=user_id).first()
        
        if product is None:
            return "product not found"
        
        if product.seller_id != user_check.seller_profile.id:
            return "seller id does not match"
        
        product.product_name = data.get('product_name', product.product_name)
        product.price = data.get('price', product.price)
        product.discount = data.get('discount', product.discount)
        product.product_desc = data.get('product_desc', product.product_desc)
        product.stock = data.get('stock', product.stock)
        product.min_stock = data.get('min_stock', product.min_stock)
        product.category_id = data.get('category_id', product.category_id)
        product.eco_point = data.get('eco_point', product.eco_point)
        product.recycle_material_percentage = data.get('recycle_material_percentage', product.recycle_material_percentage)
        product.image_url = data.get('image_url', product.image_url)
        
        db.session.add(product)
        db.session.commit()
        
        return product.to_dict()
        
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

        # Get user's interests (categories they are interested in)
        interest_ids = [category.id for category in user.interests]

        # Start building the query for recommendations
        recommendations_query = Product.query

        
        if interest_ids:
            recommendations_query = recommendations_query.filter(Product.category_id.in_(interest_ids))
        
        # Paginate the recommendations
        recommendations_paginated = recommendations_query.paginate(page=page, per_page=per_page, error_out=False)

        new_arrivals = Product.query.order_by(Product.id.desc()).limit(20).all()
        random_products = Product.query.order_by(db.func.random()).limit(20).all()
        recommendations_paginated.items += new_arrivals + random_products
            

        # Ensure uniqueness by converting to a set of product IDs
        unique_recommendations = {product.id: product for product in recommendations_paginated.items}.values()

        # Total number of items and pages
        total_items = len(unique_recommendations)
        total_pages = ceil(total_items / per_page)

        # Pagination logic
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_recommendations = list(unique_recommendations)[start_index:end_index]

        # Return the paginated recommendations
        return {
            "page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages,
            "data": [{"id": p.id, "name": p.product_name, "category": p.category.category_name} for p in paginated_recommendations]
        }
    
    
