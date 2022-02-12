"""Create Posts Table

Revision ID: 5cd04713b296
Revises: 
Create Date: 2022-02-12 00:07:48.609207

"""
from tokenize import String
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cd04713b296'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title',sa.String(),nullable=False))


def downgrade():
    op.drop_table('posts')
