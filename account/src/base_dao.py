from typing import Generic, TypeVar

from pydantic import BaseModel

from src.base_model import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = None 


    @classmethod
    async def add():
        pass 




    @classmethod
    async def update():
        pass 




    @classmethod
    async def delete():
        pass 




    @classmethod
    async def count():
        pass 




    @classmethod
    async def count():
        pass 




    @classmethod
    async def find_all():
        pass 
