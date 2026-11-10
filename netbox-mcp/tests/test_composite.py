"""Tests for netbox_composite module structure and read-only enforcement."""
import inspect
import netbox_composite


def test_no_write_verbs_in_composite():
    src = inspect.getsource(netbox_composite)
    for verb in ("requests.post", "requests.put", "requests.patch",
                 "requests.delete", ".post(", ".put(", ".patch(", ".delete("):
        assert verb not in src, f"{verb} found in netbox_composite"


def test_device_full_structure(monkeypatch):
    """device_full returns expected keys when device exists."""
    import netbox_composite as nc

    class FakeDev:
        def __init__(self):
            self.id = 1
            self.name = "SRV-01"

    monkeypatch.setattr(nc, "get_device", lambda x: {"id": 1, "name": "SRV-01"})
    monkeypatch.setattr(nc, "get_interface_info", lambda x: [])
    monkeypatch.setattr(nc, "list_cables", lambda **k: [])
    monkeypatch.setattr(nc, "get_device_power", lambda x: {"power_ports": [], "feed": None})

    result = nc.device_full("SRV-01")
    assert result is not None
    assert "device" in result
    assert "interfaces" in result
    assert "cables" in result
    assert "power" in result


def test_device_full_not_found(monkeypatch):
    import netbox_composite as nc
    monkeypatch.setattr(nc, "get_device", lambda x: None)
    assert nc.device_full("NONEXISTENT") is None
