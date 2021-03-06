"""empty message

Revision ID: a1e42eda6e1
Revises: 558fa5ce7b87
Create Date: 2014-11-13 15:58:39.277525

"""

# revision identifiers, used by Alembic.
revision = 'a1e42eda6e1'
down_revision = '558fa5ce7b87'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('picture_like', sa.Column('flickr_id', sa.BigInteger(), nullable=True))
    op.create_unique_constraint(None, 'picture_like', ['flickr_id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'picture_like')
    op.drop_column('picture_like', 'flickr_id')
    ### end Alembic commands ###
