import os
import sys
import pytest

# Ensure netbox-mcp modules are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

@pytest.fixture(autouse=True)
def dummy_env(monkeypatch):
    monkeypatch.setenv("NETBOX_URL", "https://netbox.example.com")
    monkeypatch.setenv("NETBOX_TOKEN", "test-token-12345")
    monkeypatch.setenv("NETBOX_VERIFY_TLS", "false")
