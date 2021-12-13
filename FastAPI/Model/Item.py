"""
    This is the model for database

"""
from typing import Optional
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = "tmp"
    description: Optional[str] = Field(None,
                                       description="Some desc",
                                       max_length=20,
                                       min_length=0)
    price: float = Field(10,
                         description="Price of item",
                         gt=0)
    tax: Optional[float] = 1


class Item_inDB(Item):
    user_name: str
