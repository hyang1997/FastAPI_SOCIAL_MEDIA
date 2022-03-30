"""create posts table

Revision ID: ac2e89c5d260
Revises: 
Create Date: 2022-03-29 22:51:48.320978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac2e89c5d260'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key = True))
    pass


def downgrade():
    op.drop_table("posts")
    pass
