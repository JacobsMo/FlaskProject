'''TODO finalize structure it module'''
from abc import ABC, abstractstaticmethod, abstractmethod
from typing import TypeVar, NewType
import logging

from sqlalchemy.orm import sessionmaker

from app.database import engine
from app.auth.models import User
from app.products.models import Product
from app.auth.schemas import UserModel
from app.products.schemas import ProductsModel


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
        with self.__session() as session:
            try:
                addable_user = User(user.dict())
                session.add(addable_user)
            except Exception as ex:
                session.rollback()
                raise Exception(f'''class: {__class__}; exception because
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

    def get(self, email: str) -> UserModel | list[None]:
        with self.__session() as session:
            try:
                response = session.query(User).\
                    filter(User.email == email).all()
                if response:
                    response = response[0]
            except Exception as ex:
                raise Exception(f'''class: {__class__};
                                request failed: {ex}!''')
            else:
                if response:
                    try:
                        return UserModel(**{
                            'name': response.name,
                            'email': response.email,
                            'hashed_password': response.hashed_password
                        })
                    except Exception as ex:
                        raise ValueError(f'''Invalid data for the model;
                                            Except: {ex}''')

                return []


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


class AddingSessionProduct(AddingSession):
    __instance: AddingSession | None = None

    def __new__(cls) -> AddingSession:
        if not cls.__instance:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        try:
            self.__session = sessionmaker(bind=engine)
        except Exception as ex:
            raise ConnectionError(f'''class: {__class__};
                                    engine connection failed: {ex}''')

        logger.info(f'''class: {__class__}; engine connection success!''')

    def add(self, product: ProductsModel) -> None:
        with self.__session() as session:
            try:
                product = Product(product.dict())
                session.add(product)
            except Exception as ex:
                session.rollback()
                raise Exception(f'''class: {__class__};
                                added product error: {ex}!''')

            logger.info(f'class {__class__}; added product: {product},\
                        success!')
            session.commit()


class GettingSessionProduct(GettingSession):
    pass


class ProductCRUD(ModelCRUD):
    def __init__(self) -> None:
        pass

    @staticmethod
    def add() -> AddingSession:
        return AddingSessionProduct()

    @staticmethod
    def get() -> GettingSession:
        return GettingSessionProduct()