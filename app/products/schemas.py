from decimal import Decimal

from pydantic import BaseModel, Field, validator, ValidationError


class ProductsModel(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=300)
    price: Decimal = Field(le=999999.99)
    type_id: int = Field(ge=0)

    @validator('name')
    def name_validator(cls, value: str) -> str:
        return value

    @validator('description')
    def description_validator(cls, value: str) -> str:
        return value

    @validator('price')
    def price_validator(cls, value: Decimal) -> Decimal:
        return value

    @validator('type_id')
    def typeid_validator(cls, value: int) -> int:
        return value