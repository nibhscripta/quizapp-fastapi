"""add complete column to quiz instance table

Revision ID: 1695680e8155
Revises: 962f020f2683
Create Date: 2022-04-21 11:44:05.043603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1695680e8155'
down_revision = '962f020f2683'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quizinstances', sa.Column('complete', sa.Boolean(), server_default='FALSE', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quizinstances', 'complete')
    # ### end Alembic commands ###
