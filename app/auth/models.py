from sqlalchemy import Column, Integer, String

from app.database import base


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String(150), nullable=False)

    def __repr__(self):
        return f'''name: {self.name}; email: {self.email}; hashed_password: {self.hashed_password}'''
