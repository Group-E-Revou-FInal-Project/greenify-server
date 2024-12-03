from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.temp_users import TempUser

class UserService:
    @staticmethod
    def temp_users(data):
        temp = TempUser(email=data['email'],
                        otp_code=data['code_otp'])
        temp.set_expiration(1) # 1 minute
        
        try:
            db.session(temp)
            db.session.commit()
        except IntegrityError:
            return None