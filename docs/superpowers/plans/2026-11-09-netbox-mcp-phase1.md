# NetBox MCP Phase 1 Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend netbox-mcp with 10 new read-only tools (IPAM prefixes/VLANs/VRFs, cables, sites/racks) plus 6 new bilingual skills, with security tests enforcing the read-only contract.

**Architecture:** Two new Python modules (`netbox_ipam.py`, `netbox_dcim_extra.py`) import `_get` from the existing `netbox_api.py`. `server.py` registers 10 new `@mcp.tool()` wrappers. A new `tests/` directory enforces GET-only behavior. Six new skills (EN/FA) teach Brain Bot to use the new tools.

**Tech Stack:** Python 3.8+, requests, FastMCP, pytest. Markdown for skills.

**Spec:** `docs/superpowers/specs/2026-11-09-netbox-mcp-phase1-design.md`

## Global Constraints

- **Read-only only:** Every new function calls only `_get()`. No POST/PUT/PATCH/DELETE code paths anywhere. Automated test enforces this.
- **No credential commits:** No tokens, passwords, usernames, keys in any committed file. `.env` stays gitignored. `.env.example` holds placeholders only.
- **Environment variables:** All credentials via `NETBOX_TOKEN` / `NETBOX_URL` env vars. Never hardcoded.
- **Pre-commit review:** Before every commit, inspect `git diff` for secrets. No exceptions.
- **Deployment:** Read-only token (`write_enabled=False`) preserved on the server. New tools request only GET endpoints.
- **Security wins over features:** If a security requirement conflicts with a feature, security wins.
- **Bilingual skills:** SKILL.md = English canonical, SKILL.fa.md = Persian translation. Tool names and code stay in English.
- **No rate limiting:** Single-user Brain Bot, NetBox handles load.

---

### Task 1: Security test scaffold

**Files:**
- Create: `netbox-mcp/tests/__init__.py`
- Create: `netbox-mcp/tests/conftest.py`
- Create: `netbox-mcp/tests/test_readonly.py`

**Interfaces:**
- Produces: pytest fixtures for dummy env, import path setup

- [ ] **Step 1: Create tests/__init__.py**

Empty file (package marker).

- [ ] **Step 2: Create tests/conftest.py**

```python
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
```

- [ ] **Step 3: Create tests/test_readonly.py**

```python
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
```

