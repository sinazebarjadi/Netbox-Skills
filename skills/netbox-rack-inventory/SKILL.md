---
name: netbox-rack-inventory
description: List all devices in a rack with U positions and power feed information
tools: [netbox_rack_inventory, netbox_get_device]
---

## Prefer composite tools

For complex questions, use the composite tool instead of chaining:
- "Everything in rack" → `netbox_rack_full` (not `netbox_rack_inventory` + `netbox_list_cables`)

Use the simple tool below only for quick single-fact lookups.

# NetBox Rack Inventory

## When to use

- "What's in rack R16?"
- "Show me rack R16 at SiteA"
- "List devices in rack R16"
- "رک R16 چی توشه؟"
- "دستگاه‌های رک R16 رو لیست کن"

## How to resolve

1. Call `netbox_rack_inventory` with rack name and optional site.
2. If rack not found, suggest checking rack name or site.
3. Present device list sorted by U position.

## How to present

```
**Rack:** R16 (Site: DC-Primary, Height: 42U)
**Power Feed:** PDU-A (240V, 30A, max 80% utilization)

| U | Device | Model | Serial | Role |
|---|--------|-------|--------|------|
| 10 | SRV-01 | R750 | ABC123 | Server |
| 12 | SW-01 | C3850 | DEF456 | Switch |
```

## Edge cases

- **Rack not found:** "Rack 'X' not found. Check name and site."
- **Empty rack:** "Rack 'X' is empty."
- **Tool error:** "NetBox query failed: [error]."

## Examples

**Input:** "What's in rack R16?"
**Tool call:** `netbox_rack_inventory("R16")`
**Output:** Rack summary + device table.
