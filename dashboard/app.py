"""
Market Manipulation Lab - Interactive Dashboard

Premium Streamlit dashboard for exploring market simulations with advanced features.
Redesigned for maximum UX and professional visualization.
"""

import streamlit as st
import random
from market_lab.core.market import MarketConfig
from market_lab.core.traders import build_traders
from market_lab.core.sentiment import NoSentiment
from market_lab.core.simulation import SimulationRunner
from market_lab.manipulation.manipulator import Manipulator
from market_lab.manipulation.detection import attach_anomaly_scores

# Import dashboard components
from components import (
    # Theme
    apply_custom_css,
    get_chart_config,
    # Charts
    create_candlestick_chart,
    create_price_volume_chart,
    create_order_book_chart,
    create_manipulation_heatmap,
    create_wealth_comparison_chart,
    create_comparison_chart,
    create_anomaly_timeline,
    create_distribution_chart,
    # Config
    SimulationConfig,
    render_config_panel,
    render_save_load_ui,
    # Utils
    render_export_section,
    render_metrics_cards,
    render_comparison_manager,
    render_data_table,
    # Layout
    render_header,
    render_footer,
    render_help_sidebar,
    render_tutorial_mode,
    render_welcome_screen,
    render_empty_state,
    render_error_message,
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Market Manipulation Lab",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/market-simulator',
        'Report a bug': "https://github.com/your-repo/market-simulator/issues",
        'About': "Market Manipulation Lab - Educational market simulator"
    }
)

# Apply custom theme
apply_custom_css()


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'states' not in st.session_state:
    st.session_state.states = None

if 'manipulator' not in st.session_state:
    st.session_state.manipulator = None

if 'current_config' not in st.session_state:
    st.session_state.current_config = None

if 'comparisons' not in st.session_state:
    st.session_state.comparisons = []


# ============================================================================
# SIDEBAR - CONFIGURATION
# ============================================================================

# Render configuration panel
config = render_config_panel()
st.session_state.current_config = config

# Save/Load UI
render_save_load_ui()

# Comparison manager
render_comparison_manager()

# Run simulation button
st.sidebar.markdown("---")
run_button = st.sidebar.button(
    "🚀 Run Simulation",
    use_container_width=True,
    type="primary"
)


# ============================================================================
# RUN SIMULATION
# ============================================================================

if run_button:
    try:
        with st.spinner("🔄 Running simulation... This may take a moment."):
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Setup market config
            status_text.text("⚙️ Configuring market...")
            progress_bar.progress(20)

            market_config = MarketConfig(
                n_traders=config.n_traders,
                initial_price=config.initial_price,
                initial_cash=config.initial_cash,
                initial_holdings=config.initial_holdings,
                min_price=config.initial_price * config.min_price_multiplier,
                max_price=config.initial_price * config.max_price_multiplier,
                n_price_points=config.n_price_points
            )

            # Build traders
            status_text.text("👥 Initializing traders...")
            progress_bar.progress(40)

            rng = random.Random(config.seed)
            traders = build_traders(market_config, rng, use_wealth_limit=config.use_wealth_limit)

            # Setup manipulator if enabled
            manipulator = None
            if config.use_manipulator:
                status_text.text("🎯 Setting up manipulator...")
                progress_bar.progress(50)

                manipulator = Manipulator(
                    trader_id=-1,
                    initial_cash=float(config.manip_cash),
                    initial_holdings=config.manip_holdings,
                    accumulate_days=config.accumulate_days,
                    pump_days=config.pump_days,
                    dump_days=config.dump_days,
                    pump_volume=config.pump_volume
                )

            # Run simulation
            status_text.text("📊 Simulating market days...")
            progress_bar.progress(60)

            runner = SimulationRunner(
                config=market_config,
                traders=traders,
                sentiment=NoSentiment(),
                manipulator=manipulator
            )

            states = runner.run(n_days=config.n_days)

            # Calculate detection metrics
            status_text.text("🔍 Calculating anomaly scores...")
            progress_bar.progress(80)

            attach_anomaly_scores(states, window=20)

            # Store in session state
            status_text.text("💾 Finalizing...")
            progress_bar.progress(100)

            st.session_state.states = states
            st.session_state.manipulator = manipulator

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

        st.success("✅ Simulation completed successfully!")
        st.balloons()

    except Exception as e:
        render_error_message(e, "simulation execution")


# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
render_header()

# Tutorial mode
render_tutorial_mode()

# Help sidebar
render_help_sidebar()

# Welcome screen for first-time users
if not st.session_state.get('welcomed'):
    render_welcome_screen()

# Main content tabs
if st.session_state.states:
    states = st.session_state.states
    manipulator = st.session_state.manipulator

    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "📈 Advanced Charts",
        "🔍 Detection",
        "📚 Order Book",
        "🔄 Compare",
        "📥 Data & Export"
    ])

    # ========================================================================
    # TAB 1: OVERVIEW
    # ========================================================================
    with tab1:
        st.markdown("## Overview")

        # Metrics cards
        render_metrics_cards(states)

        st.markdown("---")

        # Main charts
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Price & Volume Evolution")
            fig = create_price_volume_chart(states)
            st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

        with col2:
            st.markdown("### Distribution Analysis")
            fig = create_distribution_chart(states)
            st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

    # ========================================================================
    # TAB 2: ADVANCED CHARTS
    # ========================================================================
    with tab2:
        st.markdown("## Advanced Visualizations")

        # Chart type selector
        chart_type = st.selectbox(
            "Select visualization",
            [
                "Candlestick Chart",
                "Manipulation Heatmap",
                "Wealth Comparison",
                "Anomaly Timeline"
            ]
        )

        if chart_type == "Candlestick Chart":
            window = st.slider("Candle Window (days)", 1, 10, 1)
            fig = create_candlestick_chart(states, window=window)
            st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

            st.info(
                "💡 **Tip:** Candlestick charts show price movement patterns. "
                "Increase the window size to aggregate multiple days into single candles."
            )

        elif chart_type == "Manipulation Heatmap":
            fig = create_manipulation_heatmap(states)
            st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

            st.info(
                "💡 **Tip:** Darker colors indicate higher volatility. "
                "Look for patterns that align with manipulation phases."
            )

        elif chart_type == "Wealth Comparison":
            fig = create_wealth_comparison_chart(states, manipulator)
            st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

            st.info(
                "💡 **Tip:** Compare manipulator wealth trajectory against market average. "
                "Successful manipulation shows profit extraction."
            )

        elif chart_type == "Anomaly Timeline":
            fig = create_anomaly_timeline(states)
            st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

            st.info(
                "💡 **Tip:** Red X markers indicate detected anomalies. "
                "High manipulation scores suggest suspicious activity."
            )

    # ========================================================================
    # TAB 3: DETECTION
    # ========================================================================
    with tab3:
        st.markdown("## Manipulation Detection Analysis")

        # Detection summary
        scores = [getattr(s, 'manipulation_score', 0) or 0 for s in states]
        high_alerts = sum(1 for s in scores if s > 2.0)
        medium_alerts = sum(1 for s in scores if 1.0 < s <= 2.0)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("High Alerts", high_alerts, help="Days with score > 2.0")

        with col2:
            st.metric("Medium Alerts", medium_alerts, help="Days with score 1.0-2.0")

        with col3:
            avg_score = sum(scores) / len(scores) if scores else 0
            st.metric("Avg Score", f"{avg_score:.2f}", help="Average manipulation score")

        with col4:
            max_score = max(scores) if scores else 0
            st.metric("Max Score", f"{max_score:.2f}", help="Highest score detected")

        st.markdown("---")

        # Anomaly timeline
        fig = create_anomaly_timeline(states)
        st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

        # Detection methodology
        with st.expander("ℹ️ How does detection work?"):
            st.markdown(
                """
                **Manipulation Detection Methodology:**

                The system uses statistical anomaly detection based on:

                1. **Price Volatility Z-Score**
                   - Measures unusual price movements
                   - Rolling window comparison

                2. **Volume Anomaly Z-Score**
                   - Detects abnormal trading volume
                   - Identifies volume spikes

                3. **Combined Score**
                   - Sum of absolute z-scores
                   - Higher score = more suspicious

                **Thresholds:**
                - **< 1.0**: Normal activity
                - **1.0 - 2.0**: Suspicious, warrants attention
                - **> 2.0**: High probability of manipulation

                **Limitations:**
                - Statistical detection is not 100% accurate
                - Some legitimate events may trigger alerts
                - Sophisticated manipulation may evade detection
                """
            )

    # ========================================================================
    # TAB 4: ORDER BOOK
    # ========================================================================
    with tab4:
        st.markdown("## Order Book Analysis")

        # Day selector
        selected_day = st.slider(
            "Select day to analyze",
            min_value=0,
            max_value=len(states) - 1,
            value=len(states) // 2
        )

        selected_state = states[selected_day]

        # Display order book if available
        if hasattr(selected_state, 'order_curves') and selected_state.order_curves:
            col1, col2 = st.columns([2, 1])

            with col1:
                fig = create_order_book_chart(selected_state.order_curves)
                st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

            with col2:
                st.markdown("### Day Statistics")
                st.metric("Day", selected_day)
                st.metric("Price", f"${selected_state.price:.2f}")
                st.metric("Volume", f"{selected_state.cleared_volume:,.0f}")
                st.metric("Sentiment", f"{selected_state.sentiment_value:.2f}")

                if hasattr(selected_state, 'manipulation_score') and selected_state.manipulation_score:
                    score = selected_state.manipulation_score
                    st.metric("Manipulation Score", f"{score:.2f}")

                    if score > 2.0:
                        st.error("⚠️ High alert: Possible manipulation")
                    elif score > 1.0:
                        st.warning("⚠️ Suspicious activity detected")
                    else:
                        st.success("✅ Normal trading activity")

            st.markdown("---")

            with st.expander("ℹ️ Understanding the Order Book"):
                st.markdown(
                    """
                    **Order Book Basics:**

                    - **Green curve (Buy Orders)**: Cumulative demand at each price
                    - **Red curve (Sell Orders)**: Cumulative supply at each price
                    - **Star marker**: Equilibrium price where most volume clears

                    **What to look for:**

                    - **Balanced curves**: Healthy, liquid market
                    - **Large gap**: Low liquidity, vulnerable to manipulation
                    - **Sudden shifts**: Possible manipulator activity
                    - **Steep slopes**: Concentrated orders at specific prices
                    """
                )

        else:
            st.warning("Order book data not available for this day")

    # ========================================================================
    # TAB 5: COMPARE
    # ========================================================================
    with tab5:
        st.markdown("## Multi-Simulation Comparison")

        if st.session_state.comparisons:
            st.success(f"📊 Comparing {len(st.session_state.comparisons)} simulations")

            # Create comparison chart
            fig = create_comparison_chart(st.session_state.comparisons)
            st.plotly_chart(fig, use_container_width=True, config=get_chart_config())

            st.markdown("---")

            # Comparison table
            st.markdown("### Simulation Details")

            comparison_data = []
            for sim in st.session_state.comparisons:
                states_cmp = sim['states']
                config_cmp = sim['config']

                start_price = states_cmp[0].price
                end_price = states_cmp[-1].price
                price_change = ((end_price - start_price) / start_price) * 100

                comparison_data.append({
                    'Name': sim['name'],
                    'Days': len(states_cmp),
                    'Traders': config_cmp.get('n_traders', 'N/A'),
                    'Manipulator': '✓' if config_cmp.get('use_manipulator') else '✗',
                    'Start Price': f"${start_price:.2f}",
                    'End Price': f"${end_price:.2f}",
                    'Change %': f"{price_change:.2f}%",
                })

            import pandas as pd
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)

        else:
            render_empty_state(
                "No simulations added for comparison",
                "Run a simulation and click 'Add to Compare' in the sidebar"
            )

    # ========================================================================
    # TAB 6: DATA & EXPORT
    # ========================================================================
    with tab6:
        st.markdown("## Data & Export")

        # Export section
        render_export_section(states, config.to_dict())

        st.markdown("---")

        # Data table
        render_data_table(states)

else:
    # No simulation run yet
    render_empty_state(
        "No simulation data available",
        "Configure parameters in the sidebar and click 'Run Simulation'"
    )


# ============================================================================
# FOOTER
# ============================================================================

render_footer()
