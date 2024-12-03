from flask import Blueprint
from app.controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)
temp_bp = Blueprint('temp', __name__)

# User Routes
temp_bp.add_url_rule('/emailvalidate', view_func=UserController.temp_users, methods=['POST'])
user_bp.add_url_rule('/users', view_func=UserController.get_all_users, methods=['POST'])

