from pydantic import BaseModel, EmailStr

class OTPCode(BaseModel):
    email: EmailStr
    otp_code: str