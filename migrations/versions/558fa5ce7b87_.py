"""empty message

Revision ID: 558fa5ce7b87
Revises: 479beb9cc90d
Create Date: 2014-11-13 15:53:02.246353

"""

# revision identifiers, used by Alembic.
revision = '558fa5ce7b87'
down_revision = '479beb9cc90d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('place_picture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('thumbnail_url', sa.Text(), nullable=True),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.Column('like_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_place_picture_like_count'), 'place_picture', ['like_count'], unique=False)
    op.create_table('picture_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('liked_time', sa.DateTime(), nullable=True),
    sa.Column('place_picture_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_picture_id'], ['place_picture.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'place_picture_id', name='unq_picture_like_uid_pid')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('picture_like')
    op.drop_index(op.f('ix_place_picture_like_count'), table_name='place_picture')
    op.drop_table('place_picture')
    ### end Alembic commands ###
