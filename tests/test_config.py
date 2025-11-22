from src.utils.config import load_settings


def test_load_settings_from_env_mapping():
    env = {"APP_ENV": "staging", "LOG_LEVEL": "DEBUG", "SCORE_THRESHOLD": "0.75"}

    settings = load_settings(env)

    assert settings.environment == "staging"
    assert settings.log_level == "DEBUG"
    assert settings.score_threshold == 0.75
