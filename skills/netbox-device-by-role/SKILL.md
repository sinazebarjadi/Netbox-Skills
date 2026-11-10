---
name: netbox-device-by-role
description: List devices filtered by role name and optional site
tools: [netbox_device_by_role]
---

# NetBox Device By Role

## When to use

- "List all switches"
- "Show servers at site X"
- "Find all firewalls"
- "همه سوییچ‌ها رو لیست کن"
- "سرورهای سایت X رو نشون بده"

## How to resolve

1. Call `netbox_device_by_role` with role name and optional site.
2. Present device table.

## How to present

```
**Devices with role 'Switch' (3):**

| Name | Serial | Model | Site | Rack |
|------|--------|-------|------|------|
| SW-01 | ABC123 | C3850 | DC-Primary | R16 |
| SW-02 | ABC124 | C3850 | DC-Primary | R17 |
| SW-03 | ABC125 | C9300 | DC-Secondary | R01 |
```

## Edge cases

- **No devices:** "No devices found with role 'X'."
- **Site not found:** "Site 'X' not found."

## Examples

**Input:** "List all switches"
**Tool call:** `netbox_device_by_role("Switch")`
**Output:** Device table.

**Input:** "Show servers at DC-Primary"
**Tool call:** `netbox_device_by_role("Server", site="DC-Primary")`
**Output:** Filtered device table.
