# NetBox Comprehensive Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 8 composite read-only MCP tools, create 8 new bilingual skills, rewrite 13 existing skills to prefer composite tools, and rewrite NanoCortex prompts with a decision tree for maximum accuracy and minimum API calls.

**Architecture:** New `netbox_composite.py` module imports from existing `netbox_api`, `netbox_ipam`, and `netbox_dcim_extra`. `server.py` registers 8 new tools (total 24). Skills rewritten to prefer composite tools.

**Tech Stack:** Python 3.8+, requests, FastMCP, pytest. Markdown for skills.

**Spec:** `docs/superpowers/specs/2026-11-10-netbox-comprehensive-enhancement-design.md`

## Global Constraints

- **Read-only only:** Every function calls only `_get()`. No POST/PUT/PATCH/DELETE code paths anywhere.
- **No credential commits:** No tokens, passwords, usernames, keys in any committed file.
- **Environment variables:** All credentials via `NETBOX_TOKEN` / `NETBOX_URL` env vars. Never hardcoded.
- **Pre-commit review:** Before every commit, inspect `git diff` for secrets.
- **Security wins over features:** If a security requirement conflicts with a feature, security wins.
- **Bilingual skills:** SKILL.md = English canonical, SKILL.fa.md = Persian translation.
- **Composite tools preferred:** Agent guided to use composite tools for complex questions.

---

### Task 1: netbox_composite.py — composite data fetchers

**Files:**
- Create: `netbox-mcp/netbox_composite.py`

**Interfaces:**
- Consumes: `netbox_api._get`, `netbox_api._site_id`, `netbox_api.get_device`, `netbox_api.get_interface_info`, `netbox_api.get_rack_inventory`, `netbox_api.search_ip`, `netbox_api.get_device_power`, `netbox_ipam.list_prefixes`, `netbox_ipam.prefix_detail`, `netbox_ipam.list_vlans`, `netbox_ipam.vlan_detail`, `netbox_ipam.list_vrfs`, `netbox_dcim_extra.list_cables`, `netbox_dcim_extra.trace_cable`, `netbox_dcim_extra.site_detail`, `netbox_dcim_extra.list_racks`
- Produces: `device_full`, `rack_full`, `ip_full`, `prefix_full`, `site_full`, `device_neighbors`, `find_free_ips`, `device_by_role`

- [ ] **Step 1: Write netbox_composite.py**

```python
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
    params = {"role": role, "limit": 100}
    if site:
        sid = _site_id(site)
        if sid:
            params["site_id"] = sid
    r = _get("/api/dcim/devices/", params)
    return {"devices": r.get("results", [])}
```

- [ ] **Step 2: Verify syntax**

Run: `python -m py_compile netbox-mcp/netbox_composite.py`
Expected: No errors

- [ ] **Step 3: Commit**

```bash
git add netbox-mcp/netbox_composite.py
git commit -m "feat: add netbox_composite module (8 composite data fetchers)"
```

---

### Task 2: server.py — register 8 composite tools

**Files:**
- Modify: `netbox-mcp/server.py`

**Interfaces:**
- Consumes: `netbox_composite.*`
- Produces: 8 new `@mcp.tool()` functions

- [ ] **Step 1: Add import**

After `import netbox_dcim_extra as nb_dcim`, add:

```python
import netbox_composite as nb_comp
```

- [ ] **Step 2: Add 8 tool wrappers**

Append to server.py (before `def main()`):

```python
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
```

- [ ] **Step 3: Verify syntax**

Run: `python -m py_compile netbox-mcp/server.py`
Expected: No errors

- [ ] **Step 4: Commit**

```bash
git add netbox-mcp/server.py
git commit -m "feat: register 8 composite MCP tools (total 24)"
```

---

### Task 3: test_composite.py — composite tool tests

**Files:**
- Create: `netbox-mcp/tests/test_composite.py`

**Interfaces:**
- Produces: pytest tests for composite module

- [ ] **Step 1: Write test_composite.py**

```python
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
```

- [ ] **Step 2: Run tests**

