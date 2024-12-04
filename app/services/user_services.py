from app.models.users import User, Role  # Import Role model
from sqlalchemy.exc import IntegrityError
from app.configs.connector import db

class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()