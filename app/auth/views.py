from typing import TypeVar, TypedDict, Literal
from enum import Enum
import logging

from flask import request
from argon2 import PasswordHasher

from app.auth.schemas import UserModel
from app.crud import UserCRUD


logger = logging.getLogger(name=__name__)


template = TypeVar('template')


hash_manager = PasswordHasher()


class Message(TypedDict):

    message: str
    status: bool


class ResponseRegistration(Enum):

    success: Message = {
        'message': 'Success registration',
        'status': True
    }

    already_registered: Message = {
        'message': 'It user already registered!',
        'status': False
    }

    not_validate: Message = {
        'message': 'Data don\'t pass the check!',
        'status': False
    }


class ResponseAuthentication(Enum):

    success: Message = {
        'message': 'Success authentication!',
        'status': True
    }

    not_registered = {
        'message': 'Invalid login or password!',
        'status': False
    }


class UserData(TypedDict):

    name: str
    email: str
    password1: str
    password2: str


def is_validate(user_data: UserData) -> ResponseRegistration | None:
    if user_data['password1'] != user_data['password2']:
        return ResponseRegistration.not_validate

    for key in user_data.keys():
        if not isinstance(user_data.get(key), str):
            return ResponseRegistration.not_validate

    max_length = [50, 50, 150]
    for index in list(range(3)):
        if len(list(user_data.values())[index]) > max_length[index]:
            return ResponseRegistration.not_validate


def hashing(password: str) -> str:
    hashed_password = hash_manager.hash(password)
    return hashed_password


def format_to_model(user_data: UserData) ->\
        dict[Literal['name'] | Literal['email'] |\
             Literal['hashed_password'], str]:
    return {
        'name': user_data.get('name'),
        'email': user_data.get('email'),
        'hashed_password': hashing(user_data.get('password1'))
    }


def registration(registration_request: request) ->\
        [ResponseRegistration, UserData]:
    user = {
        'name': registration_request.form['name'],
        'email': registration_request.form['email'],
        'password1': registration_request.form['password1'],
        'password2': registration_request.form['password2']
    }

    response = is_validate(user)
    if response:
        return [response, user]

    user = format_to_model(user)

    user = UserModel(**user)
    try:
        crud_manager = UserCRUD.get()
        user_in_database = crud_manager.get(user.email)
    except Exception as ex:
        raise ConnectionError(f'''CRUD-system(get) connection
                                filed! Except: {ex};''')
    else:
        if user_in_database:
            return [ResponseRegistration.already_registered, user.dict()]

    try:
        crud_manager = UserCRUD.add()
        crud_manager.add(user)
    except Exception as ex:
        raise ConnectionError(f'''CRUD-system(add) connection
                                filed! Except: {ex};''')
    else:
        logger.info(f'''User: {user} success was registered!''')
        return [ResponseRegistration.success, user.dict()]


def authentication(authentication_request: request) ->\
        [ResponseAuthentication,
         dict[Literal['email'] | Literal['password'], str]]:
    user_request = {
        'email': authentication_request.form.get('email'),
        'password': authentication_request.form.get('password')
    }
    user = None
    try:
        crud_manager = UserCRUD.get()
        user = crud_manager.get(authentication_request.form.get('email'))
    except Exception as ex:
        raise ConnectionError(f'''CRUD-system(get) connection
                                filed! Except: {ex};''')
    else:
        if not user:
            logger.debug(f'''Problem authentication user: 
                        {user_request} in the email.''')
            return [ResponseAuthentication.not_registered, user_request]

    try:
        if hash_manager.verify(user.dict().get('hashed_password'),
                               authentication_request.form.get('password')):
            return [ResponseAuthentication.success, user_request]
    except Exception as ex:
        logger.debug(f'''Problem authentication user:
                    {user_request} in the password.''')
        logger.error(f'''Verify erorr: {ex}!''')
        return [ResponseAuthentication.not_registered, user_request]
