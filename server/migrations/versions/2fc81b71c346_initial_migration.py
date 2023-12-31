"""Initial migration

Revision ID: 2fc81b71c346
Revises: 
Create Date: 2023-10-26 11:49:23.938017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fc81b71c346'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('assets',
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('asset_name', sa.String(length=80), nullable=False),
    sa.Column('asset_category', sa.String(length=80), nullable=True),
    sa.Column('asset_image', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('asset_id')
    )
    op.create_table('requests',
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('request_reason', sa.String(length=255), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('urgency', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('request_id')
    )
    op.create_table('asset_allocations',
    sa.Column('asset_allocation_id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.asset_id'], ),
    sa.ForeignKeyConstraint(['employee_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('asset_allocation_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('asset_allocations')
    op.drop_table('requests')
    op.drop_table('assets')
    op.drop_table('users')
    # ### end Alembic commands ###
