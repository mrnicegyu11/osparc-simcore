"""add licensed resources

Revision ID: 68777fdf9539
Revises: 061607911a22
Create Date: 2025-02-09 10:24:50.533653+00:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "68777fdf9539"
down_revision = "061607911a22"
branch_labels = None
depends_on = None


# Reuse the existing Enum type
licensed_resource_type = postgresql.ENUM(
    "VIP_MODEL", name="licensedresourcetype", create_type=False
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "licensed_resources",
        sa.Column(
            "licensed_resource_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("licensed_resource_name", sa.String(), nullable=False),
        sa.Column(
            "licensed_resource_type",
            licensed_resource_type,  # Reuse existing Enum instead of redefining it
            nullable=False,
        ),
        sa.Column(
            "licensed_resource_data",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
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
        sa.Column(
            "trashed",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="The date and time when the licensed_resources was marked as trashed. Null if the licensed_resources has not been trashed [default].",
        ),
        sa.PrimaryKeyConstraint("licensed_resource_id"),
        sa.UniqueConstraint(
            "licensed_resource_name",
            "licensed_resource_type",
            name="uq_licensed_resource_name_type2",
        ),
    )
    # ### end Alembic commands ###

    # Migration of licensed resources from licensed_items table to new licensed_resources table
    op.execute(
        sa.DDL(
            """
    INSERT INTO licensed_resources (display_name, licensed_resource_name, licensed_resource_type, licensed_resource_data, created, modified)
    SELECT
        display_name,
        licensed_resource_name,
        licensed_resource_type,
        licensed_resource_data,
        CURRENT_TIMESTAMP as created,
        CURRENT_TIMESTAMP as modified
    FROM licensed_items
        """
        )
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("licensed_resources")
    # ### end Alembic commands ###
