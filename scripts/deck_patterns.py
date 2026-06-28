"""Backwards-compatibility shim — deck_patterns was renamed to block_builder in v1.3.0."""
from block_builder import *  # noqa: F401, F403
from block_builder import (  # noqa: F401
    dark_tech_theme,
    text, rich_text, shape, line, image, diagram, chart, table,
    card, title_chip, portrait_card, kpi_card, grid,
    process_flow, comparison_columns,
    slide, section, deck,
)
