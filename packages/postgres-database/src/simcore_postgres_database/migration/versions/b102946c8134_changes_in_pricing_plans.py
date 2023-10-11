"""changes in pricing plans

Revision ID: b102946c8134
Revises: 6e9f34338072
Create Date: 2023-10-01 12:50:08.671566+00:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b102946c8134"
down_revision = "6e9f34338072"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # CREATE RESOURCE_TRACKER_PRICING_UNIT_COSTS
    op.create_table(
        "resource_tracker_pricing_unit_costs",
        sa.Column("pricing_unit_cost_id", sa.BigInteger(), nullable=False),
        sa.Column("pricing_plan_id", sa.BigInteger(), nullable=False),
        sa.Column("pricing_plan_key", sa.String(), nullable=False),
        sa.Column("pricing_unit_id", sa.BigInteger(), nullable=False),
        sa.Column("pricing_unit_name", sa.String(), nullable=False),
        sa.Column("cost_per_unit", sa.Numeric(scale=2), nullable=False),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "specific_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column(
            "modified",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("pricing_unit_cost_id"),
    )
    op.create_index(
        op.f("ix_resource_tracker_pricing_unit_costs_pricing_plan_id"),
        "resource_tracker_pricing_unit_costs",
        ["pricing_plan_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_resource_tracker_pricing_unit_costs_pricing_unit_id"),
        "resource_tracker_pricing_unit_costs",
        ["pricing_unit_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_resource_tracker_pricing_unit_costs_valid_to"),
        "resource_tracker_pricing_unit_costs",
        ["valid_to"],
        unique=False,
    )

    # CREATE RESOURCE_TRACKER_PRICING_UNITS
    op.create_table(
        "resource_tracker_pricing_units",
        sa.Column("pricing_unit_id", sa.BigInteger(), nullable=False),
        sa.Column("pricing_plan_id", sa.BigInteger(), nullable=False),
        sa.Column("unit_name", sa.String(), nullable=False),
        sa.Column("default", sa.Boolean(), nullable=False),
        sa.Column(
            "specific_info", postgresql.JSONB(astext_type=sa.Text()), nullable=False
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
        sa.ForeignKeyConstraint(
            ["pricing_plan_id"],
            ["resource_tracker_pricing_plans.pricing_plan_id"],
            name="fk_resource_tracker_pricing_units_pricing_plan_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("pricing_unit_id"),
        sa.UniqueConstraint(
            "pricing_plan_id", "unit_name", name="pricing_plan_and_unit_constrain_key"
        ),
    )
    op.create_index(
        op.f("ix_resource_tracker_pricing_units_pricing_plan_id"),
        "resource_tracker_pricing_units",
        ["pricing_plan_id"],
        unique=False,
    )

    # DROP RESOURCE_TRACKER_PRICING_DETAILS
    op.drop_index(
        "ix_resource_tracker_pricing_details_pricing_plan_id",
        table_name="resource_tracker_pricing_details",
    )
    op.drop_index(
        "ix_resource_tracker_pricing_details_valid_to",
        table_name="resource_tracker_pricing_details",
    )
    op.drop_table("resource_tracker_pricing_details")

    # MODIFY RESOURCE_TRACKER_CREDIT_TRANSACTIONS
    op.add_column(
        "resource_tracker_credit_transactions",
        sa.Column("pricing_unit_id", sa.BigInteger(), nullable=True),
    )
    op.add_column(
        "resource_tracker_credit_transactions",
        sa.Column("pricing_unit_cost_id", sa.BigInteger(), nullable=True),
    )
    op.drop_column("resource_tracker_credit_transactions", "pricing_detail_id")

    # MODIFY RESOURCE_TRACKER_PRICING_PLAN_TO_SERVICE
    op.add_column(
        "resource_tracker_pricing_plan_to_service",
        sa.Column("service_default_plan", sa.Boolean(), nullable=False),
    )
    op.drop_column("resource_tracker_pricing_plan_to_service", "product")

    # MODIFY RESOURCE_TRACKER_PRICING_PLANS
    op.add_column(
        "resource_tracker_pricing_plans",
        sa.Column("display_name", sa.String(), nullable=False),
    )
    op.add_column(
        "resource_tracker_pricing_plans",
        sa.Column("pricing_plan_key", sa.String(), nullable=False),
    )
    op.create_unique_constraint(
        "pricing_plans_pricing_plan_key",
        "resource_tracker_pricing_plans",
        ["product_name", "pricing_plan_key"],
    )
    op.drop_column("resource_tracker_pricing_plans", "name")

    # MODIFY RESOURCE_TRACKER_SERVICE_RUNS
    op.add_column(
        "resource_tracker_service_runs",
        sa.Column("pricing_unit_id", sa.BigInteger(), nullable=True),
    )
    op.add_column(
        "resource_tracker_service_runs",
        sa.Column("pricing_unit_cost_id", sa.BigInteger(), nullable=True),
    )
    op.add_column(
        "resource_tracker_service_runs",
        sa.Column("pricing_unit_cost", sa.Numeric(scale=2), nullable=True),
    )
    op.drop_column("resource_tracker_service_runs", "pricing_detail_id")
    op.drop_column("resource_tracker_service_runs", "pricing_detail_cost_per_unit")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "resource_tracker_service_runs",
        sa.Column(
            "pricing_detail_cost_per_unit",
            sa.NUMERIC(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "resource_tracker_service_runs",
        sa.Column("pricing_detail_id", sa.BIGINT(), autoincrement=False, nullable=True),
    )
    op.drop_column("resource_tracker_service_runs", "pricing_unit_cost")
    op.drop_column("resource_tracker_service_runs", "pricing_unit_cost_id")
    op.drop_column("resource_tracker_service_runs", "pricing_unit_id")
    op.add_column(
        "resource_tracker_pricing_plans",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(
        "pricing_plans_pricing_plan_key",
        "resource_tracker_pricing_plans",
        type_="unique",
    )
    op.drop_column("resource_tracker_pricing_plans", "pricing_plan_key")
    op.drop_column("resource_tracker_pricing_plans", "display_name")
    op.add_column(
        "resource_tracker_pricing_plan_to_service",
        sa.Column("product", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("resource_tracker_pricing_plan_to_service", "service_default_plan")
    op.add_column(
        "resource_tracker_credit_transactions",
        sa.Column("pricing_detail_id", sa.BIGINT(), autoincrement=False, nullable=True),
    )
    op.drop_column("resource_tracker_credit_transactions", "pricing_unit_cost_id")
    op.drop_column("resource_tracker_credit_transactions", "pricing_unit_id")
    op.create_table(
        "resource_tracker_pricing_details",
        sa.Column("pricing_detail_id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("pricing_plan_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("unit_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "valid_from",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "valid_to",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "specific_info",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "modified",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("simcore_default", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("cost_per_unit", sa.NUMERIC(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["pricing_plan_id"],
            ["resource_tracker_pricing_plans.pricing_plan_id"],
            name="fk_resource_tracker_pricing_details_pricing_plan_id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "pricing_detail_id", name="resource_tracker_pricing_details_pkey"
        ),
    )
    op.create_index(
        "ix_resource_tracker_pricing_details_valid_to",
        "resource_tracker_pricing_details",
        ["valid_to"],
        unique=False,
    )
    op.create_index(
        "ix_resource_tracker_pricing_details_pricing_plan_id",
        "resource_tracker_pricing_details",
        ["pricing_plan_id"],
        unique=False,
    )
    op.drop_index(
        op.f("ix_resource_tracker_pricing_units_pricing_plan_id"),
        table_name="resource_tracker_pricing_units",
    )
    op.drop_table("resource_tracker_pricing_units")
    op.drop_index(
        op.f("ix_resource_tracker_pricing_unit_costs_valid_to"),
        table_name="resource_tracker_pricing_unit_costs",
    )
    op.drop_index(
        op.f("ix_resource_tracker_pricing_unit_costs_pricing_unit_id"),
        table_name="resource_tracker_pricing_unit_costs",
    )
    op.drop_index(
        op.f("ix_resource_tracker_pricing_unit_costs_pricing_plan_id"),
        table_name="resource_tracker_pricing_unit_costs",
    )
    op.drop_table("resource_tracker_pricing_unit_costs")
    # ### end Alembic commands ###