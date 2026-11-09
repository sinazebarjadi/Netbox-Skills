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
