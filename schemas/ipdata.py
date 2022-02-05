from typing import Optional
from pydantic import BaseModel

from .utils import PeeweeGetterDict


class IPDataBase(BaseModel):
    ip_address: str


class IPDataCreate(IPDataBase):
    pass


class IPData(IPDataCreate):
    id: Optional[int] = None
    ip_details: Optional[str]
    # user_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
