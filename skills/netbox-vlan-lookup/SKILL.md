---
name: netbox-vlan-lookup
description: Look up VLANs by ID or name and show associated prefixes
tools: [netbox_list_vlans, netbox_vlan_detail]
---

## Prefer composite tools

For complex questions, use the composite tool instead of chaining:
- "Everything about prefix including VLAN" → `netbox_prefix_full` (not `netbox_prefix_detail` + `netbox_vlan_detail`)
- "Everything about site including VLANs" → `netbox_site_full` (not `netbox_site_detail` + `netbox_list_vlans`)

Use the simple tool below only for quick single-fact lookups.

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
| 100 | Servers | City-A | active |
| 200 | Management | City-A | active |
```

VLAN detail:
```
**VLAN:** 100 (Servers)
**Site:** DC-Primary
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
