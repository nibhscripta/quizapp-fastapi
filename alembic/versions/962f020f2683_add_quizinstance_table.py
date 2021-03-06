"""add quizinstance table

Revision ID: 962f020f2683
Revises: 33e7b14673b9
Create Date: 2022-04-20 14:55:28.871648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '962f020f2683'
down_revision = '33e7b14673b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quizinstances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quizinstances')
    # ### end Alembic commands ###
