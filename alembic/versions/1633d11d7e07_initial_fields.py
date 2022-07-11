"""Initial fields

Revision ID: 1633d11d7e07
Revises: 
Create Date: 2022-07-11 14:59:48.983053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1633d11d7e07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('originalname', sa.String(), nullable=False),
    sa.Column('setup_outcome', sa.String(), nullable=True),
    sa.Column('call_outcome', sa.String(), nullable=True),
    sa.Column('teardown_outcome', sa.String(), nullable=True),
    sa.Column('coiled_runtime', sa.String(), nullable=True),
    sa.Column('dask_version', sa.String(), nullable=True),
    sa.Column('ci_run_url', sa.String(), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('average_memory', sa.Float(), nullable=True),
    sa.Column('peak_memory', sa.Float(), nullable=True),
    sa.Column('compute_time', sa.Float(), nullable=True),
    sa.Column('disk_spill_time', sa.Float(), nullable=True),
    sa.Column('serializing_time', sa.Float(), nullable=True),
    sa.Column('transfer_time', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_run')
    # ### end Alembic commands ###
