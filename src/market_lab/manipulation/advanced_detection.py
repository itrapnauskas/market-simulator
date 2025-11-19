"""Advanced machine learning and statistical methods for manipulation detection.

This module provides sophisticated anomaly detection algorithms that complement
the basic statistical methods in detection.py. All detectors return normalized
scores in the range [0, 1] where higher values indicate stronger manipulation signals.

Features:
- Optional sklearn integration with graceful fallbacks
- Multivariate anomaly detection
- Statistical significance testing
- Time-series pattern analysis
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Sequence

from ..core.market import MarketState

# Optional dependencies with graceful fallback
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler

    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


@dataclass(slots=True)
class DetectionResult:
    """Container for anomaly detection results."""

    scores: list[float]  # Per-observation anomaly scores [0, 1]
    is_anomaly: list[bool]  # Binary classification
    confidence: float  # Overall detection confidence [0, 1]
    method: str  # Detection method used
    metadata: dict  # Additional method-specific info


class IsolationForestDetector:
    """Multivariate anomaly detection using Isolation Forest algorithm.

    Isolation Forest is particularly effective for detecting market manipulation
    because it identifies observations that are "easy to isolate" - i.e., they
    require fewer random splits in a decision tree. This captures complex
    interactions between price, volume, imbalance, and volatility that simple
    univariate methods miss.

    If sklearn is not available, falls back to a simple multivariate z-score method.

    Features analyzed:
    - Price movements
    - Trading volume
    - Order imbalance (buy/sell ratio)
    - Intraday volatility

    Parameters
    ----------
    contamination : float, default=0.1
        Expected proportion of anomalies in the dataset (0.0 to 0.5)
    random_state : int | None, default=42
        Random seed for reproducibility
    n_estimators : int, default=100
        Number of isolation trees (sklearn only)

    Examples
    --------
    >>> detector = IsolationForestDetector(contamination=0.05)
    >>> result = detector.detect(market_states)
    >>> suspicious_days = [s.day for s, is_anom in zip(market_states, result.is_anomaly) if is_anom]
    """

    def __init__(
        self,
        contamination: float = 0.1,
        random_state: int | None = 42,
        n_estimators: int = 100,
    ):
        """Initialize the Isolation Forest detector."""
        self.contamination = max(0.0, min(0.5, contamination))
        self.random_state = random_state
        self.n_estimators = n_estimators
        self._model = None
        self._scaler = None

    def _extract_features(self, states: Sequence[MarketState]) -> list[list[float]]:
        """Extract multivariate features from market states.

        Returns
        -------
        features : list[list[float]]
            Each row contains [price_change, volume, imbalance, volatility]
        """
        features = []
        for i, state in enumerate(states):
            # Price change
            price_change = 0.0 if i == 0 else (state.price - states[i - 1].price) / states[i - 1].price

            # Volume
            volume = state.volume

            # Order imbalance (if available)
            imbalance = 0.0
            if state.order_curves is not None:
                buy_curve = state.order_curves.buy_curve
                sell_curve = state.order_curves.sell_curve
                if buy_curve and sell_curve:
                    total_buy = sum(buy_curve)
                    total_sell = sum(sell_curve)
                    total = total_buy + total_sell
                    imbalance = (total_buy - total_sell) / total if total > 0 else 0.0

            # Volatility proxy (absolute price change)
            volatility = abs(price_change)

            features.append([price_change, volume, imbalance, volatility])

        return features

    def detect(self, states: Sequence[MarketState]) -> DetectionResult:
        """Detect anomalies in market states.

        Parameters
        ----------
        states : Sequence[MarketState]
            Sequence of market observations to analyze

        Returns
        -------
        DetectionResult
            Contains anomaly scores, classifications, and metadata
        """
        if not states:
            return DetectionResult(
                scores=[],
                is_anomaly=[],
                confidence=0.0,
                method="isolation_forest",
                metadata={"error": "empty_input"},
            )

        features = self._extract_features(states)

        if HAS_SKLEARN:
            return self._detect_sklearn(features)
        else:
            return self._detect_fallback(features)

    def _detect_sklearn(self, features: list[list[float]]) -> DetectionResult:
        """Sklearn-based isolation forest detection."""
        # Standardize features
        self._scaler = StandardScaler()
        features_scaled = self._scaler.fit_transform(features)

        # Fit isolation forest
        self._model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
            n_estimators=self.n_estimators,
        )
        predictions = self._model.fit_predict(features_scaled)

        # Get anomaly scores (negative = anomaly, positive = normal)
        raw_scores = self._model.score_samples(features_scaled)

        # Normalize scores to [0, 1] where 1 = most anomalous
        min_score = min(raw_scores)
        max_score = max(raw_scores)
        if max_score - min_score > 0:
            normalized_scores = [1.0 - (s - min_score) / (max_score - min_score) for s in raw_scores]
        else:
            normalized_scores = [0.5] * len(raw_scores)

        # Binary classification (-1 = anomaly, 1 = normal)
        is_anomaly = [pred == -1 for pred in predictions]

        # Compute confidence based on score distribution
        anomaly_scores = [s for s, is_anom in zip(normalized_scores, is_anomaly) if is_anom]
        confidence = sum(anomaly_scores) / len(anomaly_scores) if anomaly_scores else 0.0

        return DetectionResult(
            scores=normalized_scores,
            is_anomaly=is_anomaly,
            confidence=confidence,
            method="isolation_forest_sklearn",
            metadata={
                "n_estimators": self.n_estimators,
                "contamination": self.contamination,
                "n_anomalies": sum(is_anomaly),
            },
        )

    def _detect_fallback(self, features: list[list[float]]) -> DetectionResult:
        """Fallback method using multivariate Mahalanobis-like distance."""
        n = len(features)
        n_features = len(features[0]) if features else 0

        if n < 2 or n_features == 0:
            return DetectionResult(
                scores=[0.0] * n,
                is_anomaly=[False] * n,
                confidence=0.0,
                method="isolation_forest_fallback",
                metadata={"error": "insufficient_data"},
            )

        # Compute feature-wise mean and std
        means = [sum(row[i] for row in features) / n for i in range(n_features)]
        stds = []
        for i in range(n_features):
            variance = sum((row[i] - means[i]) ** 2 for row in features) / max(1, n - 1)
            stds.append(math.sqrt(variance) if variance > 0 else 1.0)

        # Compute Euclidean distance in standardized space
        distances = []
        for row in features:
            dist_squared = sum(((row[i] - means[i]) / stds[i]) ** 2 for i in range(n_features))
            distances.append(math.sqrt(dist_squared))

        # Normalize to [0, 1]
        max_dist = max(distances) if distances else 1.0
        normalized_scores = [d / max_dist if max_dist > 0 else 0.0 for d in distances]

        # Threshold at expected contamination level
        threshold = sorted(normalized_scores, reverse=True)[int(n * self.contamination)] if n > 0 else 0.5
        is_anomaly = [score >= threshold for score in normalized_scores]

        anomaly_scores = [s for s, is_anom in zip(normalized_scores, is_anomaly) if is_anom]
        confidence = sum(anomaly_scores) / len(anomaly_scores) if anomaly_scores else 0.0

        return DetectionResult(
            scores=normalized_scores,
            is_anomaly=is_anomaly,
            confidence=confidence,
            method="isolation_forest_fallback",
            metadata={
                "contamination": self.contamination,
                "n_anomalies": sum(is_anomaly),
                "threshold": threshold,
            },
        )


class BenfordLawDetector:
    """Detect artificial volume patterns using Benford's Law.

    Benford's Law states that in many naturally occurring datasets, the leading
    digit is more likely to be small. For example, "1" appears as the leading
    digit about 30% of the time, while "9" appears only 5% of the time.

    This detector applies Benford's Law to trading volumes. Manipulated or
    fabricated volumes often violate this distribution, showing either too uniform
    or too clustered leading digits.

    The detector uses chi-squared test to measure statistical significance.

    Parameters
    ----------
    significance_level : float, default=0.05
        P-value threshold for rejecting the null hypothesis (volume follows Benford)
    min_samples : int, default=30
        Minimum samples required for reliable statistical test

    References
    ----------
    - Benford, F. (1938). "The Law of Anomalous Numbers"
    - Nigrini, M. J. (2012). "Benford's Law: Applications for Forensic Accounting"

    Examples
    --------
    >>> detector = BenfordLawDetector()
    >>> result = detector.detect(market_states)
    >>> if result.confidence > 0.7:
    ...     print("Warning: Volume distribution violates Benford's Law")
    """

    # Expected frequencies for leading digits according to Benford's Law
    BENFORD_EXPECTED = {
        1: 0.301,
        2: 0.176,
        3: 0.125,
        4: 0.097,
        5: 0.079,
        6: 0.067,
        7: 0.058,
        8: 0.051,
        9: 0.046,
    }

    def __init__(self, significance_level: float = 0.05, min_samples: int = 30):
        """Initialize Benford's Law detector."""
        self.significance_level = significance_level
        self.min_samples = min_samples

    def _get_leading_digit(self, value: float) -> int | None:
        """Extract the leading digit from a number."""
        if value <= 0:
            return None
        # Convert to scientific notation and extract first digit
        abs_val = abs(value)
        while abs_val >= 10:
            abs_val /= 10
        while abs_val < 1 and abs_val > 0:
            abs_val *= 10
        return int(abs_val)

    def _chi_squared_test(self, observed: dict[int, int], total: int) -> tuple[float, float]:
        """Perform chi-squared test against Benford's Law.

        Returns
        -------
        chi_squared : float
            Chi-squared test statistic
        p_value_proxy : float
            Approximation of p-value (simplified for no scipy dependency)
        """
        chi_squared = 0.0
        for digit in range(1, 10):
            expected_freq = self.BENFORD_EXPECTED[digit] * total
            observed_freq = observed.get(digit, 0)
            if expected_freq > 0:
                chi_squared += ((observed_freq - expected_freq) ** 2) / expected_freq

        # Degrees of freedom = 9 - 1 = 8
        # Critical value at α=0.05 for df=8 is approximately 15.51
        # This is a simplified approximation without scipy
        critical_value = 15.51
        p_value_proxy = 1.0 if chi_squared < critical_value else 0.0

        return chi_squared, p_value_proxy

    def detect(self, states: Sequence[MarketState]) -> DetectionResult:
        """Detect Benford's Law violations in trading volumes.

        Parameters
        ----------
        states : Sequence[MarketState]
            Market observations to analyze

        Returns
        -------
        DetectionResult
            Anomaly scores and Benford analysis results
        """
        if len(states) < self.min_samples:
            return DetectionResult(
                scores=[0.0] * len(states),
                is_anomaly=[False] * len(states),
                confidence=0.0,
                method="benford_law",
                metadata={"error": "insufficient_samples", "min_required": self.min_samples},
            )

        # Extract leading digits from volumes
        leading_digits = []
        for state in states:
            digit = self._get_leading_digit(state.volume)
            if digit is not None:
                leading_digits.append(digit)

        if not leading_digits:
            return DetectionResult(
                scores=[0.0] * len(states),
                is_anomaly=[False] * len(states),
                confidence=0.0,
                method="benford_law",
                metadata={"error": "no_valid_volumes"},
            )

        # Count frequency of each leading digit
        observed = Counter(leading_digits)
        total = len(leading_digits)

        # Perform chi-squared test
        chi_squared, p_value_proxy = self._chi_squared_test(observed, total)

        # Compute deviation from Benford for each observation
        scores = []
        for state in states:
            digit = self._get_leading_digit(state.volume)
            if digit is not None:
                observed_freq = observed[digit] / total
                expected_freq = self.BENFORD_EXPECTED[digit]
                # Normalized absolute deviation
                deviation = abs(observed_freq - expected_freq) / expected_freq
                score = min(1.0, deviation)
            else:
                score = 0.0
            scores.append(score)

        # Overall violation detected if p-value is low
        is_violation = p_value_proxy < self.significance_level
        is_anomaly = [is_violation] * len(states)  # Same for all if distribution is off

        # Confidence based on chi-squared magnitude
        # Higher chi-squared = more confident in violation
        confidence = min(1.0, chi_squared / 20.0) if is_violation else 0.0

        # Calculate observed vs expected frequencies for reporting
        freq_analysis = {}
        for digit in range(1, 10):
            freq_analysis[digit] = {
                "observed": observed.get(digit, 0) / total if total > 0 else 0.0,
                "expected": self.BENFORD_EXPECTED[digit],
            }

        return DetectionResult(
            scores=scores,
            is_anomaly=is_anomaly,
            confidence=confidence,
            method="benford_law",
            metadata={
                "chi_squared": chi_squared,
                "p_value_proxy": p_value_proxy,
                "is_violation": is_violation,
                "n_samples": total,
                "frequency_analysis": freq_analysis,
            },
        )


