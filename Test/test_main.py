import pytest
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient

import logger
from Security import create_jwt_access_token
from main import app

# Initiating loggers
logger = logger.logrs

client = TestClient(app)

TEST_ITEM = {
    "name": "test",
    "description": "just testing",
    "price": 23.0,
    "tax": 2.0
}

USER_NAME_VALID = "aaa"
PSWD_NAME_VALID = "11"

SKIP_ON_DEBUG = "skipping for debugging"
access_token = "asda"


def test_login_auth():
    logger.info("Working on test_login_auth")

    data = {"username": USER_NAME_VALID, "password": PSWD_NAME_VALID}
    response = client.post('/token',
                           data=data)

    global access_token
    access_token = response.json()['access_token']
    logger.info("Access token : {}".format(access_token))
    assert response.status_code == 200
    assert response.json()['token_type'] == "Bearer"


def test_get_all_users():
    logger.info("Working on test_get_all_users")
    response = client.get("/items/",
                          headers={'Authorization': 'Bearer ' + access_token},
                          )

    assert response.status_code == 200
