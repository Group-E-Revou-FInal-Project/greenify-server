from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, condecimal
from app.models.users import Gender
import re

class OTPCode(BaseModel):
    email: EmailStr
    otp_code: str
    
class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    dateofbirth: datetime
    gender: Gender
    interests: Optional[list[str]] = None
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
    
class UpdateSeller(BaseModel):
    user_id: int
    store_name: Optional[str] = None
    store_description: Optional[str] = None
    store_logo: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    
class AddCategory(BaseModel):
    category_name: str
    
class Product(BaseModel):
    product_name: str
    price: Decimal
    discount: Optional[Decimal] = None
    product_desc: str
    stock: int
    min_stock: int
    category_id: int
    eco_point: int
    recycle_material_percentage: int
    image_url: str
    
class UpdateProduct(BaseModel):
    product_name: Optional[str] = None
    price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    product_desc: Optional[str] = None
    stock: Optional[int] = None
    min_stock: Optional[int] = None
    category_id: Optional[int] = None
    eco_point: Optional[int] = None
    recycle_material_percentage: Optional[int] = None
    image_url: Optional[str] = None

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
    
class AddVoucher(BaseModel):
    seller_id: int
    product_id: int
    kode_voucher: str = Field(..., max_length=50)
    expired: datetime
    voucher_desc: Optional[str] = None
    nama_voucher: str = Field(..., max_length=100)
    discount_percentage: float = Field(..., ge=0, le=100) 
    is_active: Optional[bool] = True
    
class UpdateVoucher(BaseModel):
    product_id: Optional[int]
    kode_voucher: Optional[str] = Field(None, max_length=50)
    expired: Optional[datetime]
    voucher_desc: Optional[str]
    nama_voucher: Optional[str] = Field(None, max_length=100)
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = True
    
class Cart(BaseModel):
    user_id: int
    product_id: int
    quantity: Optional[int] = 1

class Review(BaseModel):
    invoice_number: Optional[str] = None
    product_id: int
    user_id: int
    id : Optional[int] = None
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    review: Optional[str] = Field(None, max_length=2500)
    
class createAddress(BaseModel):
    user_id: int    
    address: str
    city: str
    postal_code: str
    province: str
    name: str
    phone_number: str
    
class updateAddress(BaseModel):
    address: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    province: Optional[str]
    name: Optional[str]
    phone_number: Optional[str]

class OrderPayment(BaseModel):
    invoice_number: str
    user_id: int
    