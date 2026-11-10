# NetBox MCP server (FastMCP) — read-only inventory for Brain Bot.
#
# Start (SSE, production):  NETBOX_URL=... NETBOX_TOKEN=... python server.py --sse
# Local STDIO test:         python server.py
#
# Mount path: the server is fronted by nginx at /mcp/ (same host:443 as
# NetBox), so routes live under /mcp/sse and /mcp/ on the public URL while
# the backend itself listens on 127.0.0.1:8901 with paths /sse and /mcp.
"""MCP server: NetBox inventory tools (GET-only, read-only token)."""
import argparse
import json

import os

from mcp.server.fastmcp import FastMCP

import netbox_api as nb
import netbox_ipam as nb_ipam
import netbox_dcim_extra as nb_dcim
import netbox_composite as nb_comp

# SSE binding comes from env (MCP_HOST/MCP_PORT) — stdio is the default run mode.
mcp = FastMCP("netbox",
              host=os.environ.get("MCP_HOST", "127.0.0.1"),
              port=int(os.environ.get("MCP_PORT", "8901")))


def _compact(dev):
    if not dev:
        return None
    cf = dev.get("custom_fields") or {}
    site = dev.get("site") or {}
    rack = dev.get("rack") or {}
    role = dev.get("role") or {}
    dtype = dev.get("device_type") or {}
    mfr = getattr(dtype, "get", lambda *a: None)("manufacturer") if isinstance(dtype, dict) else None
    return {
        "id": dev.get("id"),
        "name": dev.get("name"),
        "serial": dev.get("serial"),
        "asset_tag": dev.get("asset_tag"),
        "status": (dev.get("status") or {}).get("value") if isinstance(dev.get("status"), dict) else dev.get("status"),
        "role": role.get("name") if isinstance(role, dict) else role,
        "device_type": dtype.get("model") if isinstance(dtype, dict) else dtype,
        "manufacturer": (mfr.get("name") if isinstance(mfr, dict) else mfr),
        "site": site.get("name") if isinstance(site, dict) else site,
        "rack": rack.get("name") if isinstance(rack, dict) else rack,
        "position": dev.get("position"),
        "face": dev.get("face", {}).get("value") if isinstance(dev.get("face"), dict) else dev.get("face"),
        "primary_ip4": (cf.get("bmc_ip") or (dev.get("primary_ip4") or {}).get("address") if isinstance(dev.get("primary_ip4"), dict) else cf.get("bmc_ip")),
        "custom_fields": {k: v for k, v in cf.items() if v not in (None, "", False)},
    }


@mcp.tool()
def netbox_get_device(identifier: str) -> str:
    """Full NetBox record for one device: resolve by exact name, serial, or
    management IP. Returns name, role, manufacturer, model, serial, asset tag,
    site/rack/U position, management IP, hardware specs (CPU/RAM/disk), power
    draw, status, and all set custom fields."""
    try:
        dev = nb.get_device(identifier)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not dev:
        return json.dumps({"found": False, "identifier": identifier})
    return json.dumps({"found": True, "device": _compact(dev)}, indent=2)


@mcp.tool()
def netbox_search_devices(query: str, limit: int = 10) -> str:
    """Search NetBox devices by name/serial substring. Returns compact cards:
    name, serial, role, model, site, rack."""
    try:
        devs = nb.search_devices(query, limit=min(max(limit, 1), 50))
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps({"count": len(devs), "devices": [_compact(d) for d in devs]}, indent=2)


@mcp.tool()
def netbox_rack_inventory(rack_name: str, site: str = "") -> str:
    """Every device in a named rack (optionally site-qualified) with U positions,
    the rack's power feed(s), and a device list. Use to answer 'what is in
    rack R16?'."""
    try:
        r = nb.get_rack_inventory(rack_name, site or None)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "rack": rack_name})
    return json.dumps({
        "found": True,
        "rack": {"name": r["rack"].get("name"), "u_height": r["rack"].get("u_height"),
                 "site": (r["rack"].get("site") or {}).get("name")},
        "power_feeds": [
            {"name": f.get("name"), "voltage": f.get("voltage"), "amperage": f.get("amperage"),
             "max_utilization": f.get("max_utilization"), "description": f.get("description")}
            for f in (r.get("power_feeds") or [])],
        "devices": [
            {"name": d.get("name"), "position": d.get("position"), "serial": d.get("serial"),
             "role": (d.get("role") or {}).get("name"),
             "model": (d.get("device_type") or {}).get("model")} for d in r["devices"]],
    }, indent=2)


