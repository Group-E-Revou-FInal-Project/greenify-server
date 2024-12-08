from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, condecimal
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
    interests: list[str]
    password: str
    
class Role(BaseModel):
    rolename: str
    
class UpdateProfile(BaseModel):
    name: Optional[str] = None
    dateofbirth: Optional[datetime] = None
    gender: Optional[Gender] = None
    phone_number: Optional[str] = None
    
class CreateSeller(BaseModel):
    user_id: int
    store_name: str
    store_description: str
    store_logo: str
    address: str
    phone_number: str
    
class AddCategory(BaseModel):
    category_name: str
    
class AddProduct(BaseModel):
    seller_id: int
    product_name: str
    price: Decimal
    product_desc: str
    stock: int
    min_stock: int
    category_id: int
    eco_point: int
    recycle_material_percentage: int
    image_url: str

class user_interest(BaseModel):
    user_id: int
    category_id: int   
    
class changePassword(BaseModel):
    email: str
    otp_code: str  
    password : str
    
class AddWishlist(BaseModel):
    user_id       : int
    product_id    : int  
    