import inspect
import netbox_composite


def test_no_write_verbs_in_source():
    src = inspect.getsource(netbox_composite)
    for verb in ("requests.post", "requests.put", "requests.patch",
                 "requests.delete", ".post(", ".put(", ".patch(", ".delete("):
        assert verb not in src, f"{verb} found in netbox_composite"


def test_module_exposes_expected_functions():
    expected = (
        "device_full", "rack_full", "ip_full", "prefix_full",
        "site_full", "device_neighbors", "find_free_ips", "device_by_role",
    )
    for name in expected:
        assert hasattr(netbox_composite, name), f"missing {name}"
        assert callable(getattr(netbox_composite, name))
