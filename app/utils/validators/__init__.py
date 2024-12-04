from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.users import Gender

class OTPCode(BaseModel):
    email: EmailStr
    otp_code: str
    
class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    dateofbirth: datetime
    gender: Gender
    role: str
    password: str
    
class Role(BaseModel):
    rolename: str