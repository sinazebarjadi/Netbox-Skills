---
name: netbox-prefix-full
description: Get complete prefix context including VLAN, VRF, available IPs, and child prefixes in one call
tools: [netbox_prefix_full]
---

# NetBox Prefix Full

## When to use

- "Everything about 10.0.1.0/24"
- "Full prefix details for 10.0.1.0/24"
- "Show me complete information about this subnet"
- "همه اطلاعات 10.0.1.0/24 رو بده"
- "جزئیات کامل ساب‌نت 10.0.1.0/24 رو نشون بده"

## How to resolve

1. Call `netbox_prefix_full` with the CIDR.
2. Present prefix card + VLAN + VRF + available IPs + child prefixes.

## How to present

```
**Prefix:** 10.0.1.0/24
**Status:** active
**Description:** Server subnet

**VLAN:** 100 (Servers)
**VRF:** default
**Site:** DC-Primary

**Available IPs (sample):**
| IP | Status |
|----|--------|
| 10.0.1.50 | available |
| 10.0.1.51 | available |

**Child Prefixes:**
| Prefix | Description |
|--------|-------------|
| 10.0.1.0/26 | Servers-A |
| 10.0.1.64/26 | Servers-B |
```

## Edge cases

- **Prefix not found:** "Prefix 'X' not found in NetBox."
- **No free IPs:** "No available IPs in prefix 'X'."
- **No children:** "No child prefixes for 'X'."

## Examples

**Input:** "Everything about 10.0.1.0/24"
**Tool call:** `netbox_prefix_full("10.0.1.0/24")`
**Output:** Complete prefix context.
