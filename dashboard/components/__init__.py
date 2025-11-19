"""
Dashboard components for Market Manipulation Lab.
Modular UI components for building the interactive dashboard.
"""

from .theme import COLORS, PLOTLY_TEMPLATE, apply_custom_css, get_chart_config
from .charts import (
    create_candlestick_chart,
    create_price_volume_chart,
    create_order_book_chart,
    create_manipulation_heatmap,
    create_wealth_comparison_chart,
    create_comparison_chart,
    create_anomaly_timeline,
    create_distribution_chart,
)
from .config import (
    SimulationConfig,
    PRESETS,
    render_config_panel,
    render_save_load_ui,
)
from .utils import (
    render_export_section,
    render_metrics_cards,
    render_comparison_manager,
    render_data_table,
)
from .layout import (
    render_header,
    render_footer,
    render_help_sidebar,
    render_tutorial_mode,
    render_welcome_screen,
    render_empty_state,
    render_error_message,
)

__all__ = [
    # Theme
    "COLORS",
    "PLOTLY_TEMPLATE",
    "apply_custom_css",
    "get_chart_config",
    # Charts
    "create_candlestick_chart",
    "create_price_volume_chart",
    "create_order_book_chart",
    "create_manipulation_heatmap",
    "create_wealth_comparison_chart",
    "create_comparison_chart",
    "create_anomaly_timeline",
    "create_distribution_chart",
    # Config
    "SimulationConfig",
    "PRESETS",
    "render_config_panel",
    "render_save_load_ui",
    # Utils
    "render_export_section",
    "render_metrics_cards",
    "render_comparison_manager",
    "render_data_table",
    # Layout
    "render_header",
    "render_footer",
    "render_help_sidebar",
    "render_tutorial_mode",
    "render_welcome_screen",
    "render_empty_state",
    "render_error_message",
]
