from app.models.carts import Cart
from app.models.products import Product
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.configs.connector import db
from app.utils.functions.invoice_generator import generate_invoice_number

class OrderService:
    
    @staticmethod
    def create_order(user_id):
        cart = Cart.query.filter_by(user_id=user_id).all()
        
        if cart is None:
            return None

        order = Order(user_id=user_id, invoice_number=generate_invoice_number(user_id))

        total_price = 0
        total_eco_point = 0
        for item in cart:
            total_price += item.product.price * item.product.discount / 100 * item.quantity if item.product.discount else item.product.price * item.quantity
            total_eco_point += item.product.eco_point
            order_item = OrderItem(product_id=item.product_id, order_id=order.id, quantity=item.quantity)
            db.session.add(order_item)
            
        order.total_price = total_price
        order.total_eco_point = total_eco_point
        
        db.session.add(order)
        db.session.commit()
        
        return order.to_dict()