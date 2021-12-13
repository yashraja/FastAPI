from typing import Optional, List

from pydantic import BaseModel

from FastAPI.Model.Item import Item


class ResponseMessage(BaseModel):

    meta: Optional[str] = None
    response_data: List[Item] = []
    message: str = ""
