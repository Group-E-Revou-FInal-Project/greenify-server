from datetime import datetime
from typing import Optional
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
    
class UpdateProfile(BaseModel):
    name: Optional[str] = None
    dateofbirth: Optional[datetime] = None
    gender: Optional[Gender] = None
    phone_number: Optional[str] = None