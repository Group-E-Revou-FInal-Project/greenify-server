"""change is_out_stock column constraint to not nullable

Revision ID: c81694f5e39f
Revises: 3321bc33214b
Create Date: 2024-12-16 20:50:35.992954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c81694f5e39f'
down_revision = '3321bc33214b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('is_out_of_stock',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('is_out_of_stock',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
