import importlib
import os


def test_default_host_and_port():
    import config
    importlib.reload(config)
    assert config.HOST == "127.0.0.1"
    assert config.PORT == 8771


def test_env_host_override(monkeypatch):
    monkeypatch.setenv("TROPHY_ROOM_HOST", "0.0.0.0")
    monkeypatch.setenv("TROPHY_ROOM_PORT", "9000")
    import config
    importlib.reload(config)
    assert config.HOST == "0.0.0.0"
    assert config.PORT == 9000
    # Restore defaults for other tests
    monkeypatch.delenv("TROPHY_ROOM_HOST", raising=False)
    monkeypatch.delenv("TROPHY_ROOM_PORT", raising=False)
    importlib.reload(config)
