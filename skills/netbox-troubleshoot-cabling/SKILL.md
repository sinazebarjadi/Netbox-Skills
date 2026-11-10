---
name: netbox-troubleshoot-cabling
description: Trace cabling between devices by resolving interfaces and neighbor devices
tools: [netbox_interface_info, netbox_get_device, netbox_lookup_ip]
---

## Prefer composite tools

For complex questions, use the composite tool instead of chaining:
- "Connected devices" → `netbox_device_neighbors` (not `netbox_interface_info` + `netbox_trace_cable`)
- "Full device details including cables" → `netbox_device_full` (not `netbox_get_device` + `netbox_interface_info`)

Use the simple tool below only for quick single-fact lookups.

# NetBox Troubleshoot Cabling

## When to use

- "What's connected to SW-01 Gi1/0/1?"
- "Trace path from SRV-01 to switch"
- "Show me cabling between SW-01 and SW-02"
- "به SW-01 پورت Gi1/0/1 چی وصله؟"
- "مسیر SRV-01 به سوییچ رو trace کن"

## How to resolve

1. Call `netbox_interface_info` on the source device.
2. Identify the target interface.
3. If interface has cable/linked information, extract neighbor device/interface.
4. Call `netbox_get_device` on neighbor to get details.
5. Present the chain: Device → Interface → Cable → Neighbor Device → Neighbor Interface.

## How to present

```
**Path:** SRV-01 → SW-01

| Hop | Device | Interface | IP |
|-----|--------|-----------|-----|
| 1 | SRV-01 | eth0 | 10.0.1.5 |
| 2 | SW-01 | Gi1/0/1 | 10.0.1.1 |
```

## Edge cases

- **No cable info:** "Interface 'X' has no cable information in NetBox."
- **Neighbor not found:** "Neighbor device not found in NetBox."

## Examples

**Input:** "What's connected to SW-01 Gi1/0/1?"
**Tool call:** `netbox_interface_info("SW-01")`
**Output:** Interface details with neighbor info if available.