@mcp.tool()
def netbox_interface_info(device: str) -> str:
    """All interfaces of a device (name/UUID/mode) with assigned IP addresses."""
    try:
        d = nb.get_device(device)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not d:
        return json.dumps({"found": False, "device": device})
    infos = nb.get_interface_info(d["id"])
    out = []
    for it in infos:
        i = it["interface"]
        out.append({"interface": {"name": i.get("name"), "type": i.get("type", {}).get("value") if isinstance(i.get("type"), dict) else i.get("type"),
                                  "mac_address": i.get("mac_address"), "mtu": i.get("mtu"),
                                  "mode": (i.get("mode") or {}).get("value") if isinstance(i.get("mode"), dict) else None},
                    "ip_addresses": [{"address": a.get("address"), "status": a.get("status", {}).get("value") if isinstance(a.get("status"), dict) else a.get("status"),
                                      "dns_name": a.get("dns_name"), "description": a.get("description")} for a in it["ip_addresses"]]})
    return json.dumps({"device": d.get("name"), "count": len(out), "interfaces": out}, indent=2)


@mcp.tool()
def netbox_lookup_ip(address: str) -> str:
    """Who owns an IP: device, interface, prefix, DNS, status/description."""
    try:
        info = nb.search_ip(address)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps({
        "query": address,
        "ip_records": [{"address": h.get("address"),
                        "status": h.get("status", {}).get("value") if isinstance(h.get("status"), dict) else h.get("status"),
                        "dns_name": h.get("dns_name"), "description": h.get("description")} for h in info["matches"]],
        "interface": {"name": info["interface"].get("name"), "mac": info["interface"].get("mac_address")} if info["interface"] else None,
        "device": _compact(info["device"]) if info["device"] else None,
    }, indent=2)


@mcp.tool()
def netbox_device_power(device: str) -> str:
    """Power draw for one device: measured watts on its PSU1 port (live Redfish
    reading where available, else model default) and the rack feed electrical
    spec (voltage, amps, utilization headroom)."""
    try:
        d = nb.get_device(device)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not d:
        return json.dumps({"found": False, "device": device})
    info = nb.get_device_power(d["id"])
    feed = info.get("feed") or {}
    return json.dumps({
        "device": d.get("name"),
        "power_ports": [{"name": p.get("name"), "type": p.get("type", {}).get("value") if isinstance(p.get("type"), dict) else p.get("type"),
                         "allocated_draw_w": p.get("allocated_draw"),
                         "maximum_draw_w": p.get("maximum_draw")} for p in info["power_ports"]],
        "feed": {"name": feed.get("name"), "voltage": feed.get("voltage"), "amperage": feed.get("amperage"),
                 "max_utilization": feed.get("max_utilization"), "description": feed.get("description")} if feed else None,
    }, indent=2)


@mcp.tool()
def netbox_list_prefixes(site: str = "", family: str = "", q: str = "", limit: int = 20) -> str:
    """List IPAM prefixes, optionally filtered by site, IP family (4/6), or text."""
    try:
        rows = nb_ipam.list_prefixes(site=site or None, family=family or None,
                                     q=q or None, limit=min(max(limit, 1), 100))
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps({"count": len(rows), "prefixes": rows}, indent=2)


@mcp.tool()
def netbox_prefix_detail(cidr: str) -> str:
    """Prefix detail + available IPs sample."""
    try:
        r = nb_ipam.prefix_detail(cidr)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "cidr": cidr})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_list_vlans(site: str = "", vid: str = "", q: str = "", limit: int = 20) -> str:
    """List VLANs, optionally filtered by site, VID, or text."""
    try:
        rows = nb_ipam.list_vlans(site=site or None, vid=vid or None,
                                  q=q or None, limit=min(max(limit, 1), 100))
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps({"count": len(rows), "vlans": rows}, indent=2)


