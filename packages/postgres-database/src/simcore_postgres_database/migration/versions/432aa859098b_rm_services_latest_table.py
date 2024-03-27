"""rm services_latest table

Revision ID: 432aa859098b
Revises: 9b97b12cfe47
Create Date: 2023-04-03 16:58:44.438678+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "432aa859098b"
down_revision = "9b97b12cfe47"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("services_latest")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "services_latest",
        sa.Column("key", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("version", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["key", "version"],
            ["services_meta_data.key", "services_meta_data.version"],
            name="services_latest_key_version_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("key", name="services_latest_pk"),
    )
    # ### end Alembic commands ###
