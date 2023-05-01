import os
from typing import TypedDict

from dotenv import load_dotenv


load_dotenv()


class DataDatabase(TypedDict):

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


class BaseConfig(object):

    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    @classmethod
    def get_data_database(cls) -> DataDatabase:
        return DataDatabase(**{
            'DB_USER': cls.DB_USER,
            'DB_PASS': cls.DB_PASS,
            'DB_HOST': cls.DB_HOST,
            'DB_PORT': cls.DB_PORT,
            'DB_NAME': cls.DB_NAME
        })


class DatabaseConfig(BaseConfig):

    DEBUG: bool = True


class ServerConfig(BaseConfig):

    DEBUG: bool = True

    HOST: str = os.getenv('HOST')
    PORT: int = int(os.getenv('PORT'))