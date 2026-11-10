---
name: netbox-rack-list
description: List all racks, optionally filtered by site
tools: [netbox_list_racks]
---

# NetBox Rack List

## When to use

- "List all racks"
- "What racks are in DC-Primary?"
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
| R16 | DC-Primary | 42U | 12 |
| R17 | DC-Primary | 42U | 8 |
| R01 | DC-Secondary | 48U | 20 |
```

## Edge cases

- **No racks:** "No racks found matching your criteria."
- **Site not found:** "Site 'X' not found."

## Examples

**Input:** "List all racks"
**Tool call:** `netbox_list_racks()`
**Output:** Rack table.

**Input:** "Racks in DC-Primary"
**Tool call:** `netbox_list_racks(site="DC-Primary")`
**Output:** Filtered rack table.
