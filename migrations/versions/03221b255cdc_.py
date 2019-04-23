"""empty message

Revision ID: 03221b255cdc
Revises: 6fa758320ba5
Create Date: 2019-04-11 11:30:27.494740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03221b255cdc'
down_revision = '6fa758320ba5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_striped', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_striped')
    # ### end Alembic commands ###