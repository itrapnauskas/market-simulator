#!/usr/bin/env python3
"""Demonstration of advanced manipulation detection algorithms.

This script shows how to use the advanced detection algorithms to identify
market manipulation patterns in simulated trading data.
"""

from __future__ import annotations

import random

from market_lab.core.market import MarketState
from market_lab.manipulation.advanced_detection import (
    BenfordLawDetector,
    DetectionResult,
    IsolationForestDetector,
    NetworkAnalyzer,
    VolumeProfileAnalyzer,
    ensemble_detection,
)


def create_synthetic_data(n_days: int = 100, manipulation_period: tuple[int, int] | None = None) -> list[MarketState]:
    """Create synthetic market data with optional manipulation period.

    Parameters
    ----------
    n_days : int
        Total number of trading days to simulate
    manipulation_period : tuple[int, int] | None
        Start and end day of manipulation period. If None, no manipulation.

    Returns
    -------
    list[MarketState]
        Synthetic market states
    """
    random.seed(42)
    states = []

    for day in range(n_days):
        # Check if in manipulation period
        is_manipulated = False
        if manipulation_period is not None:
            is_manipulated = manipulation_period[0] <= day <= manipulation_period[1]

        if is_manipulated:
            # Manipulated market characteristics:
            # - Higher price volatility
            # - Abnormally high volumes (often round numbers - violates Benford)
            # - Coordinated price-volume movements
            price = 100 + random.gauss(0, 15)  # 3x normal volatility

            # Use round numbers for volume (violates Benford's Law)
            if day % 2 == 0:
                volume = random.choice([1000, 2000, 3000, 5000, 10000])
            else:
                volume = random.choice([1500, 2500, 3500, 7500])

            # Add some noise
            volume += random.gauss(0, 50)
        else:
            # Normal market
            price = 100 + random.gauss(0, 5)  # Normal volatility
            volume = 1000 + random.gauss(0, 200)  # Natural volume distribution

        states.append(
            MarketState(
                day=day,
                price=max(1, price),
                volume=max(1, volume),
                sentiment_value=0.0,
            )
        )

    return states


def print_detection_summary(result: DetectionResult, title: str) -> None:
    """Print formatted detection results."""
    print(f"\n{'=' * 70}")
    print(f"{title}")
    print(f"{'=' * 70}")
    print(f"Method:           {result.method}")
    print(f"Confidence:       {result.confidence:.3f}")
    print(f"Anomalies found:  {sum(result.is_anomaly)}/{len(result.scores)}")

    if "error" not in result.metadata:
        print(f"\nMetadata:")
        for key, value in result.metadata.items():
            if key not in ["individual_metadata", "frequency_analysis"]:
                print(f"  {key}: {value}")

    # Show top anomalous days
    anomaly_days = [(i, score) for i, (score, is_anom) in enumerate(zip(result.scores, result.is_anomaly)) if is_anom]
    if anomaly_days:
        print(f"\nTop anomalous days:")
        anomaly_days.sort(key=lambda x: x[1], reverse=True)
        for day, score in anomaly_days[:5]:
            print(f"  Day {day:3d}: score = {score:.3f}")


