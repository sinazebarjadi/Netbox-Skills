---
name: netbox-find-free-ips
description: Quickly find available IP addresses across prefixes
tools: [netbox_find_free_ips]
---

# NetBox Find Free IPs

## When to use

- "Find free IPs at site X"
- "Show me available addresses in 10.0.1.0/24"
- "I need 5 free IPs for new servers"
- "IP های خالی تو سایت X رو پیدا کن"
- "۵ تا IP خالی برای سرورهای جدید می‌خوام"

## How to resolve

1. Call `netbox_find_free_ips` with optional site/family/count.
2. Present free IP table.

## How to present

```
**Available IPs (5):**

| Address | Prefix | Site | VLAN |
|---------|--------|------|------|
| 10.0.1.50 | 10.0.1.0/24 | DC-Primary | Servers |
| 10.0.1.51 | 10.0.1.0/24 | DC-Primary | Servers |
| 10.0.2.10 | 10.0.2.0/24 | DC-Primary | Management |
```

## Edge cases

- **No free IPs:** "No available IPs found matching your criteria."
- **Site not found:** "Site 'X' not found."

## Examples

**Input:** "Find 5 free IPs at DC-Primary"
**Tool call:** `netbox_find_free_ips(site="DC-Primary", count=5)`
**Output:** Free IP table.
