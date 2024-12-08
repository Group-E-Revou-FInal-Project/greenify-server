
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.categories import Category
from app.models.users import User
from app.utils.functions.unique_list import list_unique

class UserInterestService:
    # CREATE
    @staticmethod
    def add_user_interest(data):
        try:
            user = User.query.get(data['user_id'])
            category = Category.query.get(data['category_id'])
            
            if not user or not category:
                return {"error": "User or Category doesn't exist"}
            
            if category not in user.interests:
                user.interests.append(category)
                db.session.commit()
                return user.to_dict()  
            return {"error": "Category already exist"}
        
        except Exception as e:
            db.session.rollback()
            return None

    # READ
    @staticmethod
    def get_user_interests(user_id):
        try:
            user = User.query.get(user_id)
            if user:
                return [interest.to_dict() for interest in user.interests]
            return None
        except Exception as error:
            return {"error": f"Failed to fetch user interest: {str(error)}"}
        
    @staticmethod
    def update_interests(user_id, data):
        user = User.query.filter_by(id=user_id).first()
        
        if user is None:
            return {'error': 'User not found'}
        
        if not list_unique(data['interests']):
            return {'error': 'interest must be unique'}
            
        
        if not isinstance(data.get('interests'), list) or len(data['interests']) != 3:
            return {'error' : 'You must provide exactly 3 interests'}
        
        for i, interest_name in enumerate(data['interests']):
            interest = Category.query.filter_by(category_name=interest_name).first()
            user.interests[i] = interest
        
        db.session.add(user)    
        db.session.commit()
        
        return user.to_dict()

    @staticmethod
    def remove_user_interest(data):
        try:
            user = User.query.get(data['user_id'])
            category = Category.query.get(data['category_id'])
            
            if not user or not category:
                 return {"error": "Failed to delete interest category or user not exist"}
            
            if category in user.interests:
                user.interests.remove(category)
                db.session.commit()
                return user.to_dict() 
            return {"error": "Category not exist in user interest"}
            
        except Exception as error:
            db.session.rollback()
            return {"error": f"Failed to remove interest: {str(error)}"}
