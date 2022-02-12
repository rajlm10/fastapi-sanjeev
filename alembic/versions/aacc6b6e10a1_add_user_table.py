"""Add user table

Revision ID: aacc6b6e10a1
Revises: cda0cfc32fc5
Create Date: 2022-02-12 00:16:39.500508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aacc6b6e10a1'
down_revision = 'cda0cfc32fc5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
                sa.Column('email', sa.String(), nullable=False,unique=True),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False)

                )


def downgrade():
    op.drop_table('users')
