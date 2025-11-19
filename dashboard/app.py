"""
Market Manipulation Lab - Interactive Dashboard

Streamlit dashboard for exploring market simulations visually.
"""

import streamlit as st
import random
from market_lab.core.market import MarketConfig
from market_lab.core.traders import build_traders
from market_lab.core.sentiment import NoSentiment, StepSentiment
from market_lab.core.simulation import SimulationRunner
from market_lab.manipulation.manipulator import Manipulator
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Market Manipulation Lab",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Market Manipulation Lab")
st.markdown("Explore market microstructure and manipulation through interactive simulations")

# Sidebar - Configuration
st.sidebar.header("⚙️ Simulation Configuration")

n_traders = st.sidebar.slider("Number of Traders", 10, 500, 150)
n_days = st.sidebar.slider("Simulation Days", 30, 365, 120)
initial_price = st.sidebar.number_input("Initial Price", 50.0, 200.0, 100.0)

use_manipulator = st.sidebar.checkbox("Enable Manipulator", value=False)

if use_manipulator:
    st.sidebar.subheader("Manipulator Settings")
    manip_cash = st.sidebar.number_input("Manipulator Cash", 1000, 100000, 50000)
    pump_volume = st.sidebar.slider("Pump Volume Multiplier", 1, 10, 5)

# Run simulation button
if st.sidebar.button("🚀 Run Simulation"):
    with st.spinner("Running simulation..."):
        # Setup
        config = MarketConfig(
            n_traders=n_traders,
            initial_price=initial_price,
            initial_cash=10_000.0,
            initial_holdings=100,
            min_price=initial_price * 0.5,
            max_price=initial_price * 2.0,
            n_price_points=50
        )

        rng = random.Random(42)
        traders = build_traders(config, rng, use_wealth_limit=True)

        manipulator = None
        if use_manipulator:
            manipulator = Manipulator(
                trader_id=-1,
                initial_cash=float(manip_cash),
                initial_holdings=100,
                accumulate_days=30,
                pump_days=10,
                dump_days=15,
                pump_volume=pump_volume
            )

        runner = SimulationRunner(
            config=config,
            traders=traders,
            sentiment=NoSentiment(),
            manipulator=manipulator
        )

        states = runner.run(n_days=n_days)

        # Store in session state
        st.session_state['states'] = states
        st.session_state['manipulator'] = manipulator

    st.success("✅ Simulation completed!")

# Display results
if 'states' in st.session_state:
    states = st.session_state['states']

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Days Simulated", len(states))

    with col2:
        start_price = states[0].price
        end_price = states[-1].price
        price_change = ((end_price - start_price) / start_price) * 100
        st.metric("Price Change", f"{price_change:.2f}%")

    with col3:
        avg_volume = sum(s.cleared_volume for s in states) / len(states)
        st.metric("Avg Volume", f"{avg_volume:.0f}")

    with col4:
        max_price = max(s.price for s in states)
        min_price = min(s.price for s in states)
        volatility = ((max_price - min_price) / start_price) * 100
        st.metric("Volatility Range", f"{volatility:.2f}%")

    # Price chart
    st.subheader("📊 Price Evolution")

    fig, ax = plt.subplots(figsize=(12, 6))
    days = range(len(states))
    prices = [s.price for s in states]

    ax.plot(days, prices, linewidth=2)
    ax.set_xlabel("Day")
    ax.set_ylabel("Price")
    ax.set_title("Market Price Over Time")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    # Volume chart
    st.subheader("📊 Volume Evolution")

    fig, ax = plt.subplots(figsize=(12, 4))
    volumes = [s.cleared_volume for s in states]

    ax.bar(days, volumes, alpha=0.6)
    ax.set_xlabel("Day")
    ax.set_ylabel("Volume")
    ax.set_title("Trading Volume Over Time")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

else:
    st.info("👈 Configure parameters in the sidebar and click 'Run Simulation'")

# Footer
st.markdown("---")
st.markdown("**Market Manipulation Lab** - Educational simulator for market microstructure")
