"""add foreignkey to post table

Revision ID: 2d7d5d59eec6
Revises: f7f2f5633371
Create Date: 2022-03-30 11:37:40.519787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d7d5d59eec6'
down_revision = 'f7f2f5633371'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users',
                            local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")

    pass


def downgrade():
    op.drop_constraint("post_users_fk",table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