Run: `python -m pytest netbox-mcp/tests/ -v`
Expected: All PASS (existing 3 + new 3)

- [ ] **Step 3: Commit**

```bash
git add netbox-mcp/tests/test_composite.py
git commit -m "test: add composite tool tests"
```

---

### Task 4: netbox-device-full skill

**Files:**
- Create: `skills/netbox-device-full/SKILL.md`
- Create: `skills/netbox-device-full/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_device_full(identifier)`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-device-full
description: Get complete device context including interfaces, cables, and power in one call
tools: [netbox_device_full]
---

# NetBox Device Full

## When to use

User asks for complete device information:
- "Tell me everything about SRV-01"
- "Full details of device X"
- "Show me all information about server Y"
- "همه اطلاعات SRV-01 رو بده"
- "جزئیات کامل دستگاه X رو نشون بده"

## How to resolve

1. Call `netbox_device_full` with the identifier.
2. Present device card + interface table + cable list + power summary.

## How to present

```
**Device:** SRV-01
**Role:** Server
**Model:** Dell R750
**Serial:** ABC123
**Site:** DC-Primary
**Rack:** R16 (U10)
**Status:** active
**Management IP:** 10.0.1.5

**Interfaces (3):**
| Name | Type | Mode | MAC | IPs |
|------|------|------|-----|-----|
| eth0 | 1000BASE-T | access | aa:bb:cc:dd:ee:ff | 10.0.1.5/24 |
| eth1 | 1000BASE-T | trunk | aa:bb:cc:dd:ee:00 | — |

**Cables (2):**
| Local | Remote | Type |
|-------|--------|------|
| eth0 | SW-01:Gi1/0/1 | Cat6 |
| eth1 | SW-01:Gi1/0/2 | Cat6 |

**Power:**
| PSU | Allocated | Max |
|-----|-----------|-----|
| PSU1 | 450W | 750W |
| Feed: PDU-A (240V, 30A, max 80%) |
```

## Edge cases

- **Not found:** "Device 'X' not found. Try netbox_search_devices for partial matches."
- **No cables:** "No cable information for device 'X'."
- **No power data:** "No power information for device 'X'."

## Examples

**Input:** "Tell me everything about SRV-01"
**Tool call:** `netbox_device_full("SRV-01")`
**Output:** Complete device card + interfaces + cables + power.
```

- [ ] **Step 2: Write SKILL.fa.md**

Persian translation of the above.

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-device-full/
git commit -m "feat: add netbox-device-full skill (EN/FA)"
```

---

### Task 5: netbox-rack-full skill

**Files:**
- Create: `skills/netbox-rack-full/SKILL.md`
- Create: `skills/netbox-rack-full/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_rack_full(rack_name, site)`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-rack-full
description: Get complete rack context including devices, power feeds, and cables in one call
tools: [netbox_rack_full]
---

# NetBox Rack Full

## When to use

- "Everything in rack R16"
- "Full rack inventory for R16"
- "Show me all devices and cables in rack R16"
- "همه چیز رک R16 رو بده"
- "موجودی کامل رک R16 رو نشون بده"

## How to resolve

1. Call `netbox_rack_full` with rack name and optional site.
2. Present rack summary + device table + power feeds + cable list.

## How to present

```
**Rack:** R16 (Site: DC-Primary, Height: 42U)

**Power Feeds:**
| Name | Voltage | Amperage | Max Utilization |
|------|---------|----------|-----------------|
| PDU-A | 240V | 30A | 80% |

**Devices (12):**
| U | Device | Model | Serial | Role |
|---|--------|-------|--------|------|
| 10 | SRV-01 | R750 | ABC123 | Server |
| 12 | SW-01 | C3850 | DEF456 | Switch |

**Cables (8):**
| A-End | B-End | Type | Status |
|-------|-------|------|--------|
| SRV-01:eth0 | SW-01:Gi1/0/1 | Cat6 | connected |
```

## Edge cases

- **Rack not found:** "Rack 'X' not found. Check name and site."
- **Empty rack:** "Rack 'X' is empty."

