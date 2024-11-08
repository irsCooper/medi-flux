from typing import Any, Dict, Generic, Optional, TypeVar, Union
from pydantic import BaseModel

from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.base_model import Base
from src.exceptions.DatabaseException import DatabaseException, UnknowanDatabaseException


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = None 


    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        obj_in: Union[CreateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        try:
            stmt = (
                insert(cls.model)
                .values(**create_data)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalars().first()
        except SQLAlchemyError:
            raise DatabaseException
        except Exception as e:
            print(e)
            raise UnknowanDatabaseException



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
