"""Input validation utilities for service logic."""
from __future__ import annotations

from typing import Dict, List, Tuple


def validate_input(metrics: Dict[str, float]) -> Tuple[bool, List[str]]:
    """Validate that metrics are present and numeric.

    Args:
        metrics: Mapping of metric names to numeric values between 0 and 1.

    Returns:
        A tuple of (is_valid, errors).
    """

    errors: List[str] = []
    if not metrics:
        errors.append("At least one metric is required.")
        return False, errors

    for key, value in metrics.items():
        if not isinstance(value, (int, float)):
            errors.append(f"Metric '{key}' must be numeric.")
            continue
        if value < 0 or value > 1:
            errors.append(f"Metric '{key}' must be between 0 and 1.")

    return len(errors) == 0, errors
