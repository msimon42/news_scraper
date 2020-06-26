"""empty message

Revision ID: 920965fa1a5a
Revises: c668a3d03ae0
Create Date: 2020-06-26 12:54:29.048488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '920965fa1a5a'
down_revision = 'c668a3d03ae0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_filters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filter_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['filter_id'], ['filters.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_filters')
    op.drop_table('filters')
    # ### end Alembic commands ###
