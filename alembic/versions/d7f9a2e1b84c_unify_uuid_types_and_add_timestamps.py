"""unify uuid types and add timestamps

Revision ID: d7f9a2e1b84c
Revises: e534e52da7ec
Create Date: 2026-06-24 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "d7f9a2e1b84c"
down_revision: Union[str, Sequence[str], None] = "e534e52da7ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop FK constraints before altering column types
    op.drop_constraint("users_organization_id_fkey", "users", type_="foreignkey")
    op.drop_constraint("projects_organization_id_fkey", "projects", type_="foreignkey")

    # Convert String PKs to UUID using USING cast (Alembic can't auto-emit this)
    op.execute("ALTER TABLE organizations ALTER COLUMN id TYPE UUID USING id::uuid")
    op.execute("ALTER TABLE projects ALTER COLUMN id TYPE UUID USING id::uuid")

    # Convert FK columns to UUID
    op.execute(
        "ALTER TABLE users ALTER COLUMN organization_id TYPE UUID USING organization_id::uuid"
    )
    op.execute(
        "ALTER TABLE projects ALTER COLUMN organization_id TYPE UUID USING organization_id::uuid"
    )

    # Re-add FK constraints
    op.create_foreign_key(
        "users_organization_id_fkey",
        "users",
        "organizations",
        ["organization_id"],
        ["id"],
    )
    op.create_foreign_key(
        "projects_organization_id_fkey",
        "projects",
        "organizations",
        ["organization_id"],
        ["id"],
    )

    # Add timestamps to all three tables
    op.add_column(
        "organizations",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "organizations",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "projects",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "projects",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    # Drop timestamps
    for table in ("organizations", "users", "projects"):
        op.drop_column(table, "updated_at")
        op.drop_column(table, "created_at")

    # Drop FK constraints
    op.drop_constraint("users_organization_id_fkey", "users", type_="foreignkey")
    op.drop_constraint("projects_organization_id_fkey", "projects", type_="foreignkey")

    # Revert UUID columns back to VARCHAR
    op.execute("ALTER TABLE organizations ALTER COLUMN id TYPE VARCHAR USING id::text")
    op.execute("ALTER TABLE projects ALTER COLUMN id TYPE VARCHAR USING id::text")
    op.execute(
        "ALTER TABLE users ALTER COLUMN organization_id TYPE VARCHAR USING organization_id::text"
    )
    op.execute(
        "ALTER TABLE projects ALTER COLUMN organization_id TYPE VARCHAR USING organization_id::text"
    )

    # Re-add FK constraints
    op.create_foreign_key(
        "users_organization_id_fkey",
        "users",
        "organizations",
        ["organization_id"],
        ["id"],
    )
    op.create_foreign_key(
        "projects_organization_id_fkey",
        "projects",
        "organizations",
        ["organization_id"],
        ["id"],
    )
