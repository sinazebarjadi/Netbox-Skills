---
name: netbox-ipam-prefixes
description: List IPAM prefixes and find available IPs within a prefix
tools: [netbox_list_prefixes, netbox_prefix_detail]
---

# NetBox IPAM Prefixes

## When to use

- "What subnets exist at SiteA?"
- "Show me all prefixes"
- "Find free IPs in 10.0.1.0/24"
- "What VRF is 10.0.1.0/24 in?"
- "چه ساب‌نت‌هایی تو سایت A داریم؟"
- "IP های خالی تو 10.0.1.0/24 رو پیدا کن"

## How to resolve

For listing prefixes:
1. Call `netbox_list_prefixes` with optional site/family/q filters.
2. Present as table.

For prefix detail + free IPs:
1. Call `netbox_prefix_detail` with the CIDR.
2. Show prefix info + available IPs sample.

## How to present

Prefix list:
```
| Prefix | VRF | Site | VLAN | Status | Description |
|--------|-----|------|------|--------|-------------|
| 10.0.1.0/24 | default | Tehran | 100 | active | Servers |
| 10.0.2.0/24 | default | Tehran | 200 | active | Management |
```

Prefix detail:
```
**Prefix:** 10.0.1.0/24
**VRF:** default
**Site:** Tehran-DC1
**VLAN:** 100
**Status:** active
**Description:** Server subnet

**Available IPs (sample):**
| IP | Status |
|----|--------|
| 10.0.1.50 | available |
| 10.0.1.51 | available |
```

## Edge cases

- **No prefixes:** "No prefixes found matching your criteria."
- **Prefix not found:** "Prefix 'X' not found in NetBox."
- **No free IPs:** "No available IPs in prefix 'X'."

## Examples

**Input:** "What subnets at SiteA?"
**Tool call:** `netbox_list_prefixes(site="SiteA")`
**Output:** Prefix table.

**Input:** "Find free IPs in 10.0.1.0/24"
**Tool call:** `netbox_prefix_detail("10.0.1.0/24")`
**Output:** Prefix detail + available IPs.
