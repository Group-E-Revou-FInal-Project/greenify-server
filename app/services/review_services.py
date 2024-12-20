from app.configs.connector import db
from app.models.products import Product
from app.models.reviews import Review
from app.models.transactions_history import TransactionHistory
from app.models.users import User

class ReviewService:
    
    @staticmethod
    def add_review(data):
        try:
            transactions = TransactionHistory.query.filter_by(invoice_number=data['invoice_number'], status='COMPLETED').first()
            
            if transactions is None:
                return { 'error': 'Transaction not found' }
            
            new_review = Review(product_id=data['product_id'], 
                                user_id=data['user_id'], 
                                rating=data['rating'], 
                                review=data['review'],
                                transactions_id=transactions.id)
            
            db.session.add(new_review)
            db.session.commit()
            
            return new_review.to_dict()
        except ValueError as e:
            db.session.rollback()
            return {'error': f'{e}'}
        
    @staticmethod
    def get_good_reviews():
        reviews = (
            db.session.query(Review, User)
            .join(User, Review.user_id == User.id)
            .filter(Review.rating >= 4, Review.is_deleted == False)
            .all()
        )
        
        if not reviews:
            return []
        
        return {
            'reviews': [
                {
                    'id': review.id,
                    'product_id': review.product_id,
                    'user_id': review.user_id,
                    'transactions_id': review.transactions_id,
                    'rating': review.rating,
                    'review': review.review,
                    'created_at': review.created_at,
                    'updated_at': review.updated_at,
                    'is_deleted': review.is_deleted,
                    'profile_picture': user.profile_picture,
                    'name': user.name
                } for review, user in reviews
            ]
        }
        
    @staticmethod
    def get_reviews(user_id):
        try:
            reviews = Review.query.filter_by(user_id=user_id, is_deleted=False).all()
        except Exception as e:
            return {'error': f'{e}'}
         
        if reviews is None:
            return []
        
        return [review.to_dict() for review in reviews]
    
    @staticmethod
    @staticmethod
    def delete_review(data):
        try:
            reviews = Review.query.filter_by(id=data['id'], user_id=data['user_id'], product_id=data['product_id']).all()
            if not reviews:
                return None
            
            for review in reviews:
                review.soft_delete()

            db.session.add_all(reviews)
            db.session.commit()

            return [review.to_dict() for review in reviews]
        except Exception as e:
            db.session.rollback()
            return None

    
    def get_reviews_by_seller(seller_id):
        try:
            reviews = (
                db.session.query(Review)
                .join(Product, Review.product_id == Product.id)  
                .filter(Product.seller_id == seller_id)  
            )
            
        except Exception as e:
            return {'error': f'{e}'}
        
        if reviews is None:
            return []
        
        return [review.to_dict() for review in reviews]
        