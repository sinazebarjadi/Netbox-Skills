# NetBox MCP Phase 1 Expansion — Design Spec

**Date:** 2026-11-09
**Status:** Approved (brainstorming complete, pending implementation plan)
**Scope:** Extend netbox-mcp with 10 new read-only tools (IPAM prefixes/VLANs/VRFs, cables/connections, sites/racks) plus 6 new bilingual skills, without weakening the existing read-only security model.

---

## 1. Decisions (locked during brainstorming)

| Question | Decision |
|----------|----------|
| Priority areas | All: IPAM, cables, sites/racks |
| Security pattern | Keep current: GET-only `_get()` helper, token from env, no write paths |
| Rate limiting | None (single-user Brain Bot, NetBox handles load) |
| New tool count | 10 |
| New skill count | 6 (bilingual EN/FA each) |
| Module split | 3 modules: core api, ipam, dcim_extra |

## 2. Security Requirements (non-negotiable, must take priority)

1. **Read-only only:** Every new function calls only `_get()`. No POST/PUT/PATCH/DELETE code paths anywhere. Automated test enforces this.
2. **No credential commits:** No tokens, passwords, usernames, keys in any committed file. `.env` stays gitignored. `.env.example` holds placeholders only.
3. **Environment variables:** All credentials via `NETBOX_TOKEN` / `NETBOX_URL` env vars. Never hardcoded.
4. **Pre-commit review:** Before every commit, inspect `git diff` for secrets. No exceptions.
5. **Deployment:** Read-only token (`write_enabled=False`) preserved on the server. New tools request only GET endpoints.

If a security requirement conflicts with a feature, security wins.

## 3. Architecture

| File | Change |
|------|--------|
| `netbox-mcp/netbox_api.py` | Unchanged core (`_get`, `get_device`, `search_devices`, `get_rack_inventory`, `get_interface_info`, `search_ip`, `get_device_power`, `_site_id`) |
| `netbox-mcp/netbox_ipam.py` | **New** — prefix, VLAN, VRF functions |
| `netbox-mcp/netbox_dcim_extra.py` | **New** — cable, site, rack-listing functions |
| `netbox-mcp/server.py` | Modified — import new modules, register 10 new `@mcp.tool()` |
| `netbox-mcp/tests/__init__.py` | **New** — empty package marker |
| `netbox-mcp/tests/conftest.py` | **New** — env fixtures (dummy token), import path |
| `netbox-mcp/tests/test_readonly.py` | **New** — GET-only enforcement tests |
| `netbox-mcp/README.md` | Modified — document 16 tools total, update security section |

The new modules import `_get` from `netbox_api`. Dependency flow stays acyclic: `netbox_api` → {`netbox_ipam`, `netbox_dcim_extra`} → `server`.

## 4. New Tools (10)

### IPAM (`netbox_ipam.py`)

| Function | Tool | Endpoint(s) | Returns |
|----------|------|-------------|---------|
| `list_prefixes(site=None, vrf=None, family=None, q=None, limit=20)` | `netbox_list_prefixes` | `/api/ipam/prefixes/` | Prefix list (cidr, vrf, site, vlan, status, description) |
| `prefix_detail(cidr)` | `netbox_prefix_detail` | `/api/ipam/prefixes/` + `/available-ips/` | Prefix + child counts + sample free IPs |
| `list_vlans(site=None, vid=None, q=None, limit=20)` | `netbox_list_vlans` | `/api/ipam/vlans/` | VLAN list (vid, name, site, status) |
| `vlan_detail(vid_or_name, site=None)` | `netbox_vlan_detail` | `/api/ipam/vlans/` + prefixes | VLAN + prefixes in it |
| `list_vrfs(limit=20)` | `netbox_list_vrfs` | `/api/ipam/vrfs/` | VRF list (name, rd, description) |

### DCIM extras (`netbox_dcim_extra.py`)

| Function | Tool | Endpoint(s) | Returns |
|----------|------|-------------|---------|
| `list_cables(rack=None, device=None, site=None, limit=20)` | `netbox_list_cables` | `/api/dcim/cables/` | Cable list with A/B terminations |
| `trace_cable(device, interface)` | `netbox_trace_cable` | `/api/dcim/cables/` (filtered) | Endpoint resolution + neighbor |
| `list_sites(limit=50)` | `netbox_list_sites` | `/api/dcim/sites/` | Site list (name, status, region) |
| `site_detail(site)` | `netbox_site_detail` | `/api/dcim/sites/` + `/racks/` + `/devices/` | Site + rack count + device count |
| `list_racks(site=None, limit=50)` | `netbox_list_racks` | `/api/dcim/racks/` | Rack list (name, site, u_height) |

