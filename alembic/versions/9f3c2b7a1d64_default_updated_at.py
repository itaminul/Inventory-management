"""Set a database default for users.updated_at."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f3c2b7a1d64"
down_revision: Union[str, Sequence[str], None] = "cc69f006d433"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "updated_at",
        server_default=sa.text("now()"),
    )


def downgrade() -> None:
    op.alter_column("users", "updated_at", server_default=None)
