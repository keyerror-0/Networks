"""empty message

Revision ID: 02d8647ffac1
Revises: 13938ec1e138
Create Date: 2025-04-14 12:46:24.362912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02d8647ffac1'
down_revision = '13938ec1e138'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_index('ix_item_currency')
        batch_op.drop_index('ix_item_href')
        batch_op.drop_index('ix_item_name')
        batch_op.drop_index('ix_item_old_price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.create_index('ix_item_old_price', ['old_price'], unique=False)
        batch_op.create_index('ix_item_name', ['name'], unique=True)
        batch_op.create_index('ix_item_href', ['href'], unique=True)
        batch_op.create_index('ix_item_currency', ['currency'], unique=False)

    # ### end Alembic commands ###
