"""
    All the business logic is written over here.
"""
import sys

import logger as logger

# Used to import files from parent dir.. path
sys.path.append('..')

from FastAPI.Usecases.database import db_get_data, db_write_data
from FastAPI.Model.Item import Item, Item_inDB

item_db = {}
logger = logger.logrs

ITEM_DB_FILE_NAME = "item"


def op_get_all_data(item_name: str = None):
    logger.info("Working on op_get_all_data ")
    logger.debug("Item name : {}".format(item_name))
    all_data = db_get_data(ITEM_DB_FILE_NAME)
    logger.debug("Here 1")
    if item_name:
        logger.debug("Here")
        return all_data.get(item_name, None)
    else:
        return all_data


def op_fetch_item_code(name: str) -> Item:
    logger.info("Working on fetch_item_code")
    total_db_data = db_get_data(ITEM_DB_FILE_NAME)

    return total_db_data.get(name, {})


def op_create_item_code(item: Item, username: str) -> Item:
    logger.info("Working on create_item_code")
    total_db_data = db_get_data(ITEM_DB_FILE_NAME)
    logger.debug("Item is : {}".format(item))

    try:
        new_item = Item_inDB(**item.__dict__,
                         user_name=username)
    except Exception as e:
        logger.error("Exception : {}".format(e))
        raise Exception(e)

    total_db_data[item.name] = new_item.__dict__

    db_write_data(total_db_data)

    return item


def op_update_item_code(item: Item, username: str) -> bool:
    logger.info("Working on update_item_code")
    logger.debug("User name from def : {}".format(username))
    total_db_data = db_get_data(ITEM_DB_FILE_NAME)

    new_item = Item_inDB(**item.__dict__,
                         user_name=username)
    logger.debug("Here {}".format(new_item.__dict__))

    total_db_data[item.name] = new_item.__dict__

    db_write_data(total_db_data)

    return True


def op_delete_item_code(name: str) -> bool:
    logger.info("Working on delete_item_code")
    total_db_data = db_get_data(ITEM_DB_FILE_NAME)
    is_deleted = False
    if total_db_data.get(name, None):
        logger.debug("Item exists")
        total_db_data.pop(name)
        is_deleted = True
    else:
        logger.debug("Item does not exist")
    db_write_data(total_db_data)
    return is_deleted
