from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.sellers import Seller

class SellerService:
    @staticmethod
    def create_seller(data):
        new_seller = Seller(user_id=data['user_id'], 
                            store_name=data['store_name'], 
                            store_description=data['store_description'], 
                            store_logo=data['store_logo'], 
                            address=data['address'], 
                            phone_number=data['phone_number'])
        
        try:
            db.session.add(new_seller)
            db.session.commit()
            return new_seller.to_dict()
        except IntegrityError:     
            db.session.rollback()
            return None
        
    @staticmethod
    def update_seller(data):
        seller = Seller.query.filter_by(id=data['id']).first()
        
        if seller is None:
            return None
        
        seller.store_name = data['store_name']
        seller.store_description = data['store_description']
        seller.store_logo = data['store_logo']
        seller.address = data['address']
        seller.phone_number = data['phone_number']
        
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
    
        