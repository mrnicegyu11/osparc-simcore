"""Adds is_guest_allowed column

Revision ID: f73fb7d7b9b8
Revises: be29dbed0cce
Create Date: 2021-04-19 17:40:09.383350+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f73fb7d7b9b8"
down_revision = "be29dbed0cce"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "services_consume_filetypes",
        sa.Column(
            "is_guest_allowed",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("services_consume_filetypes", "is_guest_allowed")
    # ### end Alembic commands ###
