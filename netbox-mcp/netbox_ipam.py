"""NetBox IPAM read-only functions: prefixes, VLANs, VRFs.

All functions use _get() from netbox_api. No write operations.
"""
from netbox_api import _get, _site_id


def list_prefixes(site=None, vrf=None, family=None, q=None, limit=20):
    """List IPAM prefixes with optional filters."""
    params = {"limit": min(max(limit, 1), 100)}
    if site:
        sid = _site_id(site)
        if sid:
            params["site_id"] = sid
    if vrf:
        params["vrf"] = vrf
    if family:
        params["family"] = family
    if q:
        params["q"] = q
    r = _get("/api/ipam/prefixes/", params)
    return r.get("results", [])


def prefix_detail(cidr):
    """Prefix detail + available IPs sample."""
    r = _get("/api/ipam/prefixes/", {"prefix": cidr, "limit": 2})
    results = r.get("results", [])
    if not results:
        return None
    prefix = results[0]
    avail = _get(f"/api/ipam/prefixes/{prefix['id']}/available-ips/", {"limit": 10})
    return {"prefix": prefix, "available_ips": avail}


def list_vlans(site=None, vid=None, q=None, limit=20):
    """List VLANs with optional filters."""
    params = {"limit": min(max(limit, 1), 100)}
    if site:
        sid = _site_id(site)
        if sid:
            params["site_id"] = sid
    if vid:
        params["vid"] = vid
    if q:
        params["q"] = q
    r = _get("/api/ipam/vlans/", params)
    return r.get("results", [])


def vlan_detail(vid_or_name, site=None):
    """VLAN detail + prefixes in it."""
    params = {"limit": 5}
    if str(vid_or_name).isdigit():
        params["vid"] = vid_or_name
    else:
        params["name__ic"] = vid_or_name
    if site:
        sid = _site_id(site)
        if sid:
            params["site_id"] = sid
    r = _get("/api/ipam/vlans/", params)
    results = r.get("results", [])
    if not results:
        return None
    vlan = results[0]
    prefixes = _get("/api/ipam/prefixes/", {"vlan_id": vlan["id"], "limit": 20})
    return {"vlan": vlan, "prefixes": prefixes.get("results", [])}


def list_vrfs(limit=20):
    """List VRFs."""
    r = _get("/api/ipam/vrfs/", {"limit": min(max(limit, 1), 100)})
    return r.get("results", [])
