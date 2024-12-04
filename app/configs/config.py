from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SUPABASE_DB_URL')
    # MAIL SERVICE CONFIGURATION
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'clarisapp21@gmail.com'
    MAIL_PASSWORD = 'acdp ofua bjco xdrh'  
    MAIL_DEFAULT_SENDER = 'clarisapp21@gmail.com'
    