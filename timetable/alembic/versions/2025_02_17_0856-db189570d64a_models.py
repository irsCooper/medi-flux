"""models

Revision ID: db189570d64a
Revises: 9e64fd01c271
Create Date: 2025-02-17 08:56:57.743293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'db189570d64a'
down_revision: Union[str, None] = '9e64fd01c271'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timetables',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('hospital_id', sa.UUID(), nullable=False),
    sa.Column('doctor_id', sa.UUID(), nullable=False),
    sa.Column('from_column', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('to', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('room', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_timetables_doctor_id'), 'timetables', ['doctor_id'], unique=False)
    op.create_index(op.f('ix_timetables_hospital_id'), 'timetables', ['hospital_id'], unique=False)
    op.create_table('appointments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('timetable_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('time', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['timetable_id'], ['timetables.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_timetable_doctor_id', table_name='timetable')
    op.drop_index('ix_timetable_hospital_id', table_name='timetable')
    op.drop_table('timetable')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timetable',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('hospital_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('doctor_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('from_column', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('to', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('room', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='timetable_pkey')
    )
    op.create_index('ix_timetable_hospital_id', 'timetable', ['hospital_id'], unique=False)
    op.create_index('ix_timetable_doctor_id', 'timetable', ['doctor_id'], unique=False)
    op.drop_table('appointments')
    op.drop_index(op.f('ix_timetables_hospital_id'), table_name='timetables')
    op.drop_index(op.f('ix_timetables_doctor_id'), table_name='timetables')
    op.drop_table('timetables')
    # ### end Alembic commands ###