def main():
    """Run advanced detection demonstration."""
    print("\n" + "=" * 70)
    print("MARKET MANIPULATION DETECTION - ADVANCED ALGORITHMS")
    print("=" * 70)

    # Create datasets
    print("\n📊 Creating synthetic market data...")
    print("  - Normal period: Days 0-69")
    print("  - Manipulation period: Days 70-85")
    print("  - Normal period: Days 86-99")

    states = create_synthetic_data(n_days=100, manipulation_period=(70, 85))

    # Run individual detectors
    print("\n" + "▶" * 35)
    print("RUNNING INDIVIDUAL DETECTORS")
    print("▶" * 35)

    # 1. Isolation Forest
    print("\n[1/4] Running Isolation Forest Detector...")
    iso_detector = IsolationForestDetector(contamination=0.15, random_state=42)
    iso_result = iso_detector.detect(states)
    print_detection_summary(iso_result, "ISOLATION FOREST - Multivariate Anomaly Detection")

    # 2. Benford's Law
    print("\n[2/4] Running Benford's Law Detector...")
    benford_detector = BenfordLawDetector(significance_level=0.05)
    benford_result = benford_detector.detect(states)
    print_detection_summary(benford_result, "BENFORD'S LAW - Volume Distribution Analysis")

    if benford_result.metadata.get("frequency_analysis"):
        print("\n  Leading Digit Distribution:")
        freq = benford_result.metadata["frequency_analysis"]
        print("  Digit | Observed | Expected | Deviation")
        print("  " + "-" * 42)
        for digit in range(1, 10):
            if digit in freq:
                obs = freq[digit]["observed"]
                exp = freq[digit]["expected"]
                dev = abs(obs - exp) / exp * 100
                print(f"    {digit}   |  {obs:6.3f}  |  {exp:6.3f}  | {dev:6.1f}%")

    # 3. Volume Profile
    print("\n[3/4] Running Volume Profile Analyzer...")
    volume_analyzer = VolumeProfileAnalyzer(spike_threshold=2.5, window_size=5)
    volume_result = volume_analyzer.detect(states)
    print_detection_summary(volume_result, "VOLUME PROFILE - Pattern Analysis")

    # 4. Network Analysis
    print("\n[4/4] Running Network Analyzer...")
    network_analyzer = NetworkAnalyzer(correlation_window=10, sync_threshold=0.7)
    network_result = network_analyzer.detect(states)
    print_detection_summary(network_result, "NETWORK ANALYSIS - Coordination Detection")

    # Ensemble detection
    print("\n" + "▶" * 35)
    print("RUNNING ENSEMBLE DETECTION")
    print("▶" * 35)

    ensemble_result = ensemble_detection(
        states,
        use_isolation_forest=True,
        use_benford=True,
        use_volume_profile=True,
        use_network=True,
    )
    print_detection_summary(ensemble_result, "ENSEMBLE - Combined Detection")

    if "individual_confidences" in ensemble_result.metadata:
        print("\n  Individual Method Confidences:")
        for method, conf in ensemble_result.metadata["individual_confidences"].items():
            print(f"    {method:25s}: {conf:.3f}")

    # Summary and recommendations
    print("\n" + "=" * 70)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 70)

    high_risk_days = [i for i, score in enumerate(ensemble_result.scores) if score > 0.7]
    medium_risk_days = [i for i, score in enumerate(ensemble_result.scores) if 0.5 < score <= 0.7]

    print(f"\n🚨 HIGH RISK (score > 0.7):     {len(high_risk_days)} days")
    print(f"⚠️  MEDIUM RISK (0.5-0.7):      {len(medium_risk_days)} days")
    print(f"✓  LOW RISK (< 0.5):            {len(states) - len(high_risk_days) - len(medium_risk_days)} days")

    if ensemble_result.confidence > 0.7:
        print(f"\n⚠️  WARNING: High confidence ({ensemble_result.confidence:.1%}) of systematic manipulation detected!")
        print("   Recommended actions:")
        print("   1. Conduct detailed trade-by-trade analysis")
        print("   2. Review trader identities and patterns")
        print("   3. Consider regulatory investigation")
    elif ensemble_result.confidence > 0.4:
        print(f"\n⚠️  CAUTION: Moderate confidence ({ensemble_result.confidence:.1%}) of suspicious activity")
        print("   Recommended actions:")
        print("   1. Increase monitoring frequency")
        print("   2. Review high-risk days in detail")
    else:
        print(f"\n✓  Market appears normal (confidence: {ensemble_result.confidence:.1%})")

    # Performance notes
    print("\n" + "=" * 70)
    print("PERFORMANCE NOTES")
    print("=" * 70)
    print(f"Sklearn available:     {iso_result.method == 'isolation_forest_sklearn'}")
    print(f"Total days analyzed:   {len(states)}")
    print(f"Detection methods:     {len(ensemble_result.metadata.get('methods', []))}")
    print("\nFor production use, install scikit-learn for improved accuracy:")
    print("  pip install scikit-learn")


if __name__ == "__main__":
    main()
