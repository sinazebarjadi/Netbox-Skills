"""NetBox DCIM read-only functions: cables, sites, racks.

All functions use _get() from netbox_api. No write operations.
"""
from netbox_api import _get, _site_id


def list_cables(rack=None, device=None, site=None, limit=20):
    """List cables with optional filters."""
    params = {"limit": min(max(limit, 1), 100)}
    if rack:
        params["rack"] = rack
    if device:
        params["device"] = device
    if site:
        sid = _site_id(site)
        if sid:
            params["site_id"] = sid
    r = _get("/api/dcim/cables/", params)
    return r.get("results", [])


def trace_cable(device, interface):
    """Trace cable from a device interface to its neighbor."""
    # Find the interface
    ifaces = _get("/api/dcim/interfaces/", {"device": device, "name": interface, "limit": 2})
    results = ifaces.get("results", [])
    if not results:
        return None
    iface = results[0]
    # Find cables connected to this interface
    cables = _get("/api/dcim/cables/", {"interface_id": iface["id"], "limit": 5})
    cable_list = cables.get("results", [])
    if not cable_list:
        return {"interface": iface, "cable": None, "neighbor": None}
    cable = cable_list[0]
    # Resolve neighbor from cable terminations
    neighbor = None
    for term in cable.get("a_terminations", []) + cable.get("b_terminations", []):
        if term.get("object_id") != iface["id"]:
            neighbor = term
            break
    return {"interface": iface, "cable": cable, "neighbor": neighbor}


def list_sites(limit=50):
    """List all sites."""
    r = _get("/api/dcim/sites/", {"limit": min(max(limit, 1), 100)})
    return r.get("results", [])


def site_detail(site):
    """Site detail + rack count + device count."""
    sid = _site_id(site)
    if not sid:
        return None
    site_obj = _get(f"/api/dcim/sites/{sid}/")
    racks = _get("/api/dcim/racks/", {"site_id": sid, "limit": 100})
    devices = _get("/api/dcim/devices/", {"site_id": sid, "limit": 1})
    return {
        "site": site_obj,
        "rack_count": racks.get("count", 0),
        "device_count": devices.get("count", 0),
        "racks": racks.get("results", []),
    }


def list_racks(site=None, limit=50):
    """List racks, optionally filtered by site."""
    params = {"limit": min(max(limit, 1), 100)}
    if site:
        sid = _site_id(site)
        if sid:
            params["site_id"] = sid
    r = _get("/api/dcim/racks/", params)
    return r.get("results", [])
