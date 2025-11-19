"""
Utility functions for Market Manipulation Lab dashboard.
Includes data export, session management, and helper functions.
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime
from typing import List, Dict, Any, Optional
import base64


def export_to_csv(states) -> str:
    """
    Export simulation states to CSV format.

    Args:
        states: List of MarketState objects

    Returns:
        CSV string
    """
    data = []
    for state in states:
        row = {
            'day': state.day,
            'price': state.price,
            'volume': state.cleared_volume,
            'sentiment': state.sentiment_value,
        }

        # Add manipulation score if available
        if hasattr(state, 'manipulation_score') and state.manipulation_score is not None:
            row['manipulation_score'] = state.manipulation_score

        data.append(row)

    df = pd.DataFrame(data)
    return df.to_csv(index=False)


def export_to_json(states, config: Optional[Dict] = None) -> str:
    """
    Export simulation data to JSON format.

    Args:
        states: List of MarketState objects
        config: Optional configuration dict to include

    Returns:
        JSON string
    """
    data = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'n_days': len(states),
        },
        'states': []
    }

    if config:
        data['config'] = config

    for state in states:
        state_data = {
            'day': state.day,
            'price': state.price,
            'volume': state.cleared_volume,
            'sentiment': state.sentiment_value,
        }

        if hasattr(state, 'manipulation_score') and state.manipulation_score is not None:
            state_data['manipulation_score'] = state.manipulation_score

        # Include order curves if available
        if hasattr(state, 'order_curves') and state.order_curves:
            state_data['order_curves'] = {
                'price_grid': list(state.order_curves.price_grid),
                'buy_curve': list(state.order_curves.buy_curve),
                'sell_curve': list(state.order_curves.sell_curve),
            }

        data['states'].append(state_data)

    return json.dumps(data, indent=2)


def create_download_link(content: str, filename: str, mime_type: str = "text/plain") -> str:
    """
    Create a download link for content.

    Args:
        content: Content to download
        filename: Name of the file
        mime_type: MIME type of the file

    Returns:
        HTML download link
    """
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">Download {filename}</a>'
    return href


def render_export_section(states, config: Optional[Dict] = None):
    """
    Render export section with download buttons.

    Args:
        states: List of MarketState objects
        config: Optional configuration dict
    """
    st.markdown("### Export Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        # CSV export
        csv_data = export_to_csv(states)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"market_sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download simulation data as CSV"
        )

    with col2:
        # JSON export
        json_data = export_to_json(states, config)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"market_sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            help="Download complete simulation data as JSON"
        )

    with col3:
        # Configuration export
        if config:
            config_json = json.dumps(config, indent=2)
            st.download_button(
                label="Download Config",
                data=config_json,
                file_name=f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="Download simulation configuration"
            )


def calculate_metrics(states) -> Dict[str, Any]:
    """
    Calculate key metrics from simulation states.

    Args:
        states: List of MarketState objects

    Returns:
        Dictionary of calculated metrics
    """
    if not states:
        return {}

    prices = [s.price for s in states]
    volumes = [s.cleared_volume for s in states]

    start_price = prices[0]
    end_price = prices[-1]
    max_price = max(prices)
    min_price = min(prices)

    metrics = {
        'n_days': len(states),
        'start_price': start_price,
        'end_price': end_price,
        'price_change_pct': ((end_price - start_price) / start_price) * 100,
        'max_price': max_price,
        'min_price': min_price,
        'price_range': max_price - min_price,
        'volatility_pct': ((max_price - min_price) / start_price) * 100,
        'avg_volume': sum(volumes) / len(volumes),
        'total_volume': sum(volumes),
        'max_volume': max(volumes),
        'min_volume': min(volumes),
    }

    # Add manipulation metrics if available
    scores = [getattr(s, 'manipulation_score', 0) or 0 for s in states]
    if any(scores):
        metrics['avg_manipulation_score'] = sum(scores) / len(scores)
        metrics['max_manipulation_score'] = max(scores)
        metrics['high_alert_days'] = sum(1 for s in scores if s > 2.0)  # Arbitrary threshold

    return metrics


def render_metrics_cards(states):
    """
    Render metric cards in a grid layout.

    Args:
        states: List of MarketState objects
    """
    metrics = calculate_metrics(states)

    if not metrics:
        st.warning("No data available for metrics")
        return

    # Row 1: Basic metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Days Simulated",
            metrics['n_days'],
            help="Total number of trading days"
        )

    with col2:
        st.metric(
            "Price Change",
            f"{metrics['price_change_pct']:.2f}%",
            delta=f"${metrics['end_price'] - metrics['start_price']:.2f}",
            help="Percentage change from start to end"
        )

    with col3:
        st.metric(
            "Avg Volume",
            f"{metrics['avg_volume']:,.0f}",
            help="Average daily trading volume"
        )

    with col4:
        st.metric(
            "Volatility Range",
            f"{metrics['volatility_pct']:.2f}%",
            help="Price range as percentage of starting price"
        )

    # Row 2: Additional metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Max Price",
            f"${metrics['max_price']:.2f}",
            help="Highest price reached"
        )

    with col2:
        st.metric(
            "Min Price",
            f"${metrics['min_price']:.2f}",
            help="Lowest price reached"
        )

    with col3:
        st.metric(
            "Total Volume",
            f"{metrics['total_volume']:,.0f}",
            help="Total shares traded"
        )

    with col4:
        if 'high_alert_days' in metrics:
            st.metric(
                "Alert Days",
                metrics['high_alert_days'],
                help="Days with high manipulation score"
            )
        else:
            st.metric(
                "Max Volume",
                f"{metrics['max_volume']:,.0f}",
                help="Maximum daily volume"
            )


def add_simulation_to_compare(name: str, states, config: Dict):
    """
    Add a simulation to the comparison list.

    Args:
        name: Name for this simulation
        states: MarketState list
        config: Configuration dict
    """
    if 'comparisons' not in st.session_state:
        st.session_state.comparisons = []

    # Check if name already exists
    existing_names = [sim['name'] for sim in st.session_state.comparisons]
    if name in existing_names:
        # Make name unique
        counter = 1
        while f"{name} ({counter})" in existing_names:
            counter += 1
        name = f"{name} ({counter})"

    st.session_state.comparisons.append({
        'name': name,
        'states': states,
        'config': config,
        'timestamp': datetime.now()
    })


def render_comparison_manager():
    """Render UI for managing simulation comparisons."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Comparison Mode")

    if 'comparisons' not in st.session_state:
        st.session_state.comparisons = []

    # Add current simulation to comparison
    if st.sidebar.button("Add to Compare", use_container_width=True):
        if 'states' in st.session_state and st.session_state.states:
            sim_name = st.sidebar.text_input(
                "Simulation Name",
                value=f"Sim {len(st.session_state.comparisons) + 1}",
                key="comparison_name"
            )
            add_simulation_to_compare(
                sim_name,
                st.session_state.states,
                st.session_state.get('current_config', {})
            )
            st.sidebar.success(f"Added '{sim_name}' to comparison")

    # Show current comparisons
    if st.session_state.comparisons:
        st.sidebar.markdown(f"**{len(st.session_state.comparisons)} simulations** in comparison")

        if st.sidebar.button("Clear All", use_container_width=True):
            st.session_state.comparisons = []
            st.experimental_rerun()