## Examples

**Input:** "Everything in rack R16"
**Tool call:** `netbox_rack_full("R16")`
**Output:** Rack summary + devices + power + cables.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-rack-full/
git commit -m "feat: add netbox-rack-full skill (EN/FA)"
```

---

### Task 6: netbox-ip-full skill

**Files:**
- Create: `skills/netbox-ip-full/SKILL.md`
- Create: `skills/netbox-ip-full/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_ip_full(address)`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-ip-full
description: Get complete IP context including device, interface, prefix, VLAN, and VRF in one call
tools: [netbox_ip_full]
---

# NetBox IP Full

## When to use

- "Everything about IP 10.0.1.5"
- "Full details for 10.0.1.5"
- "Show me complete information about this IP"
- "همه اطلاعات IP 10.0.1.5 رو بده"
- "جزئیات کامل IP 10.0.1.5 رو نشون بده"

## How to resolve

1. Call `netbox_ip_full` with the IP address.
2. Present IP card + device + interface + prefix + VLAN + VRF.

## How to present

```
**IP:** 10.0.1.5/24
**Status:** active
**DNS:** srv-01.example.com

**Device:** SRV-01 (Dell R750, DC-Primary)
**Interface:** eth0 (MAC: aa:bb:cc:dd:ee:ff)

**Prefix:** 10.0.1.0/24
**VLAN:** 100 (Servers)
**VRF:** default
**Site:** DC-Primary
```

## Edge cases

- **IP not found:** "IP 'X' not found in NetBox."
- **No device assigned:** "IP 'X' exists but is not assigned to a device."
- **No prefix:** "IP 'X' is not part of any prefix in NetBox."

## Examples

**Input:** "Everything about 10.0.1.5"
**Tool call:** `netbox_ip_full("10.0.1.5")`
**Output:** Complete IP context.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-ip-full/
git commit -m "feat: add netbox-ip-full skill (EN/FA)"
```

---

### Task 7: netbox-prefix-full skill

**Files:**
- Create: `skills/netbox-prefix-full/SKILL.md`
- Create: `skills/netbox-prefix-full/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_prefix_full(cidr)`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-prefix-full
description: Get complete prefix context including VLAN, VRF, available IPs, and child prefixes in one call
tools: [netbox_prefix_full]
---

# NetBox Prefix Full

## When to use

- "Everything about 10.0.1.0/24"
- "Full prefix details for 10.0.1.0/24"
- "Show me complete information about this subnet"
- "همه اطلاعات 10.0.1.0/24 رو بده"
- "جزئیات کامل ساب‌نت 10.0.1.0/24 رو نشون بده"

## How to resolve

1. Call `netbox_prefix_full` with the CIDR.
2. Present prefix card + VLAN + VRF + available IPs + child prefixes.

## How to present

```
**Prefix:** 10.0.1.0/24
**Status:** active
**Description:** Server subnet

**VLAN:** 100 (Servers)
**VRF:** default
**Site:** DC-Primary

**Available IPs (sample):**
| IP | Status |
|----|--------|
| 10.0.1.50 | available |
| 10.0.1.51 | available |

**Child Prefixes:**
| Prefix | Description |
|--------|-------------|
| 10.0.1.0/26 | Servers-A |
| 10.0.1.64/26 | Servers-B |
```

## Edge cases

- **Prefix not found:** "Prefix 'X' not found in NetBox."
- **No free IPs:** "No available IPs in prefix 'X'."
- **No children:** "No child prefixes for 'X'."

## Examples

**Input:** "Everything about 10.0.1.0/24"
**Tool call:** `netbox_prefix_full("10.0.1.0/24")`
**Output:** Complete prefix context.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-prefix-full/
git commit -m "feat: add netbox-prefix-full skill (EN/FA)"
```

---

### Task 8: netbox-site-full skill

**Files:**
- Create: `skills/netbox-site-full/SKILL.md`
- Create: `skills/netbox-site-full/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_site_full(site)`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-site-full
description: Get complete site context including racks, devices, prefixes, and VLANs in one call
tools: [netbox_site_full]
---

# NetBox Site Full

## When to use

- "Everything about site X"
- "Full site overview for DC-Primary"
- "Show me complete information about this site"
- "همه اطلاعات سایت X رو بده"
- "نمای کامل سایت X رو نشون بده"

## How to resolve

1. Call `netbox_site_full` with site name.
2. Present site card + rack list + device count + prefix table + VLAN table.

## How to present

```
**Site:** DC-Primary
**Status:** active
**Region:** City-A

