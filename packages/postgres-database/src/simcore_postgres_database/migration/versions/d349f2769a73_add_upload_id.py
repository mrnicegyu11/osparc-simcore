"""add upload_id

Revision ID: d349f2769a73
Revises: 2cc556e5c52d
Create Date: 2022-06-30 15:04:55.073244+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d349f2769a73"
down_revision = "2cc556e5c52d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("file_meta_data", sa.Column("upload_id", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("file_meta_data", "upload_id")
    # ### end Alembic commands ###
