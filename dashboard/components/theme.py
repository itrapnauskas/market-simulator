"""
Custom theme configuration for Market Manipulation Lab dashboard.
Professional color scheme and styling constants.
"""

import streamlit as st

# Color Palette - Professional Dark Theme
COLORS = {
    # Primary colors
    "primary": "#00D4FF",  # Cyan Blue
    "secondary": "#FF6B6B",  # Coral Red
    "accent": "#4ECDC4",  # Teal
    "warning": "#FFD93D",  # Yellow
    "success": "#6BCB77",  # Green
    "danger": "#FF6B6B",  # Red

    # Chart colors
    "price": "#00D4FF",
    "volume": "#4ECDC4",
    "manipulation": "#FF6B6B",
    "buy_orders": "#6BCB77",
    "sell_orders": "#FF6B6B",

    # Background colors
    "bg_dark": "#0E1117",
    "bg_secondary": "#1E2530",
    "bg_card": "#262B38",

    # Text colors
    "text_primary": "#FAFAFA",
    "text_secondary": "#B3B3B3",
    "text_muted": "#808080",
}

# Chart Templates
PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": COLORS["bg_dark"],
        "plot_bgcolor": COLORS["bg_secondary"],
        "font": {"color": COLORS["text_primary"], "family": "Inter, sans-serif"},
        "xaxis": {
            "gridcolor": "#2E3440",
            "zerolinecolor": "#2E3440",
        },
        "yaxis": {
            "gridcolor": "#2E3440",
            "zerolinecolor": "#2E3440",
        },
        "colorway": [
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["accent"],
            COLORS["success"],
            COLORS["warning"],
        ],
    }
}


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit dashboard."""
    st.markdown(
        f"""
        <style>
        /* Main app styling */
        .stApp {{
            background-color: {COLORS["bg_dark"]};
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {COLORS["bg_secondary"]};
        }}

        /* Card styling */
        .card {{
            background-color: {COLORS["bg_card"]};
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }}

        /* Metric cards */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 700;
            color: {COLORS["primary"]};
        }}

        [data-testid="stMetricDelta"] {{
            font-size: 1rem;
        }}

        /* Headers */
        h1 {{
            color: {COLORS["primary"]};
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        h2 {{
            color: {COLORS["text_primary"]};
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid {COLORS["primary"]};
            padding-bottom: 0.5rem;
        }}

        h3 {{
            color: {COLORS["text_secondary"]};
            font-weight: 600;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {COLORS["primary"]};
            color: {COLORS["bg_dark"]};
            font-weight: 600;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 2rem;
            transition: all 0.3s ease;
        }}

        .stButton > button:hover {{
            background-color: {COLORS["accent"]};
            box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}

        .stTabs [data-baseweb="tab"] {{
            background-color: {COLORS["bg_card"]};
            border-radius: 6px 6px 0 0;
            padding: 12px 24px;
            color: {COLORS["text_secondary"]};
        }}

        .stTabs [aria-selected="true"] {{
            background-color: {COLORS["primary"]};
            color: {COLORS["bg_dark"]};
        }}

        /* Tooltips */
        .tooltip {{
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted {COLORS["text_muted"]};
            cursor: help;
        }}

        /* Info boxes */
        .info-box {{
            background-color: {COLORS["bg_card"]};
            border-left: 4px solid {COLORS["primary"]};
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }}

        .warning-box {{
            background-color: {COLORS["bg_card"]};
            border-left: 4px solid {COLORS["warning"]};
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }}

        /* Loading animation */
        .loading {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}

        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: {COLORS["bg_dark"]};
        }}

        ::-webkit-scrollbar-thumb {{
            background: {COLORS["primary"]};
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS["accent"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_chart_config():
    """Return default Plotly chart configuration."""
    return {
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        "toImageButtonOptions": {
            "format": "png",
            "filename": "market_lab_chart",
            "height": 1080,
            "width": 1920,
            "scale": 2,
        },
    }


__all__ = ["COLORS", "PLOTLY_TEMPLATE", "apply_custom_css", "get_chart_config"]
