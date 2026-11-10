---
name: netbox-device-neighbors
description: Show directly connected devices via cables for a given device
tools: [netbox_device_neighbors]
---

# NetBox Device Neighbors

## When to use

- "What's connected to SRV-01?"
- "Show neighbors of SW-01"
- "What devices are directly connected to this server?"
- "به SRV-01 چی وصله؟"
- "همسایه‌های SW-01 رو نشون بده"

## How to resolve

1. Call `netbox_device_neighbors` with the device identifier.
2. Present device + neighbor table.

## How to present

```
**Device:** SRV-01

**Directly Connected Devices:**
| Local Interface | Cable | Neighbor Device | Neighbor Interface |
|-----------------|-------|-----------------|--------------------|
| eth0 | #101 | SW-01 | Gi1/0/1 |
| eth1 | #102 | SW-01 | Gi1/0/2 |
```

## Edge cases

- **Device not found:** "Device 'X' not found."
- **No neighbors:** "No directly connected devices found for 'X'."

## Examples

**Input:** "What's connected to SRV-01?"
**Tool call:** `netbox_device_neighbors("SRV-01")`
**Output:** Device + neighbor table.
