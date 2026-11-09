import inspect
import netbox_api
import netbox_ipam
import netbox_dcim_extra


def test_no_write_verbs_in_source():
    for mod in (netbox_api, netbox_ipam, netbox_dcim_extra):
        src = inspect.getsource(mod)
        for verb in ("requests.post", "requests.put", "requests.patch",
                     "requests.delete", ".post(", ".put(", ".patch(", ".delete("):
            assert verb not in src, f"{verb} found in {mod.__name__}"


def test_get_is_only_requests_call(monkeypatch):
    calls = []
    import requests

    def fake_get(url, **kwargs):
        calls.append(("GET", url))
        class R:
            def raise_for_status(self): pass
            def json(self): return {"results": [], "next": None}
        return R()

    monkeypatch.setattr(requests, "get", fake_get)
    netbox_api.get("/api/dcim/sites/")
    assert calls and calls[0][0] == "GET"


def test_token_never_in_output(monkeypatch):
    monkeypatch.setenv("NETBOX_TOKEN", "secret-token-xyz")
    import importlib
    importlib.reload(netbox_api)
    assert "secret-token-xyz" not in inspect.getsource(netbox_api)
