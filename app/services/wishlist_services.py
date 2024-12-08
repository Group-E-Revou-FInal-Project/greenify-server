from app.configs.connector import db
from app.models.wishlist import Wishlist
from app.models.products import Product

class WishlistService:
    
    @staticmethod
    def add_to_wishlist(user_id, data):
        product_id = data['product_id']
        existing_wishlist = Wishlist.query.filter_by(user_id=user_id, 
                                                     product_id=product_id,
                                                     is_active=True).first()
        
        if existing_wishlist:
            return None  
        
        new_wishlist = Wishlist(user_id=user_id, product_id=product_id)
        
        try:
            db.session.add(new_wishlist)
            db.session.commit()
            return new_wishlist.to_dict()
        except Exception:
            db.session.rollback()
            return None
    
    @staticmethod
    def get_user_wishlist(user_id):
        wishlist_items = Wishlist.query.filter_by(user_id=user_id, is_active=True).all()
        return [item.to_dict() for item in wishlist_items]
    
    @staticmethod
    def remove_from_wishlist(user_id, product_id):
        wishlist_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id, is_active=True).first()
        
        if not wishlist_item:
            return False
        
        try:
            wishlist_item.is_active = False  # Soft delete (set is_active to False)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def clear_wishlist(user_id):
        wishlist_items = Wishlist.query.filter_by(user_id=user_id, is_active=True).all()
        
        try:
            for item in wishlist_items:
                item.is_active = False  # Soft delete all items
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
