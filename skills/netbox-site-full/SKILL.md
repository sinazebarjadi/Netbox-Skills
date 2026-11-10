---
name: netbox-site-full
description: Get complete site context including racks, devices, prefixes, and VLANs in one call
tools: [netbox_site_full]
---

# NetBox Site Full

## When to use

- "Everything about site X"
- "Full site overview for DC-Primary"
- "Show me complete information about this site"
- "همه اطلاعات سایت X رو بده"
- "نمای کامل سایت X رو نشون بده"

## How to resolve

1. Call `netbox_site_full` with site name.
2. Present site card + rack list + device count + prefix table + VLAN table.

## How to present

```
**Site:** DC-Primary
**Status:** active
**Region:** City-A

**Racks (5):**
| Name | U Height | Devices |
|------|----------|---------|
| R16 | 42U | 12 |
| R17 | 42U | 8 |

**Total Devices:** 42

**Prefixes (10):**
| Prefix | VRF | VLAN | Description |
|--------|-----|------|-------------|
| 10.0.1.0/24 | default | 100 | Servers |
| 10.0.2.0/24 | default | 200 | Management |

**VLANs (5):**
| VID | Name | Status |
|-----|------|--------|
| 100 | Servers | active |
| 200 | Management | active |
```

## Edge cases

- **Site not found:** "Site 'X' not found."
- **No racks:** "Site 'X' has no racks."

## Examples

**Input:** "Everything about DC-Primary"
**Tool call:** `netbox_site_full("DC-Primary")`
**Output:** Complete site context.
