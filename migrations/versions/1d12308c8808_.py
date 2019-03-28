"""empty message

Revision ID: 1d12308c8808
Revises: 2e50e616bcbd
Create Date: 2019-03-26 15:23:53.351856

"""
from alembic import op
import sqlalchemy as sa

from app.models import ChallScoreType, ChallTeamType


# revision identifiers, used by Alembic.
revision = '1d12308c8808'
down_revision = '2e50e616bcbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    challenge_table = op.create_table('challenge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('challenge_name', sa.String(length=64), nullable=True),
    sa.Column('score_type', sa.Integer(), nullable=True),
    sa.Column('team_type', sa.Integer(), nullable=True),
    sa.Column('juge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['juge_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_challenge_challenge_name'), 'challenge', ['challenge_name'], unique=True)
    # ### end Alembic commands ###




def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_challenge_challenge_name'), table_name='challenge')
    op.drop_table('challenge')
    # ### end Alembic commands ###
