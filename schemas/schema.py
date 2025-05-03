from typing import Optional
from pydantic import BaseModel

class Book(BaseModel):
    id: Optional[int] = 0
    name: str
    isbn: str
    editorial: str
    autor: str
    disponible: Optional[bool] = True

class User(BaseModel):
    id: Optional[int] = 0
    username: str
    password: str