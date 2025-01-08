from typing import Any, Dict, Generic, Optional, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.exception import DatabaseException, UnknowanDatabaseException



ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

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
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseException
        except Exception as e:
            print(e)
            raise UnknowanDatabaseException
            