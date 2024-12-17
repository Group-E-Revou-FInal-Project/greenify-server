from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.sellers import Seller
from app.models.users import User, Role

class SellerService:
    @staticmethod
    def create_seller(data):
        role = Role.query.filter_by(rolename='seller').first()
        
        if role is None:
            return { 'error': 'Role not found' }
        
        user = User.query.filter_by(id=data['user_id']).first()
        
        if user is None:
            return { 'error': 'User not found' }
        
        new_seller = Seller(user_id=data['user_id'], 
                            store_name=data['store_name'], 
                            store_description=data['store_description'], 
                            store_logo=data['store_logo'], 
                            address=data['address'], 
                            phone_number=data['phone_number'])
        
        try:
            user.roles.append(role)
            db.session.add(new_seller)
            db.session.commit()
            return new_seller.to_dict()
        except IntegrityError:     
            db.session.rollback()
            return None
        
    @staticmethod
    def get_id_seller(user_id):
        seller = Seller.query.filter_by(user_id=user_id).first()
        
        if seller is None:
            return None
        
        return seller.id
        
    @staticmethod
    def seller_profile(seller_id):
        seller = Seller.query.filter_by(id=seller_id).first()
        
        if seller is None:
            return None
        
        return seller.to_dict()
        
    @staticmethod
    def update_seller(data):
        seller = Seller.query.filter_by(user_id=data['user_id']).first()
        
        if seller is None:
            return None
        
        seller.store_name = data.get('store_name', seller.store_name)
        seller.store_description = data.get('store_description', seller.store_description)
        seller.store_logo = data.get('store_logo', seller.store_logo)
        seller.address = data.get('address', seller.address)
        seller.phone_number = data.get('phone_number', seller.phone_number)
        
        try:
            db.session.add(seller)
            db.session.commit()
            return seller.to_dict()
        except IntegrityError:     
            db.session.rollback()
            return None
    
    @staticmethod
    def deactive_seller(seller_id, action=False):
        seller = Seller.query.filter_by(id=seller_id).first()
        
        if seller is None:
            return None
        
        seller.is_active = action
        
        try:
            db.session.add(seller)
            db.session.commit()
            return seller.to_dict()
        except IntegrityError:     
            db.session.rollback()
            return None
    
        