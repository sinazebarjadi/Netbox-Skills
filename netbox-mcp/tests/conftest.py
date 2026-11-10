import os
import sys

# Set dummy credentials before importing modules that require them.
os.environ.setdefault("NETBOX_URL", "https://netbox.example.com")
os.environ.setdefault("NETBOX_TOKEN", "test-token-for-local-tests")
os.environ.setdefault("NETBOX_VERIFY_TLS", "false")

import pytest

# Ensure netbox-mcp modules are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

@pytest.fixture(autouse=True)
def dummy_env(monkeypatch):
    monkeypatch.setenv("NETBOX_URL", "https://netbox.example.com")
    monkeypatch.setenv("NETBOX_TOKEN", "test-token-12345")
    monkeypatch.setenv("NETBOX_VERIFY_TLS", "false")
