"""create adzuna_jobs table

Revision ID: 99f88cf077cf
Revises: 
Create Date: 2026-08-03 07:15:19.932270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99f88cf077cf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE adzuna_jobs (
            id                  BIGINT PRIMARY KEY,
            title               TEXT NOT NULL,
            description         TEXT,
            company_name        TEXT,
            salary_min          NUMERIC(10,2),
            salary_max          NUMERIC(10,2),
            salary_is_predicted BOOLEAN,
            contract_type       TEXT,
            contract_time       TEXT,
            category_label      TEXT,
            latitude            NUMERIC(9,6),
            longitude           NUMERIC(9,6),
            location_display    TEXT,
            location_area       TEXT,
            redirect_url        TEXT,
            adref               TEXT,
            is_active           BOOLEAN DEFAULT TRUE,
            created             TIMESTAMPTZ,
            last_seen_at        TIMESTAMPTZ DEFAULT now(),
            inserted_at         TIMESTAMPTZ DEFAULT now()
        );
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS adzuna_jobs;")
