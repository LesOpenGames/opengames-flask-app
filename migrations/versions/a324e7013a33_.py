"""empty message

Revision ID: a324e7013a33
Revises: 03221b255cdc
Create Date: 2019-04-26 14:45:46.252383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a324e7013a33'
down_revision = '03221b255cdc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score',
    sa.Column('challenge_id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('chrono_s', sa.Integer(), nullable=True),
    sa.Column('tournament_pos', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenge.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('challenge_id', 'player_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('score')
    # ### end Alembic commands ###
