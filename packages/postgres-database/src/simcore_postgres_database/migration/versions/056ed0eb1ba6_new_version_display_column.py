"""new version_display column

Revision ID: 056ed0eb1ba6
Revises: d0e56c2d0a0d
Create Date: 2024-07-18 19:06:50.142232+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "056ed0eb1ba6"
down_revision = "d0e56c2d0a0d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "services_meta_data", sa.Column("version_display", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("services_meta_data", "version_display")
    # ### end Alembic commands ###
