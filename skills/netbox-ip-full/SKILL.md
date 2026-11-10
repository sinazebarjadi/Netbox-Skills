---
name: netbox-ip-full
description: Get complete IP context including device, interface, prefix, VLAN, and VRF in one call
tools: [netbox_ip_full]
---

# NetBox IP Full

## When to use

- "Everything about IP 10.0.1.5"
- "Full details for 10.0.1.5"
- "Show me complete information about this IP"
- "همه اطلاعات IP 10.0.1.5 رو بده"
- "جزئیات کامل IP 10.0.1.5 رو نشون بده"

## How to resolve

1. Call `netbox_ip_full` with the IP address.
2. Present IP card + device + interface + prefix + VLAN + VRF.

## How to present

```
**IP:** 10.0.1.5/24
**Status:** active
**DNS:** srv-01.example.com

**Device:** SRV-01 (Dell R750, DC-Primary)
**Interface:** eth0 (MAC: aa:bb:cc:dd:ee:ff)

**Prefix:** 10.0.1.0/24
**VLAN:** 100 (Servers)
**VRF:** default
**Site:** DC-Primary
```

## Edge cases

- **IP not found:** "IP 'X' not found in NetBox."
- **No device assigned:** "IP 'X' exists but is not assigned to a device."
- **No prefix:** "IP 'X' is not part of any prefix in NetBox."

## Examples

**Input:** "Everything about 10.0.1.5"
**Tool call:** `netbox_ip_full("10.0.1.5")`
**Output:** Complete IP context.
