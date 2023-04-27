from sqlalchemy import Column, Integer, String

from app.database import base
from schemas import User


class User(base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String(150), nullable=False)

    def __init__(self, user: User):
        self.name = user.name
        self.email = user.email
        self.hashed_password = user.password

    def __repr__(self):
        return f'Login: {self.name}; Email: {self.email}'
