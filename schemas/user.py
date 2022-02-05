from typing import List, Optional
from pydantic import BaseModel, EmailStr

from .utils import PeeweeGetterDict
from .item import Item
from .ipdata import IPData


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    fullname: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    email: EmailStr
    password: str
    fullname: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    items: List[Item] = []
    ipdata: IPData = None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
