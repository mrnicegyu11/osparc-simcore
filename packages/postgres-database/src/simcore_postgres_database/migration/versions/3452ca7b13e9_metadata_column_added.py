"""metadata column added

Revision ID: 3452ca7b13e9
Revises: a23183ac1742
Create Date: 2020-12-05 18:08:12.347930+00:00

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3452ca7b13e9"
down_revision = "a23183ac1742"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "services_meta_data",
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("services_meta_data", "metadata")
    # ### end Alembic commands ###
