"""empty message

Revision ID: e341aed5de71
Revises: ce53fe0dc424
Create Date: 2020-05-19 00:06:24.790719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e341aed5de71'
down_revision = 'ce53fe0dc424'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'token')
    # ### end Alembic commands ###
