"""add user_table

Revision ID: f7f2f5633371
Revises: 7a192f64e573
Create Date: 2022-03-29 23:02:50.401401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7f2f5633371'
down_revision = '7a192f64e573'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                            server_default=sa.text('now()') ,nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
