from datetime import timedelta, datetime
from typing import Optional

import jwt
from fastapi import HTTPException
from starlette import status

from FastAPI.Model.Token import TokenData
from FastAPI.Model.User import User
from FastAPI.Usecases.user_operations import user_op_get_user_data
from main import logger

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30


# Create new JWT Token
def create_jwt_access_token(data: dict, expire_time: Optional[timedelta] = None):
    to_encode = data.copy()

    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def security_op_security_check(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials using token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")

        if user_name is None:
            raise credentials_exception

        token_data = TokenData(user_name=user_name)
    except Exception:
        raise credentials_exception

    user: User = user_op_get_user_data(token_data.user_name)
    if not user:
        raise  HTTPException(status_code=400, detail="Wrong user.")
    user_data = User(**user)

    logger.debug("User here is : {}".format(user))
    if not user:
        raise credentials_exception

    if user_data.disabled:
        raise HTTPException(status_code=400, detail="User is disabled.")

    return user
