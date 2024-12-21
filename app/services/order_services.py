from app.models import transactions_history
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
        try:
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
        except Exception as e:
            db.session.rollback()
            return { 'error': f'Oops, something went wrong: {e}' }
    
    @staticmethod
    def payment_order(data):
        try:
            order_id = data['order_id']
            user_id = data['user_id']
            order = Order.query.filter_by(id=order_id, user_id=user_id).first()
            
            if order is None:
                return None
            
            order.status = OrderStatus.COMPLETED
            order.invoice_number = generate_invoice_number(user_id, is_temp=False)
            
            # Add to transaction history
            transactions_history = []
            orders_items = OrderItem.query.filter_by(order_id=order.id).all()
            for item in orders_items:
                item.product.stock -= item.quantity
                if item.product.stock == item.product.min_stock:
                    item.product.is_out_of_stock = True
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
        except Exception as e:
            db.session.rollback()
            return { 'error': f'Oops, something went wrong: {e}' }
    
    @staticmethod
    def get_order(user_id):
        orders = Order.query.filter_by(user_id=user_id).all()
       
        if orders is None:
            return None
        
        return { 'orders': [order.to_dict() for order in orders]}
    
    @staticmethod
    def get_order_by_id(order_id, user_id):
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if order is None:
            return { 'error': 'Order not found' }
        
        return order.to_dict()
    
    @staticmethod
    def get_order_items(order_id, user_id):
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if order is None:
            return { 'error': 'Order not found' }
        
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        
        if order_items is None:
            return { 'error': 'Order items not found' }
        
        return [order_item.to_dict() for order_item in order_items]
        
    @staticmethod
    def get_order_by_status(user_id, status):
        orders = Order.query.filter_by(user_id=user_id, status=status).all()
       
        if orders is None:
            return None
        
        return [order.to_dict() for order in orders]
    @staticmethod
    def get_user_transaction_history(user_id):
        transactions = TransactionHistory.query.filter_by(user_id=user_id).all()
        
        if transactions is None:
            return None
        
        return [transaction.to_dict() for transaction in transactions]
    @staticmethod
    def get_seller_transaction_history(seller_id):
        transactions = TransactionHistory.query.filter_by(seller_id=seller_id).all()
        
        if transactions is None:
            return None
        
        return [transaction.to_dict() for transaction in transactions]
    
    @staticmethod 
    def cancel_order(invoice_number, user_id):
        try:
            order = Order.query.filter_by(invoice_number=invoice_number, user_id=user_id).first()
            
            if order is None:
                return None
            
            transactions_history = []
            OrderItem = OrderItem.query.filter_by(order_id=order.id).all()
            for item in OrderItem:
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
                    status=OrderStatus.CANCELLED.name
                )
            )
            db.session.add_all(transactions_history)
            order.status = OrderStatus.CANCELED
            db.session.add(order)
            db.session.commit()
            return order.to_dict()
        except Exception as e:
            db.session.rollback()
            return None
        
        
    