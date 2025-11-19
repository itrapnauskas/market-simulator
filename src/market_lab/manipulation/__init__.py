"""Market manipulation strategies and detection tools."""

from .detection import *
from .layering import *
from .manipulator import *
from .metrics import *
from .spoofing import *
from .wash_trading import *

__all__ = [
    # Detection
    "detect_manipulation",
    # Metrics
    "calculate_manipulation_metrics",
    # Manipulators
    "Manipulator",
    "SpoofingManipulator",
    "WashTradingManipulator",
    "LayeringManipulator",
]
