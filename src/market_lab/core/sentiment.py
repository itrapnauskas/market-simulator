"""Sentiment curve helpers."""

from __future__ import annotations

from dataclasses import dataclass


class SentimentCurve:
    """Interface for objects that provide a daily sentiment adjustment."""

    def value_at(self, day: int) -> float:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass(slots=True)
class NoSentiment(SentimentCurve):
    """Always returns zero sentiment."""

    def value_at(self, day: int) -> float:
        return 0.0


@dataclass(slots=True)
class StepSentiment(SentimentCurve):
    """Adds a constant offset starting from a particular day."""

    start_day: int
    magnitude: float

    def value_at(self, day: int) -> float:
        return self.magnitude if day >= self.start_day else 0.0


@dataclass(slots=True)
class PulseSentiment(SentimentCurve):
    """Applies a temporary spike in sentiment for a fixed duration."""

    center_day: int
    width: int
    magnitude: float

    def value_at(self, day: int) -> float:
        half_width = self.width // 2
        if self.center_day - half_width <= day <= self.center_day + half_width:
            return self.magnitude
        return 0.0


__all__ = [
    "SentimentCurve",
    "NoSentiment",
    "StepSentiment",
    "PulseSentiment",
]
