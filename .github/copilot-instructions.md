<!-- Copilot instructions for AI coding agents working on this repo -->
# Roberta App — Copilot Instructions

Purpose: give an AI code agent the minimal, actionable context to be productive immediately.

- **Big picture**: This repository exposes a small HTTP backend that computes a numeric "score" from submitted metrics and provides a few utility endpoints. The active entrypoint is `src/api/app.py` (FastAPI + Pydantic). There is also an older, partially broken Flask `app.py` at the project root — prefer the FastAPI implementation unless the user explicitly asks to work on the Flask app.

- **Major components**:
  - `src/api/app.py` — HTTP routes, Pydantic request/response models, error handling, and the ASGI `app` used by `uvicorn`.
  - `src/services/score_service.py` — pure scoring logic. Raises `ScoreComputationError` on invalid input.
  - `src/services/validation.py` — input validation helper. Returns `(is_valid, errors)` rather than raising.
  - `src/utils/config.py` — `Settings` dataclass and `load_settings()` that reads from `os.environ` (keys used: `APP_ENV`, `LOG_LEVEL`, `SCORE_THRESHOLD`).
  - `src/utils/logger.py` — returns configured `logging.Logger` instances. Code expects `get_logger(__name__, settings)`.
  - `tests/` — small PyTest suite that verifies scoring/validation behavior. Use tests as canonical examples of intended behavior and numeric rounding.

- **Data flow / patterns**:
  - HTTP request -> `src/api/app.py` handlers -> `validate_input()` -> `compute_score()` -> return `ScoreResponse`.
  - Validation does not raise; the caller inspects `(is_valid, errors)` and converts failures into HTTP 400 with details.
  - `compute_score()` returns a dict `{"score": float, "status": "pass"|"review"}` and uses rounding to 3 decimals. Tests rely on exact values (see `tests/test_score_service.py`).

- **Errors & exceptions**:
  - Use `ScoreComputationError` for scoring failure cases (existing code raises it when metrics are empty).
  - In FastAPI handlers convert domain errors to `HTTPException` with appropriate status codes (see `src/api/app.py`).

- **Stylistic / repository conventions**:
  - Prefer small, pure functions in `src/services/*` (they are unit-tested directly).
  - Configuration is environment-driven — add keys to `load_settings()` when introducing new runtime configuration.
  - Logging uses `get_logger(name, settings)` and the `Settings.log_level` string.

- **How to run & test (examples)**:
  - Install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
  - Run API (development): `uvicorn src.api.app:app --host 0.0.0.0 --port 8000`
  - Or run via module (entrypoint runs uvicorn): `python -m src.api.app`
  - Run tests: `pytest -q`
  - Build with docker-compose: `docker-compose up --build` (project contains `Dockerfile` and `docker-compose.yml`).

- **Concrete examples**:
  - Score request (JSON): `{"metrics": {"accuracy": 0.8, "latency": 0.6}}`
  - Example successful response: `{"score": 0.7, "status": "pass"}` (note 3-decimal rounding in implementation)

- **What to watch for when editing code**:
  - Tests assert exact numeric rounding — changing `compute_score()`'s rounding or average calculation requires updating tests.
  - Keep `validate_input()`'s return shape `(bool, list[str])`; handlers expect this pattern to create HTTP error details.
  - `src/api/app.py` depends on `load_settings()` for `score_threshold`. If you add new env-driven options, extend `Settings` and `load_settings()`.
  - Don’t remove or silently change the `ScoreComputationError` type; it is used to distinguish domain computation failures.

- **Files to reference when making changes**:
  - `src/api/app.py` — route handlers and how errors/validation are converted to HTTP responses.
  - `src/services/validation.py` and `src/services/score_service.py` — canonical logic and unit tests.
  - `src/utils/config.py` and `src/utils/logger.py` — configuration and logging patterns.
  - `tests/` — small but authoritative test suite; mirror its patterns when adding behaviour.

If anything here is unclear or you want additional examples (e.g., new endpoints, env vars, or CI specifics), tell me which area to expand and I will iterate.