**Racks (5):**
| Name | U Height | Devices |
|------|----------|---------|
| R16 | 42U | 12 |
| R17 | 42U | 8 |

**Total Devices:** 42

**Prefixes (10):**
| Prefix | VRF | VLAN | Description |
|--------|-----|------|-------------|
| 10.0.1.0/24 | default | 100 | Servers |
| 10.0.2.0/24 | default | 200 | Management |

**VLANs (5):**
| VID | Name | Status |
|-----|------|--------|
| 100 | Servers | active |
| 200 | Management | active |
```

## Edge cases

- **Site not found:** "Site 'X' not found."
- **No racks:** "Site 'X' has no racks."

## Examples

**Input:** "Everything about DC-Primary"
**Tool call:** `netbox_site_full("DC-Primary")`
**Output:** Complete site context.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-site-full/
git commit -m "feat: add netbox-site-full skill (EN/FA)"
```

---

### Task 9: netbox-device-neighbors skill

**Files:**
- Create: `skills/netbox-device-neighbors/SKILL.md`
- Create: `skills/netbox-device-neighbors/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_device_neighbors(identifier)`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-device-neighbors
description: Show directly connected devices via cables for a given device
tools: [netbox_device_neighbors]
---

# NetBox Device Neighbors

## When to use

- "What's connected to SRV-01?"
- "Show neighbors of SW-01"
- "What devices are directly connected to this server?"
- "به SRV-01 چی وصله؟"
- "همسایه‌های SW-01 رو نشون بده"

## How to resolve

1. Call `netbox_device_neighbors` with the device identifier.
2. Present device + neighbor table.

## How to present

```
**Device:** SRV-01

**Directly Connected Devices:**
| Local Interface | Cable | Neighbor Device | Neighbor Interface |
|-----------------|-------|-----------------|--------------------|
| eth0 | #101 | SW-01 | Gi1/0/1 |
| eth1 | #102 | SW-01 | Gi1/0/2 |
```

## Edge cases

- **Device not found:** "Device 'X' not found."
- **No neighbors:** "No directly connected devices found for 'X'."

## Examples

**Input:** "What's connected to SRV-01?"
**Tool call:** `netbox_device_neighbors("SRV-01")`
**Output:** Device + neighbor table.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-device-neighbors/
git commit -m "feat: add netbox-device-neighbors skill (EN/FA)"
```

---

### Task 10: netbox-find-free-ips skill

**Files:**
- Create: `skills/netbox-find-free-ips/SKILL.md`
- Create: `skills/netbox-find-free-ips/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_find_free_ips(site, family, count)`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-find-free-ips
description: Quickly find available IP addresses across prefixes
tools: [netbox_find_free_ips]
---

# NetBox Find Free IPs

## When to use

- "Find free IPs at site X"
- "Show me available addresses in 10.0.1.0/24"
- "I need 5 free IPs for new servers"
- "IP های خالی تو سایت X رو پیدا کن"
- "۵ تا IP خالی برای سرورهای جدید می‌خوام"

## How to resolve

1. Call `netbox_find_free_ips` with optional site/family/count.
2. Present free IP table.

## How to present

```
**Available IPs (5):**

| Address | Prefix | Site | VLAN |
|---------|--------|------|------|
| 10.0.1.50 | 10.0.1.0/24 | DC-Primary | Servers |
| 10.0.1.51 | 10.0.1.0/24 | DC-Primary | Servers |
| 10.0.2.10 | 10.0.2.0/24 | DC-Primary | Management |
```

## Edge cases

- **No free IPs:** "No available IPs found matching your criteria."
- **Site not found:** "Site 'X' not found."

## Examples

**Input:** "Find 5 free IPs at DC-Primary"
**Tool call:** `netbox_find_free_ips(site="DC-Primary", count=5)`
**Output:** Free IP table.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-find-free-ips/
git commit -m "feat: add netbox-find-free-ips skill (EN/FA)"
```

