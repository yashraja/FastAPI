"""
    All the logging specifications are handled in this file
"""

import logging

LOF_FILE_NAME = "item_log.log"

LOG_FORMATTER = "%(asctime)s  [%(filename)s:%(lineno)s - %(funcName)10s() ] %(levelname)s - %(message)s"

logging.basicConfig(
    filename='app.log',
    filemode='w',
    format=LOG_FORMATTER,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Prints logs to console- helps in debugging purposes.
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(LOG_FORMATTER))
logging.getLogger().addHandler(consoleHandler)

logrs = logging.getLogger(__name__)
