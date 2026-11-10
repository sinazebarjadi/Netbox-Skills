# NetBox Assistant Comprehensive Enhancement — Design Spec

**Date:** 2026-11-10
**Status:** Approved (brainstorming complete, pending implementation plan)
**Scope:** Add 8 composite read-only MCP tools that batch related NetBox data into single calls, create 8 new bilingual skills, rewrite 13 existing skills to prefer composite tools, and rewrite NanoCortex prompts with a decision tree that maximizes accuracy and minimizes API calls.

---

## 1. Decisions (locked during brainstorming)

| Question | Decision |
|----------|----------|
| Common query types | Device inventory, troubleshooting, IPAM, capacity planning — all equally common |
| Speed vs completeness | Balanced (2-4 calls), but batch related data into composite tools |
| Approach | A — Composite tools + smart skills |
| New composite tools | 8 |
| New skills | 8 (bilingual EN/FA) |
| Existing skills | Rewrite all 13 to prefer composite tools |
| Prompt strategy | Composite tools = primary; simple tools = fallback |
| Security | Unchanged: GET-only, env token, no write paths |

## 2. Architecture

| File | Change |
|------|--------|
| `netbox-mcp/netbox_composite.py` | **New** — 8 composite data fetchers |
| `netbox-mcp/server.py` | Modified — register 8 new tools (total 24) |
| `netbox-mcp/tests/test_composite.py` | **New** — composite tool tests |
| `skills/netbox-*/SKILL.md` + `SKILL.fa.md` | 8 new + 13 rewritten |
| `nanocortex/netbox-prompt.md` + `.fa.md` | Rewritten with decision tree |

Dependency flow: `netbox_api` → {`netbox_ipam`, `netbox_dcim_extra`} → `netbox_composite` → `server`.

## 3. New Composite Tools (8)

### 3.1 `netbox_device_full(identifier)`

Fetches in one call:
- Device record (via `get_device`)
- All interfaces + assigned IPs (via `get_interface_info`)
- Cables for each interface (via `list_cables` filtered by device)
- Power ports + rack feed (via `get_device_power`)

Returns: `{device, interfaces, cables, power}`

### 3.2 `netbox_rack_full(rack_name, site="")`

Fetches:
- Rack record + devices (via `get_rack_inventory`)
- Power feeds (included in rack_inventory)
- Cables in rack (via `list_cables` filtered by rack)

Returns: `{rack, devices, power_feeds, cables}`

### 3.3 `netbox_ip_full(address)`

