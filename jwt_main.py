from datetime import timedelta
from typing import List

# Modules
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Models
from FastAPI.Model.Item import Item
from FastAPI.Model.Token import Token

# Operations
from FastAPI.Model.User import User, User_in_DB
from FastAPI.Usecases.Item_operations import op_get_all_data
from FastAPI.Usecases.user_operations import user_op_validate_user, user_op_create_new_user

# Security
from Security import security_op_security_check, create_jwt_access_token, ACCESS_TOKEN_EXPIRE_MIN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


# authenticate token
def user_op_authenticate_user(token: str = Depends(oauth2_scheme)):
    user = security_op_security_check(token)

    return user


@app.post("/token", tags=["login"],
          response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_op_validate_user(form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)

    access_token = create_jwt_access_token(
        data={"sub": user.username},
        expire_time=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@app.get("/items/{item_name}",
         tags=["items"],
         description="Get an item based on item name",
         response_model=List[Item])
async def get_all_items(item_name: str = Depends(user_op_authenticate_user)):
    item_list: List[Item] = []
    for key, val in op_get_all_data().items():
        item_list.append(val)

    return item_list


@app.post("/users/create/",
          tags=["users"],
          description="Create a new User",
          response_model=User,
          dependencies=[Depends(user_op_authenticate_user)])
async def create_user_data(user_data: User_in_DB):
    user: User = user_op_create_new_user(user_data)
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
