"""empty message

Revision ID: f9f4ba4e9b4b
Revises: 
Create Date: 2019-10-12 13:08:44.553226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9f4ba4e9b4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('finger_touch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stb_id', sa.String(), nullable=True),
    sa.Column('fingerprint_id', sa.String(), nullable=True),
    sa.Column('timestamp', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('remote_press',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.String(), nullable=True),
    sa.Column('stb_id', sa.String(), nullable=True),
    sa.Column('button_pressed', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stb',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stb_id', sa.String(), nullable=True),
    sa.Column('active_status', sa.String(), nullable=True),
    sa.Column('lat', sa.String(), nullable=True),
    sa.Column('lon', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stb_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('fingerprint_id', sa.String(), nullable=True),
    sa.Column('stb_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stb_user')
    op.drop_table('stb')
    op.drop_table('remote_press')
    op.drop_table('finger_touch')
    # ### end Alembic commands ###