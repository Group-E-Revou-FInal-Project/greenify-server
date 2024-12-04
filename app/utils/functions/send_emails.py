# app/services/email_service.py

from flask_mail import Message
from app import mail
from app.constants.response_status import Response

def send_email(subject, recipients, body):
    """
    Sends an email using Flask-Mail.

    Args:
        subject (str): The email subject.
        recipients (list): A list of recipient email addresses.
        body (str): The email body.

    Returns:
        Response: A Response object with a success or error message.
    """

    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body
        )
        mail.send(msg)
        return None
    except Exception as e:
        error_message = {"error": f"Error sending email: {str(e)}"}
        return error_message
    
    
