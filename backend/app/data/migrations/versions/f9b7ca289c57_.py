"""

Revision ID: f9b7ca289c57
Revises:
Create Date: 2024-08-30 15:46:06.641603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9b7ca289c57'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('alias', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('buildings',
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sections',
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('building_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('floors',
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('properties',
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('building_id', sa.UUID(), nullable=True),
    sa.Column('section_id', sa.UUID(), nullable=True),
    sa.Column('floor_id', sa.UUID(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ),
    sa.ForeignKeyConstraint(['floor_id'], ['floors.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('properties')
    op.drop_table('floors')
    op.drop_table('sections')
    op.drop_table('buildings')
    op.drop_table('projects')
    # ### end Alembic commands ###
