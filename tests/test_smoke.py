from brain import __version__
from brain.config import Settings
from brain.database import Base
from brain import models  # noqa: F401


def test_version_is_defined() -> None:
    assert __version__ == "0.1.0"


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.environment == "local"
    assert settings.log_level == "INFO"


def test_foundation_tables_are_registered() -> None:
    assert set(Base.metadata.tables) == {
        "users",
        "profiles",
        "portfolios",
        "sessions",
        "research_artifacts",
        "sources",
    }
