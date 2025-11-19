"""
Advanced interactive charts for Market Manipulation Lab dashboard.
All visualizations use Plotly for maximum interactivity.
"""

from typing import List, Optional, Sequence
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from .theme import COLORS, PLOTLY_TEMPLATE


def create_candlestick_chart(states, window: int = 1) -> go.Figure:
    """
    Create an interactive candlestick chart from market states.

    Args:
        states: List of MarketState objects
        window: Window size for aggregating data into candles
    """
    days = [s.day for s in states]
    prices = [s.price for s in states]

    # For simple version, use price as OHLC
    # In a real scenario, you'd aggregate intraday data
    fig = go.Figure()

    if window == 1:
        # Simple line chart if window is 1
        fig.add_trace(go.Scatter(
            x=days,
            y=prices,
            mode='lines',
            name='Price',
            line=dict(color=COLORS["price"], width=2),
            hovertemplate='Day %{x}<br>Price: $%{y:.2f}<extra></extra>'
        ))
    else:
        # Create candlestick-like representation
        opens = []
        highs = []
        lows = []
        closes = []
        candle_days = []

        for i in range(0, len(prices), window):
            chunk = prices[i:i+window]
            if chunk:
                opens.append(chunk[0])
                closes.append(chunk[-1])
                highs.append(max(chunk))
                lows.append(min(chunk))
                candle_days.append(days[i])

        fig.add_trace(go.Candlestick(
            x=candle_days,
            open=opens,
            high=highs,
            low=lows,
            close=closes,
            name='Price',
            increasing_line_color=COLORS["success"],
            decreasing_line_color=COLORS["danger"],
        ))

    fig.update_layout(
        title="Price Evolution - Candlestick View",
        xaxis_title="Day",
        yaxis_title="Price ($)",
        template=PLOTLY_TEMPLATE,
        hovermode='x unified',
        height=500,
    )

    return fig


