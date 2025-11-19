"""Quantitative helpers used by detection functions."""

from __future__ import annotations

from typing import Iterable, List


def rolling_zscore(values: Iterable[float], window: int = 10) -> list[float]:
    """Return z-scores computed over a sliding window."""

    series = list(values)
    if not series:
        return []
    zscores: List[float] = [0.0 for _ in series]
    for idx in range(len(series)):
        start = max(0, idx - window + 1)
        window_slice = series[start : idx + 1]
        mean = sum(window_slice) / len(window_slice)
        if len(window_slice) > 1:
            variance = sum((value - mean) ** 2 for value in window_slice) / (len(window_slice) - 1)
            std = variance**0.5
        else:
            std = 0.0
        if std == 0:
            zscores[idx] = 0.0
        else:
            zscores[idx] = (series[idx] - mean) / std
    return zscores


def band_distance(series: Iterable[float], *, lower: Iterable[float], upper: Iterable[float]) -> list[float]:
    """Measure how far values are from a reference band."""

    values = list(series)
    low = list(lower)
    up = list(upper)
    if not (len(values) == len(low) == len(up)):
        raise ValueError("Input series must share the same length")
    distance: List[float] = [0.0 for _ in values]
    for idx, val in enumerate(values):
        if val < low[idx]:
            distance[idx] = low[idx] - val
        elif val > up[idx]:
            distance[idx] = val - up[idx]
        else:
            distance[idx] = 0.0
    return distance


__all__ = ["rolling_zscore", "band_distance"]
