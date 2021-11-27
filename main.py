"""
    Main class is used to handle requests from endpoints(swagger/curl)
"""
import uvicorn
from fastapi import FastAPI, Header, HTTPException

import logger
from FastAPI.Model.Item import Item
from FastAPI.Usecases.Item_operations import op_create_item_code, op_update_item_code, op_delete_item_code, \
    op_get_all_data, \
    op_fetch_item_code

app = FastAPI()

item_data = {}
SECURITY_TOKEN = "asfafqqdvhq2312@21!"

# Initiating loggers
logger = logger.logrs


# Fetches out all the data present in DB
@app.get("/")
async def list_all_data(x_token: str = Header(...)):
    logger.info("Working on list_all_data")
    validate_security_token(x_token)
    return op_get_all_data()


# Fetches a particular Item data from DB
@app.get("/items/{name}", response_model=Item)
async def fetch_data(name: str, x_token: str = Header(...)):
    logger.info("Working on fetch_data : {}".format(name))
    validate_security_token(x_token)
    return op_fetch_item_code(name)


# Creates a new Item in DB
@app.post("/items/create", response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
    logger.info("Working on create_item {}".format(item.name))
    validate_security_token(x_token)
    return op_create_item_code(item)


# Updates/Create Iteam in DB
@app.post("/items/update")
async def update(item: Item, x_token: str = Header(...)):
    logger.info("Working on update Item {}".format(item.name))
    validate_security_token(x_token)
    return op_update_item_code(item)


# Deletes a particular Item data if exists
@app.delete("/items/delete/{name}")
async def delete_item(name: str, x_token: str = Header(...)):
    logger.info("Working on delete_item {}".format(name))
    validate_security_token(x_token)
    if op_delete_item_code(name):
        result = "Item: {} is deleted.".format(name)
    else:
        result = "Item: {} does not exist.".format(name)
    return result


def validate_security_token(token: str):
    logger.debug("Validating security token")
    if token != SECURITY_TOKEN:
        logger.warning("Security token is in-valid")
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    logger.debug("Security token is valid")
    return None


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
