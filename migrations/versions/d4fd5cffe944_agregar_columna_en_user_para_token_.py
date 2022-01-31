"""Agregar columna en user para token activo

Revision ID: d4fd5cffe944
Revises: 38291e1434a3
Create Date: 2022-01-31 16:27:17.697325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4fd5cffe944'
down_revision = '38291e1434a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active_token', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'active_token')
    # ### end Alembic commands ###
