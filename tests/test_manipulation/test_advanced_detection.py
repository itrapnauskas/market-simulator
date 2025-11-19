"""Unit tests for advanced manipulation detection algorithms."""

from __future__ import annotations

import random

import pytest

from market_lab.core.market import MarketState
from market_lab.manipulation.advanced_detection import (
    BenfordLawDetector,
    DetectionResult,
    IsolationForestDetector,
    NetworkAnalyzer,
    VolumeProfileAnalyzer,
    ensemble_detection,
)


@pytest.fixture
def normal_market_states() -> list[MarketState]:
    """Create normal market states without manipulation."""
    random.seed(42)
    states = []
    for day in range(50):
        price = 100 + random.gauss(0, 2)
        volume = 1000 + random.gauss(0, 100)
        states.append(
            MarketState(
                day=day,
                price=max(1, price),
                volume=max(1, volume),
                sentiment_value=0.0,
            )
        )
    return states


@pytest.fixture
def manipulated_market_states() -> list[MarketState]:
    """Create market states with manipulation in the middle."""
    random.seed(42)
    states = []
    for day in range(100):
        # Manipulation on days 40-60
        if 40 <= day <= 60:
            price = 100 + random.gauss(0, 10)  # Higher volatility
            volume = 5000 + random.gauss(0, 500)  # Abnormal volume
        else:
            price = 100 + random.gauss(0, 2)
            volume = 1000 + random.gauss(0, 100)

        states.append(
            MarketState(
                day=day,
                price=max(1, price),
                volume=max(1, volume),
                sentiment_value=0.0,
            )
        )
    return states


@pytest.fixture
def benford_violating_states() -> list[MarketState]:
    """Create states with volumes that violate Benford's Law."""
    random.seed(42)
    states = []
    # Use mostly round numbers (violates Benford)
    round_volumes = [1000, 2000, 3000, 5000, 10000]

    for day in range(50):
        price = 100 + random.gauss(0, 2)
        volume = random.choice(round_volumes) + random.gauss(0, 10)
        states.append(
            MarketState(
                day=day,
                price=max(1, price),
                volume=max(1, volume),
                sentiment_value=0.0,
            )
        )
    return states


class TestIsolationForestDetector:
    """Tests for Isolation Forest detector."""

    def test_initialization(self):
        """Test detector initialization."""
        detector = IsolationForestDetector(contamination=0.1, random_state=42)
        assert detector.contamination == 0.1
        assert detector.random_state == 42
        assert detector.n_estimators == 100

    def test_contamination_bounds(self):
        """Test contamination parameter is bounded [0, 0.5]."""
        detector = IsolationForestDetector(contamination=-0.1)
        assert detector.contamination == 0.0

        detector = IsolationForestDetector(contamination=0.8)
        assert detector.contamination == 0.5

    def test_detect_normal_market(self, normal_market_states):
        """Test detection on normal market data."""
        detector = IsolationForestDetector(contamination=0.1)
        result = detector.detect(normal_market_states)

        assert isinstance(result, DetectionResult)
        assert len(result.scores) == len(normal_market_states)
        assert len(result.is_anomaly) == len(normal_market_states)
        assert 0.0 <= result.confidence <= 1.0
        assert all(0.0 <= score <= 1.0 for score in result.scores)

    def test_detect_manipulated_market(self, manipulated_market_states):
        """Test detection on manipulated market data."""
        detector = IsolationForestDetector(contamination=0.2)
        result = detector.detect(manipulated_market_states)

        # Should detect some anomalies
        assert sum(result.is_anomaly) > 0
        assert result.confidence > 0.0

        # Scores should be valid
        assert all(0.0 <= score <= 1.0 for score in result.scores)

    def test_detect_empty_input(self):
        """Test detection with empty input."""
        detector = IsolationForestDetector()
        result = detector.detect([])

        assert len(result.scores) == 0
        assert len(result.is_anomaly) == 0
        assert result.confidence == 0.0
        assert "error" in result.metadata

    def test_feature_extraction(self, normal_market_states):
        """Test feature extraction method."""
        detector = IsolationForestDetector()
        features = detector._extract_features(normal_market_states)

        assert len(features) == len(normal_market_states)
        assert all(len(f) == 4 for f in features)  # 4 features per observation
        # Features: [price_change, volume, imbalance, volatility]

    def test_method_name(self, normal_market_states):
        """Test that method name reflects sklearn availability."""
        detector = IsolationForestDetector()
        result = detector.detect(normal_market_states)

        # Method name should indicate which implementation was used
        assert "isolation_forest" in result.method


