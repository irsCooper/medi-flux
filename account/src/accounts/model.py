import uuid
from sqlalchemy import UUID, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..base_model import BaseModel


class UserRolesModel(BaseModel):
    __tablename__ = 'user_roles'

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)



class RoleModel(BaseModel):
    __tablename__ = 'roles'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name_role: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        secondary="user_roles",
        back_populates="roles",
    )



class UserModel(BaseModel):
    __tablename__ = 'users'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False) 
    user_name: Mapped[str] = mapped_column(String, unique=True, nullable=False) 
    hashed_password: Mapped[bytes]  

    active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    roles: Mapped[list["RoleModel"]] = relationship(
        "RoleModel", 
        secondary="user_roles",
        back_populates="users"
    )