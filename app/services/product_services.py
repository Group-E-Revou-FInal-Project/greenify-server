from datetime import datetime, timezone
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
    
    