def create_price_volume_chart(states) -> go.Figure:
    """Create a dual-axis chart with price and volume."""
    days = [s.day for s in states]
    prices = [s.price for s in states]
    volumes = [s.cleared_volume for s in states]

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=("Price Evolution", "Trading Volume")
    )

    # Price trace
    fig.add_trace(
        go.Scatter(
            x=days,
            y=prices,
            mode='lines',
            name='Price',
            line=dict(color=COLORS["price"], width=2),
            hovertemplate='Day %{x}<br>Price: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )

    # Volume trace
    fig.add_trace(
        go.Bar(
            x=days,
            y=volumes,
            name='Volume',
            marker_color=COLORS["volume"],
            hovertemplate='Day %{x}<br>Volume: %{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        hovermode='x unified',
        height=600,
        showlegend=True,
    )

    fig.update_xaxes(title_text="Day", row=2, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig


def create_order_book_chart(order_curves) -> go.Figure:
    """Create an animated order book visualization."""
    if order_curves is None:
        return go.Figure()

    fig = go.Figure()

    # Buy orders (demand)
    fig.add_trace(go.Scatter(
        x=order_curves.price_grid,
        y=order_curves.buy_curve,
        mode='lines',
        name='Buy Orders (Demand)',
        line=dict(color=COLORS["buy_orders"], width=3),
        fill='tozeroy',
        fillcolor=f'rgba(107, 203, 119, 0.2)',
        hovertemplate='Price: $%{x:.2f}<br>Cumulative Volume: %{y:,.0f}<extra></extra>'
    ))

    # Sell orders (supply)
    fig.add_trace(go.Scatter(
        x=order_curves.price_grid,
        y=order_curves.sell_curve,
        mode='lines',
        name='Sell Orders (Supply)',
        line=dict(color=COLORS["sell_orders"], width=3),
        fill='tozeroy',
        fillcolor=f'rgba(255, 107, 107, 0.2)',
        hovertemplate='Price: $%{x:.2f}<br>Cumulative Volume: %{y:,.0f}<extra></extra>'
    ))

    # Mark intersection (equilibrium)
    # Find approximate intersection
    buy = np.array(order_curves.buy_curve)
    sell = np.array(order_curves.sell_curve)
    prices = np.array(order_curves.price_grid)

    satisfaction = np.minimum(buy, sell)
    if len(satisfaction) > 0 and max(satisfaction) > 0:
        max_idx = np.argmax(satisfaction)
        eq_price = prices[max_idx]
        eq_volume = satisfaction[max_idx]

        fig.add_trace(go.Scatter(
            x=[eq_price],
            y=[eq_volume],
            mode='markers',
            name='Equilibrium',
            marker=dict(color=COLORS["warning"], size=15, symbol='star'),
            hovertemplate='Equilibrium<br>Price: $%{x:.2f}<br>Volume: %{y:,.0f}<extra></extra>'
        ))

    fig.update_layout(
        title="Order Book - Supply & Demand Curves",
        xaxis_title="Price ($)",
        yaxis_title="Cumulative Volume",
        template=PLOTLY_TEMPLATE,
        hovermode='closest',
        height=500,
    )

    return fig


def create_manipulation_heatmap(states, window: int = 20) -> go.Figure:
    """Create a heatmap showing manipulation intensity over time."""
    days = [s.day for s in states]
    prices = [s.price for s in states]
    volumes = [s.cleared_volume for s in states]

    # Calculate rolling statistics
    price_changes = [0] + [abs(prices[i] - prices[i-1]) for i in range(1, len(prices))]
    volume_changes = [0] + [abs(volumes[i] - volumes[i-1]) for i in range(1, len(volumes))]

    # Normalize for heatmap
    max_price_change = max(price_changes) if price_changes else 1
    max_volume_change = max(volume_changes) if volume_changes else 1

    normalized_price = [p / max_price_change for p in price_changes]
    normalized_volume = [v / max_volume_change for v in volume_changes]

    # Create heatmap matrix
    heatmap_data = [normalized_price, normalized_volume]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=days,
        y=['Price Volatility', 'Volume Volatility'],
        colorscale=[
            [0, COLORS["success"]],
            [0.5, COLORS["warning"]],
            [1, COLORS["danger"]]
        ],
        hoverongaps=False,
        hovertemplate='Day %{x}<br>%{y}: %{z:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title="Trading Pattern Heatmap - Anomaly Detection",
        xaxis_title="Day",
        template=PLOTLY_TEMPLATE,
        height=300,
    )

    return fig


def create_wealth_comparison_chart(states, manipulator=None) -> go.Figure:
    """Create wealth comparison between manipulator and regular traders."""
    fig = go.Figure()

    days = [s.day for s in states]

    # Calculate average trader wealth (placeholder - would need actual trader data)
    # For now, we'll simulate this
    if manipulator:
        # This would need to be calculated from actual simulation data
        # For demo purposes, showing conceptual visualization
        fig.add_trace(go.Scatter(
            x=days,
            y=[100 + i * 0.5 for i in days],  # Placeholder
            mode='lines',
            name='Average Trader',
            line=dict(color=COLORS["text_secondary"], width=2, dash='dot'),
            hovertemplate='Day %{x}<br>Avg Wealth: $%{y:,.0f}<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=days,
            y=[100 + i * 2 for i in days],  # Placeholder - would use actual manipulator wealth
            mode='lines',
            name='Manipulator',
            line=dict(color=COLORS["danger"], width=3),
            hovertemplate='Day %{x}<br>Manipulator Wealth: $%{y:,.0f}<extra></extra>'
        ))

    fig.update_layout(
        title="Wealth Comparison - Manipulator vs Market",
        xaxis_title="Day",
        yaxis_title="Wealth ($)",
        template=PLOTLY_TEMPLATE,
        hovermode='x unified',
        height=400,
    )

    return fig


def create_comparison_chart(simulations: List[dict]) -> go.Figure:
    """Compare multiple simulation runs side by side."""
    fig = go.Figure()

    for i, sim in enumerate(simulations):
        states = sim.get("states", [])
        name = sim.get("name", f"Simulation {i+1}")

        days = [s.day for s in states]
        prices = [s.price for s in states]

        fig.add_trace(go.Scatter(
            x=days,
            y=prices,
            mode='lines',
            name=name,
            line=dict(width=2),
            hovertemplate=f'{name}<br>Day %{{x}}<br>Price: $%{{y:.2f}}<extra></extra>'
        ))

    fig.update_layout(
        title="Multi-Simulation Comparison",
        xaxis_title="Day",
        yaxis_title="Price ($)",
        template=PLOTLY_TEMPLATE,
        hovermode='x unified',
        height=500,
    )

    return fig


def create_anomaly_timeline(states) -> go.Figure:
    """Create an annotated timeline highlighting anomalous events."""
    days = [s.day for s in states]
    prices = [s.price for s in states]
    scores = [getattr(s, 'manipulation_score', 0) or 0 for s in states]

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.6, 0.4],
        subplot_titles=("Price with Anomaly Markers", "Manipulation Score")
    )

    # Price line
    fig.add_trace(
        go.Scatter(
            x=days,
            y=prices,
            mode='lines',
            name='Price',
            line=dict(color=COLORS["price"], width=2),
        ),
        row=1, col=1
    )

    # Highlight anomalies (high manipulation scores)
    if scores:
        threshold = np.percentile(scores, 90)  # Top 10% as anomalies
        anomaly_days = [d for d, s in zip(days, scores) if s > threshold]
        anomaly_prices = [p for p, s in zip(prices, scores) if s > threshold]

        if anomaly_days:
            fig.add_trace(
                go.Scatter(
                    x=anomaly_days,
                    y=anomaly_prices,
                    mode='markers',
                    name='Anomaly',
                    marker=dict(color=COLORS["danger"], size=10, symbol='x'),
                ),
                row=1, col=1
            )

    # Manipulation score
    fig.add_trace(
        go.Scatter(
            x=days,
            y=scores,
            mode='lines',
            name='Score',
            line=dict(color=COLORS["manipulation"], width=2),
            fill='tozeroy',
            fillcolor=f'rgba(255, 107, 107, 0.2)',
        ),
        row=2, col=1
    )

    # Add threshold line
    if scores:
        threshold = np.percentile(scores, 90)
        fig.add_hline(
            y=threshold,
            line_dash="dash",
            line_color=COLORS["warning"],
            annotation_text="Alert Threshold",
            row=2, col=1
        )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        hovermode='x unified',
        height=600,
        showlegend=True,
    )

    fig.update_xaxes(title_text="Day", row=2, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Score", row=2, col=1)

    return fig


def create_distribution_chart(states) -> go.Figure:
    """Create price and volume distribution histograms."""
    prices = [s.price for s in states]
    volumes = [s.cleared_volume for s in states]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Price Distribution", "Volume Distribution")
    )

    fig.add_trace(
        go.Histogram(
            x=prices,
            name='Price',
            marker_color=COLORS["price"],
            nbinsx=30,
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Histogram(
            x=volumes,
            name='Volume',
            marker_color=COLORS["volume"],
            nbinsx=30,
        ),
        row=1, col=2
    )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=400,
        showlegend=False,
    )

    fig.update_xaxes(title_text="Price ($)", row=1, col=1)
    fig.update_xaxes(title_text="Volume", row=1, col=2)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=2)

    return fig


__all__ = [
    "create_candlestick_chart",
    "create_price_volume_chart",
    "create_order_book_chart",
    "create_manipulation_heatmap",
    "create_wealth_comparison_chart",
    "create_comparison_chart",
    "create_anomaly_timeline",
    "create_distribution_chart",
]
