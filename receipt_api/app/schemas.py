from typing import List
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    name: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: float

class PaymentInfo(BaseModel):
    type: str
    amount: float

class ReceiptCreate(BaseModel):
    products: List[ProductCreate]
    payment: PaymentInfo

class ReceiptItemOut(BaseModel):
    name: str
    price: float
    quantity: float
    total: float

class ReceiptOut(BaseModel):
    id: int
    products: List[ReceiptItemOut]
    payment: PaymentInfo
    total: float
    rest: float
    created_at: str