class TestBenfordLawDetector:
    """Tests for Benford's Law detector."""

    def test_initialization(self):
        """Test detector initialization."""
        detector = BenfordLawDetector(significance_level=0.05, min_samples=30)
        assert detector.significance_level == 0.05
        assert detector.min_samples == 30

    def test_benford_expected_probabilities(self):
        """Test Benford's Law expected probabilities."""
        detector = BenfordLawDetector()
        expected = detector.BENFORD_EXPECTED

        # Should have probabilities for digits 1-9
        assert len(expected) == 9
        assert all(digit in expected for digit in range(1, 10))

        # Probabilities should sum to ~1.0
        assert abs(sum(expected.values()) - 1.0) < 0.001

        # First digit should be most common
        assert expected[1] > expected[9]

    def test_get_leading_digit(self):
        """Test leading digit extraction."""
        detector = BenfordLawDetector()

        assert detector._get_leading_digit(123.45) == 1
        assert detector._get_leading_digit(987.65) == 9
        assert detector._get_leading_digit(42.0) == 4
        assert detector._get_leading_digit(0.056) == 5
        assert detector._get_leading_digit(0.0) is None
        assert detector._get_leading_digit(-0.0) is None

    def test_detect_normal_market(self, normal_market_states):
        """Test detection on normal market data."""
        detector = BenfordLawDetector()
        result = detector.detect(normal_market_states)

        assert isinstance(result, DetectionResult)
        assert len(result.scores) == len(normal_market_states)
        assert 0.0 <= result.confidence <= 1.0

    def test_detect_benford_violation(self, benford_violating_states):
        """Test detection on data violating Benford's Law."""
        detector = BenfordLawDetector()
        result = detector.detect(benford_violating_states)

        # Should detect violation
        assert result.metadata.get("is_violation", False) is True
        assert result.metadata.get("chi_squared", 0) > 15.51  # Critical value

    def test_insufficient_samples(self):
        """Test behavior with insufficient samples."""
        detector = BenfordLawDetector(min_samples=30)
        small_dataset = [
            MarketState(day=i, price=100.0, volume=1000.0, sentiment_value=0.0)
            for i in range(10)
        ]

        result = detector.detect(small_dataset)
        assert "error" in result.metadata
        assert result.confidence == 0.0

    def test_chi_squared_test(self):
        """Test chi-squared statistical test."""
        detector = BenfordLawDetector()

        # Perfect Benford distribution
        observed_perfect = {i: int(detector.BENFORD_EXPECTED[i] * 100) for i in range(1, 10)}
        chi_sq, p_val = detector._chi_squared_test(observed_perfect, 100)

        # Should have low chi-squared (close to expected)
        assert chi_sq < 10.0

    def test_frequency_analysis_metadata(self, benford_violating_states):
        """Test that frequency analysis is included in metadata."""
        detector = BenfordLawDetector()
        result = detector.detect(benford_violating_states)

        assert "frequency_analysis" in result.metadata
        freq = result.metadata["frequency_analysis"]

        # Should have analysis for each digit
        assert len(freq) == 9
        for digit in range(1, 10):
            assert "observed" in freq[digit]
            assert "expected" in freq[digit]


