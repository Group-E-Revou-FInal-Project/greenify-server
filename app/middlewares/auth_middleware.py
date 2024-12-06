from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
import json
from app.services.user_services import UserService
from app.utils.functions.role_checker import role_check_validation
from app.utils.validators.user_validate import user_validation

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = json.loads(get_jwt_identity())['user_id']
        user = user_validation(user_id)
        if user['error'] is not None:
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
        role_check_validation(user_id=user_id,roles='seller')
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
