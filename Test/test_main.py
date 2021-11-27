import pytest
from fastapi.testclient import TestClient

import logger
from main import app

# Initiating loggers
logger = logger.logrs

client = TestClient(app)

VALID_SECURITY_TOKEN = "asfafqqdvhq2312@21!"
IN_VALID_SECURITY_TOKEN = "ASDAQQ@21!"

TEST_ITEM = {
        "name": "test",
        "description": "just testing",
        "price": 23.0,
        "tax": 2.0
    }


def test_read_main():
    logger.info("Working on test_read_main")
    response = client.get("/",
                          headers={"X-Token": VALID_SECURITY_TOKEN})
    assert response.status_code == 200


def test_read_main_invalid_token():
    logger.info("Working on test_read_main")
    response = client.get("/",
                          headers={"X-Token": IN_VALID_SECURITY_TOKEN})

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_item():
    logger.info("Working on test_create_item")
    new_item = {
        "name": "test",
        "description": "just testing",
        "price": 23.0,
        "tax": 2.0
    }

    response = client.post("/items/create",
                           headers={"X-Token": VALID_SECURITY_TOKEN},
                           json=new_item)
    assert response.status_code == 200
    assert response.json() == new_item


def test_update_item():
    logger.info("Working on test_update_item")

    response = client.post("/items/update",
                           headers={"X-Token": VALID_SECURITY_TOKEN},
                           json=TEST_ITEM)
    assert response.status_code == 200
    assert response.text == "true"


def test_fetch_existing_item():
    logger.info("Working on fetch_existing_item")
    test_name = TEST_ITEM["name"]

    response = client.get("/items/{}".format(test_name),
                          headers={"X-Token": VALID_SECURITY_TOKEN})
    assert response.status_code == 200
    assert response.json() == TEST_ITEM


# @pytest.mark.skip(reason="To see if the test ITEM exists")
def test_delete_item():
    logger.info("Working on test_delete_item")
    test_name = TEST_ITEM["name"]
    response = client.delete("/items/delete/{}".format(test_name),
                             headers={"X-Token": VALID_SECURITY_TOKEN}, )
    assert response.status_code == 200
    assert response.text == '"Item: ' + test_name + ' is deleted."'
