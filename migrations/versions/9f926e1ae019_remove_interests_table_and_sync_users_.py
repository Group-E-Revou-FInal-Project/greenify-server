"""remove interests table, and sync users_interest with categories table

Revision ID: 9f926e1ae019
Revises: 4fdaa1273b31
Create Date: 2024-12-06 21:37:33.673248

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9f926e1ae019'
down_revision = '4fdaa1273b31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('interests')
    with op.batch_alter_table('user_interests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        # batch_op.drop_constraint('user_interests_interest_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'categories', ['category_id'], ['id'])
        # batch_op.drop_column('interest_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_interests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('interest_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_interests_interest_id_fkey', 'interests', ['interest_id'], ['id'])
        batch_op.drop_column('category_id')

    op.create_table('interests',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('interest', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name='interests_category_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='interests_pkey'),
    sa.UniqueConstraint('interest', name='interests_interest_key')
    )
    # ### end Alembic commands ###