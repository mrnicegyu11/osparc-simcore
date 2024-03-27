"""added_user_prefereces_tables

Revision ID: f53806935760
Revises: c4245e9e0f72
Create Date: 2023-09-08 13:41:07.591760+00:00

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f53806935760"
down_revision = "c4245e9e0f72"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_preferences_frontend",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("product_name", sa.String(), nullable=False),
        sa.Column("preference_name", sa.String(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_name"],
            ["products.name"],
            name="fk_user_preferences_frontend_name_products",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_user_preferences_frontend_id_users",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "user_id",
            "product_name",
            "preference_name",
            name="user_preferences_frontend_pk",
        ),
    )
    op.create_table(
        "user_preferences_user_service",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("product_name", sa.String(), nullable=False),
        sa.Column("preference_name", sa.String(), nullable=False),
        sa.Column("payload", sa.LargeBinary(), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_name"],
            ["products.name"],
            name="fk_user_preferences_user_service_name_products",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_user_preferences_user_service_id_users",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "user_id",
            "product_name",
            "preference_name",
            name="user_preferences_user_service_pk",
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_preferences_user_service")
    op.drop_table("user_preferences_frontend")
    # ### end Alembic commands ###
