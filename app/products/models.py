from sqlalchemy import Column, String, Integer, ForeignKey, Numeric

from app.database import base


class Type(base):
    __tablename__ = 'product_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)


class Product(base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(300), nullable=True)
    price = Column(Numeric(8, 2), nullable=False)
    type_id = Column(Integer, ForeignKey('product_types.id'), nullable=False)

    def __repr__(self):
        return f'Name: {self.name}; Description: {self.description}'