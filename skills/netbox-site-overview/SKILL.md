---
name: netbox-site-overview
description: List all sites and show detailed site information including racks and devices
tools: [netbox_list_sites, netbox_site_detail]
---

## Prefer composite tools

For complex questions, use the composite tool instead of chaining:
- "Everything about site" → `netbox_site_full` (not `netbox_site_detail` + `netbox_list_prefixes`)

Use the simple tool below only for quick single-fact lookups.

# NetBox Site Overview

## When to use

- "List all sites"
- "What sites do we have?"
- "Show me details for DC-Primary"
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
| DC-Primary | active | City-A |
| DC-Secondary | active | City-B |
```

Site detail:
```
**Site:** DC-Primary
**Status:** active
**Region:** City-A
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

**Input:** "Summary of DC-Primary"
**Tool call:** `netbox_site_detail("DC-Primary")`
**Output:** Site detail + racks.
