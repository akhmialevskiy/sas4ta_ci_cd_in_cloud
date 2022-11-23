"""Create all tables

Revision ID: e8157da48aac
Revises: 
Create Date: 2022-11-23 00:19:38.183483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8157da48aac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('location', sa.String(length=200), nullable=True),
    sa.Column('followers', sa.Integer(), nullable=True),
    sa.Column('friends', sa.Integer(), nullable=True),
    sa.Column('statuses', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tweets',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('text', sa.String(length=320), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('retweets', sa.Integer(), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('lang', sa.String(length=3), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweets')
    op.drop_table('users')
    # ### end Alembic commands ###
