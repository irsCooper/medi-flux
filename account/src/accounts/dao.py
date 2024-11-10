
from typing import Any, Dict, Optional, Union

from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.exceptions.DatabaseException import ConflictUnicueAttribute, UnknowanDatabaseException, DatabaseException
from src.accounts.schemas import ROLE_ADMIN, UserCreateDB, UserUpdateDB, ROLE_USER
from src.accounts.model import RoleModel, UserModel
from src.base_dao import BaseDAO


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel

    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        obj_in: Union[UserCreateDB, Dict[str, Any]]
    ) -> Optional[UserModel]:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else: 
            create_data = obj_in.model_dump(exclude_unset=True)
        
        roles = create_data.pop("roles", None)
        print(roles)

        try:
            stmt = (
                insert(cls.model)
                .values(**create_data)
                .returning(cls.model)
                .options(
                    selectinload(cls.model.roles)
                )
            )
            result = await session.execute(stmt)
            await session.commit()
            user: UserModel = result.scalars().first()

            if user:
                if not roles:
                    roles = [ROLE_USER]

                new_roles_check = await session.execute(
                    select(RoleModel)
                    .where(RoleModel.name_role.in_(roles))
                )
                new_roles = new_roles_check.scalars().all()
                user.roles.extend(new_roles)
                await session.commit()
                return user
        except IntegrityError:
            raise ConflictUnicueAttribute('Username is already exists')
        except SQLAlchemyError:
            raise DatabaseException
        except Exception:
            raise UnknowanDatabaseException
        

    @classmethod
    async def find_one_or_none(
        cls,
        session: AsyncSession,
        *filters,
        **filter_by
    ) -> Optional[UserModel]:
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.roles)
            )
            .filter(*filters)
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        return result.scalars().one_or_none()
    
    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        *filters,
        offset: int = 0,
        limit: int = 100,
        **filter_by
    ):
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.roles)
            )
            .join(cls.model.roles)
            .filter(*filters)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        ) 
        result = await session.execute(stmt)
        return result.scalars().all()