---
name: netbox-rack-full
description: Get complete rack context including devices, power feeds, and cables in one call
tools: [netbox_rack_full]
---

# NetBox Rack Full

## When to use

- "Everything in rack R16"
- "Full rack inventory for R16"
- "Show me all devices and cables in rack R16"
- "همه چیز رک R16 رو بده"
- "موجودی کامل رک R16 رو نشون بده"

## How to resolve

1. Call `netbox_rack_full` with rack name and optional site.
2. Present rack summary + device table + power feeds + cable list.

## How to present

```
**Rack:** R16 (Site: DC-Primary, Height: 42U)

**Power Feeds:**
| Name | Voltage | Amperage | Max Utilization |
|------|---------|----------|-----------------|
| PDU-A | 240V | 30A | 80% |

**Devices (12):**
| U | Device | Model | Serial | Role |
|---|--------|-------|--------|------|
| 10 | SRV-01 | R750 | ABC123 | Server |
| 12 | SW-01 | C3850 | DEF456 | Switch |

**Cables (8):**
| A-End | B-End | Type | Status |
|-------|-------|------|--------|
| SRV-01:eth0 | SW-01:Gi1/0/1 | Cat6 | connected |
```

## Edge cases

- **Rack not found:** "Rack 'X' not found. Check name and site."
- **Empty rack:** "Rack 'X' is empty."

## Examples

**Input:** "Everything in rack R16"
**Tool call:** `netbox_rack_full("R16")`
**Output:** Rack summary + devices + power + cables.
