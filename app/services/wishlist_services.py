from app.configs.connector import db
from app.models.wishlist import Wishlist
from app.models.products import Product

class WishlistService:
    
    @staticmethod
    def add_to_wishlist(user_id, data):
        product_id = data.get('product_id')
        
        if not product_id:
            return {"error": "Product ID is required."}, 400

        # Check for existing wishlist
        existing_wishlist = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()

        if existing_wishlist:
            # If already active, return success with existing wishlist
            if existing_wishlist.is_active:
                return {
                    "success": True,
                    "message": "Product is already in the wishlist.",
                    "wishlist": existing_wishlist.to_dict()
                }

            # Reactivate soft-deleted wishlist
            existing_wishlist.is_active = True
            try:
                db.session.commit()
                return {
                    "success": True,
                    "message": "Wishlist reactivated successfully.",
                    "wishlist": existing_wishlist.to_dict()
                }
            except Exception as error:
                db.session.rollback()
                return {"error": f"Failed to reactivate wishlist: {str(error)}"}, 500

        # Create a new wishlist entry
        new_wishlist = Wishlist(user_id=user_id, product_id=product_id)
        try:
            db.session.add(new_wishlist)
            db.session.commit()
            return {
                "success": True,
                "message": "Product added to wishlist successfully.",
                "wishlist": new_wishlist.to_dict()
            }
        except Exception as error:
            db.session.rollback()
            return {"error": f"Failed to add to wishlist: {str(error)}"}, 500


    
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
