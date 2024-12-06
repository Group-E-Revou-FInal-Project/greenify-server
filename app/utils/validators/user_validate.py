# app/services/email_service.py
from app.services.user_services import UserService

def user_validation(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        if user is None:
            return {"error": "User is not found"}
        if user.is_active == False:
            return {"error": "User is not active"}
        return user
    except Exception as e:
        error_message = {"error": f"Error sending email: {str(e)}"}
        return error_message
    
    
