from pydantic import BaseModel, EmailStr

class OTPCode(BaseModel):
    ootp_code: str