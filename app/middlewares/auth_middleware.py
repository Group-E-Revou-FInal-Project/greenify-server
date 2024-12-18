from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import app, jsonify, request
import json
from app.models.users import User
from app.services.user_services import UserService
from app.utils.functions.role_checker import role_check_seller, role_check_validation
from app.utils.validators.user_validate import user_validation
from app.configs.connector import db
def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = json.loads(get_jwt_identity())['user_id']
        user = user_validation(user_id)
        if isinstance(user, dict) and 'error' in user:
            return jsonify({'error': {'code': 401, 'message': user['error']}}), 401
        
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = json.loads(get_jwt_identity())['user_id']
        role_check_validation(user_id=user_id,roles='admin')
        return fn(*args, **kwargs)
    return wrapper


def seller_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = json.loads(get_jwt_identity())['user_id']
        role_check_seller(user_id=user_id,roles='seller')
        return fn(*args, **kwargs)
    return wrapper

def two_fa_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = json.loads(get_jwt_identity())['user_id']
        user = UserService.get_user_by_id(user_id)
        # Check if the user has verified 2FA
        if not user.two_factor_verified:
            return jsonify({'error': {'code': 403, 'message': '2FA verification required'}}), 403
        return fn(*args, **kwargs)
    return wrapper

from flask import request

def reset_is_seller():
    if request.method == 'OPTIONS':
        return None
    print('MASUK RESET SELLER')

    # Skip OPTIONS requests
    if request.method == 'OPTIONS':
        return

    try:
        # Try verifying the JWT
        verify_jwt_in_request(optional=True)  # Optional, no error if token is missing
        identity = get_jwt_identity()
    except Exception as e:
        print(f"No valid JWT provided: {e}")
        return  # No valid token, skip further processing

    if not identity:
        return  # No identity, do nothing

    user_id = json.loads(identity).get('user_id')
    if not user_id:
        return

    user = UserService.get_user_by_id(user_id)
    if not user:
        return

    print(user.email)
    print(request.path)

    # Define seller-specific routes
    seller_routes = [
        "/api/v1/sellers/dashboard",
        "/api/v1/sellers/products",
        "/api/v1/sellers/reviews",
        "/api/v1/sellers/get-seller-reviews",
    ]

    # Reset `is_seller` if the user is outside seller routes
    if request.path not in seller_routes and user.is_seller:
        print('MASUK RESET SELLER2')
        user.is_seller = False
        db.session.commit()

