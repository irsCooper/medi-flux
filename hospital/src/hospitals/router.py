import uuid
from fastapi import APIRouter, Depends, Query

from src.hospitals.service import HospitalService
from src.hospitals.schemas import HospitalCreate, HospitalSchema, HospitalUpdate, RoomSchema
from src.core.db_helper import db
from src.core.config import ROLE_ADMIN
from src.dependencies import validate_token, get_current_role

from sqlalchemy.ext.asyncio import AsyncSession

router =APIRouter(
    prefix="/Hospitals",
    tags=["Hospitals"]
)

@router.get("", response_model=list[HospitalSchema])
async def get_list_hospitals(
    offset: int = Query(..., alias='from', ge=0),
    limit: int = Query(..., alias='count', ge=1),
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: dict = Depends(validate_token)
):
    return await HospitalService.get_hospitals(
        offset=offset,
        limit=limit,
        session=session
    )


@router.get("/{id}", response_model=HospitalSchema)
async def get_hospital_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: dict = Depends(validate_token)
):
    return await HospitalService.get_hospital(
        hospital_id=id,
        session=session
    )


@router.get("/{id}/Rooms", response_model=list[RoomSchema])
async def get_romms_in_hospital_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: dict = Depends(validate_token)
):
    return await HospitalService.get_list_rooms(
        hospital_id=id,
        session=session
    )


@router.post("", response_model=HospitalSchema)
async def create_hospital_only_admin(
    data: HospitalCreate,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: dict = Depends(validate_token)
):
    await get_current_role([ROLE_ADMIN], valid_token)
    return await HospitalService.create_hospital(
        data=data,
        session=session
    ) 


@router.put("/{id}", response_model=HospitalSchema)
async def update_hospital_info_by_id_only_admin(
    data: HospitalUpdate,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: dict = Depends(validate_token)
):
    await get_current_role([ROLE_ADMIN], valid_token)
    return await HospitalService.update_hospital(
        hospital_id=data.id,
        data=data,
        session=session
    ) 


@router.delete("/{id}")
async def delete_hospital_by_id_only_admin(
    id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
    valid_token: dict = Depends(validate_token)
):
    await get_current_role([ROLE_ADMIN], valid_token)
    return await HospitalService.delete_hospital(
        hospital_id=id,
        session=session
    )