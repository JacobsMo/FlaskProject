from sqlalchemy.orm import sessionmaker
from database import engine


class Session:

    def __init__(self):
        '''TODO'''
        try:
            self.__session = sessionmaker(bind=engine)
        except Exception as ex:
            raise ConnectionError()