---

### Task 11: netbox-device-by-role skill

**Files:**
- Create: `skills/netbox-device-by-role/SKILL.md`
- Create: `skills/netbox-device-by-role/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_device_by_role(role, site)`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-device-by-role
description: List devices filtered by role name and optional site
tools: [netbox_device_by_role]
---

# NetBox Device By Role

## When to use

- "List all switches"
- "Show servers at site X"
- "Find all firewalls"
- "همه سوییچ‌ها رو لیست کن"
- "سرورهای سایت X رو نشون بده"

## How to resolve

1. Call `netbox_device_by_role` with role name and optional site.
2. Present device table.

## How to present

```
**Devices with role 'Switch' (3):**

| Name | Serial | Model | Site | Rack |
|------|--------|-------|------|------|
| SW-01 | ABC123 | C3850 | DC-Primary | R16 |
| SW-02 | ABC124 | C3850 | DC-Primary | R17 |
| SW-03 | ABC125 | C9300 | DC-Secondary | R01 |
```

## Edge cases

- **No devices:** "No devices found with role 'X'."
- **Site not found:** "Site 'X' not found."

## Examples

**Input:** "List all switches"
**Tool call:** `netbox_device_by_role("Switch")`
**Output:** Device table.

**Input:** "Show servers at DC-Primary"
**Tool call:** `netbox_device_by_role("Server", site="DC-Primary")`
**Output:** Filtered device table.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-device-by-role/
git commit -m "feat: add netbox-device-by-role skill (EN/FA)"
```

---

### Task 12: Rewrite 13 existing skills to prefer composite tools

**Files:**
- Modify: `skills/netbox-device-lookup/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-rack-inventory/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-ip-lookup/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-interface-details/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-power-check/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-search-devices/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-troubleshoot-cabling/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-ipam-prefixes/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-vlan-lookup/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-vrf-list/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-cable-inventory/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-site-overview/SKILL.md` + `SKILL.fa.md`
- Modify: `skills/netbox-rack-list/SKILL.md` + `SKILL.fa.md`

**Interfaces:**
- Consumes: All 8 new composite tools

- [ ] **Step 1: Add composite guidance to each skill**

Insert after the frontmatter in each SKILL.md (and SKILL.fa.md):

```markdown
## Prefer composite tools

For complex questions, use the composite tool instead of chaining:
- "Full device details" → `netbox_device_full` (not `netbox_get_device` + `netbox_interface_info`)
- "Everything in rack" → `netbox_rack_full` (not `netbox_rack_inventory` + `netbox_list_cables`)
- "Everything about IP" → `netbox_ip_full` (not `netbox_lookup_ip` + `netbox_prefix_detail`)
- "Everything about prefix" → `netbox_prefix_full` (not `netbox_prefix_detail` + `netbox_vlan_detail`)
- "Everything about site" → `netbox_site_full` (not `netbox_site_detail` + `netbox_list_prefixes`)
- "Connected devices" → `netbox_device_neighbors` (not `netbox_interface_info` + `netbox_trace_cable`)

