from datetime import datetime, timezone
from math import ceil
import random
from flask import Response, jsonify
from sqlalchemy import func, or_
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
    def get_categories(data):
        categories = Category.query.all()
        return [category.to_dict() for category in categories]        
        
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
                              recycle_material_percentage=data['recycle_material_percentage'],
                              image_url=data['image_url'])
        
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
        try:
            product = Product.query.filter_by(id=product_id).first()
            if product is None:
                return {"error": "product not found"}

            user_check = User.query.filter_by(id=user_id).first()
            print(user_check)
            if user_check is None or user_check.seller_profile is None:
                return {"error": "user or seller profile not found"}

            if product.seller_id != user_check.seller_profile.id:
                return {"error": "seller id does not match"}

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

        except IntegrityError as e:
            db.session.rollback()
            return {"error": "integrity error occurred", "details": str(e)}
        except Exception as e:
            db.session.rollback()
            return {"error": "an unexpected error occurred", "details": str(e)}

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
        try:
            product = Product.query.filter_by(id=id).first()
            if product is None:
                return None        

            product.soft_delete()
            db.session.add(product)        
            db.session.commit()      
        except Exception as e:
            db.session.rollback()
            return None
          
        return product.to_dict()
    
    @staticmethod
    def restore_product(id):
        try:
            product = Product.query.filter_by(id=id).first()
            
            if product is None:
                return None        

            product.restore()
            db.session.add(product)        
            db.session.commit()       
        except Exception as e:
            db.session.rollback()
            return None
        return product.to_dict()
    

    @staticmethod
    def get_products_by_filters(words, category, min_price, max_price, has_discount, page, per_page, sort_order="asc"):
        try:
            # Default price range if not provided
            min_price = float(min_price) if min_price is not None else 0
            max_price = float(max_price) if max_price is not None else 99999999999

            # Ensure `words` is not None, as `.contains()` cannot operate on None
            words = (words or "").strip().lower() 
            words = ' '.join(words.split()) 

            # Start building the query
            query = Product.query.filter(
                Product.product_name.ilike(f"%{words}%"),  # Use ilike for case-insensitive search
                Product.price.between(min_price, max_price),
                Product.is_deleted.is_(False)  # Use is_ for boolean checks
            )

            # Handle category filter
            if category:
                category_obj = Category.query.filter_by(category_name=category).first()
                if category_obj:
                    query = query.filter(Product.category_id == category_obj.id)

            # Handle has_discount filter
            if has_discount is not None:
                if has_discount:  
                    query = query.filter(Product.discount > 0)
                else: 
                    query = query.filter(or_(Product.discount.is_(None), Product.discount == 0))  # Handle NULL or 0 discount

            # Handle sort order
            if sort_order == "asc":
                query = query.order_by(Product.created_at.asc())  # Ascending order
            elif sort_order == "desc":
                query = query.order_by(Product.created_at.desc())  # Descending order

            # Pagination logic
            total_products = query.count()
            products = query.offset((page - 1) * per_page).limit(per_page).all()
            total_pages = ceil(total_products / per_page)

            # Return the response
            return {
                "products": [product.to_dict() for product in products],
                "pagination": {
                    "total_products": total_products,
                    "total_pages": total_pages,
                    "current_page": page,
                    "per_page": per_page
                }
            }
        except Exception as e:
            # Log the error for debugging
            print(f"Error in get_products_by_filters: {e}")
            raise e  # Re-raise the exception for visibility

    
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
        
    @staticmethod
    def get_all_seller_products(seller_id):
        products = Product.query.filter_by(seller_id=seller_id, is_deleted=False).all()
        
        if not products:
            return None
    
        return [product.to_dict() for product in products]
    
    
