"""FastAPI entrypoint wiring HTTP routes to service functions."""
from __future__ import annotations

from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from src.services.score_service import ScoreComputationError, compute_score
from src.services.validation import validate_input
from src.utils.config import load_settings
from src.utils.logger import get_logger

settings = load_settings()
logger = get_logger(__name__, settings)
app = FastAPI(title="Roberta App Backend")


class ScoreRequest(BaseModel):
    metrics: Dict[str, float] = Field(..., description="Normalized metric values")


class ScoreResponse(BaseModel):
    score: float
    status: str


@app.get("/health")
async def health() -> Dict[str, str]:
    """Simple liveness probe."""

    return {"status": "ok", "environment": settings.environment}


@app.post("/score", response_model=ScoreResponse)
async def score(payload: ScoreRequest) -> ScoreResponse:
    """Compute a score from submitted metrics."""

    is_valid, errors = validate_input(payload.metrics)
    if not is_valid:
        logger.warning("Validation failed", extra={"errors": errors})
        raise HTTPException(status_code=400, detail=errors)

    try:
        result = compute_score(payload.metrics, settings.score_threshold)
    except ScoreComputationError as exc:
        logger.error("Failed to compute score", exc_info=exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    logger.info("Score computed", extra=result)
    return ScoreResponse(**result)


if __name__ == "__main__":
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=False)
