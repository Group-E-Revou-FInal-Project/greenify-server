
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.categories import Category
from app.models.users import User

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
