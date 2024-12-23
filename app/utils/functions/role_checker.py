from flask import jsonify
from app.constants.response_status import Response
from app.services.user_services import UserService


def role_check_validation(user_id,roles):
    user = UserService.get_user_by_id(user_id)
    if not any(role.rolename == roles for role in user.roles):
        return Response.error(f"Role access required : {(roles)}", 400)