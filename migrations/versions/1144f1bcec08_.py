"""empty message

Revision ID: 1144f1bcec08
Revises: a1e42eda6e1
Create Date: 2014-11-13 16:00:25.831725

"""

# revision identifiers, used by Alembic.
revision = '1144f1bcec08'
down_revision = 'a1e42eda6e1'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    #op.drop_column('picture_like', 'flickr_id')
    #op.drop_constraint(u'flickr_id_UNIQUE', 'picture_like', type_='unique')
    op.add_column('place_picture', sa.Column('flickr_id', sa.BigInteger(), nullable=True))
    op.create_unique_constraint(None, 'place_picture', ['flickr_id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'place_picture')
    op.drop_column('place_picture', 'flickr_id')
    op.create_unique_constraint(u'flickr_id', 'picture_like', ['flickr_id'])
    op.add_column('picture_like', sa.Column('flickr_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True))
    ### end Alembic commands ###
