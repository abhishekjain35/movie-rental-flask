"""empty message

Revision ID: 84fea051b1f6
Revises: 
Create Date: 2021-07-18 17:51:07.908574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84fea051b1f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_name', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('movie_name')
    )
    op.create_table('rents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('charges', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rents')
    op.drop_table('movies')
    # ### end Alembic commands ###
