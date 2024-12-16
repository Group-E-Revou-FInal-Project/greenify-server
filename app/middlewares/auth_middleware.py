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


def reset_is_seller():
    print('MASUK RESET SELLER')
    """Middleware untuk mengatur is_seller menjadi False jika user berada di luar lingkungan seller."""
    verify_jwt_in_request(optional=True)  # Memverifikasi token JWT (opsional)
    identity = get_jwt_identity()
    if not identity:
        return  # Jika tidak ada JWT, abaikan

    user_id = json.loads(identity).get('user_id')
    user = UserService.get_user_by_id(user_id)
    if not user:
        return  # Jika user tidak ditemukan, abaikan
    print(user.email)
    # Daftar rute khusus untuk seller
    # Tambahkan jika perlu
    seller_routes = [
        "/api/v1/sellers/dashboard",
        "/api/v1/sellers/products",
        "/api/v1/sellers/reviews",
        "/api/v1/sellers/get-seller-reviews",
    ]
    print(request.path)
    # Set `is_seller` ke False jika user keluar dari rute seller
    if request.path not in seller_routes and user.is_seller:
        print('MASUK RESET SELLER2')
        user.is_seller = False
        db.session.commit()
