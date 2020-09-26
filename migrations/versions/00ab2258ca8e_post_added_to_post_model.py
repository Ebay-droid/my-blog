""" post added to Post model

Revision ID: 00ab2258ca8e
Revises: 93f9b883d794
Create Date: 2020-09-26 20:49:21.213205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00ab2258ca8e'
down_revision = '93f9b883d794'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('post', sa.String(length=255), nullable=True))
    op.drop_column('posts', 'blog')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('blog', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('posts', 'post')
    # ### end Alembic commands ###