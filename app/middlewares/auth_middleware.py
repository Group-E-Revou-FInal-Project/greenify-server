from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.services.user_services import UserService

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()['user_id']
        user = UserService.get_user_by_id(user_id)
        if not any(role.name == 'Admin' for role in user.roles):
            return jsonify({'error': {'code': 403, 'message': 'Admin access required'}}), 403
        return fn(*args, **kwargs)
    return wrapper

def two_fa_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()['user_id']
        user = UserService.get_user_by_id(user_id)
        # Check if the user has verified 2FA
        if not user.two_factor_verified:
            return jsonify({'error': {'code': 403, 'message': '2FA verification required'}}), 403
        return fn(*args, **kwargs)
    return wrapper
