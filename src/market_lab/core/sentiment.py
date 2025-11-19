"""Sentiment curve helpers."""

from __future__ import annotations

from dataclasses import dataclass


class SentimentCurve:
    """Interface for objects that provide a daily sentiment adjustment."""

    def value_at(self, day: int) -> float:  # pragma: no cover - interface
        """
        Retorna o ajuste de sentimento para um determinado dia.

        Args:
            day: Número do dia da simulação (começando em 0)

        Returns:
            Valor de ajuste a ser aplicado ao preço base
        """
        raise NotImplementedError


@dataclass(slots=True)
class NoSentiment(SentimentCurve):
    """Always returns zero sentiment."""

    def value_at(self, day: int) -> float:
        """
        Retorna sentimento neutro (zero) para qualquer dia.

        Args:
            day: Número do dia da simulação

        Returns:
            Sempre 0.0 (sem ajuste de sentimento)
        """
        return 0.0


@dataclass(slots=True)
class StepSentiment(SentimentCurve):
    """Adds a constant offset starting from a particular day."""

    start_day: int
    magnitude: float

    def value_at(self, day: int) -> float:
        """
        Retorna um ajuste constante a partir de um dia específico.

        Implementa uma função degrau: zero antes do start_day e magnitude
        constante a partir do start_day (inclusive).

        Args:
            day: Número do dia da simulação

        Returns:
            magnitude se day >= start_day, caso contrário 0.0

        Example:
            >>> sentiment = StepSentiment(start_day=10, magnitude=5.0)
            >>> sentiment.value_at(9)
            0.0
            >>> sentiment.value_at(10)
            5.0
        """
        return self.magnitude if day >= self.start_day else 0.0


@dataclass(slots=True)
class PulseSentiment(SentimentCurve):
    """Applies a temporary spike in sentiment for a fixed duration."""

    center_day: int
    width: int
    magnitude: float

    def value_at(self, day: int) -> float:
        """
        Retorna um pulso de sentimento centrado em um dia específico.

        Implementa uma janela retangular de sentimento: magnitude dentro da
        janela de width dias centrada em center_day, zero fora dela.

        Args:
            day: Número do dia da simulação

        Returns:
            magnitude se day estiver dentro da janela [center_day - width//2,
            center_day + width//2], caso contrário 0.0

        Example:
            >>> sentiment = PulseSentiment(center_day=15, width=4, magnitude=10.0)
            >>> sentiment.value_at(13)  # 15 - 4//2 = 13
            10.0
            >>> sentiment.value_at(17)  # 15 + 4//2 = 17
            10.0
            >>> sentiment.value_at(18)
            0.0
        """
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
