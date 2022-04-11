"""добавлена колонка с датой создания в таблицу с комментарием

Revision ID: 10cad10d0c23
Revises: 
Create Date: 2022-04-11 16:49:07.341281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10cad10d0c23'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('date_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'date_time')
    # ### end Alembic commands ###
