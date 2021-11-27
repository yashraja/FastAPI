import logging

LOF_FILE_NAME = "item_log.log"

logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='%(asctime)s  [%(filename)s:%(lineno)s - %(funcName)10s() ] %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
)

logrs = logging.getLogger(__name__)
