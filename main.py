"""
    Main class is used to handle requests from endpoints(swagger/curl)
"""

import uvicorn
from fastapi import Header, HTTPException, FastAPI, Query, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

import logger
from FastAPI.Model.Exceptions import TokenException
from FastAPI.Model.Item import Item
from FastAPI.Usecases.Item_operations import op_create_item_code, op_update_item_code, op_delete_item_code, \
    op_get_all_data, \
    op_fetch_item_code


# app = FastAPI()


# Second way of verifying- using Depends
# Used for fetch_data_2 for learning purpose
# This function should be defined before you use it in the code
#       *This is not working if I keep this def after usage
async def verify_token_dependency(x_token: str = Header(...)):
    logger.debug("Validating security token")
    if x_token != SECURITY_TOKEN:
        logger.warning("Security token is in-valid")
        raise TokenException(name="Invalid token")
    logger.debug("Security token is valid")
    return None


# Adding authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Global dependencies
app = FastAPI(dependencies=[Depends(verify_token_dependency)])

item_data = {}
SECURITY_TOKEN = "asfafqqdvhq2312@21!"

# Initiating loggers
logger = logger.logrs


# Fetches out all the data present in DB
@app.get("/", tags=['Items'], description="Fetches without JWT auth, but token")
async def list_all_data():
    logger.info("Working on list_all_data")

    return op_get_all_data()


# Fetches out all the data present in DB
@app.get("/deprecate_example", tags=['Items'], deprecated=True,
         summary="Just an example place holder for deprecate functionality")
async def list_all_data(x_token: str = Header(...)):
    logger.info("Working on list_all_data")
    validate_security_token(x_token)
    return op_get_all_data()


# Fetches a particular Item data from DB
# Query(...)  ->  ... means *required
# tags is used to organize categories for api's in swagger
@app.get("/items/{name}",
         response_model=Item,
         tags=['Items', 'List'],
         summary="Fetches a particular data from Item db",
         description="All the description from app.get will show in swagger for user friendly messages")
async def fetch_data(name: str,
                     q: str = Query(...,
                                    min_length=3,
                                    max_length=10,
                                    title="Title str",
                                    description="just a dummy- learning purpose",
                                    alias="alias_name_for_q"),
                     x_token: str = Header(...)):
    logger.info("Working on fetch_data : {}".format(name))
    # just for learning purpose
    print("Q is {}".format(q))
    validate_security_token(x_token)
    return op_fetch_item_code(name)


# Creates a new Item in DB
@app.post("/items/create", response_model=Item, tags=['Items', 'List'])
async def create_item(item: Item,
                      x_token: str = Header(...),
                      ):
    logger.info("Working on create_item {}".format(item.name))
    validate_security_token(x_token)
    return op_create_item_code(item)


# Updates/Create Iteam in DB
@app.post("/items/update", tags=['Items'])
async def update(item: Item,
                 x_token: str = Header(...)):
    logger.info("Working on update Item {}".format(item.name))
    validate_security_token(x_token)
    return op_update_item_code(item)


# Deletes a particular Item data if exists
@app.delete("/items/delete/{name}", tags=['Items'])
async def delete_item(name: str,
                      x_token: str = Header(...)):
    logger.info("Working on delete_item {}".format(name))
    validate_security_token(x_token)
    if op_delete_item_code(name):
        result = "Item: {} is deleted.".format(name)
    else:
        result = "Item: {} does not exist.".format(name)
    return result


# Fetches a particular Item data from DB
# Query can be used to restrict/validate data from user in FrontEnd
@app.get("/items/id/{id}", tags=['Items'],
         dependencies=[Depends(verify_token_dependency)])
async def fetch_data_2(id: int):
    logger.info("Working on fetch_data : {}".format(id))
    # just for learning purpose

    return id


def validate_security_token(token: str):
    logger.debug("Validating security token")
    if token != SECURITY_TOKEN:
        logger.warning("Security token is in-valid")
        raise TokenException(name="Invalid token")
    logger.debug("Security token is valid")
    return None


@app.exception_handler(TokenException)
async def unicorn_exception_handler(request: Request, exc: TokenException):
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! {exc.name} did something."},
    )


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
