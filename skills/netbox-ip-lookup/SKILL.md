---
name: netbox-ip-lookup
description: Resolve an IP address to its owning device, interface, prefix, and DNS record
tools: [netbox_lookup_ip]
---

# NetBox IP Lookup

## When to use

- "Who owns IP 10.0.1.5?"
- "What device has IP 10.0.1.5?"
- "Show me details for 10.0.1.5"
- "IP 10.0.1.5 مال کیه؟"
- "چه دستگاهی IP 10.0.1.5 رو داره؟"

## How to resolve

1. Call `netbox_lookup_ip` with the IP address.
2. Extract device, interface, prefix, and DNS from result.
3. If no matches, report IP not found.

## How to present

```
**IP:** 10.0.1.5/24
**Status:** active
**DNS:** srv-01.example.com
**Device:** SRV-01 (Dell R750, Tehran-DC1)
**Interface:** eth0 (MAC: aa:bb:cc:dd:ee:ff)
**Prefix:** 10.0.1.0/24 (VLAN 100)
```

## Edge cases

- **IP not found:** "IP 'X' not found in NetBox."
- **Multiple records:** "Multiple records for 'X':" + list
- **No device assigned:** "IP 'X' exists but is not assigned to a device."

## Examples

**Input:** "Who owns 10.0.1.5?"
**Tool call:** `netbox_lookup_ip("10.0.1.5")`
**Output:** IP ownership card.
