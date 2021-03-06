"""empty message

Revision ID: 5651c8539e9f
Revises: 138ad6638c1e
Create Date: 2014-11-13 21:49:20.958943

"""

# revision identifiers, used by Alembic.
revision = '5651c8539e9f'
down_revision = '138ad6638c1e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email_authorized', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email_authorized')
    ### end Alembic commands ###
