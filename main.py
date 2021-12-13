from datetime import timedelta
from typing import List, Optional

import logger as logger
import uvicorn

# Modules
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Models
from FastAPI.Model.ResponseMessage import ResponseMessage
from FastAPI.Model.Item import Item
from FastAPI.Model.Token import Token

# Operations
from FastAPI.Model.User import User, User_Create
from FastAPI.Usecases.Item_operations import op_get_all_data, op_create_item_code, op_update_item_code, \
    op_delete_item_code
from FastAPI.Usecases.user_operations import user_op_validate_user, user_op_create_new_user

# Security
from Security import security_op_security_check, create_jwt_access_token, ACCESS_TOKEN_EXPIRE_MIN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

# Initiating loggers
logger = logger.logrs

ITEM_TAG = "item"
USER_TAG = "user"
LOGIN_TAG = "login"

current_user_name: str = ""


# authenticate token
def authenticate_user(token: str = Depends(oauth2_scheme)):
    logger.info("Working on authenticate_user")
    user = security_op_security_check(token)
    logger.info("User is : {}".format(user))
    logger.debug("User type : {}".format(type(user)))
    global current_user_name
    current_user_name = user.username
    return user


@app.post("/token", tags=[LOGIN_TAG],
          response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info("Working on authenticate_user")
    user = user_op_validate_user(form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)

    access_token = create_jwt_access_token(
        data={"sub": user.username},
        expire_time=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@app.post("/users/create/",
          tags=[USER_TAG],
          description="Create a new User",
          response_model=User,
          dependencies=[Depends(authenticate_user)])
async def create_user_data(user_data: User_Create):
    logger.info("Working on create_user_data")
    user: User = user_op_create_new_user(user_data)
    return user


@app.get("/items/",
         tags=[ITEM_TAG],
         description="Get an item based on item name",
         response_model=ResponseMessage)
async def get_all_items(item_name: Optional[str] = None, dummy: str = Depends(authenticate_user)):
    logger.info("Working on get_all_items")
    item_list: List[Item] = []
    all_item_data = op_get_all_data(item_name)
    logger.debug("Print all data: {}".format(all_item_data))

    return_data: ResponseMessage = ResponseMessage()

    # Return None when there is no data available for this req
    if not all_item_data:
        return_data.meta = ""
        return_data.response_data = []
        return_data.message = "No data for this item"
        return return_data.__dict__
    if item_name:
        return_data.meta = ""
        return_data.response_data = [all_item_data]
        return_data.message = "Successfully retrieved data for this items"
        return return_data.__dict__

    for key, val in all_item_data.items():
        logger.debug("Here")
        item_list.append(val)

    return_data.meta = ""
    return_data.response_data = item_list
    return_data.message = "Successfully retrieved data for all items"

    return return_data.__dict__


@app.post("/items/create/",
          tags=[ITEM_TAG],
          description="Create new Item",
          dependencies=[Depends(authenticate_user)],
          response_model=Item
          )
async def create_items(item_data: Item):
    logger.info("Working on create_items")
    return op_create_item_code(item_data, current_user_name)


@app.post("/items/update/",
          tags=[ITEM_TAG],
          description="Update an Item",
          dependencies=[Depends(authenticate_user)]
          )
async def update_item(item_data: Item):
    logger.info("Working on update_item")
    return op_update_item_code(item_data, current_user_name)


@app.delete("/items/delete/",
            tags=[ITEM_TAG],
            dependencies=[Depends(authenticate_user)])
async def delete_item(item_name: str):
    logger.info("Working on delete_item")
    return op_delete_item_code(item_name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
