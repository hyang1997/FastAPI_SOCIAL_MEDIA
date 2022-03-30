"""add content column to table

Revision ID: 7a192f64e573
Revises: ac2e89c5d260
Create Date: 2022-03-29 22:58:16.604348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a192f64e573'
down_revision = 'ac2e89c5d260'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
