from app.models.carts import Cart
from app.models.products import Product
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.transactions_history import TransactionHistory
from app.configs.connector import db
from app.utils.functions.invoice_generator import generate_invoice_number
from app.constants.enums import OrderStatus
from app.utils.functions.calculate_total_prices import calculate_total_prices

class OrderService:
    
    @staticmethod
    def create_order(user_id):
        cart = Cart.query.filter_by(user_id=user_id).all()
        
        if cart is None:
            return None

        count_order_completed = Order.query.filter_by(user_id=user_id, status=OrderStatus.COMPLETED).count()
        
        print(count_order_completed)
        
        new_order = Order(user_id=user_id, 
                      invoice_number=generate_invoice_number(user_id, count=count_order_completed + 1, is_temp=True))
        db.session.add(new_order)
        db.session.flush()

        total_price = 0
        total_eco_point = 0
        for item in cart:
            total_price += calculate_total_prices(item.product.price, item.quantity)
            total_eco_point += item.product.eco_point
            order_item = OrderItem(product_id=item.product_id, order_id=new_order.id, quantity=item.quantity)
            db.session.add(order_item)
            db.session.delete(item)
            
        new_order.total_price = total_price
        new_order.total_eco_point = total_eco_point
        
        db.session.commit()
        
        return new_order.to_dict()
    
    @staticmethod
    def payment_order(invoice_number, user_id):
        order = Order.query.filter_by(invoice_number=invoice_number, user_id=user_id).first()
        
        if order is None:
            return None
        
        order.status = OrderStatus.COMPLETED
        order.invoice_number = generate_invoice_number(user_id, is_temp=False)
        
        # Add transaction history
        transactions_history = []
        orders_items = OrderItem.query.filter_by(order_id=order.id).all()
        for item in orders_items:
            transactions_history.append(
                TransactionHistory(
                    invoice_number=order.invoice_number,
                    user_id=user_id,
                    seller_id=item.product.seller_id,
                    price=item.product.price,
                    eco_point=item.product.eco_point,
                    quantity=item.quantity,
                    voucher_id=item.voucher_id,
                    discount=item.product.discount,
                    status=OrderStatus.COMPLETED.name
                )
            )
        
        db.session.add_all(transactions_history)
        db.session.add(order)
        db.session.commit()
        
        return {
            'order': order.to_dict(),
            'transactions': [transaction.to_dict() for transaction in transactions_history]
        }
    
    @staticmethod
    def get_order(user_id):
        orders = Order.query.filter_by(user_id=user_id).all()
       
        if orders is None:
            return None
        
        return {
                'orders': [order.to_dict() for order in orders]
            }
        
    @staticmethod
    def get_order_by_status(user_id, status):
        orders = Order.query.filter_by(user_id=user_id, status=status).all()
       
        if orders is None:
            return None
        
        return [order.to_dict() for order in orders]