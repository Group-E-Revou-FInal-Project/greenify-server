from flask import Blueprint
from app.controllers.user_controller import UserController
from app.controllers.auth_controller import AuthController
from app.controllers.profile_controller import ProfileController
from app.controllers.product_controller import ProductController
from app.controllers.cart_controller import CartController
from app.controllers.seller_controller import SellerController
from app.controllers.UserInterestController import UserInterestController
from app.controllers.wishlist_controller import WishlistController
from app.middlewares.auth_middleware import admin_required,seller_required, token_required, two_fa_required 


user_bp = Blueprint('users', __name__)
profile_bp = Blueprint('profile', __name__)
auth_bp = Blueprint('auth', __name__) 
product_bp = Blueprint('product', __name__)
seller_bp = Blueprint('seller', __name__)
cart_bp = Blueprint('cart', __name__)
wishlist_bp = Blueprint('wishlist', __name__)

# User Routes
user_bp.add_url_rule('/email-validation', view_func=UserController.email_validaton, methods=['POST'])
user_bp.add_url_rule('/otp-validation', view_func=UserController.otp_validation, methods=['POST'])
user_bp.add_url_rule('/register', view_func=UserController.register_user, methods=['POST'])
user_bp.add_url_rule('/users', view_func=UserController.get_all_users, methods=['POST'])
user_bp.add_url_rule('/otp-refresh', view_func=UserController.otp_refresh, methods=['POST'])
user_bp.add_url_rule('/add-role', view_func=UserController.add_role, methods=['POST'])
user_bp.add_url_rule('/change-password', view_func=AuthController.change_password, methods=['POST'])

# Profile Routes
profile_bp.add_url_rule('/me', view_func=ProfileController.get_profile_data, methods=['GET'])
profile_bp.add_url_rule('/me', view_func=ProfileController.update_profile, methods=['PUT'])
profile_bp.add_url_rule('/interests', view_func=token_required(UserInterestController.add_interest), methods=['POST'])
profile_bp.add_url_rule('/interests', view_func=token_required(UserInterestController.get_interests), methods=['GET'])
profile_bp.add_url_rule('/interests', view_func=token_required(UserInterestController.update_interests), methods=['PUT'])
profile_bp.add_url_rule('/interests', view_func=token_required(UserInterestController.remove_interest), methods=['DELETE'])

# Product Routes
product_bp.add_url_rule('/category', view_func=ProductController.add_category, methods=['POST'])
product_bp.add_url_rule('/add-product', view_func=token_required(seller_required(ProductController.add_product)), methods=['POST'])
product_bp.add_url_rule('/<int:product_id>', view_func=ProductController.get_product_by_id, methods=['GET'])
product_bp.add_url_rule('/<int:product_id>', view_func=token_required(seller_required(ProductController.update_product)), methods=['PUT'])
product_bp.add_url_rule('/<int:product_id>', view_func=token_required(seller_required(ProductController.delete_product)), methods=['DELETE'])
product_bp.add_url_rule('/<int:product_id>', view_func=token_required(seller_required(ProductController.restore_product)), methods=['PATCH'])
product_bp.add_url_rule('/recommendation', view_func=token_required(ProductController.recommendation_product), methods=['GET'])

# Seller Routes
seller_bp.add_url_rule('/create-seller', view_func=token_required(SellerController.create_seller), methods=['POST'])

# Authentication Routes
auth_bp.add_url_rule('/login', view_func=AuthController.login, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=token_required(AuthController.logout), methods=['POST'])  # Requires token
auth_bp.add_url_rule('/enable-2fa', view_func=token_required(AuthController.enable_2fa), methods=['POST'])
auth_bp.add_url_rule('/verify-2fa', view_func=token_required(AuthController.verify_2fa), methods=['POST'])
auth_bp.add_url_rule('/refresh', view_func=AuthController.refresh_token, methods=['POST'])  # Refresh JWT token
auth_bp.add_url_rule('/forgot-password', view_func=AuthController.forgot_password, methods=['POST'])
auth_bp.add_url_rule('/forgot-change-password', view_func=AuthController.forgot_change_password, methods=['POST'])

# Cart Routes
cart_bp.add_url_rule('/', view_func=token_required(CartController.get_carts), methods=['GET'])
cart_bp.add_url_rule('/add-to-cart', view_func=token_required(CartController.add_to_cart), methods=['POST'])
cart_bp.add_url_rule('/decrease-cart', view_func=token_required(CartController.decrease_cart), methods=['PUT'])
cart_bp.add_url_rule('/update-quantity', view_func=token_required(CartController.update_cart_quantity), methods=['PUT'])

# wishlist Routes
wishlist_bp.add_url_rule('/add-to-wishlist', view_func=token_required(WishlistController.add_to_wishlist), methods=['POST'])
wishlist_bp.add_url_rule('/get-wishlist', view_func=token_required(WishlistController.get_user_wishlist), methods=['GET'])
wishlist_bp.add_url_rule('/remove-from-wishlist', view_func=token_required(WishlistController.remove_from_wishlist), methods=['DELETE'])    
wishlist_bp.add_url_rule('/clear-wishlist', view_func=token_required(WishlistController.clear_wishlist), methods=['DELETE'])




