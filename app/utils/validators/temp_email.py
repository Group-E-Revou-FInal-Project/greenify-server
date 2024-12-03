from pydantic import BaseModel, EmailStr

class TempEmail(BaseModel):
    email: EmailStr