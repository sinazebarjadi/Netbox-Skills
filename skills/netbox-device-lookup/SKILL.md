---
name: netbox-device-lookup
description: Resolve a device by name, serial, or management IP and present its full inventory record
tools: [netbox_get_device, netbox_search_devices]
---

# NetBox Device Lookup

## When to use

User asks about a specific device:
- "What is SRV-01?"
- "Tell me about server web-02"
- "Show me device with serial ABC123"
- "What device has IP 10.0.1.5?"
- "دستگاه SRV-01 چیست؟"
- "سریال ABC123 رو نشون بده"

## How to resolve

1. Call `netbox_get_device` with the identifier (name, serial, or IP).
2. If result has `"found": false`, call `netbox_search_devices` with the same identifier to find partial matches.
3. If search returns candidates, present them and ask user to clarify.
4. If no candidates, report device not found.

## How to present

Single device → compact card:

```
**Device:** SRV-01
**Role:** Server
**Model:** Dell PowerEdge R750
**Serial:** ABC123
**Asset Tag:** 35350123
**Site:** DC-Primary
**Rack:** R16 (U10)
**Status:** active
**Management IP:** 10.0.1.5
**Custom Fields:** cpu=64 cores, ram=512GB
```

Multiple matches → table:

```
| Name | Serial | Role | Model | Site |
|------|--------|------|-------|------|
| SRV-01 | ABC123 | Server | R750 | City-A |
| SRV-01B | ABC124 | Server | R750 | City-A |
```

## Edge cases

- **Not found:** "Device 'X' not found. Try a partial name search."
- **Multiple matches:** "Multiple devices match 'X'. Which one?" + table
- **Tool error:** "NetBox query failed: [error]. Check NetBox connectivity."

## Examples

**Input:** "What is SRV-01?"
**Tool call:** `netbox_get_device("SRV-01")`
**Output:** Compact card with device details.

**Input:** "دستگاه با سریال ABC123 رو پیدا کن"
**Tool call:** `netbox_get_device("ABC123")`
**Output:** Compact card in Persian.
