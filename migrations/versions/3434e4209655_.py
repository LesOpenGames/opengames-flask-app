"""empty message

Revision ID: 3434e4209655
Revises: 7d6ce327dced
Create Date: 2019-02-19 14:22:58.532951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3434e4209655'
down_revision = '7d6ce327dced'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('is_paid', sa.Boolean(), nullable=True))
    op.add_column('team', sa.Column('is_partner', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('team', 'is_partner')
    op.drop_column('team', 'is_paid')
    # ### end Alembic commands ###