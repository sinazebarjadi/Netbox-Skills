---
name: netbox-device-full
description: Get complete device context including interfaces, cables, and power in one call
tools: [netbox_device_full]
---

# NetBox Device Full

## When to use

User asks for complete device information:
- "Tell me everything about SRV-01"
- "Full details of device X"
- "Show me all information about server Y"
- "همه اطلاعات SRV-01 رو بده"
- "جزئیات کامل دستگاه X رو نشون بده"

## How to resolve

1. Call `netbox_device_full` with the identifier.
2. Present device card + interface table + cable list + power summary.

## How to present

```
**Device:** SRV-01
**Role:** Server
**Model:** Dell R750
**Serial:** ABC123
**Site:** DC-Primary
**Rack:** R16 (U10)
**Status:** active
**Management IP:** 10.0.1.5

**Interfaces (3):**
| Name | Type | Mode | MAC | IPs |
|------|------|------|-----|-----|
| eth0 | 1000BASE-T | access | aa:bb:cc:dd:ee:ff | 10.0.1.5/24 |
| eth1 | 1000BASE-T | trunk | aa:bb:cc:dd:ee:00 | — |

**Cables (2):**
| Local | Remote | Type |
|-------|--------|------|
| eth0 | SW-01:Gi1/0/1 | Cat6 |
| eth1 | SW-01:Gi1/0/2 | Cat6 |

**Power:**
| PSU | Allocated | Max |
|-----|-----------|-----|
| PSU1 | 450W | 750W |
| Feed: PDU-A (240V, 30A, max 80%) |
```

## Edge cases

- **Not found:** "Device 'X' not found. Try netbox_search_devices for partial matches."
- **No cables:** "No cable information for device 'X'."
- **No power data:** "No power information for device 'X'."

## Examples

**Input:** "Tell me everything about SRV-01"
**Tool call:** `netbox_device_full("SRV-01")`
**Output:** Complete device card + interfaces + cables + power.
