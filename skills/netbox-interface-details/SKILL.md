---
name: netbox-interface-details
description: Show all interfaces of a device with their assigned IP addresses
tools: [netbox_interface_info]
---

## Prefer composite tools

For complex questions, use the composite tool instead of chaining:
- "Full device details" → `netbox_device_full` (not `netbox_get_device` + `netbox_interface_info`)
- "Connected devices" → `netbox_device_neighbors` (not `netbox_interface_info` + `netbox_trace_cable`)

Use the simple tool below only for quick single-fact lookups.

# NetBox Interface Details

## When to use

- "Show interfaces on SW-01"
- "What interfaces does SRV-01 have?"
- "IPs on Gi1/0/1"
- "اینترفیس‌های SW-01 رو نشون بده"
- "اینترفیس Gi1/0/1 چه IP هایی داره؟"

## How to resolve

1. Call `netbox_interface_info` with device name.
2. Filter or highlight specific interface if user asked for one.
3. Present as table.

## How to present

```
**Device:** SW-01

| Interface | Type | Mode | MAC | IPs |
|-----------|------|------|-----|-----|
| Gi1/0/1 | 1000BASE-T | access | aa:bb:cc:dd:ee:ff | 10.0.1.1/24 |
| Gi1/0/2 | 1000BASE-T | trunk | aa:bb:cc:dd:ee:ff | — |
```

## Edge cases

- **Device not found:** "Device 'X' not found."
- **No interfaces:** "Device 'X' has no interfaces in NetBox."
- **Interface not found:** "Interface 'Y' not found on device 'X'."

## Examples

**Input:** "Show interfaces on SW-01"
**Tool call:** `netbox_interface_info("SW-01")`
**Output:** Interface table.
