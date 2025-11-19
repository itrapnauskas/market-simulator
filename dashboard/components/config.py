"""
Configuration UI components and presets for Market Manipulation Lab.
Includes quick-start configurations for common scenarios.
"""

import streamlit as st
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import json


@dataclass
class SimulationConfig:
    """Configuration for a market simulation."""
    # Basic parameters
    n_traders: int = 150
    n_days: int = 120
    initial_price: float = 100.0
    initial_cash: float = 10_000.0
    initial_holdings: int = 100

    # Market parameters
    min_price_multiplier: float = 0.5
    max_price_multiplier: float = 2.0
    n_price_points: int = 50

    # Manipulator parameters
    use_manipulator: bool = False
    manip_cash: float = 50_000.0
    manip_holdings: int = 100
    accumulate_days: int = 30
    pump_days: int = 10
    dump_days: int = 15
    pump_volume: int = 5

    # Advanced
    seed: Optional[int] = 42
    use_wealth_limit: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SimulationConfig':
        """Create config from dictionary."""
        return cls(**data)


# Preset configurations
PRESETS = {
    "Quick Start": SimulationConfig(
        n_traders=100,
        n_days=60,
        initial_price=100.0,
        use_manipulator=False,
    ),
    "Pump & Dump Demo": SimulationConfig(
        n_traders=200,
        n_days=120,
        initial_price=100.0,
        use_manipulator=True,
        manip_cash=100_000.0,
        accumulate_days=40,
        pump_days=15,
        dump_days=20,
        pump_volume=8,
    ),
    "Small Market": SimulationConfig(
        n_traders=50,
        n_days=90,
        initial_price=50.0,
        initial_cash=5_000.0,
        use_manipulator=True,
        manip_cash=25_000.0,
        pump_volume=10,
    ),
    "Large Market": SimulationConfig(
        n_traders=500,
        n_days=180,
        initial_price=150.0,
        initial_cash=20_000.0,
        use_manipulator=False,
    ),
    "Extreme Manipulation": SimulationConfig(
        n_traders=150,
        n_days=100,
        initial_price=100.0,
        use_manipulator=True,
        manip_cash=200_000.0,
        accumulate_days=30,
        pump_days=20,
        dump_days=10,
        pump_volume=15,
    ),
    "Random Walk": SimulationConfig(
        n_traders=300,
        n_days=200,
        initial_price=100.0,
        use_manipulator=False,
        use_wealth_limit=False,
    ),
}


def render_preset_selector() -> Optional[SimulationConfig]:
    """
    Render preset selector dropdown.

    Returns:
        Selected preset config, or None if Custom is selected
    """
    st.sidebar.markdown("### Quick Start Presets")

    preset_names = ["Custom"] + list(PRESETS.keys())
    selected = st.sidebar.selectbox(
        "Choose a preset",
        preset_names,
        help="Select a pre-configured scenario or choose Custom for manual configuration"
    )

    if selected == "Custom":
        return None

    config = PRESETS[selected]

    # Show preset description
    descriptions = {
        "Quick Start": "Small, fast simulation without manipulation - great for beginners",
        "Pump & Dump Demo": "Classic pump-and-dump manipulation strategy showcase",
        "Small Market": "Small market with high manipulator influence",
        "Large Market": "Large, stable market simulation",
        "Extreme Manipulation": "Aggressive manipulation with high capital",
        "Random Walk": "Pure random walk without wealth constraints",
    }

    st.sidebar.info(f"**{selected}**: {descriptions.get(selected, '')}")

    return config


def render_basic_config(preset_config: Optional[SimulationConfig] = None) -> SimulationConfig:
    """
    Render basic simulation configuration UI.

    Args:
        preset_config: Optional preset to use as defaults

    Returns:
        SimulationConfig with user selections
    """
    config = preset_config or SimulationConfig()

    st.sidebar.markdown("### Basic Parameters")

    n_traders = st.sidebar.slider(
        "Number of Traders",
        min_value=10,
        max_value=1000,
        value=config.n_traders,
        step=10,
        help="Number of traders participating in the market"
    )

    n_days = st.sidebar.slider(
        "Simulation Days",
        min_value=30,
        max_value=365,
        value=config.n_days,
        step=10,
        help="Number of trading days to simulate"
    )

    initial_price = st.sidebar.number_input(
        "Initial Price ($)",
        min_value=1.0,
        max_value=1000.0,
        value=config.initial_price,
        step=10.0,
        help="Starting price of the asset"
    )

    config.n_traders = n_traders
    config.n_days = n_days
    config.initial_price = initial_price

    return config


