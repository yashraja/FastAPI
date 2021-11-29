"""
    All the business logic is written over here.
"""
import sys

from fastapi import HTTPException
from passlib.context import CryptContext
import bcrypt
import logger as logger

# Used to import files from parent dir.. path
from FastAPI.Model.User import User, User_in_DB

sys.path.append('..')

from FastAPI.Usecases.database import db_get_data, db_write_data

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_db = {}
logger = logger.logrs

USER_DB_NAME = "user"


def user_op_validate_user(username: str, password: str):
    logger.info("Working on user_op_authenticate_user")
    user_dict = user_op_get_user_data(username)

    # Verify if user exists
    if not user_dict:
        raise HTTPException(status_code=400, detail="Invalid Username")

    user = User_in_DB(**user_dict)

    # Verify user status
    if user.disabled:
        raise HTTPException(status_code=400, detail="User is disabled")

    # Verify password
    if validate_password(password, user.hashed_password):
        logger.debug("Validating password")
        # raise HTTPException(status_code=400, detail="Incorrect password")
        pass  # Passing for now!

    logger.debug("User validation passed!")
    return User(**user_dict)


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return pwd_context.hash(plain_text_password)


def validate_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return pwd_context.verify(plain_text_password, hashed_password)


def user_op_get_all_data():
    logger.info("Working on user_op_get_all_data")
    return db_get_data(USER_DB_NAME)


def user_op_get_user_data(user_name: str) -> User:
    logger.info("Working on user_op_get_user_data")
    all_user_data = db_get_data(USER_DB_NAME)
    if all_user_data.get(user_name):
        logger.debug("User data is : {}".format(all_user_data[user_name]))
        return all_user_data[user_name]
    else:
        logger.debug("There is not user with the given username")
        return None


def user_op_create_new_user(user_data: User_in_DB) -> User:
    # Check if User exists
    if user_op_get_user_data(user_data.username):
        raise HTTPException(status_code=400, detail="User already exists")

    total_user_data = user_op_get_all_data()

    new_user = User_in_DB(username=user_data.username,
                           hashed_password=get_hashed_password(user_data.hashed_password),
                           fullname=user_data.full_name,
                           email=user_data.email,
                           disabled=user_data.disabled)
    total_user_data[new_user.username] = new_user.__dict__
    logger.debug("Total Users are : {}".format(total_user_data))
    db_write_data(total_user_data, USER_DB_NAME)
    return user_data
