"""add table for quiz instance answers

Revision ID: 8d69d3fb7208
Revises: 1695680e8155
Create Date: 2022-04-21 17:23:34.068041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d69d3fb7208'
down_revision = '1695680e8155'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quizinstanceanswers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['instance_id'], ['quizinstances.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quizinstanceanswers')
    # ### end Alembic commands ###
