from app.configs.connector import db
from app.models.carts import Cart
from app.models.products import Product
from sqlalchemy.exc import IntegrityError

class CartService:
    
    @staticmethod
    def add_to_cart(data):
        try:
            cart = Cart.query.filter_by(user_id=data['user_id'], product_id=data['product_id']).first()
            
            if cart is not None:
                cart.quantity += 1
                if cart.quantity > cart.product.stock:
                    return { 'error': f'Stock of {cart.product.product_name} is not enough' }
            else:
                product = Product.query.filter_by(id=data['product_id']).first()
                if 1 > product.stock:
                    return { 'error': f'Stock of {product.product_name} is not enough' }
                cart = Cart(user_id=data['user_id'], 
                            product_id=data['product_id'])
            
            db.session.add(cart)
            db.session.commit()
            return cart.to_dict()
        except ValueError as e:
            db.session.rollback()
            return { 'error': f'{e}' }
        except IntegrityError as e:
            db.session.rollback()
            return { 'error': 'Integrity error occured' }
    
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
            
            if cart.quantity <= 0:
                db.session.delete(cart)
                db.session.commit()
                return None
            
            db.session.add(cart)
            db.session.commit()

            return cart.to_dict()
        except IntegrityError:
             db.session.rollback()
             return { 'error': 'Integrity error occured' }
            
    @staticmethod
    def update_cart_quantity(data):
        try:
            cart = Cart.query.filter_by(user_id=data['user_id'], product_id=data['product_id']).first()
            
            if cart is None:
                return { 'error': 'Product not found' }
            
            cart.quantity = data['quantity']
            
            if cart.quantity >= cart.product.stock:
                return { 'error': f'Stock of {cart.product.product_name} is not enough' }
            
            if cart.quantity <= 0:
                db.session.delete(cart)
                db.session.commit()
                return None
            
            db.session.add(cart)
            db.session.commit()
            return cart.to_dict()
        except IntegrityError:
            db.session.rollback()
            return { 'error': 'Integrity error occured' }
            