class VolumeProfileAnalyzer:
    """Analyze intraday volume profiles for suspicious patterns.

    This detector examines the temporal distribution of trading volume to identify
    abnormal patterns that may indicate manipulation, such as:
    - Concentrated volume at market open/close (painting the tape)
    - Unusual volume spikes during low-liquidity periods
    - Repetitive volume patterns (wash trading)

    The analyzer clusters volume behaviors and identifies outliers.

    Parameters
    ----------
    n_clusters : int, default=3
        Number of volume behavior clusters (low, normal, high activity)
    window_size : int, default=5
        Rolling window for pattern detection
    spike_threshold : float, default=2.5
        Z-score threshold for volume spike detection

    Examples
    --------
    >>> analyzer = VolumeProfileAnalyzer(spike_threshold=3.0)
    >>> result = analyzer.detect(market_states)
    >>> suspicious = [i for i, score in enumerate(result.scores) if score > 0.8]
    """

    def __init__(
        self,
        n_clusters: int = 3,
        window_size: int = 5,
        spike_threshold: float = 2.5,
    ):
        """Initialize volume profile analyzer."""
        self.n_clusters = n_clusters
        self.window_size = window_size
        self.spike_threshold = spike_threshold

    def _compute_volume_features(self, states: Sequence[MarketState]) -> list[dict]:
        """Extract volume profile features for each state."""
        features = []
        volumes = [s.volume for s in states]

        for i, state in enumerate(states):
            # Rolling statistics
            start_idx = max(0, i - self.window_size + 1)
            window_volumes = volumes[start_idx : i + 1]

            mean_vol = sum(window_volumes) / len(window_volumes)
            if len(window_volumes) > 1:
                var_vol = sum((v - mean_vol) ** 2 for v in window_volumes) / (len(window_volumes) - 1)
                std_vol = math.sqrt(var_vol)
            else:
                std_vol = 0.0

            # Z-score
            z_score = (state.volume - mean_vol) / std_vol if std_vol > 0 else 0.0

            # Velocity (rate of change)
            velocity = 0.0
            if i > 0:
                velocity = (state.volume - volumes[i - 1]) / (volumes[i - 1] + 1e-9)

            # Acceleration (second derivative)
            acceleration = 0.0
            if i > 1:
                prev_velocity = (volumes[i - 1] - volumes[i - 2]) / (volumes[i - 2] + 1e-9)
                acceleration = velocity - prev_velocity

            features.append(
                {
                    "volume": state.volume,
                    "z_score": z_score,
                    "velocity": velocity,
                    "acceleration": acceleration,
                    "mean": mean_vol,
                    "std": std_vol,
                }
            )

        return features

    def _simple_kmeans_1d(self, values: list[float], k: int, max_iter: int = 10) -> list[int]:
        """Simple 1D k-means clustering (fallback without sklearn)."""
        if not values or k <= 0:
            return [0] * len(values)

        # Initialize centroids with quantiles
        sorted_vals = sorted(values)
        step = len(sorted_vals) // k
        centroids = [sorted_vals[min(i * step, len(sorted_vals) - 1)] for i in range(k)]

        labels = [0] * len(values)

        for _ in range(max_iter):
            # Assign to nearest centroid
            new_labels = []
            for val in values:
                distances = [abs(val - c) for c in centroids]
                new_labels.append(distances.index(min(distances)))

            # Update centroids
            new_centroids = []
            for cluster_id in range(k):
                cluster_vals = [v for v, label in zip(values, new_labels) if label == cluster_id]
                if cluster_vals:
                    new_centroids.append(sum(cluster_vals) / len(cluster_vals))
                else:
                    new_centroids.append(centroids[cluster_id])

            # Check convergence
            if new_labels == labels:
                break

            labels = new_labels
            centroids = new_centroids

        return labels

    def detect(self, states: Sequence[MarketState]) -> DetectionResult:
        """Detect suspicious volume patterns.

        Parameters
        ----------
        states : Sequence[MarketState]
            Market observations to analyze

        Returns
        -------
        DetectionResult
            Volume pattern anomaly scores and analysis
        """
        if len(states) < self.window_size:
            return DetectionResult(
                scores=[0.0] * len(states),
                is_anomaly=[False] * len(states),
                confidence=0.0,
                method="volume_profile",
                metadata={"error": "insufficient_data"},
            )

        features = self._compute_volume_features(states)

        # Detect volume spikes using z-score
        spike_scores = [min(1.0, abs(f["z_score"]) / self.spike_threshold) for f in features]

        # Cluster volume levels
        volumes = [f["volume"] for f in features]
        cluster_labels = self._simple_kmeans_1d(volumes, self.n_clusters)

        # Detect cluster transitions (unusual volume regime changes)
        transition_scores = []
        for i in range(len(cluster_labels)):
            if i == 0:
                transition_scores.append(0.0)
            else:
                # Penalize frequent cluster changes
                change = 1.0 if cluster_labels[i] != cluster_labels[i - 1] else 0.0
                transition_scores.append(change)

        # Detect acceleration anomalies (sudden volume changes)
        accelerations = [abs(f["acceleration"]) for f in features]
        max_accel = max(accelerations) if accelerations else 1.0
        accel_scores = [a / max_accel if max_accel > 0 else 0.0 for a in accelerations]

        # Combine scores (weighted average)
        combined_scores = []
        for spike, transition, accel in zip(spike_scores, transition_scores, accel_scores):
            combined = 0.5 * spike + 0.3 * accel + 0.2 * transition
            combined_scores.append(min(1.0, combined))

        # Identify anomalies (top 10% by default)
        threshold = sorted(combined_scores, reverse=True)[len(combined_scores) // 10] if combined_scores else 0.5
        is_anomaly = [score >= threshold for score in combined_scores]

        # Confidence based on number and magnitude of anomalies
        anomaly_scores = [s for s, is_anom in zip(combined_scores, is_anomaly) if is_anom]
        confidence = sum(anomaly_scores) / len(anomaly_scores) if anomaly_scores else 0.0

        # Pattern analysis
        spike_count = sum(1 for s in spike_scores if s > 0.8)
        transition_count = sum(transition_scores)

        return DetectionResult(
            scores=combined_scores,
            is_anomaly=is_anomaly,
            confidence=confidence,
            method="volume_profile",
            metadata={
                "n_spikes": spike_count,
                "n_transitions": int(transition_count),
                "n_clusters": self.n_clusters,
                "spike_threshold": self.spike_threshold,
                "anomaly_threshold": threshold,
            },
        )


class NetworkAnalyzer:
    """Analyze trading patterns to detect collusion and coordinated manipulation.

    This detector examines the temporal correlation and synchronization of trades
    to identify potential collusion between manipulators. While we don't have
    explicit trader identity in MarketState, we can infer coordination patterns from:

    - Synchronized volume spikes
    - Correlated price movements
    - Repetitive patterns suggesting coordination

    This is a simplified network analysis that doesn't require explicit graph libraries.

    Parameters
    ----------
    correlation_window : int, default=10
        Window size for computing temporal correlations
    sync_threshold : float, default=0.7
        Correlation threshold for detecting synchronization
    pattern_memory : int, default=20
        Number of past observations to check for repetitive patterns

    Examples
    --------
    >>> analyzer = NetworkAnalyzer(sync_threshold=0.8)
    >>> result = analyzer.detect(market_states)
    >>> if result.confidence > 0.6:
    ...     print("Potential coordinated manipulation detected")
    """

    def __init__(
        self,
        correlation_window: int = 10,
        sync_threshold: float = 0.7,
        pattern_memory: int = 20,
    ):
        """Initialize network analyzer."""
        self.correlation_window = correlation_window
        self.sync_threshold = sync_threshold
        self.pattern_memory = pattern_memory

    def _compute_correlation(self, series1: list[float], series2: list[float]) -> float:
        """Compute Pearson correlation coefficient between two series."""
        n = min(len(series1), len(series2))
        if n < 2:
            return 0.0

        mean1 = sum(series1[:n]) / n
        mean2 = sum(series2[:n]) / n

        numerator = sum((series1[i] - mean1) * (series2[i] - mean2) for i in range(n))
        denom1 = math.sqrt(sum((series1[i] - mean1) ** 2 for i in range(n)))
        denom2 = math.sqrt(sum((series2[i] - mean2) ** 2 for i in range(n)))

        if denom1 == 0 or denom2 == 0:
            return 0.0

        return numerator / (denom1 * denom2)

    def _detect_pattern_repetition(self, values: list[float], current_idx: int) -> float:
        """Detect if current pattern has appeared before (wash trading indicator)."""
        if current_idx < 3:
            return 0.0

        # Create a simple pattern signature (last 3 values normalized)
        pattern_len = 3
        if current_idx < pattern_len:
            return 0.0

        current_pattern = values[current_idx - pattern_len + 1 : current_idx + 1]
        if not current_pattern or len(current_pattern) < pattern_len:
            return 0.0

        # Normalize pattern
        pattern_mean = sum(current_pattern) / len(current_pattern)
        pattern_std = math.sqrt(sum((v - pattern_mean) ** 2 for v in current_pattern) / len(current_pattern))
        if pattern_std == 0:
            pattern_std = 1.0

        norm_pattern = [(v - pattern_mean) / pattern_std for v in current_pattern]

        # Look for similar patterns in history
        max_similarity = 0.0
        lookback = min(self.pattern_memory, current_idx - pattern_len)

        for i in range(max(0, current_idx - lookback), current_idx - pattern_len):
            hist_pattern = values[i : i + pattern_len]
            if len(hist_pattern) != pattern_len:
                continue

            hist_mean = sum(hist_pattern) / len(hist_pattern)
            hist_std = math.sqrt(sum((v - hist_mean) ** 2 for v in hist_pattern) / len(hist_pattern))
            if hist_std == 0:
                hist_std = 1.0

            norm_hist = [(v - hist_mean) / hist_std for v in hist_pattern]

            # Compute similarity (inverse of Euclidean distance)
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(norm_pattern, norm_hist)))
            similarity = 1.0 / (1.0 + dist)
            max_similarity = max(max_similarity, similarity)

        return max_similarity

    def detect(self, states: Sequence[MarketState]) -> DetectionResult:
        """Detect coordinated trading patterns.

        Parameters
        ----------
        states : Sequence[MarketState]
            Market observations to analyze

        Returns
        -------
        DetectionResult
            Coordination scores and network analysis results
        """
        if len(states) < self.correlation_window:
            return DetectionResult(
                scores=[0.0] * len(states),
                is_anomaly=[False] * len(states),
                confidence=0.0,
                method="network_analysis",
                metadata={"error": "insufficient_data"},
            )

        prices = [s.price for s in states]
        volumes = [s.volume for s in states]

        # Compute rolling correlation between price and volume changes
        correlation_scores = []
        for i in range(len(states)):
            if i < self.correlation_window:
                correlation_scores.append(0.0)
                continue

            window_prices = prices[i - self.correlation_window + 1 : i + 1]
            window_volumes = volumes[i - self.correlation_window + 1 : i + 1]

            # Compute changes
            price_changes = [window_prices[j] - window_prices[j - 1] for j in range(1, len(window_prices))]
            volume_changes = [window_volumes[j] - window_volumes[j - 1] for j in range(1, len(window_volumes))]

            # High correlation suggests synchronized manipulation
            correlation = abs(self._compute_correlation(price_changes, volume_changes))
            correlation_scores.append(correlation)

        # Detect repetitive patterns (wash trading)
        pattern_scores = [self._detect_pattern_repetition(volumes, i) for i in range(len(states))]

        # Detect synchronized spikes (coordinated action)
        sync_scores = []
        for i in range(len(states)):
            if i < 2:
                sync_scores.append(0.0)
                continue

            # Check if both price and volume spike simultaneously
            price_change = abs(prices[i] - prices[i - 1]) / (prices[i - 1] + 1e-9)
            volume_change = abs(volumes[i] - volumes[i - 1]) / (volumes[i - 1] + 1e-9)

            # Synchronization = both change significantly
            sync = min(1.0, (price_change + volume_change) / 2.0)
            sync_scores.append(sync)

        # Combine scores
        combined_scores = []
        for corr, pattern, sync in zip(correlation_scores, pattern_scores, sync_scores):
            # Weight: correlation 40%, pattern 30%, sync 30%
            combined = 0.4 * corr + 0.3 * pattern + 0.3 * sync
            combined_scores.append(min(1.0, combined))

        # Detect anomalies based on threshold
        is_anomaly = [score >= self.sync_threshold for score in combined_scores]

        # Confidence based on consistency of high scores
        high_score_periods = sum(1 for s in combined_scores if s >= self.sync_threshold)
        confidence = min(1.0, high_score_periods / len(combined_scores)) if combined_scores else 0.0

        # Additional metrics
        avg_correlation = sum(correlation_scores) / len(correlation_scores) if correlation_scores else 0.0
        max_pattern_similarity = max(pattern_scores) if pattern_scores else 0.0

        return DetectionResult(
            scores=combined_scores,
            is_anomaly=is_anomaly,
            confidence=confidence,
            method="network_analysis",
            metadata={
                "avg_correlation": avg_correlation,
                "max_pattern_similarity": max_pattern_similarity,
                "n_coordinated_periods": high_score_periods,
                "sync_threshold": self.sync_threshold,
            },
        )


