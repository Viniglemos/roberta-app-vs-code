"""Core scoring logic used by the API endpoints."""
from __future__ import annotations

from typing import Dict


class ScoreComputationError(ValueError):
    """Raised when scoring cannot be performed."""


def compute_score(metrics: Dict[str, float], threshold: float) -> Dict[str, float | str]:
    """Compute an aggregate score from the provided metrics.

    Args:
        metrics: Mapping of metric names to normalized numeric values.
        threshold: Score boundary that determines the status label.

    Returns:
        A dictionary with the numeric score and derived status.
    """

    if not metrics:
        raise ScoreComputationError("Metrics are required to compute a score.")

    total = sum(metrics.values())
    score = round(total / len(metrics), 3)
    status = "pass" if score >= threshold else "review"
    return {"score": score, "status": status}
