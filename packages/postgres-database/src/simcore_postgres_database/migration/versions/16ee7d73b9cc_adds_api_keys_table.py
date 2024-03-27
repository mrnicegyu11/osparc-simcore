"""Adds api_keys table

Revision ID: 16ee7d73b9cc
Revises: f3555bb4bc34
Create Date: 2020-04-28 08:11:42.785688+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "16ee7d73b9cc"
down_revision = "f3555bb4bc34"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "api_keys",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=False),
        sa.Column("api_secret", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "display_name", "user_id", name="display_name_userid_uniqueness"
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("api_keys")
    # ### end Alembic commands ###
