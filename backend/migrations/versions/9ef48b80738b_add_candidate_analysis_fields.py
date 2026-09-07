from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9ef48b80738b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "candidates",
        sa.Column(
            "ai_signals",
            sa.Text(),
            nullable=False,
            server_default="[]",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "ai_contributions",
            sa.Text(),
            nullable=False,
            server_default="[]",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "bot_reasons",
            sa.Text(),
            nullable=False,
            server_default="[]",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "bot_reason_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "rate_limited",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "sentence_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "average_sentence_length",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "burstiness",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "bigram_density",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "trigram_density",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "candidates",
        sa.Column(
            "vocabulary_diversity",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "candidates",
        "vocabulary_diversity",
    )

    op.drop_column(
        "candidates",
        "trigram_density",
    )

    op.drop_column(
        "candidates",
        "bigram_density",
    )

    op.drop_column(
        "candidates",
        "burstiness",
    )

    op.drop_column(
        "candidates",
        "average_sentence_length",
    )

    op.drop_column(
        "candidates",
        "sentence_count",
    )

    op.drop_column(
        "candidates",
        "rate_limited",
    )

    op.drop_column(
        "candidates",
        "bot_reason_count",
    )

    op.drop_column(
        "candidates",
        "bot_reasons",
    )

    op.drop_column(
        "candidates",
        "ai_contributions",
    )

    op.drop_column(
        "candidates",
        "ai_signals",
    )