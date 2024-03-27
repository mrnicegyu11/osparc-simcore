"""rm two_factor_enabled col in users

Revision ID: 0ad000429e3d
Revises: 215b2cac1dbc
Create Date: 2023-11-21 18:30:35.437738+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0ad000429e3d"
down_revision = "215b2cac1dbc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "two_factor_enabled")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "two_factor_enabled",
            sa.BOOLEAN(),
            server_default=sa.text("true"),
            autoincrement=False,
            nullable=False,
        ),
    )
    # ### end Alembic commands ###
