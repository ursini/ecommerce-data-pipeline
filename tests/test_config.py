import pytest

import src.config as config


def test_validate_config_accepts_database_url(monkeypatch):
    monkeypatch.setattr(
        config,
        "DATABASE_URL",
        "postgresql://postgres:test@localhost:5432/postgres",
    )

    config.validate_config()


def test_validate_config_rejects_missing_database_url(monkeypatch):
    monkeypatch.setattr(
        config,
        "DATABASE_URL",
        None,
    )

    with pytest.raises(
        RuntimeError,
        match="DATABASE_URL environment variable is not configured",
    ):
        config.validate_config()