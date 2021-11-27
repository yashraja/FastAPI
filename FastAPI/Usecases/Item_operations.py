"""
    All the business logic is written over here.
"""
import sys

import logger as logger

# Used to import files from parent dir.. path
sys.path.append('..')

from FastAPI.Usecases.database import db_get_data, db_write_data
from FastAPI.Model.Item import Item

item_db = {}
logger = logger.logrs


def op_get_all_data():
    logger.info("Working on get_all_data")
    return db_get_data()


def op_fetch_item_code(name: str) -> Item:
    logger.info("Working on fetch_item_code")
    total_db_data = db_get_data()

    return total_db_data.get(name, {})


def op_create_item_code(item: Item) -> Item:
    logger.info("Working on create_item_code")
    total_db_data = db_get_data()

    new_item = {item.name: item.dict()}
    total_db_data.update(new_item)

    db_write_data(total_db_data)

    return item


def op_update_item_code(item: Item) -> bool:
    logger.info("Working on update_item_code")
    total_db_data = db_get_data()

    total_db_data.update({item.name: item.dict()})

    db_write_data(total_db_data)

    return True


def op_delete_item_code(name: str) -> bool:
    logger.info("Working on delete_item_code")
    total_db_data = db_get_data()
    is_deleted = False
    if total_db_data.get(name, None):
        logger.debug("Item exists")
        total_db_data.pop(name)
        is_deleted = True
    else:
        logger.debug("Item does not exist")
    db_write_data(total_db_data)
    return is_deleted
