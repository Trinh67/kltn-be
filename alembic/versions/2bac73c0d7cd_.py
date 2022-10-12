"""empty message

Revision ID: 2bac73c0d7cd
Revises: d2d8615dd472
Create Date: 2022-10-04 22:52:29.623035

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2bac73c0d7cd'
down_revision = 'd2d8615dd472'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('refuse_reason', sa.Text(length=255), nullable=True))
    op.alter_column('file', 'user_id',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=50),
               existing_nullable=False)
    op.alter_column('file', 'google_driver_id',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=50),
               existing_nullable=True)
    op.alter_column('user', 'name',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=50),
               existing_nullable=False)
    op.alter_column('user', 'user_id',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=50),
               existing_nullable=False)
    op.alter_column('user', 'source',
               existing_type=mysql.TINYTEXT(),
               type_=sa.Text(length=50),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'source',
               existing_type=sa.Text(length=50),
               type_=mysql.TINYTEXT(),
               existing_nullable=True)
    op.alter_column('user', 'user_id',
               existing_type=sa.Text(length=50),
               type_=mysql.TINYTEXT(),
               existing_nullable=False)
    op.alter_column('user', 'name',
               existing_type=sa.Text(length=50),
               type_=mysql.TINYTEXT(),
               existing_nullable=False)
    op.alter_column('file', 'google_driver_id',
               existing_type=sa.Text(length=50),
               type_=mysql.TINYTEXT(),
               existing_nullable=True)
    op.alter_column('file', 'user_id',
               existing_type=sa.Text(length=50),
               type_=mysql.TINYTEXT(),
               existing_nullable=False)
    op.drop_column('file', 'refuse_reason')
    # ### end Alembic commands ###