@mcp.tool()
def netbox_vlan_detail(vid_or_name: str, site: str = "") -> str:
    """VLAN detail + prefixes in it."""
    try:
        r = nb_ipam.vlan_detail(vid_or_name, site=site or None)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "vlan": vid_or_name})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_list_vrfs(limit: int = 20) -> str:
    """List VRFs."""
    try:
        rows = nb_ipam.list_vrfs(limit=min(max(limit, 1), 100))
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps({"count": len(rows), "vrfs": rows}, indent=2)


@mcp.tool()
def netbox_list_cables(rack: str = "", device: str = "", site: str = "", limit: int = 20) -> str:
    """List cables, optionally filtered by rack, device, or site."""
    try:
        rows = nb_dcim.list_cables(rack=rack or None, device=device or None,
                                   site=site or None, limit=min(max(limit, 1), 100))
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps({"count": len(rows), "cables": rows}, indent=2)


@mcp.tool()
def netbox_trace_cable(device: str, interface: str) -> str:
    """Trace cable from a device interface to its neighbor."""
    try:
        r = nb_dcim.trace_cable(device, interface)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "device": device, "interface": interface})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_list_sites(limit: int = 50) -> str:
    """List all sites."""
    try:
        rows = nb_dcim.list_sites(limit=min(max(limit, 1), 100))
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps({"count": len(rows), "sites": rows}, indent=2)


@mcp.tool()
def netbox_site_detail(site: str) -> str:
    """Site detail + rack count + device count."""
    try:
        r = nb_dcim.site_detail(site)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "site": site})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_list_racks(site: str = "", limit: int = 50) -> str:
    """List racks, optionally filtered by site."""
    try:
        rows = nb_dcim.list_racks(site=site or None, limit=min(max(limit, 1), 100))
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps({"count": len(rows), "racks": rows}, indent=2)


@mcp.tool()
def netbox_device_full(identifier: str) -> str:
    """Full device context: device + interfaces + cables + power in one call."""
    try:
        r = nb_comp.device_full(identifier)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "identifier": identifier})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_rack_full(rack_name: str, site: str = "") -> str:
    """Full rack context: rack + devices + power feeds + cables in one call."""
    try:
        r = nb_comp.rack_full(rack_name, site or None)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "rack": rack_name})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_ip_full(address: str) -> str:
    """Full IP context: IP + device + interface + prefix + VLAN + VRF in one call."""
    try:
        r = nb_comp.ip_full(address)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_prefix_full(cidr: str) -> str:
    """Full prefix context: prefix + VLAN + VRF + available IPs + children in one call."""
    try:
        r = nb_comp.prefix_full(cidr)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "cidr": cidr})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_site_full(site: str) -> str:
    """Full site context: site + racks + devices + prefixes + VLANs in one call."""
    try:
        r = nb_comp.site_full(site)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "site": site})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_device_neighbors(identifier: str) -> str:
    """Device + directly connected devices via cables."""
    try:
        r = nb_comp.device_neighbors(identifier)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    if not r:
        return json.dumps({"found": False, "identifier": identifier})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_find_free_ips(site: str = "", family: str = "", count: int = 10) -> str:
    """Quick free IP finder across prefixes."""
    try:
        r = nb_comp.find_free_ips(site=site or None, family=family or None,
                                  count=min(max(count, 1), 50))
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps(r, indent=2)


@mcp.tool()
def netbox_device_by_role(role: str, site: str = "") -> str:
    """Devices filtered by role name and optional site."""
    try:
        r = nb_comp.device_by_role(role, site or None)
    except Exception as e:
        return json.dumps({"error": f"NetBox query failed: {e}"})
    return json.dumps(r, indent=2)


def main():
    parser = argparse.ArgumentParser(description="NetBox read-only MCP server")
    parser.add_argument("--sse", action="store_true",
                        help="Serve SSE on MCP_HOST:MCP_PORT (default stdio), mounted at MCP_MOUNT_PATH (default /mcp)")
    parser.add_argument("--http", dest="http", action="store_true",
                        help="Serve Streamable HTTP on MCP_HOST:MCP_PORT instead of stdio")
    args = parser.parse_args()
    if args.sse:
        mcp.run(transport="sse", mount_path=os.environ.get("MCP_MOUNT_PATH", "/mcp"))
    elif args.http:
        mcp.run(transport="streamable-http")
    else:
        mcp.run()


if __name__ == "__main__":
    main()
