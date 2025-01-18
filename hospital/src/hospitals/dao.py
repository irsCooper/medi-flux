from typing import Any, Dict, Optional, Union

from sqlalchemy import insert, select, update

from src.exception.HospitalException import HospitalNotFound
from src.exception import DatabaseException, UnknowanDatabaseException
from src.hospitals.schemas import HospitalCreate, HospitalUpdate
from src.hospitals.model import HospitalModel, RoomModel
from src.base_dao import BaseDAO

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload


class HospitalDAO(BaseDAO[HospitalModel, HospitalCreate, HospitalUpdate]):
    model = HospitalModel

    
    @classmethod
    async def get_rooms(
        cls,
        session: AsyncSession,
        *filters,
        **filter_by
    ):
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.rooms)
            )
            .filter(*filters)
            .filter_by(**filter_by)
        )

        result = await session.execute(stmt)
        hospitals = result.scalars().one_or_none()

        if not hospitals:
            raise HospitalNotFound

        return hospitals.rooms


    @classmethod
    async def update_romms(
        cls,
        session: AsyncSession,
        rooms,
        hospital: HospitalModel
    ):
        room_names = [room['name'] for room in rooms]
        
        existing_rooms_stmt = (
            select(RoomModel)
            .where(RoomModel.name.in_(room_names))
        )

        result = await session.execute(existing_rooms_stmt)
        existing_rooms = result.scalars().all()

        # Убираем существующие комнаты, оставляем только те, которые нужно создать
        new_rooms_names = set(room_names) - {room.name for room in existing_rooms}

        if new_rooms_names:
            new_rooms_stmt = (
                insert(RoomModel)
                .values([{"name": name} for name in new_rooms_names])
                .returning(RoomModel)
            )

            result = await session.execute(new_rooms_stmt)
            new_rooms = result.scalars().all()
            all_rooms = existing_rooms + new_rooms
        else: 
            all_rooms = existing_rooms
        
        # Обновляем комнаты
        hospital.rooms = all_rooms




    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        obj_in: Union[HospitalCreate, Dict[str, Any]]
    ) -> Optional[HospitalModel]:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        rooms = create_data.pop("rooms", None)

        try:
            stmt = (
                insert(cls.model)
                .values(**create_data)
                .returning(cls.model)
                .options(
                    selectinload(cls.model.rooms)
                )
            )

            result = await session.execute(stmt)
            hospital: HospitalModel = result.scalars().first()

            if rooms:
                await cls.update_romms(session, rooms, hospital)

            await session.commit()
            return hospital
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseException
        except Exception as e:
            print(e)
            raise UnknowanDatabaseException
        

    @classmethod
    async def update(
        cls, 
        session: AsyncSession,
        *where,
        obj_in: Union[HospitalUpdate, Dict[str, Any]]
    ) -> Optional[HospitalModel]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else: 
            update_data = obj_in.model_dump(exclude_unset=True)

        rooms = update_data.pop("rooms", None)

        try:
            stmt = (
                update(cls.model)
                .where(*where)
                .values(**update_data)
                .returning(cls.model)
                .options(
                    selectinload(cls.model.rooms)
                )
            )

            result = await session.execute(stmt)
            hospital: HospitalModel = result.scalars().first()

            if rooms:
                await cls.update_romms(session, rooms, hospital)

            await session.commit()
            return hospital
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseException
        except Exception as e:
            print(e)
            raise UnknowanDatabaseException
        

    @classmethod
    async def find_one_or_none(
        cls,
        session: AsyncSession,
        *filters,
        **filter_by
    ) -> Optional[HospitalModel]:
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.rooms)
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
    ) -> Optional[list[HospitalModel]]:
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.rooms)
            )
            # .join(cls.model.rooms)
            .filter(*filters)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )

        result = await session.execute(stmt)
        return result.scalars().all()