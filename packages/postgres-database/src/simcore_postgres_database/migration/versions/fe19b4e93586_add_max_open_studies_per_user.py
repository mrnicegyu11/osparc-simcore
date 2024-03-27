"""add max_open_studies_per_user

Revision ID: fe19b4e93586
Revises: 61394494e942
Create Date: 2022-11-28 14:50:47.411150+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "fe19b4e93586"
down_revision = "61394494e942"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "products", sa.Column("max_open_studies_per_user", sa.Integer(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("products", "max_open_studies_per_user")
    # ### end Alembic commands ###
