from flask import Blueprint
from app.controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)


# User Routes
user_bp.add_url_rule('/', view_func=UserController.get_all_users, methods=['POST'])

