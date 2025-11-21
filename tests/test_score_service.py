import pytest

from src.services.score_service import ScoreComputationError, compute_score


def test_compute_score_returns_average_and_status():
    result = compute_score({"accuracy": 0.8, "latency": 0.6}, threshold=0.7)

    assert result["score"] == 0.7
    assert result["status"] == "pass"


def test_compute_score_handles_review_status():
    result = compute_score({"accuracy": 0.3, "latency": 0.2}, threshold=0.6)

    assert result["score"] == 0.25
    assert result["status"] == "review"


def test_compute_score_requires_metrics():
    with pytest.raises(ScoreComputationError):
        compute_score({}, threshold=0.5)
