"""add new profile_picture column in user table

Revision ID: 9da704d9d05b
Revises: c81694f5e39f
Create Date: 2024-12-21 00:07:17.599982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9da704d9d05b'
down_revision = 'c81694f5e39f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_interests', schema=None) as batch_op:
        batch_op.drop_column('id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=255), nullable=True))
        batch_op.alter_column('is_seller',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_seller',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.drop_column('profile_picture')

    with op.batch_alter_table('user_interests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False))

    # ### end Alembic commands ###