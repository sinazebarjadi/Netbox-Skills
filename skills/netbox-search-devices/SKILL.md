---
name: netbox-search-devices
description: Search NetBox devices by name, serial, role, or model substring
tools: [netbox_search_devices]
---

# NetBox Search Devices

## When to use

- "Find all Cisco switches"
- "List servers at SiteA"
- "Search for Dell devices"
- "Find devices with serial starting ABC"
- "همه سوییچ‌های سیسکو رو پیدا کن"
- "سرورهای سایت A رو لیست کن"

## How to resolve

1. Call `netbox_search_devices` with query string.
2. If user specified site/role/model, filter results client-side after retrieval.
3. Present as table.

## How to present

```
**Found 3 devices:**

| Name | Serial | Role | Model | Site |
|------|--------|------|-------|------|
| SW-01 | ABC123 | Switch | C3850 | City-A |
| SW-02 | ABC124 | Switch | C3850 | City-A |
| SW-03 | ABC125 | Switch | C9300 | City-B |
```

## Edge cases

- **No results:** "No devices found matching 'X'."
- **Too many results:** "Found N devices. Showing first 10. Narrow your search."

## Examples

**Input:** "Find all Cisco switches"
**Tool call:** `netbox_search_devices("Cisco")`
**Output:** Filtered device table.
