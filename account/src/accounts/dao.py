
from typing import Any, Dict, Optional, Union

from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.exceptions.DatabaseException import ConflictUnicueAttribute, UnknowanDatabaseException, DatabaseException
from src.accounts.schemas import UserCreateDB, UserUpdateDB
from src.accounts.model import ROLE_USER, RoleModel, UserModel
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
                roles = new_roles_check.scalars().all()
                user.roles.extend(roles)
                return user
        except IntegrityError:
            raise ConflictUnicueAttribute('Username is already exists')
        except SQLAlchemyError:
            raise DatabaseException
        except Exception:
            raise UnknowanDatabaseException