import logging

from app.database import init_database
from app.crud import UserCRUD
from app.auth.schemas import UserModel


logging.basicConfig(filename='loggs.log', level=logging.INFO)


if __name__ == '__main__':
    init_database()
    user_get = UserCRUD.get()
    print(user_get.get('doom-e@bk2.ru'))