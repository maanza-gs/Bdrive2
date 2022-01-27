from typing import Optional,List

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from datetime import datetime

class Item(BaseModel):
    name: str
    item_type:str
    timeing: datetime


class UserBase(BaseModel):
    email: EmailStr

class User(UserBase):
    username: str
    email: EmailStr
    #items: List[Item] = []

    class Config:
        orm_mode = True

class UserCreate(User):
    password: str