class TestVolumeProfileAnalyzer:
    """Tests for Volume Profile analyzer."""

    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = VolumeProfileAnalyzer(n_clusters=3, window_size=5, spike_threshold=2.5)
        assert analyzer.n_clusters == 3
        assert analyzer.window_size == 5
        assert analyzer.spike_threshold == 2.5

    def test_detect_normal_market(self, normal_market_states):
        """Test analysis on normal market data."""
        analyzer = VolumeProfileAnalyzer()
        result = analyzer.detect(normal_market_states)

        assert isinstance(result, DetectionResult)
        assert len(result.scores) == len(normal_market_states)
        assert 0.0 <= result.confidence <= 1.0

    def test_detect_volume_spikes(self):
        """Test detection of volume spikes."""
        random.seed(42)
        states = []

        for day in range(50):
            # Create a spike on day 25
            if day == 25:
                volume = 10000.0  # Large spike
            else:
                volume = 1000 + random.gauss(0, 50)

            states.append(
                MarketState(
                    day=day,
                    price=100.0,
                    volume=max(1, volume),
                    sentiment_value=0.0,
                )
            )

        analyzer = VolumeProfileAnalyzer(spike_threshold=2.0)
        result = analyzer.detect(states)

        # Day 25 should have high score
        assert result.scores[25] > 0.5

    def test_compute_volume_features(self, normal_market_states):
        """Test volume feature computation."""
        analyzer = VolumeProfileAnalyzer()
        features = analyzer._compute_volume_features(normal_market_states)

        assert len(features) == len(normal_market_states)
        for feat in features:
            assert "volume" in feat
            assert "z_score" in feat
            assert "velocity" in feat
            assert "acceleration" in feat
            assert "mean" in feat
            assert "std" in feat

    def test_simple_kmeans(self):
        """Test simple 1D k-means clustering."""
        analyzer = VolumeProfileAnalyzer()
        values = [1.0, 1.1, 1.2, 5.0, 5.1, 5.2, 10.0, 10.1, 10.2]
        labels = analyzer._simple_kmeans_1d(values, k=3)

        assert len(labels) == len(values)
        assert len(set(labels)) <= 3  # Should have at most 3 clusters

    def test_insufficient_data(self):
        """Test behavior with insufficient data."""
        analyzer = VolumeProfileAnalyzer(window_size=10)
        small_dataset = [
            MarketState(day=i, price=100.0, volume=1000.0, sentiment_value=0.0)
            for i in range(5)
        ]

        result = analyzer.detect(small_dataset)
        assert "error" in result.metadata


class TestNetworkAnalyzer:
    """Tests for Network analyzer."""

    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = NetworkAnalyzer(correlation_window=10, sync_threshold=0.7, pattern_memory=20)
        assert analyzer.correlation_window == 10
        assert analyzer.sync_threshold == 0.7
        assert analyzer.pattern_memory == 20

    def test_detect_normal_market(self, normal_market_states):
        """Test analysis on normal market data."""
        analyzer = NetworkAnalyzer()
        result = analyzer.detect(normal_market_states)

        assert isinstance(result, DetectionResult)
        assert len(result.scores) == len(normal_market_states)
        assert 0.0 <= result.confidence <= 1.0

    def test_compute_correlation(self):
        """Test Pearson correlation computation."""
        analyzer = NetworkAnalyzer()

        # Perfect positive correlation
        series1 = [1.0, 2.0, 3.0, 4.0, 5.0]
        series2 = [2.0, 4.0, 6.0, 8.0, 10.0]
        corr = analyzer._compute_correlation(series1, series2)
        assert abs(corr - 1.0) < 0.001

        # Perfect negative correlation
        series3 = [5.0, 4.0, 3.0, 2.0, 1.0]
        corr = analyzer._compute_correlation(series1, series3)
        assert abs(corr + 1.0) < 0.001

        # No correlation
        series4 = [1.0, 1.0, 1.0, 1.0, 1.0]
        corr = analyzer._compute_correlation(series1, series4)
        assert corr == 0.0

    def test_detect_pattern_repetition(self):
        """Test repetitive pattern detection."""
        analyzer = NetworkAnalyzer(pattern_memory=20)

        # Create repeating pattern
        values = [1.0, 2.0, 3.0] * 10  # Repeats 10 times

        # Later patterns should have high similarity to earlier ones
        similarity = analyzer._detect_pattern_repetition(values, current_idx=15)
        assert similarity > 0.7

    def test_detect_synchronized_manipulation(self):
        """Test detection of synchronized price-volume movements."""
        random.seed(42)
        states = []

        for day in range(50):
            # Synchronized spike on day 25
            if day == 25:
                price = 150.0  # Price spike
                volume = 5000.0  # Volume spike
            else:
                price = 100 + random.gauss(0, 1)
                volume = 1000 + random.gauss(0, 50)

            states.append(
                MarketState(
                    day=day,
                    price=max(1, price),
                    volume=max(1, volume),
                    sentiment_value=0.0,
                )
            )

        analyzer = NetworkAnalyzer()
        result = analyzer.detect(states)

        # Day 25 should have elevated score
        assert result.scores[25] > 0.3

    def test_insufficient_data(self):
        """Test behavior with insufficient data."""
        analyzer = NetworkAnalyzer(correlation_window=20)
        small_dataset = [
            MarketState(day=i, price=100.0, volume=1000.0, sentiment_value=0.0)
            for i in range(10)
        ]

        result = analyzer.detect(small_dataset)
        assert "error" in result.metadata


