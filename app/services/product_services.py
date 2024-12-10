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
    def add_product(user_id, data):
        user = User.query.filter_by(id=user_id).first()
        
        if user is None:
            return None
        
        print(user.seller_profile)
        
        seller_id = user.seller_profile.id
        
        if seller_id is None:
            return None
        
        new_product = Product(seller_id=seller_id, 
                              product_name=data['product_name'], 
                              price=data['price'],
                              discount=data['discount'], 
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
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            return None
        
    @staticmethod
    def update_product(user_id, product_id, data):
        product = Product.query.filter_by(id=product_id).first()
        user_check = User.query.filter_by(id=user_id).first()
        
        if product is None:
            return { "error" : "product not found" }
        
        if product.seller_id != user_check.seller_profile.id:
            return { "error" : "seller id does not match" }
        
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
        if product is None:
            return None
        return product.to_dict()
    
    @staticmethod
    def delete_product(id):
        product = Product.query.filter_by(id=id).first()
        if product is None:
            return None        

        product.soft_delete()
        db.session.add(product)        
        db.session.commit()        
        return product.to_dict()
    
    @staticmethod
    def restore_product(id):
        product = Product.query.filter_by(id=id).first()
        
        if product is None:
            return None        

        product.restore()
        db.session.add(product)        
        db.session.commit()        
        return product.to_dict()
    
    @staticmethod
    def get_products_by_filters(category, min_price, max_price, page, per_page):
        if max_price is None:
            max_price = 99999999999
            
        if min_price is None:
            min_price = 0
            
        category_id = Category.query.filter_by(category_name=category).first()
            
        if category_id is None:
            products = Product.query.filter(Product.price.between(min_price, max_price))
        else:
            products = Product.query.filter(Product.category_id == category_id.id, Product.price.between(min_price, max_price))
            
        # Pagination products
        products = products.paginate(page=page, per_page=per_page, error_out=False)
        
        # Calculate pagination details
        total_pages = products.pages
        total_products = products.total
        start_page = (page - 1) * per_page
        end_page = start_page + per_page
        products_paginated = products.items[start_page:end_page]
            
        return {
                "total_pages": total_pages, 
                "total_products": total_products, 
                "products": [product.to_dict() for product in products_paginated]
        }              
    
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
    
    