def render_manipulator_config(config: SimulationConfig) -> SimulationConfig:
    """
    Render manipulator configuration UI.

    Args:
        config: Base configuration to modify

    Returns:
        Updated configuration
    """
    st.sidebar.markdown("### Manipulator Settings")

    use_manipulator = st.sidebar.checkbox(
        "Enable Manipulator",
        value=config.use_manipulator,
        help="Add a manipulator agent to the simulation"
    )

    config.use_manipulator = use_manipulator

    if use_manipulator:
        with st.sidebar.expander("Manipulator Details", expanded=True):
            config.manip_cash = st.number_input(
                "Manipulator Cash ($)",
                min_value=1_000,
                max_value=1_000_000,
                value=int(config.manip_cash),
                step=10_000,
                help="Starting cash for the manipulator"
            )

            config.accumulate_days = st.slider(
                "Accumulation Days",
                min_value=10,
                max_value=100,
                value=config.accumulate_days,
                help="Days spent accumulating position"
            )

            config.pump_days = st.slider(
                "Pump Days",
                min_value=5,
                max_value=50,
                value=config.pump_days,
                help="Days spent pumping the price"
            )

            config.dump_days = st.slider(
                "Dump Days",
                min_value=5,
                max_value=50,
                value=config.dump_days,
                help="Days spent dumping the position"
            )

            config.pump_volume = st.slider(
                "Pump Volume Multiplier",
                min_value=1,
                max_value=20,
                value=config.pump_volume,
                help="Volume multiplier during pump phase"
            )

    return config


def render_advanced_config(config: SimulationConfig) -> SimulationConfig:
    """
    Render advanced configuration options.

    Args:
        config: Base configuration to modify

    Returns:
        Updated configuration
    """
    with st.sidebar.expander("Advanced Settings", expanded=False):
        config.initial_cash = st.number_input(
            "Trader Initial Cash ($)",
            min_value=1_000,
            max_value=100_000,
            value=int(config.initial_cash),
            step=1_000,
            help="Starting cash for each regular trader"
        )

        config.initial_holdings = st.number_input(
            "Trader Initial Holdings",
            min_value=0,
            max_value=1000,
            value=config.initial_holdings,
            step=10,
            help="Starting asset holdings for each trader"
        )

        config.use_wealth_limit = st.checkbox(
            "Use Wealth Limits",
            value=config.use_wealth_limit,
            help="Enforce wealth constraints on traders"
        )

        config.seed = st.number_input(
            "Random Seed",
            min_value=0,
            max_value=9999,
            value=config.seed or 42,
            help="Seed for reproducible results (0 for random)"
        )

        if config.seed == 0:
            config.seed = None

    return config


def render_config_panel() -> SimulationConfig:
    """
    Render complete configuration panel in sidebar.

    Returns:
        Complete SimulationConfig
    """
    st.sidebar.header("Configuration")

    # Preset selector
    preset_config = render_preset_selector()

    st.sidebar.markdown("---")

    # Basic config
    config = render_basic_config(preset_config)

    # Manipulator config
    config = render_manipulator_config(config)

    st.sidebar.markdown("---")

    # Advanced config
    config = render_advanced_config(config)

    return config


def save_config(config: SimulationConfig, name: str = "config"):
    """Save configuration to session state."""
    if 'saved_configs' not in st.session_state:
        st.session_state.saved_configs = {}

    st.session_state.saved_configs[name] = config.to_dict()


def load_config(name: str) -> Optional[SimulationConfig]:
    """Load configuration from session state."""
    if 'saved_configs' not in st.session_state:
        return None

    config_dict = st.session_state.saved_configs.get(name)
    if config_dict:
        return SimulationConfig.from_dict(config_dict)

    return None


def render_save_load_ui():
    """Render save/load configuration UI."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Save/Load Config")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        config_name = st.text_input(
            "Config Name",
            value="my_config",
            key="config_name_input",
            label_visibility="collapsed"
        )

    with col2:
        if st.button("Save", use_container_width=True):
            if 'current_config' in st.session_state:
                save_config(st.session_state.current_config, config_name)
                st.sidebar.success(f"Saved '{config_name}'")

    # Load configs
    if 'saved_configs' in st.session_state and st.session_state.saved_configs:
        saved_names = list(st.session_state.saved_configs.keys())
        selected_config = st.sidebar.selectbox(
            "Load Configuration",
            [""] + saved_names,
            key="load_config_select"
        )

        if selected_config:
            loaded = load_config(selected_config)
            if loaded:
                st.session_state.current_config = loaded
                st.sidebar.success(f"Loaded '{selected_config}'")
                st.experimental_rerun()


def export_config_json(config: SimulationConfig) -> str:
    """Export configuration as JSON string."""
    return json.dumps(config.to_dict(), indent=2)


def import_config_json(json_str: str) -> Optional[SimulationConfig]:
    """Import configuration from JSON string."""
    try:
        data = json.loads(json_str)
        return SimulationConfig.from_dict(data)
    except Exception as e:
        st.error(f"Error importing config: {e}")
        return None


__all__ = [
    "SimulationConfig",
    "PRESETS",
    "render_config_panel",
    "render_save_load_ui",
    "save_config",
    "load_config",
    "export_config_json",
    "import_config_json",
]