class TestEnsembleDetection:
    """Tests for ensemble detection."""

    def test_ensemble_all_detectors(self, manipulated_market_states):
        """Test ensemble with all detectors enabled."""
        result = ensemble_detection(
            manipulated_market_states,
            use_isolation_forest=True,
            use_benford=True,
            use_volume_profile=True,
            use_network=True,
        )

        assert result.method == "ensemble"
        assert len(result.scores) == len(manipulated_market_states)
        assert "methods" in result.metadata
        assert len(result.metadata["methods"]) == 4

    def test_ensemble_selective_detectors(self, normal_market_states):
        """Test ensemble with selective detectors."""
        result = ensemble_detection(
            normal_market_states,
            use_isolation_forest=True,
            use_benford=False,
            use_volume_profile=True,
            use_network=False,
        )

        assert len(result.metadata["methods"]) == 2
        assert "isolation_forest" in result.metadata["methods"]
        assert "volume_profile" in result.metadata["methods"]

    def test_ensemble_empty_input(self):
        """Test ensemble with empty input."""
        result = ensemble_detection([])

        assert len(result.scores) == 0
        assert result.confidence == 0.0
        assert "error" in result.metadata

    def test_ensemble_no_detectors(self, normal_market_states):
        """Test ensemble with no detectors enabled."""
        result = ensemble_detection(
            normal_market_states,
            use_isolation_forest=False,
            use_benford=False,
            use_volume_profile=False,
            use_network=False,
        )

        assert "error" in result.metadata

    def test_ensemble_weights_normalized(self, normal_market_states):
        """Test that ensemble weights are normalized."""
        result = ensemble_detection(normal_market_states)

        weights = result.metadata.get("weights", [])
        assert len(weights) > 0
        # Weights should sum to ~1.0
        assert abs(sum(weights) - 1.0) < 0.001

    def test_ensemble_individual_confidences(self, manipulated_market_states):
        """Test that individual detector confidences are tracked."""
        result = ensemble_detection(manipulated_market_states)

        assert "individual_confidences" in result.metadata
        confidences = result.metadata["individual_confidences"]

        # Should have confidence for each method
        assert len(confidences) > 0
        for method, conf in confidences.items():
            assert 0.0 <= conf <= 1.0

    def test_ensemble_majority_voting(self):
        """Test ensemble majority voting for binary classification."""
        random.seed(42)
        states = []

        # Create clear manipulation signal
        for day in range(100):
            if 45 <= day <= 55:
                # Strong manipulation signal
                price = 100 + random.gauss(0, 20)
                volume = 10000 + random.gauss(0, 1000)
            else:
                price = 100 + random.gauss(0, 2)
                volume = 1000 + random.gauss(0, 100)

            states.append(
                MarketState(
                    day=day,
                    price=max(1, price),
                    volume=max(1, volume),
                    sentiment_value=0.0,
                )
            )

        result = ensemble_detection(states)

        # Should detect some anomalies in manipulation period
        manipulation_period_anomalies = sum(result.is_anomaly[45:56])
        assert manipulation_period_anomalies > 0

    def test_ensemble_score_combination(self, normal_market_states):
        """Test that ensemble properly combines scores."""
        result = ensemble_detection(normal_market_states)

        # All scores should be in [0, 1]
        assert all(0.0 <= score <= 1.0 for score in result.scores)

        # Scores should be properly weighted (not just averaged)
        assert len(result.scores) == len(normal_market_states)


class TestDetectionResult:
    """Tests for DetectionResult dataclass."""

    def test_detection_result_creation(self):
        """Test creating DetectionResult instance."""
        result = DetectionResult(
            scores=[0.1, 0.5, 0.9],
            is_anomaly=[False, False, True],
            confidence=0.7,
            method="test_method",
            metadata={"key": "value"},
        )

        assert len(result.scores) == 3
        assert len(result.is_anomaly) == 3
        assert result.confidence == 0.7
        assert result.method == "test_method"
        assert result.metadata["key"] == "value"

    def test_detection_result_consistency(self):
        """Test that scores and is_anomaly have consistent lengths."""
        result = DetectionResult(
            scores=[0.1, 0.5],
            is_anomaly=[False, True],
            confidence=0.5,
            method="test",
            metadata={},
        )

        assert len(result.scores) == len(result.is_anomaly)
