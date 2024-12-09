from app.configs.connector import db
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
            return {'error': f'message'}
        
    @staticmethod
    def get_reviews(user_id):
        reviews = Review.query.filter_by(user_id=user_id, is_deleted=False).all()
        
        if reviews is None:
            return []
        
        return [review.to_dict() for review in reviews]
    
    @staticmethod
    def delete_review(data):
        reviews = Review.query.filter_by(user_id=data['user_id'], product_id=data['product_id']).all()
        
        if review is None:
            return None
        
        for review in reviews:
            review.soft_delete()
            
        db.session.add_all(reviews)
        db.session.commit()
        
        return [review.to_dict() for review in reviews]
        