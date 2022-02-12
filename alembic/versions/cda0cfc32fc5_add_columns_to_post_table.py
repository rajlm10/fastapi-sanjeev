"""Add columns to Post Table

Revision ID: cda0cfc32fc5
Revises: 5cd04713b296
Create Date: 2022-02-12 00:13:51.611302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cda0cfc32fc5'
down_revision = '5cd04713b296'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade():
    op.drop_column('posts','content')
