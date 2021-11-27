import sys

import logger as logger

sys.path.append('..')

from FastAPI.Usecases.database import get_data, write_data
from FastAPI.Mock.Item import Item

item_db = {}
logger = logger.logrs


def get_all_data():
    logger.info("Working on get_all_data")
    return get_data()


def fetch_item_code(name: str):
    logger.info("Working on fetch_item_code")
    total_db_data = get_data()

    return total_db_data.get(name, None)


def create_item_code(item: Item):
    logger.info("Working on create_item_code")
    total_db_data = get_data()

    new_item = {item.name: item.dict()}
    total_db_data.update(new_item)

    write_data(total_db_data)

    return item


def update_item_code(item: Item):
    logger.info("Working on update_item_code")
    total_db_data = get_data()

    total_db_data.update({item.name: item.dict()})

    write_data(total_db_data)

    return True


def delete_item_code(name: str):
    logger.info("Working on delete_item_code")
    total_db_data = get_data()
    is_deleted = False
    if total_db_data.get(name, None):
        logger.debug("Item exists")
        total_db_data.pop(name)
        is_deleted = True
    else:
        logger.debug("Item does not exist")
    write_data(total_db_data)
    return is_deleted