Use the simple tool below only for quick single-fact lookups.
```

Customize the composite guidance per skill (e.g., netbox-device-lookup only shows device_full; netbox-rack-inventory only shows rack_full).

- [ ] **Step 2: Commit**

```bash
git add skills/
git commit -m "docs: rewrite 13 skills to prefer composite tools"
```

---

### Task 13: Update skills README indexes

**Files:**
- Modify: `skills/README.md`
- Modify: `skills/README.fa.md`

**Interfaces:**
- Consumes: All 21 skills (13 existing + 8 new)

- [ ] **Step 1: Update README.md**

Add 8 new rows to the skills table:

```markdown
| Device Full | [SKILL.md](netbox-device-full/SKILL.md) | [SKILL.fa.md](netbox-device-full/SKILL.fa.md) | Complete device context in one call |
| Rack Full | [SKILL.md](netbox-rack-full/SKILL.md) | [SKILL.fa.md](netbox-rack-full/SKILL.fa.md) | Complete rack context in one call |
| IP Full | [SKILL.md](netbox-ip-full/SKILL.md) | [SKILL.fa.md](netbox-ip-full/SKILL.fa.md) | Complete IP context in one call |
| Prefix Full | [SKILL.md](netbox-prefix-full/SKILL.md) | [SKILL.fa.md](netbox-prefix-full/SKILL.fa.md) | Complete prefix context in one call |
| Site Full | [SKILL.md](netbox-site-full/SKILL.md) | [SKILL.fa.md](netbox-site-full/SKILL.fa.md) | Complete site context in one call |
| Device Neighbors | [SKILL.md](netbox-device-neighbors/SKILL.md) | [SKILL.fa.md](netbox-device-neighbors/SKILL.fa.md) | Directly connected devices |
| Find Free IPs | [SKILL.md](netbox-find-free-ips/SKILL.md) | [SKILL.fa.md](netbox-find-free-ips/SKILL.fa.md) | Quick free IP finder |
| Device By Role | [SKILL.md](netbox-device-by-role/SKILL.md) | [SKILL.fa.md](netbox-device-by-role/SKILL.fa.md) | Devices filtered by role |
```

- [ ] **Step 2: Update README.fa.md**

Add the same 8 rows with Persian descriptions.

- [ ] **Step 3: Commit**

```bash
git add skills/README.md skills/README.fa.md
git commit -m "docs: update skills README with 8 new composite skills"
```

---

### Task 14: Rewrite NanoCortex prompts

**Files:**
- Modify: `nanocortex/netbox-prompt.md`
- Modify: `nanocortex/netbox-prompt.fa.md`

**Interfaces:**
- Consumes: All 24 tools

- [ ] **Step 1: Rewrite netbox-prompt.md**

Replace entire content with:

```markdown
# NetBox Assistant — Brain Bot System Prompt

You are a NetBox inventory assistant with 24 read-only tools. Your goal is accurate, fast, context-aware answers.

## Tool Selection Strategy

**Prefer composite tools** for complex questions (1 call instead of 3-5):
- "Everything about X" → composite tool
- "Full details" → composite tool
- "Connected to" → netbox_device_neighbors
- "Complete context" → composite tool

**Use simple tools** for quick single-fact lookups:
- "What is X?" → netbox_get_device
- "List Y" → netbox_list_*

## Available Tools (24)

### Composite Tools (prefer these for complex questions)

1. **netbox_device_full(identifier)** — device + interfaces + cables + power
2. **netbox_rack_full(rack_name, site="")** — rack + devices + power feeds + cables
3. **netbox_ip_full(address)** — IP + device + interface + prefix + VLAN + VRF
4. **netbox_prefix_full(cidr)** — prefix + VLAN + VRF + available IPs + children
5. **netbox_site_full(site)** — site + racks + devices + prefixes + VLANs
6. **netbox_device_neighbors(identifier)** — device + directly connected devices
7. **netbox_find_free_ips(site="", family="", count=10)** — quick free IP list
8. **netbox_device_by_role(role, site="")** — devices filtered by role

### Simple Tools (fallback for quick lookups)

9. **netbox_get_device(identifier)** — device record by name/serial/IP
10. **netbox_search_devices(query, limit=10)** — search devices by substring
11. **netbox_rack_inventory(rack_name, site="")** — devices in a rack
12. **netbox_interface_info(device)** — interfaces + IPs of a device
13. **netbox_lookup_ip(address)** — IP → device/interface/prefix
14. **netbox_device_power(device)** — power draw + rack feed
15. **netbox_list_prefixes(site, family, q, limit)** — list prefixes
16. **netbox_prefix_detail(cidr)** — prefix + available IPs
17. **netbox_list_vlans(site, vid, q, limit)** — list VLANs
18. **netbox_vlan_detail(vid_or_name, site)** — VLAN + prefixes
19. **netbox_list_vrfs(limit)** — list VRFs
20. **netbox_list_cables(rack, device, site, limit)** — list cables
21. **netbox_trace_cable(device, interface)** — trace cable to neighbor
22. **netbox_list_sites(limit)** — list all sites
23. **netbox_site_detail(site)** — site + rack/device counts
24. **netbox_list_racks(site, limit)** — list racks

