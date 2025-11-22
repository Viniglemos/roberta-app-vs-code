import pytest

from src.services.validation import validate_input


def test_validation_passes_with_valid_metrics():
    is_valid, errors = validate_input({"accuracy": 0.9, "latency": 0.4})

    assert is_valid is True
    assert errors == []


def test_validation_fails_for_missing_metrics():
    is_valid, errors = validate_input({})

    assert is_valid is False
    assert "At least one metric is required." in errors


def test_validation_fails_for_out_of_range_value():
    is_valid, errors = validate_input({"accuracy": 1.2})

    assert is_valid is False
    assert "between 0 and 1" in errors[0]


def test_validation_fails_for_non_numeric_value():
    is_valid, errors = validate_input({"accuracy": "high"})

    assert is_valid is False
    assert "must be numeric" in errors[0]
