# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime
#
# class UserBase(BaseModel):
#     username: str
#     email: str
#     full_name: Optional[str] = None
#
# class UserCreate(UserBase):
#     password: str
#
# class UserUpdate(BaseModel):
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     password: Optional[str] = None
#
# class UserInDB(UserBase):
#     id: int
#     is_active: bool
#     created_at: datetime
#     updated_at: Optional[datetime] = None
#
#     class Config:
#         from_attributes = True
#
# class UserResponse(UserBase):
#     id: int
#     is_active: bool
#
#     class Config:
#         from_attributes = True


from pydantic import BaseModel
from typing import Optional

class User:
    username: str
    email: str
    full_name: Optional[str]
    id: int
    is_active: bool

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True