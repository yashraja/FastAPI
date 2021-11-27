from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    name: str = "tmp"
    description: Optional[str] = None
    price: float = 10
    tax: Optional[float] = 1
