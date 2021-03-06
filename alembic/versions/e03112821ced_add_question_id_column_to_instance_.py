"""add question id column to instance answer table

Revision ID: e03112821ced
Revises: fc67918b653c
Create Date: 2022-04-30 22:27:04.441442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e03112821ced'
down_revision = 'fc67918b653c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quizinstanceanswers', sa.Column('question_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quizinstanceanswers', 'question_id')
    # ### end Alembic commands ###
