"""Configuration utilities for loading environment-driven settings."""
from dataclasses import dataclass
import os


@dataclass
class Settings:
    """Simple settings container for runtime configuration."""

    environment: str = "development"
    log_level: str = "INFO"
    score_threshold: float = 0.5


def load_settings(source: dict | None = None) -> Settings:
    """Load settings from the provided mapping or the OS environment.

    Args:
        source: Optional mapping; defaults to ``os.environ`` when omitted.

    Returns:
        Settings: populated configuration values.
    """

    env = source or os.environ
    return Settings(
        environment=env.get("APP_ENV", "development"),
        log_level=env.get("LOG_LEVEL", "INFO"),
        score_threshold=float(env.get("SCORE_THRESHOLD", 0.5)),
    )
