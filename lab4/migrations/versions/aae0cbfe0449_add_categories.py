"""Add categories

Revision ID: aae0cbfe0449
Revises: 02d8647ffac1
Create Date: 2025-04-14 18:06:30.584586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aae0cbfe0449'
down_revision = '02d8647ffac1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('item_category',
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], )
    )
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['href'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    op.drop_table('item_category')
    op.drop_table('category')
    # ### end Alembic commands ###
