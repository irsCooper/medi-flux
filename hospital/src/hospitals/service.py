from typing import Optional
import uuid

from sqlalchemy import and_

from src.exception.HospitalException import HospitalNotFound
from src.hospitals.dao import HospitalDAO
from src.hospitals.model import HospitalModel
from src.hospitals.schemas import HospitalCreate, HospitalUpdate

from sqlalchemy.ext.asyncio import AsyncSession


class HospitalService:
    @classmethod
    async def create_hospital(
        cls,
        data: HospitalCreate,
        session: AsyncSession
    ) -> Optional[HospitalModel]:
        return await HospitalDAO.add(
            session=session,
            obj_in=HospitalCreate(**data.model_dump())
        )
    

    @classmethod
    async def update_hospital(
        cls,
        hospital_id: uuid.UUID,
        data: HospitalUpdate,
        session: AsyncSession
    ) -> Optional[HospitalModel]:
        hospital = await HospitalDAO.update(
            session,
            and_(
                HospitalModel.id == hospital_id,
                HospitalModel.is_deleted == False
            ),
            obj_in=HospitalUpdate(**data.model_dump())
        )

        if not hospital:
            raise HospitalNotFound
        
        return hospital
    

    @classmethod
    async def delete_hospital(
        cls,
        hospital_id: uuid.UUID,
        session: AsyncSession
    ):
        hospital = await HospitalDAO.update(
            session,
            and_(
                HospitalModel.id == hospital_id,
                HospitalModel.is_deleted == False
            ),
            obj_in={'is_deleted': True}
        )
    
        if not hospital:
            raise HospitalNotFound


    @classmethod
    async def get_hospitals(
        cls,
        offset: int,
        limit: int,
        session: AsyncSession
    ) -> Optional[list[HospitalModel]]:
        return await HospitalDAO.find_all(
            session,
            HospitalModel.is_deleted == False,
            offset=offset,
            limit=limit
        )
    

    @classmethod
    async def get_hospital(
        cls,
        hospital_id: uuid.UUID,
        session: AsyncSession
    ) -> Optional[HospitalModel]:
        hospital: HospitalModel = await HospitalDAO.find_one_or_none(
            session,
            HospitalModel.id == hospital_id
        )

        if not hospital or hospital.is_deleted:
            raise HospitalNotFound
        
        return hospital
    

    @classmethod
    async def get_list_rooms(
        cls,
        hospital_id: uuid.UUID,
        session: AsyncSession
    ):
        return await HospitalDAO.get_rooms(
            session,
            and_(
                HospitalModel.id == hospital_id,
                HospitalModel.is_deleted == False
            )
        )