All functions accept filters, paginate where needed (reuse the `offset` loop pattern from `get_rack_inventory`), and return plain dicts.

## 5. Site Resolution Helper

`netbox_api._site_id(site)` already resolves a site name to an ID. The new DCIM module reuses it (import from `netbox_api`). IPAM functions that filter by site call `_site_id` too.

## 6. server.py New Tool Wrappers

Each wrapper follows the existing pattern: try/except around the call, `json.dumps` error on failure, `json.dumps` compact result on success. Example:

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
```

## 7. Security Tests (`tests/test_readonly.py`)

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

Additional assertion: the module sets `_HEADERS["Authorization"]` from env but never logs or returns it.

## 8. New Skills (6, bilingual)

| Skill | Trigger examples | Tools |
|-------|------------------|-------|
| `netbox-ipam-prefixes` | "What subnets at SiteA?", "Free IPs in 10.0.1.0/24", "ساب‌نت‌های سایت A" | `netbox_list_prefixes`, `netbox_prefix_detail` |
| `netbox-vlan-lookup` | "Show VLAN 100", "VLANs at site", "VLAN 100 چیست" | `netbox_list_vlans`, `netbox_vlan_detail` |
| `netbox-vrf-list` | "List VRFs", "Which VRF for prefix X", "VRFها را لیست کن" | `netbox_list_vrfs` |
| `netbox-cable-inventory` | "Cables in rack R16", "Trace cable from SW-01 Gi1/0/1", "کابل‌های رک R16" | `netbox_list_cables`, `netbox_trace_cable` |
| `netbox-site-overview` | "List all sites", "Summary of Tehran-DC1", "همه سایت‌ها" | `netbox_list_sites`, `netbox_site_detail` |
| `netbox-rack-list` | "All racks at site", "What racks exist", "همه رک‌ها" | `netbox_list_racks` |

Each has `SKILL.md` (English) + `SKILL.fa.md` (Persian). Same section structure as existing skills: When to use / How to resolve / How to present / Edge cases / Examples.

## 9. Skill Output Formats

- Prefixes → table: CIDR, VRF, Site, VLAN, Status, Description
- Prefix detail → prefix header + utilization % + free-IP sample table
- VLANs → table: VID, Name, Site, Status
- VRFs → table: Name, RD, Description
- Cables → table: Cable ID, A-end (device:interface), B-end (device:interface), Type, Status
- Sites → table: Name, Status, Region, Rack count
- Site detail → site header + rack count + device count + rack list
- Racks → table: Name, Site, U height, Device count

## 10. NanoCortex Prompt Updates

Add the 10 new tools to the "Available Tools" list and extend the "Decision Guide" table:

| User asks about... | Use tool |
|-------------------|----------|
| Subnets / prefixes | netbox_list_prefixes / netbox_prefix_detail |
| VLANs | netbox_list_vlans / netbox_vlan_detail |
| VRFs | netbox_list_vrfs |
| Cables / connections | netbox_list_cables / netbox_trace_cable |
| Sites | netbox_list_sites / netbox_site_detail |
| Racks (all) | netbox_list_racks |

Both `netbox-prompt.md` and `netbox-prompt.fa.md` updated.

## 11. File Manifest

```
netbox-mcp/
  netbox_api.py             (unchanged)
  netbox_ipam.py            (new)
  netbox_dcim_extra.py      (new)
  server.py                 (modified)
  requirements.txt          (add pytest to requirements-dev or note)
  README.md                 (modified)
  tests/
    __init__.py             (new)
    conftest.py             (new)
    test_readonly.py        (new)

skills/
  netbox-ipam-prefixes/SKILL.md + SKILL.fa.md
  netbox-vlan-lookup/SKILL.md + SKILL.fa.md
  netbox-vrf-list/SKILL.md + SKILL.fa.md
  netbox-cable-inventory/SKILL.md + SKILL.fa.md
  netbox-site-overview/SKILL.md + SKILL.fa.md
  netbox-rack-list/SKILL.md + SKILL.fa.md
  README.md                 (modified: add 6 rows)
  README.fa.md              (modified: add 6 rows)

nanocortex/
  netbox-prompt.md          (modified)
  netbox-prompt.fa.md       (modified)
```

**Totals:** 2 new Python modules, 3 new test files, 1 modified server.py, 1 modified README (netbox-mcp), 12 new skill files, 2 modified skill indexes, 2 modified prompts.

## 12. Testing Strategy

- **Unit:** `pytest netbox-mcp/tests/` — GET-only enforcement, token safety.
- **Manual:** run `python e2e_test.py` against live NetBox to confirm new tools respond.
- **Skill validation:** feed each new SKILL.md example to Brain Bot and confirm tool selection + output format.
