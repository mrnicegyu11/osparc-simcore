"""rm created_ip and add DELETED user status

Revision ID: be0dece4e67c
Revises: 76d106b243c3
Create Date: 2023-10-23 17:36:46.349925+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "be0dece4e67c"
down_revision = "76d106b243c3"
branch_labels = None
depends_on = None

column_name = "status"
enum_typename = "userstatus"
new_value = "DELETED"


def upgrade():
    # SEE https://medium.com/makimo-tech-blog/upgrading-postgresqls-enum-type-with-sqlalchemy-using-alembic-migration-881af1e30abe

    with op.get_context().autocommit_block():
        op.execute(f"ALTER TYPE {enum_typename} ADD VALUE '{new_value}'")

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "created_ip")
    # ### end Alembic commands ###


def downgrade():

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("created_ip", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###

    # NOTE: Downgrade new updates requires re-building the entire enum!
    op.execute(f"ALTER TYPE {enum_typename} RENAME TO {enum_typename}_old")
    op.execute(
        f"CREATE TYPE {enum_typename} AS ENUM('CONFIRMATION_PENDING', 'ACTIVE', 'BANNED')"
    )
    op.execute(
        f"ALTER TABLE users ALTER COLUMN {column_name} TYPE {enum_typename} USING "
        f"{column_name}::text::{enum_typename}"
    )
    op.execute(f"DROP TYPE {enum_typename}_old")
