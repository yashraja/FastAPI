from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str

    full_name: Optional[str] = None
    email: str = None
    disabled: Optional[bool] = None


class User_in_DB(User):
    hashed_password: str