def create_summary_table(states) -> pd.DataFrame:
    """
    Create a summary DataFrame from states.

    Args:
        states: List of MarketState objects

    Returns:
        pandas DataFrame with summary statistics
    """
    data = {
        'Day': [s.day for s in states],
        'Price': [s.price for s in states],
        'Volume': [s.cleared_volume for s in states],
        'Sentiment': [s.sentiment_value for s in states],
    }

    # Add manipulation score if available
    if hasattr(states[0], 'manipulation_score'):
        data['Manipulation Score'] = [
            getattr(s, 'manipulation_score', 0) or 0 for s in states
        ]

    return pd.DataFrame(data)


def render_data_table(states, max_rows: int = 100):
    """
    Render interactive data table.

    Args:
        states: List of MarketState objects
        max_rows: Maximum rows to display
    """
    df = create_summary_table(states)

    st.markdown("### Simulation Data")

    # Show summary stats
    col1, col2 = st.columns([3, 1])

    with col1:
        st.dataframe(
            df.head(max_rows),
            use_container_width=True,
            height=400
        )

    with col2:
        st.markdown("**Summary Statistics**")
        st.dataframe(
            df.describe(),
            use_container_width=True
        )

    if len(df) > max_rows:
        st.info(f"Showing first {max_rows} of {len(df)} rows. Download full data using export buttons above.")


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with thousand separators."""
    if decimals == 0:
        return f"{num:,.0f}"
    return f"{num:,.{decimals}f}"


def get_trend_emoji(change: float) -> str:
    """Get emoji based on trend."""
    if change > 5:
        return "📈"
    elif change < -5:
        return "📉"
    else:
        return "➡️"


def create_info_box(title: str, content: str, box_type: str = "info"):
    """
    Create a styled info box.

    Args:
        title: Box title
        content: Box content
        box_type: Type of box (info, warning, success, danger)
    """
    box_class = f"{box_type}-box"
    st.markdown(
        f"""
        <div class="{box_class}">
            <h4>{title}</h4>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


__all__ = [
    "export_to_csv",
    "export_to_json",
    "render_export_section",
    "calculate_metrics",
    "render_metrics_cards",
    "add_simulation_to_compare",
    "render_comparison_manager",
    "create_summary_table",
    "render_data_table",
    "format_number",
    "get_trend_emoji",
    "create_info_box",
]
