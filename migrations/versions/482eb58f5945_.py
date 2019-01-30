"""empty message

Revision ID: 482eb58f5945
Revises: e28d0da492b0
Create Date: 2019-01-24 15:55:46.955290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '482eb58f5945'
down_revision = 'e28d0da492b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    rolestype = postgresql.ENUM('active', 'inactive', 'archive', name='rolestype')
    rolestype.create(op.get_bind())
    op.add_column('user', sa.Column('role', sa.Enum('ADMIN', 'JUGE', 'PLAYER', 'PUBLIC', name='rolestype'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TYPE rolestype;")
    op.drop_column('user', 'role')
    # ### end Alembic commands ###
