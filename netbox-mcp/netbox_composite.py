"""NetBox composite read-only data fetchers.

Each function batches related NetBox data into a single call structure,
reducing the number of API round-trips the agent needs to make.
All functions use _get() from netbox_api. No write operations.
"""
from netbox_api import (
    _get, _site_id, get_device, get_interface_info, get_rack_inventory,
    search_ip, get_device_power,
)
from netbox_ipam import (
    list_prefixes, prefix_detail, list_vlans, vlan_detail, list_vrfs,
)
from netbox_dcim_extra import (
    list_cables, trace_cable, site_detail, list_racks,
)


def device_full(identifier):
    """Device + interfaces + cables + power in one structure."""
    dev = get_device(identifier)
    if not dev:
        return None
    dev_id = dev["id"]
    interfaces = get_interface_info(dev_id)
    cables = list_cables(device=dev.get("name"), limit=100)
    power = get_device_power(dev_id)
    return {
        "device": dev,
        "interfaces": interfaces,
        "cables": cables,
        "power": power,
    }


def rack_full(rack_name, site=None):
    """Rack + devices + power feeds + cables in one structure."""
    inv = get_rack_inventory(rack_name, site)
    if not inv:
        return None
    rack = inv["rack"]
    cables = list_cables(rack=rack.get("name"), limit=100)
    return {
        "rack": rack,
        "devices": inv["devices"],
        "power_feeds": inv.get("power_feeds", []),
        "cables": cables,
    }


def ip_full(address):
    """IP + device + interface + prefix + VLAN + VRF in one structure."""
    info = search_ip(address)
    result = {
        "ip_records": info.get("matches", []),
        "device": info.get("device"),
        "interface": info.get("interface"),
        "prefix": None,
        "vlan": None,
        "vrf": None,
    }
    # Resolve prefix from the first matching IP record
    for rec in info.get("matches", []):
        prefix_addr = rec.get("address")
        if prefix_addr and "/" in prefix_addr:
            # Find the parent prefix
            bare_ip = prefix_addr.split("/")[0]
            prefixes = list_prefixes(q=bare_ip, limit=5)
            if prefixes:
                # Find the most specific matching prefix
                best = None
                for p in prefixes:
                    if bare_ip.startswith(p["prefix"].split("/")[0][:7]):
                        best = p
                        break
                if best:
                    result["prefix"] = best
                    if best.get("vrf"):
                        result["vrf"] = best["vrf"]
                    if best.get("vlan"):
                        result["vlan"] = best["vlan"]
                    break
    return result


def prefix_full(cidr):
    """Prefix + VLAN + VRF + available IPs + child prefixes in one structure."""
    detail = prefix_detail(cidr)
    if not detail:
        return None
    prefix = detail["prefix"]
    result = {
        "prefix": prefix,
        "available_ips": detail.get("available_ips", []),
        "vlan": None,
        "vrf": prefix.get("vrf"),
        "children": [],
    }
    if prefix.get("vlan"):
        vlan = vlan_detail(prefix["vlan"].get("vid") or prefix["vlan"].get("name"))
        result["vlan"] = vlan
    # Child prefixes
    children = list_prefixes(q=prefix["prefix"].split("/")[0], limit=50)
    result["children"] = [p for p in children if p["id"] != prefix["id"]]
    return result


def site_full(site):
    """Site + racks + devices + prefixes + VLANs in one structure."""
    detail = site_detail(site)
    if not detail:
        return None
    sid = detail["site"]["id"]
    prefixes = list_prefixes(site=site, limit=100)
    vlans = list_vlans(site=site, limit=100)
    return {
        "site": detail["site"],
        "racks": detail.get("racks", []),
        "device_count": detail.get("device_count", 0),
        "prefixes": prefixes,
        "vlans": vlans,
    }


def device_neighbors(identifier):
    """Device + directly connected devices via cables."""
    dev = get_device(identifier)
    if not dev:
        return None
    dev_id = dev["id"]
    interfaces = get_interface_info(dev_id)
    neighbors = []
    for it in interfaces:
        iface = it["interface"]
        trace = trace_cable(dev.get("name"), iface["name"])
        if trace and trace.get("neighbor"):
            neighbors.append({
                "interface": iface["name"],
                "cable": trace.get("cable"),
                "neighbor": trace.get("neighbor"),
            })
    return {
        "device": dev,
        "neighbors": neighbors,
    }


def find_free_ips(site=None, family=None, count=10):
    """Quick free IP finder across prefixes."""
    prefixes = list_prefixes(site=site, family=family, limit=50)
    free = []
    for p in prefixes:
        if len(free) >= count:
            break
        detail = prefix_detail(p["prefix"])
        if not detail:
            continue
        for ip in detail.get("available_ips", [])[:count - len(free)]:
            free.append({
                "address": ip.get("address") if isinstance(ip, dict) else ip,
                "prefix": p["prefix"],
                "site": p.get("site", {}).get("name") if isinstance(p.get("site"), dict) else p.get("site"),
                "vlan": p.get("vlan", {}).get("name") if isinstance(p.get("vlan"), dict) else p.get("vlan"),
            })
    return {"free_ips": free}


def device_by_role(role, site=None):
    """Devices filtered by role name and optional site."""
    from netbox_api import search_devices
    # NetBox API supports role filter directly
    params = {"role": role.lower(), "limit": 100}
    if site:
        sid = _site_id(site)
        if sid:
            params["site_id"] = sid
    r = _get("/api/dcim/devices/", params)
    return {"devices": r.get("results", [])}
