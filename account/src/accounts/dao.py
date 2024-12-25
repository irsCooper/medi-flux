
from typing import Any, Dict, Optional, Union

from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.exceptions.DatabaseException import ConflictUnicueAttribute, UnknowanDatabaseException, DatabaseException
from src.accounts.schemas import ROLE_ADMIN, ROLE_DOCTOR, ROLE_MANAGER, UserCreateDB, UserUpdateDB, ROLE_USER
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
        
        system_roles = [ROLE_ADMIN, ROLE_USER, ROLE_DOCTOR, ROLE_MANAGER]
        if roles:
            for role in roles:
                if role not in system_roles:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Role {role} not found"
                    )

        try:
            stmt = (
                insert(cls.model)
                .values(**create_data)
                .returning(cls.model)
                .options(
                    selectinload(cls.model.roles),
                    # selectinload(cls.model.refresh_session)
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
                # await session.commit()
                return user
        except IntegrityError:
            raise ConflictUnicueAttribute('Username is already exists')
        except SQLAlchemyError as e:
            print(e)
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
        res = result.scalars().all()
        return res


    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        *where,
        obj_in: Union[UserUpdateDB, Dict[str, Any]]
    ) -> Optional[UserModel]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        roles = update_data.pop("roles", None)

        stmt = (
            update(cls.model)
            .where(*where)
            .values(**update_data)
            .returning(cls.model)
            .options(
                selectinload(cls.model.roles)
            )
        )
        
        result = await session.execute(stmt)
        update_user = result.scalars().one_or_none()

        if update_user and roles is not None:
            current_roles = {role.name_role for role in update_user.roles}

            new_roles_query = await session.execute(
                select(RoleModel)
                .where(RoleModel.name_role.in_(roles))
            )
            new_roles = new_roles_query.scalars().all()

            new_roles_set = {role.name_role for role in new_roles}

            roles_to_add = new_roles_set - current_roles
            for role in new_roles:
                if role.name_role in roles_to_add:
                    update_user.roles.append(role)

            roles_to_remove = current_roles - new_roles_set
            update_user.roles = [role for role in update_user.roles if role.name_role not in roles_to_remove]

        await session.commit()
        return update_user