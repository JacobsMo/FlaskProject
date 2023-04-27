from typing import TypeVar, NewType
from enum import Enum
import logging

from pydantic import BaseModel, Field, EmailStr, validator, ValidationError


logger = logging.getLogger(__name__)


T = TypeVar('T')


class Types(Enum):
    INT: int = 123
    STR: str = '123'
    BOOL: bool = True
    FLOAT: float = 123.0


class User(BaseModel):

    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    password: str = Field(max_length=150)

    @staticmethod
    def type_validation(attribute: T, name: str,
                        type_for_attribute: Types) -> None:
        if not isinstance(attribute, type(type_for_attribute)):
            raise ValidationError(f'''{__class__}_pydantic_model:
                                    Input {name} it\'s not valid''')

        logger.info(f'{name} passed the test!')

    @staticmethod
    def len_validation(attribute: str, name: str, length: int) -> None:
        if len(attribute) > length:
            raise ValidationError(f'''{__class__}_pydantic_model:
                                    Input {name} it\'s not valid''')

        logger.info(f'{name} passed the test!')

    @validator('name')
    @classmethod
    def name_validator(cls, value) -> str:
        cls.type_validation(value, 'name', Types.STR)
        cls.len_validation(value, 'name', 50)

        return value

    @validator('email')
    @classmethod
    def email_validator(cls, value) -> str:
        cls.type_validation(value, 'email', Types.STR)
        cls.len_validation(value, 'email', 50)

        if '@' not in value:
            raise ValidationError(f'''{__class__}_pydantic_model:
                                    Input email it\'s not valid''')

        return value

    @validator('password')
    @classmethod
    def password_validator(cls, value) -> str:
        cls.type_validation(value, 'password', Types.STR)
        cls.len_validation(value, 'password', Types.STR)

        return value