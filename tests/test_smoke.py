from brain import __version__
from brain.config import Settings


def test_version_is_defined() -> None:
    assert __version__ == "0.1.0"


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.environment == "local"
    assert settings.log_level == "INFO"
