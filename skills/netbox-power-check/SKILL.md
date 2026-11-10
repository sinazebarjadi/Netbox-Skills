---
name: netbox-power-check
description: Check power draw of a device or power capacity of a rack
tools: [netbox_device_power, netbox_rack_inventory]
---

## Prefer composite tools

For complex questions, use the composite tool instead of chaining:
- "Full device details including power" → `netbox_device_full` (not `netbox_get_device` + `netbox_device_power`)
- "Everything in rack including power feeds" → `netbox_rack_full` (not `netbox_rack_inventory` + `netbox_list_cables`)

Use the simple tool below only for quick single-fact lookups.

# NetBox Power Check

## When to use

- "Power draw of SRV-01"
- "How much power does SRV-01 use?"
- "Rack R16 power capacity"
- "مصرف برق SRV-01 چقدره؟"
- "ظرفیت برق رک R16 چقدره؟"

## How to resolve

For device power:
1. Call `netbox_device_power` with device name.
2. Present PSU draw and rack feed context.

For rack power:
1. Call `netbox_rack_inventory` with rack name.
2. Extract power feed information.
3. Present feed spec and utilization.

## How to present

Device power:
```
**Device:** SRV-01
**PSU1:** 450W allocated / 750W max
**Rack Feed:** PDU-A (240V, 30A, max 80% = 5.76kW)
```

Rack power:
```
**Rack R16 Power**
**Feed:** PDU-A
**Spec:** 240V, 30A
**Max Utilization:** 80% (5.76kW)
```

## Edge cases

- **No power data:** "No power information for device 'X'."
- **Rack not found:** "Rack 'X' not found."

## Examples

**Input:** "Power draw of SRV-01"
**Tool call:** `netbox_device_power("SRV-01")`
**Output:** PSU draw + feed context.
