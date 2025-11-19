"""
Layout components for Market Manipulation Lab dashboard.
Includes headers, footers, help sections, and tutorial mode.
"""

import streamlit as st
from .theme import COLORS


def render_header():
    """Render the main dashboard header."""
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
            f"""
            <h1 style='margin-bottom: 0;'>
                <span style='color: {COLORS["primary"]}'>Market Manipulation Lab</span>
            </h1>
            <p style='color: {COLORS["text_secondary"]}; font-size: 1.1rem; margin-top: 0.5rem;'>
                Interactive simulation and analysis of market microstructure and manipulation
            </p>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # Quick actions
        if st.button("Help", key="header_help", use_container_width=True):
            st.session_state.show_help = not st.session_state.get('show_help', False)


def render_footer():
    """Render the dashboard footer."""
    st.markdown("---")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.markdown(
            f"""
            <p style='color: {COLORS["text_muted"]}; font-size: 0.9rem;'>
                <strong>Market Manipulation Lab</strong><br>
                Educational simulator for market microstructure analysis
            </p>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <p style='color: {COLORS["text_muted"]}; font-size: 0.9rem;'>
                <strong>Disclaimer:</strong> For educational purposes only.<br>
                Not financial advice. Markets are more complex than simulations.
            </p>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <p style='color: {COLORS["text_muted"]}; font-size: 0.9rem; text-align: right;'>
                Version 1.0<br>
                Built with Streamlit
            </p>
            """,
            unsafe_allow_html=True
        )


def render_help_sidebar():
    """Render comprehensive help sidebar."""
    if not st.session_state.get('show_help', False):
        return

    with st.sidebar:
        st.markdown("---")
        st.markdown("## Help & Tutorial")

        help_section = st.selectbox(
            "Select topic",
            [
                "Getting Started",
                "Configuration",
                "Manipulator Strategy",
                "Interpreting Results",
                "Export & Compare",
                "Glossary"
            ]
        )

        if help_section == "Getting Started":
            st.markdown(
                """
                ### Getting Started

                **Quick Start:**
                1. Choose a preset from the dropdown
                2. Click "Run Simulation"
                3. Explore the results in different tabs

                **Tips:**
                - Start with "Quick Start" preset
                - Enable manipulator to see price manipulation
                - Use comparison mode to compare scenarios
                """
            )

        elif help_section == "Configuration":
            st.markdown(
                """
                ### Configuration Guide

                **Basic Parameters:**
                - **Traders**: More traders = more stable market
                - **Days**: Longer simulations show trends better
                - **Initial Price**: Starting asset price

                **Manipulator:**
                - **Cash**: More cash = stronger manipulation
                - **Accumulation**: Phase of building position
                - **Pump**: Phase of artificially inflating price
                - **Dump**: Phase of selling at profit
                """
            )

        elif help_section == "Manipulator Strategy":
            st.markdown(
                f"""
                ### Manipulator Strategy

                **Classic Pump & Dump:**

                <div style='background: {COLORS["bg_card"]}; padding: 1rem; border-radius: 4px; margin: 1rem 0;'>

                **Phase 1: Accumulation** 📊
                - Buy gradually at low prices
                - Avoid raising suspicion

                **Phase 2: Pump** 🚀
                - Place large buy orders
                - Drive price up artificially
                - Create FOMO

                **Phase 3: Dump** 📉
                - Sell holdings at peak
                - Exit before price crashes
                - Maximize profit

                </div>

                **Detection Signs:**
                - Unusual volume spikes
                - Price jumps without news
                - Order book imbalance
                """,
                unsafe_allow_html=True
            )

        elif help_section == "Interpreting Results":
            st.markdown(
                """
                ### Interpreting Results

                **Price Chart:**
                - Smooth curves = normal trading
                - Sharp spikes = possible manipulation
                - Returns to baseline = market correction

                **Volume Chart:**
                - Consistent volume = healthy market
                - Sudden spikes = unusual activity
                - Volume + Price spike = red flag

                **Manipulation Score:**
                - Low (< 1.0) = Normal activity
                - Medium (1.0-2.0) = Suspicious
                - High (> 2.0) = Likely manipulation

                **Order Book:**
                - Balanced curves = fair market
                - Large imbalance = price pressure
                - Intersection = equilibrium price
                """
            )

        elif help_section == "Export & Compare":
            st.markdown(
                """
                ### Export & Compare

                **Export Options:**
                - **CSV**: Spreadsheet-friendly format
                - **JSON**: Complete data with metadata
                - **Config**: Save your settings

                **Comparison Mode:**
                1. Run first simulation
                2. Click "Add to Compare"
                3. Adjust parameters
                4. Run another simulation
                5. Go to Compare tab

                **Use Cases:**
                - Test different manipulator strategies
                - Compare market sizes
                - Validate detection methods
                """
            )

        elif help_section == "Glossary":
            st.markdown(
                f"""
                ### Glossary

                <div style='background: {COLORS["bg_card"]}; padding: 1rem; border-radius: 4px;'>

                **Order Book**: List of buy and sell orders

                **Equilibrium Price**: Price where supply meets demand

                **Pump & Dump**: Artificial inflation then sell-off

                **Wash Trading**: Self-trading to fake volume

                **Manipulation Score**: Metric for detecting anomalies

                **Volatility**: Price variation range

                **Liquidity**: Ease of buying/selling

                **Market Depth**: Total volume in order book

                </div>
                """,
                unsafe_allow_html=True
            )


def render_tutorial_mode():
    """Render interactive tutorial overlay."""
    if 'tutorial_step' not in st.session_state:
        st.session_state.tutorial_step = 0

    if st.session_state.tutorial_step == 0:
        return  # Tutorial not active

    # Tutorial overlay
    steps = [
        {
            "title": "Welcome to Market Manipulation Lab!",
            "content": "This tutorial will guide you through the dashboard. Click Next to continue.",
        },
        {
            "title": "Step 1: Choose a Preset",
            "content": "Select a preset configuration from the sidebar. Try 'Pump & Dump Demo' to see manipulation in action.",
        },
        {
            "title": "Step 2: Run Simulation",
            "content": "Click the 'Run Simulation' button in the sidebar to start. This may take a few seconds.",
        },
        {
            "title": "Step 3: Explore Results",
            "content": "Navigate through tabs to see different visualizations. The Overview tab shows key metrics.",
        },
        {
            "title": "Step 4: Analyze Manipulation",
            "content": "Check the Detection tab to see manipulation scores and anomalies detected by the system.",
        },
        {
            "title": "Step 5: Export & Compare",
            "content": "Export your results or add simulations to comparison mode to analyze multiple scenarios.",
        },
    ]

    current_step = st.session_state.tutorial_step
    if current_step > 0 and current_step <= len(steps):
        step = steps[current_step - 1]

        # Create tutorial box
        st.info(
            f"""
            **Tutorial ({current_step}/{len(steps)}): {step['title']}**

            {step['content']}
            """
        )

        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:
            if current_step > 1:
                if st.button("← Previous"):
                    st.session_state.tutorial_step -= 1
                    st.experimental_rerun()

        with col2:
            if current_step < len(steps):
                if st.button("Next →"):
                    st.session_state.tutorial_step += 1
                    st.experimental_rerun()
            else:
                if st.button("Finish"):
                    st.session_state.tutorial_step = 0
                    st.experimental_rerun()


def render_loading_state(message: str = "Running simulation..."):
    """Render elegant loading state."""
    with st.spinner(message):
        # Progress bar simulation
        progress_bar = st.progress(0)
        status_text = st.empty()

        import time
        for i in range(100):
            # Update progress
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("Initializing market...")
            elif i < 60:
                status_text.text("Simulating trading days...")
            elif i < 90:
                status_text.text("Calculating metrics...")
            else:
                status_text.text("Finalizing results...")

            time.sleep(0.01)

        progress_bar.empty()
        status_text.empty()


def render_welcome_screen():
    """Render welcome screen for first-time users."""
    if 'welcomed' in st.session_state:
        return

    st.markdown(
        f"""
        <div style='background: {COLORS["bg_card"]}; padding: 2rem; border-radius: 8px; margin: 2rem 0;'>
            <h2 style='color: {COLORS["primary"]}; margin-top: 0;'>
                Welcome to Market Manipulation Lab! 👋
            </h2>

            <p style='font-size: 1.1rem; color: {COLORS["text_primary"]}; margin-bottom: 1.5rem;'>
                An educational platform for understanding market microstructure and manipulation detection.
            </p>

            <h3 style='color: {COLORS["text_primary"]}'>What can you do here?</h3>

            <ul style='color: {COLORS["text_secondary"]}; font-size: 1rem;'>
                <li>🎯 Simulate market dynamics with configurable parameters</li>
                <li>🚀 Test pump-and-dump manipulation strategies</li>
                <li>📊 Visualize price, volume, and order book evolution</li>
                <li>🔍 Detect manipulation using statistical anomalies</li>
                <li>📈 Compare multiple scenarios side-by-side</li>
                <li>💾 Export results for further analysis</li>
            </ul>

            <h3 style='color: {COLORS["text_primary"]}; margin-top: 1.5rem;'>Quick Start:</h3>

            <ol style='color: {COLORS["text_secondary"]}; font-size: 1rem;'>
                <li>Choose "Pump & Dump Demo" from presets in the sidebar</li>
                <li>Click "Run Simulation"</li>
                <li>Explore the visualizations in different tabs</li>
            </ol>

            <p style='color: {COLORS["warning"]}; font-size: 0.9rem; margin-top: 1.5rem;'>
                ⚠️ <strong>Educational Purpose Only:</strong> This is a simplified simulation.
                Real markets are far more complex. Not financial advice.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("Start Tutorial", use_container_width=True):
            st.session_state.tutorial_step = 1
            st.session_state.welcomed = True
            st.experimental_rerun()

    with col2:
        if st.button("Skip to Dashboard", use_container_width=True):
            st.session_state.welcomed = True
            st.experimental_rerun()


def render_error_message(error: Exception, context: str = ""):
    """Render user-friendly error message."""
    st.error(
        f"""
        **An error occurred{' during ' + context if context else ''}**

        {str(error)}

        **Troubleshooting:**
        - Check your configuration parameters
        - Try a preset configuration
        - Reduce the number of days or traders
        - Restart the simulation

        If the problem persists, this may be a bug.
        """
    )


def render_empty_state(message: str, action_text: str = "Get Started"):
    """Render empty state with call to action."""
    st.markdown(
        f"""
        <div style='text-align: center; padding: 3rem; color: {COLORS["text_secondary"]};'>
            <h2 style='color: {COLORS["text_muted"]}; margin-bottom: 1rem;'>
                {message}
            </h2>
            <p style='font-size: 1.1rem;'>
                👈 {action_text}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


__all__ = [
    "render_header",
    "render_footer",
    "render_help_sidebar",
    "render_tutorial_mode",
    "render_loading_state",
    "render_welcome_screen",
    "render_error_message",
    "render_empty_state",
]
