"""create posts table

Revision ID: 4351af5c8de2
Revises: 
Create Date: 2022-02-25 14:02:42.391573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4351af5c8de2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # op.create_table('posts', sa.column('id', sa.Integer(), nullable=False, primary_key=True), sa.column(
    #     'title', sa.String(), nullable=False), sa.column('content', sa.Text(), nullable=False), sa.column(
    #         'published', sa.Boolean(), nullable=False), sa.column('owner_id', sa.Integer(), nullable=False), sa.column(
    #             'created_at', sa.DateTime(), nullable=False), sa.column('updated_at', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'), sa.ForeignKeyConstraint(
    #                 ['owner_id'], ['users.id'], ), sa.UniqueConstraint('title'))
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False), sa.Column(
        'content', sa.String(), nullable=False), sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'), sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade():
    op.drop_table('posts')