Fetches:
- IP record + device + interface (via `search_ip`)
- Prefix detail (via `prefix_detail` on the IP's prefix)
- VLAN detail (via `vlan_detail` on the prefix's VLAN)
- VRF (from prefix record)

Returns: `{ip_records, device, interface, prefix, vlan, vrf}`

### 3.4 `netbox_prefix_full(cidr)`

Fetches:
- Prefix record + available IPs (via `prefix_detail`)
- VLAN detail (via `vlan_detail` on prefix's VLAN)
- VRF (from prefix record)
- Child prefixes (via `list_prefixes` with `within` filter)

Returns: `{prefix, available_ips, vlan, vrf, children}`

### 3.5 `netbox_site_full(site)`

Fetches:
- Site record + racks + device count (via `site_detail`)
- Prefixes at site (via `list_prefixes` filtered by site)
- VLANs at site (via `list_vlans` filtered by site)

Returns: `{site, racks, device_count, prefixes, vlans}`

### 3.6 `netbox_device_neighbors(identifier)`

Fetches:
- Device record (via `get_device`)
- Interfaces (via `get_interface_info`)
- For each interface with a cable, the neighbor device/interface (via `trace_cable`)

Returns: `{device, neighbors: [{interface, cable, neighbor_device, neighbor_interface}]}`

### 3.7 `netbox_find_free_ips(site="", family="", count=10)`

Fetches:
- Prefixes at site (via `list_prefixes`)
- For each prefix, available IPs (via `prefix_detail`)
- Aggregates and returns first N free IPs

Returns: `{free_ips: [{address, prefix, site, vlan}]}`

### 3.8 `netbox_device_by_role(role, site="")`

Fetches:
- Devices filtered by role name (via `search_devices` with role filter)
- Optionally filtered by site

Returns: `{devices: [...]}`

## 4. New Skills (8, bilingual)

| Skill | Trigger examples | Tool |
|-------|-----------------|------|
| `netbox-device-full` | "Tell me everything about SRV-01", "Full details of device X" | `netbox_device_full` |
| `netbox-rack-full` | "Everything in rack R16", "Full rack inventory" | `netbox_rack_full` |
| `netbox-ip-full` | "Everything about IP 10.0.1.5", "Full IP details" | `netbox_ip_full` |
| `netbox-prefix-full` | "Everything about 10.0.1.0/24", "Full prefix details" | `netbox_prefix_full` |
| `netbox-site-full` | "Everything about site X", "Full site overview" | `netbox_site_full` |
| `netbox-device-neighbors` | "What's connected to SRV-01?", "Show neighbors" | `netbox_device_neighbors` |
| `netbox-find-free-ips` | "Find free IPs at site X", "Available addresses" | `netbox_find_free_ips` |
| `netbox-device-by-role` | "List all switches", "Show servers at site X" | `netbox_device_by_role` |

Each skill has `SKILL.md` (English) + `SKILL.fa.md` (Persian) with: When to use / How to resolve / How to present / Edge cases / Examples.

## 5. Existing Skill Rewrites (13)

Each existing skill gets a new section at the top:

```markdown
## Prefer composite tools

For complex questions, use the composite tool instead of chaining:
- "Full device details" → `netbox_device_full` (not `netbox_get_device` + `netbox_interface_info`)
- "Everything in rack" → `netbox_rack_full` (not `netbox_rack_inventory` + `netbox_list_cables`)
```

The rest of each skill remains as fallback guidance for simple queries.

## 6. NanoCortex Prompt Rewrite

New structure:

```markdown
# NetBox Assistant — Brain Bot System Prompt

You are a NetBox inventory assistant with 24 read-only tools.

## Tool Selection Strategy

**Prefer composite tools** for complex questions (1 call instead of 3-5):
- "Everything about X" → composite tool
- "Full details" → composite tool
- "Connected to" → netbox_device_neighbors

**Use simple tools** for quick lookups:
- "What is X?" → netbox_get_device
- "List Y" → netbox_list_*

## Available Tools (24)

### Composite Tools (prefer these)
1. netbox_device_full(identifier) — device + interfaces + cables + power
2. netbox_rack_full(rack_name, site) — rack + devices + power + cables
3. netbox_ip_full(address) — IP + device + prefix + VLAN + VRF
4. netbox_prefix_full(cidr) — prefix + VLAN + VRF + available IPs + children
5. netbox_site_full(site) — site + racks + devices + prefixes + VLANs
6. netbox_device_neighbors(identifier) — device + connected devices
7. netbox_find_free_ips(site, family, count) — quick free IP list
8. netbox_device_by_role(role, site) — devices by role

### Simple Tools (fallback)
9-24. [existing 16 tools]

## Decision Tree

| Question pattern | Tool |
|-----------------|------|
| "Everything about device X" | netbox_device_full |
| "Full rack inventory" | netbox_rack_full |
| "Everything about IP X" | netbox_ip_full |
| "Everything about prefix X" | netbox_prefix_full |
| "Everything about site X" | netbox_site_full |
| "What's connected to X" | netbox_device_neighbors |
| "Find free IPs" | netbox_find_free_ips |
| "List devices by role" | netbox_device_by_role |
| "What is X?" (simple) | netbox_get_device |
| "List Y" (simple) | netbox_list_* |

## Language Rule
[unchanged]

## Output Formatting
[unchanged + composite formats]

## Error Handling
[unchanged + composite-specific errors]
```

## 7. Security (unchanged, non-negotiable)

- All composite functions use `_get()` only
- No new write paths
- Token from env only
- `test_readonly.py` verifies no write verbs in all modules including `netbox_composite.py`
- `test_composite.py` verifies composite tools return expected structure

## 8. Performance Strategy

- Composite tools batch related data: 1 call instead of 3-5
- Agent guided to prefer composite tools for complex questions
- Simple tools remain for quick single-fact lookups
- `limit` parameters cap response sizes

## 9. File Manifest

```
netbox-mcp/
  netbox_composite.py        (new)
  server.py                  (modified: +8 tools)
  tests/
    test_composite.py        (new)

skills/
  netbox-device-full/        SKILL.md + SKILL.fa.md
  netbox-rack-full/          SKILL.md + SKILL.fa.md
  netbox-ip-full/            SKILL.md + SKILL.fa.md
  netbox-prefix-full/        SKILL.md + SKILL.fa.md
  netbox-site-full/          SKILL.md + SKILL.fa.md
  netbox-device-neighbors/   SKILL.md + SKILL.fa.md
  netbox-find-free-ips/      SKILL.md + SKILL.fa.md
  netbox-device-by-role/     SKILL.md + SKILL.fa.md
  (13 existing skills rewritten)
  README.md                  (modified: +8 rows)
  README.fa.md               (modified: +8 rows)

nanocortex/
  netbox-prompt.md           (rewritten)
  netbox-prompt.fa.md        (rewritten)
```

**Totals:** 1 new Python module, 1 new test file, 1 modified server.py, 16 new skill files, 26 rewritten skill files, 2 modified indexes, 2 rewritten prompts.
