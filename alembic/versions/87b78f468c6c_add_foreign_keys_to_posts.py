"""add foreign keys to posts

Revision ID: 87b78f468c6c
Revises: b58926bbcae6
Create Date: 2022-02-26 11:21:06.921849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87b78f468c6c'
down_revision = 'b58926bbcae6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
