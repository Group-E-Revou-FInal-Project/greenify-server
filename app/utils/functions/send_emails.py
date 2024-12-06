# app/services/email_service.py

from flask_mail import Message
from app import mail
from app.constants.response_status import Response

def send_email(user_email, header, content, subject):
    footer = """
    <div style="text-align: center; font-size: 12px; color: #999; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px;">
        <p>© 2024 Greenify. All rights reserved.</p>
        <p><a href="#" style="color: #32a852; text-decoration: none;">Unsubscribe</a></p>
    </div>
    """
    html_content = f"""
     <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 0; border-radius: 10px; overflow: hidden;">
        <!-- Header Section -->
        <div style="background-color: #32a852; color: white; text-align: center; padding: 20px 10px;">
            <h1 style="margin: 0; font-size: 24px; font-weight: bold;">{header}</h1>
        </div>
        <div style="padding: 20px;">
            {content}
        </div>
        {footer}
    </div>
    """
    try:
        msg = Message(
            subject= subject,
            recipients=[user_email],
            html=html_content
        )
        mail.send(msg)
        return None
    except Exception as e:
        error_message = {"error": f"Error sending email: {str(e)}"}
        return error_message
    
    
