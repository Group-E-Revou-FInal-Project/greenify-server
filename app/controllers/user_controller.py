# user_controller.py
from app.services.user_services import UserService
class UserController:
    
    @staticmethod
    def get_all_users():
        return 200