## Decision Tree

| Question pattern | Tool |
|-----------------|------|
| "Everything about device X" | netbox_device_full |
| "Full details of device X" | netbox_device_full |
| "Everything in rack R16" | netbox_rack_full |
| "Full rack inventory" | netbox_rack_full |
| "Everything about IP X" | netbox_ip_full |
| "Full IP details" | netbox_ip_full |
| "Everything about prefix X" | netbox_prefix_full |
| "Full prefix details" | netbox_prefix_full |
| "Everything about site X" | netbox_site_full |
| "Full site overview" | netbox_site_full |
| "What's connected to X" | netbox_device_neighbors |
| "Show neighbors" | netbox_device_neighbors |
| "Find free IPs" | netbox_find_free_ips |
| "Available addresses" | netbox_find_free_ips |
| "List devices by role" | netbox_device_by_role |
| "Show all switches" | netbox_device_by_role |
| "What is X?" (simple) | netbox_get_device |
| "List Y" (simple) | netbox_list_* |
| "Who owns IP X?" (simple) | netbox_lookup_ip |
| "What VLAN is X?" | netbox_vlan_detail |
| "Power draw of X" | netbox_device_power |

## Language Rule

- User writes in English → respond in English
- User writes in Persian → respond in Persian
- Tool names and technical terms stay in English

## Output Formatting

- Single device → compact card
- Multiple devices → table
- Rack → summary + table
- IP → ownership card
- Composite results → structured sections (device card + interface table + cable list + power summary)

## Error Handling

- Device not found → suggest netbox_search_devices with partial name
- Multiple matches → list options, ask user to clarify
- Tool error → report error, suggest checking NetBox connectivity
- Empty result → explain search scope, offer alternative query

## Examples

**User:** "Tell me everything about SRV-01"
**Action:** netbox_device_full("SRV-01")
**Response:** Device card + interface table + cable list + power summary.

**User:** "What's connected to SRV-01?"
**Action:** netbox_device_neighbors("SRV-01")
**Response:** Device + neighbor table.

**User:** "Find 5 free IPs at DC-Primary"
**Action:** netbox_find_free_ips(site="DC-Primary", count=5)
**Response:** Free IP table.

**User:** "رک R16 چی توشه؟"
**Action:** netbox_rack_full("R16")
**Response:** Rack summary + device table + power feeds + cables in Persian.
```

- [ ] **Step 2: Rewrite netbox-prompt.fa.md**

Persian translation of the above.

- [ ] **Step 3: Commit**

```bash
git add nanocortex/
git commit -m "docs: rewrite NanoCortex prompts with 24 tools and decision tree"
```

---

### Task 15: Final verification and push

**Files:**
- Verify all files exist

- [ ] **Step 1: Run all tests**

Run: `python -m pytest netbox-mcp/tests/ -v`
Expected: All PASS (3 readonly + 3 composite = 6 total)

- [ ] **Step 2: Verify file count**

Run:
```bash
Get-ChildItem -Recurse skills/, nanocortex/, netbox-mcp/ -File | Measure-Object | Select-Object -ExpandProperty Count
```
Expected: 70+ files (53 previous + 16 new skill files + 1 new module + 1 new test + modifications)

- [ ] **Step 3: Verify no credentials in diff**

Run: `git diff HEAD~15..HEAD -- netbox-mcp/ | Select-String -Pattern "token|password|secret|key" -CaseSensitive:$false`
Expected: Only placeholder/example values

- [ ] **Step 4: Push to GitHub**

```bash
git push origin main
```
