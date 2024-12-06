from datetime import datetime, timezone
from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.products import Product
from app.models.categories import Category


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
            return "Ops, something went wrong"
        
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
    
    
