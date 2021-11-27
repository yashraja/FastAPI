from fastapi import FastAPI

import logger
from FastAPI.Mock.Item import Item
from FastAPI.Usecases.Item_operations import create_item_code, update_item_code, delete_item_code, get_all_data, \
    fetch_item_code

app = FastAPI()

item_data = {}

logger = logger.logrs


@app.get("/")
async def list_all_data():
    logger.info("Working on list_all_data")
    return get_all_data()


@app.get("/items/{item_name}")
async def fetch_data(name: str):
    logger.info("Working on fetch_data : {}".format(name))
    return fetch_item_code(name)


@app.post("/items/create")
async def create_item(item: Item):
    logger.info("Working on create_item {}".format(item.name))
    return create_item_code(item)


@app.post("/items/update")
async def update(item: Item):
    logger.info("Working on update Item {}".format(item.name))
    return update_item_code(item)


@app.delete("/items/")
async def delete_item(name: str):
    logger.info("Working on delete_item {}".format(name))
    if delete_item_code(name):
        result = "Item: {} is deleted.".format(name)
    else:
        result = "Item: {} does not exist.".format(name)
    return result
