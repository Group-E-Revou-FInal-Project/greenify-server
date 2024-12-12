from app.configs.connector import db
from app.models.products import Product
from app.models.reviews import Review

class ReviewService:
    
    @staticmethod
    def add_review(data):
        try:
            new_review = Review(product_id=data['product_id'], 
                                user_id=data['user_id'], 
                                rating=data['rating'], 
                                review=data['review'])
            
            db.session.add(new_review)
            db.session.commit()
            
            return new_review.to_dict()
        except ValueError as message:
            db.session.rollback()
            return {'error': f'message'}
        
    @staticmethod
    def get_good_reviews():
        reviews = Review.query.filter(Review.rating >= 4, Review.is_deleted == False).all()
        
        if reviews is None:
            return []
        
        return { 'reviews': [review.to_dict() for review in reviews] }
        
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
            reviews = Review.query.filter_by(id=data['id'], user_id=data['user_id'], product_id=data['product_id']).first()
            if not reviews:
                return None
            
            reviews.soft_delete()

            db.session.add_all(reviews)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return None
        return [review.to_dict() for review in reviews]

    
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
        