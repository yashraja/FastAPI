"""
    All the database operations are handled here
"""

import json
from pathlib import Path

import logger as logger

ITEM_DB_FILE_NAME = "item_db.json"
logger = logger.logrs


def db_check_file_exists():
    logger.info("Working on check_file_exists")
    my_file = Path(ITEM_DB_FILE_NAME)
    logger.debug("Results on file exists {}".format(my_file.is_file()))
    return my_file.is_file()


def db_write_data(items_data):
    logger.info("Working on write_data")
    # Writing to sample.json
    with open(ITEM_DB_FILE_NAME, "w") as outfile:
        logger.info("\n json obj to write : {}".format(items_data))
        outfile.write(json.dumps(items_data, indent=4))
    logger.info("Data inserted in database file")


def db_get_data():
    logger.info("Working on get_data")
    if not db_check_file_exists():
        logger.warn("DB File does not exist")
        return {}
    with open(ITEM_DB_FILE_NAME, 'r') as openfile:
        logger.info("Reading data from DB")
        # Reading from json file
        try:
            item_db_data = json.load(openfile)
        except Exception as e:
            logger.error("Exception is {}".format(e))
            item_db_data = {}

    logger.debug("File data collected")
    return item_db_data