def ensemble_detection(
    states: Sequence[MarketState],
    use_isolation_forest: bool = True,
    use_benford: bool = True,
    use_volume_profile: bool = True,
    use_network: bool = True,
) -> DetectionResult:
    """Run multiple detectors and combine their results using ensemble voting.

    This function provides a robust detection pipeline by combining multiple
    independent detection methods. Each detector votes on each observation,
    and the final score is a weighted combination.

    Parameters
    ----------
    states : Sequence[MarketState]
        Market observations to analyze
    use_isolation_forest : bool, default=True
        Enable multivariate anomaly detection
    use_benford : bool, default=True
        Enable Benford's Law analysis
    use_volume_profile : bool, default=True
        Enable volume pattern analysis
    use_network : bool, default=True
        Enable coordination pattern analysis

    Returns
    -------
    DetectionResult
        Combined ensemble detection results

    Examples
    --------
    >>> result = ensemble_detection(market_states)
    >>> critical_days = [s.day for s, score in zip(market_states, result.scores) if score > 0.8]
    """
    if not states:
        return DetectionResult(
            scores=[],
            is_anomaly=[],
            confidence=0.0,
            method="ensemble",
            metadata={"error": "empty_input"},
        )

    results = []
    weights = []
    methods_used = []

    # Isolation Forest - weight 0.30
    if use_isolation_forest:
        detector = IsolationForestDetector(contamination=0.1)
        result = detector.detect(states)
        results.append(result)
        weights.append(0.30)
        methods_used.append("isolation_forest")

    # Benford's Law - weight 0.25
    if use_benford:
        detector = BenfordLawDetector()
        result = detector.detect(states)
        results.append(result)
        weights.append(0.25)
        methods_used.append("benford_law")

    # Volume Profile - weight 0.25
    if use_volume_profile:
        analyzer = VolumeProfileAnalyzer()
        result = analyzer.detect(states)
        results.append(result)
        weights.append(0.25)
        methods_used.append("volume_profile")

    # Network Analysis - weight 0.20
    if use_network:
        analyzer = NetworkAnalyzer()
        result = analyzer.detect(states)
        results.append(result)
        weights.append(0.20)
        methods_used.append("network_analysis")

    if not results:
        return DetectionResult(
            scores=[0.0] * len(states),
            is_anomaly=[False] * len(states),
            confidence=0.0,
            method="ensemble",
            metadata={"error": "no_detectors_enabled"},
        )

    # Normalize weights
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]

    # Combine scores using weighted average
    n_states = len(states)
    combined_scores = [0.0] * n_states

    for result, weight in zip(results, weights):
        for i, score in enumerate(result.scores):
            combined_scores[i] += score * weight

    # Majority voting for binary classification
    is_anomaly = [False] * n_states
    for i in range(n_states):
        votes = sum(1 for result in results if i < len(result.is_anomaly) and result.is_anomaly[i])
        is_anomaly[i] = votes > len(results) / 2

    # Combined confidence (weighted average of individual confidences)
    combined_confidence = sum(r.confidence * w for r, w in zip(results, weights))

    # Collect metadata from all methods
    ensemble_metadata = {
        "methods": methods_used,
        "weights": weights,
        "individual_confidences": {r.method: r.confidence for r in results},
        "individual_metadata": {r.method: r.metadata for r in results},
    }

    return DetectionResult(
        scores=combined_scores,
        is_anomaly=is_anomaly,
        confidence=combined_confidence,
        method="ensemble",
        metadata=ensemble_metadata,
    )


__all__ = [
    "DetectionResult",
    "IsolationForestDetector",
    "BenfordLawDetector",
    "VolumeProfileAnalyzer",
    "NetworkAnalyzer",
    "ensemble_detection",
    "HAS_SKLEARN",
]