- [ ] **Step 4: Run tests to verify they fail (modules don't exist yet)**

Run: `python -m pytest netbox-mcp/tests/ -v`
Expected: FAIL with "No module named 'netbox_ipam'"

- [ ] **Step 5: Commit**

```bash
git add netbox-mcp/tests/
git commit -m "test: add read-only security test scaffold"
```

---

### Task 2: netbox_ipam.py — IPAM functions

**Files:**
- Create: `netbox-mcp/netbox_ipam.py`

**Interfaces:**
- Consumes: `netbox_api._get`, `netbox_api._site_id`
- Produces: `list_prefixes`, `prefix_detail`, `list_vlans`, `vlan_detail`, `list_vrfs`

- [ ] **Step 1: Write netbox_ipam.py**

```python
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
```

- [ ] **Step 2: Run security tests**

Run: `python -m pytest netbox-mcp/tests/test_readonly.py::test_no_write_verbs_in_source -v`
Expected: PASS (netbox_ipam has no write verbs)

- [ ] **Step 3: Commit**

```bash
git add netbox-mcp/netbox_ipam.py
git commit -m "feat: add netbox_ipam module (prefixes, VLANs, VRFs)"
```

---

### Task 3: netbox_dcim_extra.py — cables, sites, racks

**Files:**
- Create: `netbox-mcp/netbox_dcim_extra.py`

**Interfaces:**
- Consumes: `netbox_api._get`, `netbox_api._site_id`
- Produces: `list_cables`, `trace_cable`, `list_sites`, `site_detail`, `list_racks`

- [ ] **Step 1: Write netbox_dcim_extra.py**

```python
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
```

- [ ] **Step 2: Run security tests**

Run: `python -m pytest netbox-mcp/tests/test_readonly.py -v`
Expected: All PASS

- [ ] **Step 3: Commit**

```bash
git add netbox-mcp/netbox_dcim_extra.py
git commit -m "feat: add netbox_dcim_extra module (cables, sites, racks)"
```

---

### Task 4: server.py — register 10 new tools

**Files:**
- Modify: `netbox-mcp/server.py`

**Interfaces:**
- Consumes: `netbox_ipam.*`, `netbox_dcim_extra.*`
- Produces: 10 new `@mcp.tool()` functions

- [ ] **Step 1: Add imports to server.py**

After `import netbox_api as nb`, add:

```python
import netbox_ipam as nb_ipam
import netbox_dcim_extra as nb_dcim
```

- [ ] **Step 2: Add 10 new tool wrappers**

Append to server.py (before `def main()`):

```python
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
```

- [ ] **Step 3: Verify server.py syntax**

Run: `python -m py_compile netbox-mcp/server.py`
Expected: No errors

- [ ] **Step 4: Commit**

```bash
git add netbox-mcp/server.py
git commit -m "feat: register 10 new read-only MCP tools"
```

---

### Task 5: Update netbox-mcp README

**Files:**
- Modify: `netbox-mcp/README.md`

**Interfaces:**
- Consumes: All 16 tools (6 existing + 10 new)

- [ ] **Step 1: Update README.md**

Replace the Tools table with:

```markdown
| Tool | Description |
|------|-------------|
| `netbox_get_device` | Full device record by name / serial / management IP |
| `netbox_search_devices` | Substring search across name + serial |
| `netbox_rack_inventory` | All devices in a rack with U positions + power feed |
| `netbox_interface_info` | Interfaces of a device + assigned IPs |
| `netbox_lookup_ip` | Who owns an IP: device, interface, prefix, DNS |
| `netbox_device_power` | Live PSU draw + rack feed electrical spec |
| `netbox_list_prefixes` | List IPAM prefixes with filters |
| `netbox_prefix_detail` | Prefix detail + available IPs |
| `netbox_list_vlans` | List VLANs with filters |
| `netbox_vlan_detail` | VLAN detail + prefixes |
| `netbox_list_vrfs` | List VRFs |
| `netbox_list_cables` | List cables with filters |
| `netbox_trace_cable` | Trace cable from interface to neighbor |
| `netbox_list_sites` | List all sites |
| `netbox_site_detail` | Site detail + rack/device counts |
| `netbox_list_racks` | List racks with optional site filter |
```

Update the Security model section to mention the test:

```markdown
## Security model

- NetBox token is read-only at API + object-permission level
- This server only issues HTTP GET (see `netbox_api.py` — GET-only client)
- Token never appears in tool output, logs, or replies
- nginx front is the same TLS as NetBox itself
- **Automated enforcement:** `pytest tests/test_readonly.py` verifies no write verbs exist in source
```

- [ ] **Step 2: Commit**

```bash
git add netbox-mcp/README.md
git commit -m "docs: update netbox-mcp README with 16 tools"
```

---

### Task 6: netbox-ipam-prefixes skill

**Files:**
- Create: `skills/netbox-ipam-prefixes/SKILL.md`
- Create: `skills/netbox-ipam-prefixes/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_list_prefixes`, `netbox_prefix_detail`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-ipam-prefixes
description: List IPAM prefixes and find available IPs within a prefix
tools: [netbox_list_prefixes, netbox_prefix_detail]
---

# NetBox IPAM Prefixes

## When to use

- "What subnets exist at SiteA?"
- "Show me all prefixes"
- "Find free IPs in 10.0.1.0/24"
- "What VRF is 10.0.1.0/24 in?"
- "چه ساب‌نت‌هایی تو سایت A داریم؟"
- "IP های خالی تو 10.0.1.0/24 رو پیدا کن"

## How to resolve

For listing prefixes:
1. Call `netbox_list_prefixes` with optional site/family/q filters.
2. Present as table.

For prefix detail + free IPs:
1. Call `netbox_prefix_detail` with the CIDR.
2. Show prefix info + available IPs sample.

## How to present

Prefix list:
```
| Prefix | VRF | Site | VLAN | Status | Description |
|--------|-----|------|------|--------|-------------|
| 10.0.1.0/24 | default | Tehran | 100 | active | Servers |
| 10.0.2.0/24 | default | Tehran | 200 | active | Management |
```

Prefix detail:
```
**Prefix:** 10.0.1.0/24
**VRF:** default
**Site:** Tehran-DC1
**VLAN:** 100
**Status:** active
**Description:** Server subnet

**Available IPs (sample):**
| IP | Status |
|----|--------|
| 10.0.1.50 | available |
| 10.0.1.51 | available |
```

## Edge cases

- **No prefixes:** "No prefixes found matching your criteria."
- **Prefix not found:** "Prefix 'X' not found in NetBox."
- **No free IPs:** "No available IPs in prefix 'X'."

## Examples

**Input:** "What subnets at SiteA?"
**Tool call:** `netbox_list_prefixes(site="SiteA")`
**Output:** Prefix table.

**Input:** "Find free IPs in 10.0.1.0/24"
**Tool call:** `netbox_prefix_detail("10.0.1.0/24")`
**Output:** Prefix detail + available IPs.
```

- [ ] **Step 2: Write SKILL.fa.md**

Persian translation of the above.

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-ipam-prefixes/
git commit -m "feat: add netbox-ipam-prefixes skill (EN/FA)"
```

---

### Task 7: netbox-vlan-lookup skill

**Files:**
- Create: `skills/netbox-vlan-lookup/SKILL.md`
- Create: `skills/netbox-vlan-lookup/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_list_vlans`, `netbox_vlan_detail`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-vlan-lookup
description: Look up VLANs by ID or name and show associated prefixes
tools: [netbox_list_vlans, netbox_vlan_detail]
---

# NetBox VLAN Lookup

## When to use

- "Show me VLAN 100"
- "What VLANs exist at SiteA?"
- "List all VLANs"
- "VLAN 100 چیست؟"
- "VLAN های سایت A رو نشون بده"

## How to resolve

For listing VLANs:
1. Call `netbox_list_vlans` with optional site/vid/q filters.
2. Present as table.

For VLAN detail:
1. Call `netbox_vlan_detail` with VID or name.
2. Show VLAN info + prefixes.

## How to present

VLAN list:
```
| VID | Name | Site | Status |
|-----|------|------|--------|
| 100 | Servers | Tehran | active |
| 200 | Management | Tehran | active |
```

VLAN detail:
```
**VLAN:** 100 (Servers)
**Site:** Tehran-DC1
**Status:** active

**Prefixes in this VLAN:**
| Prefix | VRF | Description |
|--------|-----|-------------|
| 10.0.1.0/24 | default | Server subnet |
```

## Edge cases

- **VLAN not found:** "VLAN 'X' not found."
- **No VLANs:** "No VLANs found matching your criteria."

## Examples

**Input:** "Show VLAN 100"
**Tool call:** `netbox_vlan_detail("100")`
**Output:** VLAN detail + prefixes.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-vlan-lookup/
git commit -m "feat: add netbox-vlan-lookup skill (EN/FA)"
```

---

### Task 8: netbox-vrf-list skill

**Files:**
- Create: `skills/netbox-vrf-list/SKILL.md`
- Create: `skills/netbox-vrf-list/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_list_vrfs`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-vrf-list
description: List VRFs (Virtual Routing and Forwarding instances) in NetBox
tools: [netbox_list_vrfs]
---

# NetBox VRF List

## When to use

- "List all VRFs"
- "What VRFs exist?"
- "Show me VRF information"
- "VRF ها رو لیست کن"
- "چه VRF هایی داریم؟"

## How to resolve

1. Call `netbox_list_vrfs`.
2. Present as table.

## How to present

```
| Name | RD | Description |
|------|----|-------------|
| default | — | Default VRF |
| management | 65000:100 | Management network |
| production | 65000:200 | Production network |
```

## Edge cases

- **No VRFs:** "No VRFs found in NetBox."

## Examples

**Input:** "List all VRFs"
**Tool call:** `netbox_list_vrfs()`
**Output:** VRF table.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-vrf-list/
git commit -m "feat: add netbox-vrf-list skill (EN/FA)"
```

---

### Task 9: netbox-cable-inventory skill

**Files:**
- Create: `skills/netbox-cable-inventory/SKILL.md`
- Create: `skills/netbox-cable-inventory/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_list_cables`, `netbox_trace_cable`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-cable-inventory
description: List cables and trace connections between device interfaces
tools: [netbox_list_cables, netbox_trace_cable]
---

# NetBox Cable Inventory

## When to use

- "Show me all cables in rack R16"
- "List cables for device SW-01"
- "Trace cable from SW-01 Gi1/0/1"
- "What's connected to SW-01 Gi1/0/1?"
- "کابل‌های رک R16 رو نشون بده"
- "کابل از SW-01 پورت Gi1/0/1 رو trace کن"

## How to resolve

For listing cables:
1. Call `netbox_list_cables` with optional rack/device/site filters.
2. Present as table.

For tracing a cable:
1. Call `netbox_trace_cable` with device and interface.
2. Show interface → cable → neighbor chain.

## How to present

Cable list:
```
| Cable | A-End | B-End | Type | Status |
|-------|-------|-------|------|--------|
| #101 | SW-01:Gi1/0/1 | SRV-01:eth0 | Cat6 | connected |
| #102 | SW-01:Gi1/0/2 | SRV-02:eth0 | Cat6 | connected |
```

Cable trace:
```
**Source:** SW-01 Gi1/0/1
**Cable:** #101 (Cat6)
**Neighbor:** SRV-01 eth0
```

## Edge cases

- **No cables:** "No cables found matching your criteria."
- **Interface not found:** "Interface 'X' not found on device 'Y'."
- **No cable on interface:** "No cable connected to 'X' on 'Y'."

## Examples

**Input:** "Cables in rack R16"
**Tool call:** `netbox_list_cables(rack="R16")`
**Output:** Cable table.

**Input:** "Trace cable from SW-01 Gi1/0/1"
**Tool call:** `netbox_trace_cable("SW-01", "Gi1/0/1")`
**Output:** Cable trace chain.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-cable-inventory/
git commit -m "feat: add netbox-cable-inventory skill (EN/FA)"
```

---

### Task 10: netbox-site-overview skill

**Files:**
- Create: `skills/netbox-site-overview/SKILL.md`
- Create: `skills/netbox-site-overview/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_list_sites`, `netbox_site_detail`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-site-overview
description: List all sites and show detailed site information including racks and devices
tools: [netbox_list_sites, netbox_site_detail]
---

# NetBox Site Overview

## When to use

- "List all sites"
- "What sites do we have?"
- "Show me details for Tehran-DC1"
- "How many racks in SiteA?"
- "همه سایت‌ها رو لیست کن"
- "خلاصه سایت تهران رو نشون بده"

## How to resolve

For listing sites:
1. Call `netbox_list_sites`.
2. Present as table.

For site detail:
1. Call `netbox_site_detail` with site name.
2. Show site info + rack count + device count + rack list.

## How to present

Site list:
```
| Name | Status | Region |
|------|--------|--------|
| Tehran-DC1 | active | Tehran |
| Isfahan-DC1 | active | Isfahan |
```

Site detail:
```
**Site:** Tehran-DC1
**Status:** active
**Region:** Tehran
**Racks:** 5
**Devices:** 42

**Racks:**
| Name | U Height | Devices |
|------|----------|---------|
| R16 | 42U | 12 |
| R17 | 42U | 8 |
```

## Edge cases

- **Site not found:** "Site 'X' not found."
- **No sites:** "No sites found in NetBox."

## Examples

**Input:** "List all sites"
**Tool call:** `netbox_list_sites()`
**Output:** Site table.

**Input:** "Summary of Tehran-DC1"
**Tool call:** `netbox_site_detail("Tehran-DC1")`
**Output:** Site detail + racks.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-site-overview/
git commit -m "feat: add netbox-site-overview skill (EN/FA)"
```

---

### Task 11: netbox-rack-list skill

**Files:**
- Create: `skills/netbox-rack-list/SKILL.md`
- Create: `skills/netbox-rack-list/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_list_racks`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-rack-list
description: List all racks, optionally filtered by site
tools: [netbox_list_racks]
---

# NetBox Rack List

## When to use

- "List all racks"
- "What racks are in Tehran-DC1?"
- "Show me all racks at SiteA"
- "همه رک‌ها رو لیست کن"
- "رک‌های سایت تهران رو نشون بده"

## How to resolve

1. Call `netbox_list_racks` with optional site filter.
2. Present as table.

## How to present

```
| Name | Site | U Height | Devices |
|------|------|----------|---------|
| R16 | Tehran-DC1 | 42U | 12 |
| R17 | Tehran-DC1 | 42U | 8 |
| R01 | Isfahan-DC1 | 48U | 20 |
```

## Edge cases

- **No racks:** "No racks found matching your criteria."
- **Site not found:** "Site 'X' not found."

## Examples

**Input:** "List all racks"
**Tool call:** `netbox_list_racks()`
**Output:** Rack table.

**Input:** "Racks in Tehran-DC1"
**Tool call:** `netbox_list_racks(site="Tehran-DC1")`
**Output:** Filtered rack table.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-rack-list/
git commit -m "feat: add netbox-rack-list skill (EN/FA)"
```

---

### Task 12: Update skills README indexes

**Files:**
- Modify: `skills/README.md`
- Modify: `skills/README.fa.md`

**Interfaces:**
- Consumes: All 13 skills (7 existing + 6 new)

- [ ] **Step 1: Update README.md**

Add 6 new rows to the skills table:

```markdown
| IPAM Prefixes | [SKILL.md](netbox-ipam-prefixes/SKILL.md) | [SKILL.fa.md](netbox-ipam-prefixes/SKILL.fa.md) | List prefixes and find free IPs |
| VLAN Lookup | [SKILL.md](netbox-vlan-lookup/SKILL.md) | [SKILL.fa.md](netbox-vlan-lookup/SKILL.fa.md) | Look up VLANs and associated prefixes |
| VRF List | [SKILL.md](netbox-vrf-list/SKILL.md) | [SKILL.fa.md](netbox-vrf-list/SKILL.fa.md) | List VRFs |
| Cable Inventory | [SKILL.md](netbox-cable-inventory/SKILL.md) | [SKILL.fa.md](netbox-cable-inventory/SKILL.fa.md) | List cables and trace connections |
| Site Overview | [SKILL.md](netbox-site-overview/SKILL.md) | [SKILL.fa.md](netbox-site-overview/SKILL.fa.md) | List sites and show site details |
| Rack List | [SKILL.md](netbox-rack-list/SKILL.md) | [SKILL.fa.md](netbox-rack-list/SKILL.fa.md) | List all racks with optional site filter |
```

- [ ] **Step 2: Update README.fa.md**

Add the same 6 rows with Persian descriptions.

- [ ] **Step 3: Commit**

```bash
git add skills/README.md skills/README.fa.md
git commit -m "docs: update skills README with 6 new skills"
```

---

### Task 13: Update NanoCortex prompts

**Files:**
- Modify: `nanocortex/netbox-prompt.md`
- Modify: `nanocortex/netbox-prompt.fa.md`

**Interfaces:**
- Consumes: All 16 tools

- [ ] **Step 1: Update netbox-prompt.md**

Add to Available Tools:

```markdown
7. **netbox_list_prefixes(site, family, q, limit)** — List IPAM prefixes
8. **netbox_prefix_detail(cidr)** — Prefix detail + available IPs
9. **netbox_list_vlans(site, vid, q, limit)** — List VLANs
10. **netbox_vlan_detail(vid_or_name, site)** — VLAN detail + prefixes
11. **netbox_list_vrfs(limit)** — List VRFs
12. **netbox_list_cables(rack, device, site, limit)** — List cables
13. **netbox_trace_cable(device, interface)** — Trace cable to neighbor
14. **netbox_list_sites(limit)** — List all sites
15. **netbox_site_detail(site)** — Site detail + rack/device counts
16. **netbox_list_racks(site, limit)** — List racks
```

Add to Decision Guide:

```markdown
| Subnets / prefixes | netbox_list_prefixes / netbox_prefix_detail |
| VLANs | netbox_list_vlans / netbox_vlan_detail |
| VRFs | netbox_list_vrfs |
| Cables / connections | netbox_list_cables / netbox_trace_cable |
| Sites | netbox_list_sites / netbox_site_detail |
| Racks (all) | netbox_list_racks |
```

- [ ] **Step 2: Update netbox-prompt.fa.md**

Same additions in Persian.

- [ ] **Step 3: Commit**

```bash
git add nanocortex/
git commit -m "docs: update NanoCortex prompts with 16 tools"
```

---

### Task 14: Final verification and push

**Files:**
- Verify all files exist

- [ ] **Step 1: Run security tests**

Run: `python -m pytest netbox-mcp/tests/ -v`
Expected: All PASS

- [ ] **Step 2: Verify file count**

Run:
```bash
Get-ChildItem -Recurse skills/, nanocortex/, netbox-mcp/ -File | Measure-Object | Select-Object -ExpandProperty Count
```
Expected: 30+ files (18 existing + 12 new skill files + 2 new Python modules + 3 test files + modifications)

- [ ] **Step 3: Verify no credentials in diff**

Run: `git diff HEAD~14..HEAD -- netbox-mcp/ | Select-String -Pattern "token|password|secret|key" -CaseSensitive:$false`
Expected: Only placeholder/example values, no real credentials

- [ ] **Step 4: Push to GitHub**

```bash
git push origin main
```
