---
name: netbox-vrf-list
description: List VRFs (Virtual Routing and Forwarding instances) in NetBox
tools: [netbox_list_vrfs]
---

# NetBox VRF List

## When to use

- "List all VRFs"
- "What VRFs exist?"
- "Show me VRF information"
- "VRF ها رو لیست کن"
- "چه VRF هایی داریم؟"

## How to resolve

1. Call `netbox_list_vrfs`.
2. Present as table.

## How to present

```
| Name | RD | Description |
|------|----|-------------|
| default | — | Default VRF |
| management | 65000:100 | Management network |
| production | 65000:200 | Production network |
```

## Edge cases

- **No VRFs:** "No VRFs found in NetBox."

## Examples

**Input:** "List all VRFs"
**Tool call:** `netbox_list_vrfs()`
**Output:** VRF table.
