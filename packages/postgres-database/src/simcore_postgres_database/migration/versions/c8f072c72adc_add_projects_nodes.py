"""add projects nodes

Revision ID: c8f072c72adc
Revises: e0a2557dec27
Create Date: 2023-06-13 16:26:26.920891+00:00

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c8f072c72adc"
down_revision = "e0a2557dec27"
branch_labels = None
depends_on = None

# TRIGGERS -----------------
drop_projects_to_projects_nodes_deleted_trigger = sa.DDL(
    "DROP TRIGGER IF EXISTS entry_deleted on projects;"
)
projects_to_projects_nodes_deleted_trigger = sa.DDL(
    """
DROP TRIGGER IF EXISTS entry_deleted on projects;
CREATE TRIGGER entry_deleted
AFTER DELETE ON projects
FOR EACH ROW
EXECUTE FUNCTION delete_orphaned_project_nodes();
    """
)
drop_modified_timestamp_trigger = sa.DDL(
    "DROP TRIGGER IF EXISTS trigger_auto_update on projects_nodes;"
    "DROP TRIGGER IF EXISTS trigger_auto_update on projects_to_projects_nodes;"
)
modified_timestamp_trigger = sa.DDL(
    """
DROP TRIGGER IF EXISTS trigger_auto_update on projects_nodes;
CREATE TRIGGER trigger_auto_update
BEFORE INSERT OR UPDATE ON projects_nodes
FOR EACH ROW EXECUTE PROCEDURE projects_nodes_auto_update_modified();
DROP TRIGGER IF EXISTS trigger_auto_update on projects_to_projects_nodes;
CREATE TRIGGER trigger_auto_update
BEFORE INSERT OR UPDATE ON projects_to_projects_nodes
FOR EACH ROW EXECUTE PROCEDURE projects_to_projects_nodes_auto_update_modified();
    """
)

# PROCEDURES -------------------
drop_delete_orphaned_project_nodes_procedure = sa.DDL(
    "DROP FUNCTION delete_orphaned_project_nodes();"
)
delete_orphaned_project_nodes_procedure = sa.DDL(
    """
CREATE OR REPLACE FUNCTION delete_orphaned_project_nodes()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM projects_nodes
    WHERE NOT EXISTS (
        SELECT 1 FROM projects_to_projects_nodes
        WHERE projects_to_projects_nodes.node_id = projects_nodes.node_id
    );
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
    """
)
drop_update_modified_timestamp_procedure = sa.DDL(
    "DROP FUNCTION projects_nodes_auto_update_modified();"
    "DROP FUNCTION projects_to_projects_nodes_auto_update_modified();"
)
update_modified_timestamp_procedure = sa.DDL(
    """
CREATE OR REPLACE FUNCTION projects_nodes_auto_update_modified()
RETURNS TRIGGER AS $$
BEGIN
  NEW.modified := current_timestamp;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION projects_to_projects_nodes_auto_update_modified()
RETURNS TRIGGER AS $$
BEGIN
  NEW.modified := current_timestamp;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
    """
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "projects_nodes",
        sa.Column("node_id", sa.String(), nullable=False),
        sa.Column(
            "required_resources",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "modified",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("node_id"),
    )
    op.create_table(
        "projects_to_projects_nodes",
        sa.Column("project_uuid", sa.String(), nullable=True),
        sa.Column("node_id", sa.String(), nullable=True),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "modified",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["node_id"],
            ["projects_nodes.node_id"],
            name="fk_projects_to_projects_nodes_to_projects_nodes_node_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_uuid"],
            ["projects.uuid"],
            name="fk_projects_to_projects_nodes_to_projects_uuid",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("project_uuid", "node_id"),
    )
    # ### end Alembic commands ###

    # custom
    op.execute(delete_orphaned_project_nodes_procedure)
    op.execute(projects_to_projects_nodes_deleted_trigger)
    op.execute(update_modified_timestamp_procedure)
    op.execute(modified_timestamp_trigger)


def downgrade():
    # custom
    op.execute(drop_projects_to_projects_nodes_deleted_trigger)
    op.execute(drop_delete_orphaned_project_nodes_procedure)
    op.execute(drop_modified_timestamp_trigger)
    op.execute(drop_update_modified_timestamp_procedure)

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("projects_to_projects_nodes")
    op.drop_table("projects_nodes")
    # ### end Alembic commands ###
