'''TODO finalize structure it module'''
from abc import ABC, abstractstaticmethod, abstractmethod
from typing import TypeVar, NewType
import logging

from sqlalchemy.orm import sessionmaker

from app.database import engine
from app.auth.models import User
from app.auth.schemas import UserModel


logger = logging.getLogger(name=__name__)

T = TypeVar('T')
link = NewType('link', T)


class AddingSession(ABC):

    def __new__(cls) -> link:
        return super().__new__(cls)

    def __init__(self):
        raise NotImplementedError(f'''class {__class__} it\'s abstract
                                    and can\'s have object\'s!''')

    @abstractmethod
    def add(self, model: T) -> None:
        pass


class GettingSession(ABC):

    def __new__(cls) -> link:
        return super().__new__(cls)

    def __init__(self):
        raise NotImplementedError(f'''class {__class__} is\'s abstract
                                    and can\'t have objects\'s!''')

    @abstractmethod
    def get(self, model: T) -> None:
        pass


class AddingSessionUser(AddingSession):

    __instance: AddingSession | None = None

    def __new__(cls) -> AddingSession:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        try:
            self.__session = sessionmaker(bind=engine)
        except Exception as ex:
            raise ConnectionError(f'''class: {__class__};
                                    engine connection failed: {ex}''')
        else:
            logger.info(f'class {__class__}; engine connection success!')

    def add(self, user: UserModel) -> None:
        '''TODO Create checking data'''
        with self.__session() as session:
            try:
                addable_user = User(name=user.name,
                                    email=user.email,
                                    hashed_password=user.hashed_password)
                session.add(addable_user)
            except Exception as ex:
                session.rollback()
                raise Exception(f'''class: {__class__} exception because
                                added user error: {ex}''')
            else:
                logger.info(f'class {__class__}; added user success!')
                session.commit()


class GettingSessionUser(GettingSession):

    __instance = None

    def __new__(cls) -> link:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self):
        try:
            self.__session = sessionmaker(bind=engine)
        except Exception as ex:
            raise ConnectionError(f'''class: {__class__};
                                    engine connection failed: {ex}''')
        else:
            logger.info(f'class {__class__}; engine connection success!')

    def get(self, email: str) -> UserModel.dict():
        with self.__session() as session:
            try:
                response = session.query(User).filter(User.email == email).all()[0]
                return UserModel(**{
                    'name': response.name,
                    'email': response.email,
                    'hashed_password': response.hashed_password
                }).dict()
            except Exception as ex:
                raise Exception(f'''class: {__class__};
                                request failed: {ex}!''')


class ModelCRUD(ABC):

    def __init__(self) -> None:
        raise NotImplementedError(f'''class \'{__class__}\'
                                    can\'t have object\'s''')

    @abstractstaticmethod
    def add() -> AddingSession:
        pass

    @abstractstaticmethod
    def get() -> GettingSession:
        pass


class UserCRUD(ModelCRUD):

    def __init__(self) -> None:
        pass

    @staticmethod
    def add() -> AddingSession:
        return AddingSessionUser()

    @staticmethod
    def get() -> GettingSession:
        return GettingSessionUser()