"""migrate voucher table

Revision ID: 617fe4f4855a
Revises: c5ba8d9a2787
Create Date: 2024-12-09 19:56:56.442580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '617fe4f4855a'
down_revision = 'c5ba8d9a2787'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('voucher',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('seller_id', sa.BigInteger(), nullable=False),
    sa.Column('product_id', sa.BigInteger(), nullable=False),
    sa.Column('kode_voucher', sa.String(length=50), nullable=False),
    sa.Column('expired', sa.DateTime(), nullable=False),
    sa.Column('voucher_desc', sa.String(length=255), nullable=True),
    sa.Column('nama_voucher', sa.String(length=100), nullable=False),
    sa.Column('discount_percentage', sa.Float(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['seller_profile.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('kode_voucher')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('voucher')
    # ### end Alembic commands ###
