"""removed project-snapshots table

Revision ID: a1b757834a8a
Revises: e1227c539ff4
Create Date: 2021-10-01 13:18:57.108487+00:00

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a1b757834a8a"
down_revision = "e1227c539ff4"
branch_labels = None
depends_on = None


def upgrade():
    # NOTE: no need to maintain backwards compatibility
    # This table was never released
    op.drop_table("projects_snapshots")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "projects_snapshots",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("parent_uuid", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("project_uuid", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("deleted", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_uuid"],
            ["projects.uuid"],
            name="fk_snapshots_parent_uuid_projects",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_uuid"],
            ["projects.uuid"],
            name="fk_snapshots_project_uuid_projects",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="projects_snapshots_pkey"),
        sa.UniqueConstraint(
            "parent_uuid", "created_at", name="snapshot_from_project_uniqueness"
        ),
        sa.UniqueConstraint("project_uuid", name="projects_snapshots_project_uuid_key"),
    )
    # ### end Alembic commands ###
