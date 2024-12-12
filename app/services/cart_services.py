from app.configs.connector import db
from app.models.carts import Cart

class CartService:
    
    @staticmethod
    def add_to_cart(data):
        try:
            cart = Cart.query.filter_by(user_id=data['user_id'], product_id=data['product_id']).first()
            
            if cart is not None:
                cart.quantity += 1
            else:
                cart = Cart(user_id=data['user_id'], 
                            product_id=data['product_id'])
            
            db.session.add(cart)
            db.session.commit()
        except ValueError:
            db.session.rollback()
            return None
        return cart.to_dict()
    
    @staticmethod
    def get_carts(user_id):
        carts = Cart.query.filter_by(user_id=user_id).all()
        
        if carts is None:
            return []
        
        return [cart.to_dict() for cart in carts]
    
    @staticmethod
    def decrease_cart(data):
        try:
            cart = Cart.query.filter_by(user_id=data['user_id'], product_id=data['product_id']).first()
            
            if cart is None:
                return { 'error': 'Product not found' }
            
            cart.quantity -= 1
            
            db.session.add(cart)
            db.session.commit()
        except ValueError:
             db.session.rollback()
             return None
            
        return cart.to_dict()
    
    @staticmethod
    def update_cart_quantity(data):
        try:
            cart = Cart.query.filter_by(user_id=data['user_id'], product_id=data['product_id']).first()
            
            if cart is None:
                return { 'error': 'Cart not found' }
            
            cart.quantity = data['quantity']
            
            
            db.session.add(cart)
            db.session.commit()
        except ValueError:
            db.session.rollback()
            return None
            
        return cart.to_dict()