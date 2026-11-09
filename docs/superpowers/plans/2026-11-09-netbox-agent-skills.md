# NetBox Agent Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create 7 bilingual (EN/FA) task-oriented agent skills for Brain Bot (NanoCortex) plus 2 compiled system prompts, all read-only against netbox-mcp.

**Architecture:** Each skill lives in `skills/netbox-<name>/` with `SKILL.md` (English, canonical) and `SKILL.fa.md` (Persian). A compiled NanoCortex prompt aggregates all skills into a single system prompt file for Brain Bot.

**Tech Stack:** Markdown with YAML frontmatter. No code dependencies.

**Spec:** `docs/superpowers/specs/2026-11-09-netbox-agent-skills-design.md`

## Global Constraints

- All NetBox operations are **read-only** via netbox-mcp tools only.
- `SKILL.md` is always English (canonical); `SKILL.fa.md` is the Persian translation.
- Brain Bot responds in the user's language (EN query → EN response, FA query → FA response).
- Each skill's frontmatter must include: `name`, `description`, `tools` (list of MCP tool names).
- Output formats: tables for multi-item results, compact cards for single devices.
- Error handling: not found → suggest search; multiple matches → ask to clarify; error → report and suggest connectivity check.

---

### Task 1: netbox-device-lookup skill

**Files:**
- Create: `skills/netbox-device-lookup/SKILL.md`
- Create: `skills/netbox-device-lookup/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_get_device(identifier: str) -> str`, `netbox_search_devices(query: str, limit: int = 10) -> str`

- [ ] **Step 1: Write SKILL.md**

```markdown
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
**Site:** Tehran-DC1
**Rack:** R16 (U10)
**Status:** active
**Management IP:** 10.0.1.5
**Custom Fields:** cpu=64 cores, ram=512GB
```

Multiple matches → table:

```
| Name | Serial | Role | Model | Site |
|------|--------|------|-------|------|
| SRV-01 | ABC123 | Server | R750 | Tehran |
| SRV-01B | ABC124 | Server | R750 | Tehran |
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
```

- [ ] **Step 2: Write SKILL.fa.md**

Persian translation of the above, keeping tool names and code in English.

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-device-lookup/
git commit -m "feat: add netbox-device-lookup skill (EN/FA)"
```

---

### Task 2: netbox-rack-inventory skill

**Files:**
- Create: `skills/netbox-rack-inventory/SKILL.md`
- Create: `skills/netbox-rack-inventory/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_rack_inventory(rack_name: str, site: str = "") -> str`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-rack-inventory
description: List all devices in a rack with U positions and power feed information
tools: [netbox_rack_inventory, netbox_get_device]
---

# NetBox Rack Inventory

## When to use

- "What's in rack R16?"
- "Show me rack R16 at SiteA"
- "List devices in rack R16"
- "رک R16 چی توشه؟"
- "دستگاه‌های رک R16 رو لیست کن"

## How to resolve

1. Call `netbox_rack_inventory` with rack name and optional site.
2. If rack not found, suggest checking rack name or site.
3. Present device list sorted by U position.

## How to present

```
**Rack:** R16 (Site: Tehran-DC1, Height: 42U)
**Power Feed:** PDU-A (240V, 30A, max 80% utilization)

| U | Device | Model | Serial | Role |
|---|--------|-------|--------|------|
| 10 | SRV-01 | R750 | ABC123 | Server |
| 12 | SW-01 | C3850 | DEF456 | Switch |
```

## Edge cases

- **Rack not found:** "Rack 'X' not found. Check name and site."
- **Empty rack:** "Rack 'X' is empty."
- **Tool error:** "NetBox query failed: [error]."

## Examples

**Input:** "What's in rack R16?"
**Tool call:** `netbox_rack_inventory("R16")`
**Output:** Rack summary + device table.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-rack-inventory/
git commit -m "feat: add netbox-rack-inventory skill (EN/FA)"
```

---

### Task 3: netbox-ip-lookup skill

**Files:**
- Create: `skills/netbox-ip-lookup/SKILL.md`
- Create: `skills/netbox-ip-lookup/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_lookup_ip(address: str) -> str`

- [ ] **Step 1: Write SKILL.md**

```markdown
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
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-ip-lookup/
git commit -m "feat: add netbox-ip-lookup skill (EN/FA)"
```

---

### Task 4: netbox-interface-details skill

**Files:**
- Create: `skills/netbox-interface-details/SKILL.md`
- Create: `skills/netbox-interface-details/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_interface_info(device: str) -> str`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-interface-details
description: Show all interfaces of a device with their assigned IP addresses
tools: [netbox_interface_info]
---

# NetBox Interface Details

## When to use

- "Show interfaces on SW-01"
- "What interfaces does SRV-01 have?"
- "IPs on Gi1/0/1"
- "اینترفیس‌های SW-01 رو نشون بده"
- "اینترفیس Gi1/0/1 چه IP هایی داره؟"

## How to resolve

1. Call `netbox_interface_info` with device name.
2. Filter or highlight specific interface if user asked for one.
3. Present as table.

## How to present

```
**Device:** SW-01

| Interface | Type | Mode | MAC | IPs |
|-----------|------|------|-----|-----|
| Gi1/0/1 | 1000BASE-T | access | aa:bb:cc:dd:ee:ff | 10.0.1.1/24 |
| Gi1/0/2 | 1000BASE-T | trunk | aa:bb:cc:dd:ee:ff | — |
```

## Edge cases

- **Device not found:** "Device 'X' not found."
- **No interfaces:** "Device 'X' has no interfaces in NetBox."
- **Interface not found:** "Interface 'Y' not found on device 'X'."

## Examples

**Input:** "Show interfaces on SW-01"
**Tool call:** `netbox_interface_info("SW-01")`
**Output:** Interface table.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-interface-details/
git commit -m "feat: add netbox-interface-details skill (EN/FA)"
```

---

### Task 5: netbox-power-check skill

**Files:**
- Create: `skills/netbox-power-check/SKILL.md`
- Create: `skills/netbox-power-check/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_device_power(device: str) -> str`, `netbox_rack_inventory(rack_name: str, site: str = "") -> str`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-power-check
description: Check power draw of a device or power capacity of a rack
tools: [netbox_device_power, netbox_rack_inventory]
---

# NetBox Power Check

## When to use

- "Power draw of SRV-01"
- "How much power does SRV-01 use?"
- "Rack R16 power capacity"
- "مصرف برق SRV-01 چقدره؟"
- "ظرفیت برق رک R16 چقدره؟"

## How to resolve

For device power:
1. Call `netbox_device_power` with device name.
2. Present PSU draw and rack feed context.

For rack power:
1. Call `netbox_rack_inventory` with rack name.
2. Extract power feed information.
3. Present feed spec and utilization.

## How to present

Device power:
```
**Device:** SRV-01
**PSU1:** 450W allocated / 750W max
**Rack Feed:** PDU-A (240V, 30A, max 80% = 5.76kW)
```

Rack power:
```
**Rack R16 Power**
**Feed:** PDU-A
**Spec:** 240V, 30A
**Max Utilization:** 80% (5.76kW)
```

## Edge cases

- **No power data:** "No power information for device 'X'."
- **Rack not found:** "Rack 'X' not found."

## Examples

**Input:** "Power draw of SRV-01"
**Tool call:** `netbox_device_power("SRV-01")`
**Output:** PSU draw + feed context.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-power-check/
git commit -m "feat: add netbox-power-check skill (EN/FA)"
```

---

### Task 6: netbox-search-devices skill

**Files:**
- Create: `skills/netbox-search-devices/SKILL.md`
- Create: `skills/netbox-search-devices/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_search_devices(query: str, limit: int = 10) -> str`

- [ ] **Step 1: Write SKILL.md**

```markdown
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
| SW-01 | ABC123 | Switch | C3850 | Tehran |
| SW-02 | ABC124 | Switch | C3850 | Tehran |
| SW-03 | ABC125 | Switch | C9300 | Isfahan |
```

## Edge cases

- **No results:** "No devices found matching 'X'."
- **Too many results:** "Found N devices. Showing first 10. Narrow your search."

## Examples

**Input:** "Find all Cisco switches"
**Tool call:** `netbox_search_devices("Cisco")`
**Output:** Filtered device table.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-search-devices/
git commit -m "feat: add netbox-search-devices skill (EN/FA)"
```

---

### Task 7: netbox-troubleshoot-cabling skill

**Files:**
- Create: `skills/netbox-troubleshoot-cabling/SKILL.md`
- Create: `skills/netbox-troubleshoot-cabling/SKILL.fa.md`

**Interfaces:**
- Produces: `netbox_interface_info(device: str) -> str`, `netbox_get_device(identifier: str) -> str`, `netbox_lookup_ip(address: str) -> str`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: netbox-troubleshoot-cabling
description: Trace cabling between devices by resolving interfaces and neighbor devices
tools: [netbox_interface_info, netbox_get_device, netbox_lookup_ip]
---

# NetBox Troubleshoot Cabling

## When to use

- "What's connected to SW-01 Gi1/0/1?"
- "Trace path from SRV-01 to switch"
- "Show me cabling between SW-01 and SW-02"
- "به SW-01 پورت Gi1/0/1 چی وصله؟"
- "مسیر SRV-01 به سوییچ رو trace کن"

## How to resolve

1. Call `netbox_interface_info` on the source device.
2. Identify the target interface.
3. If interface has cable/linked information, extract neighbor device/interface.
4. Call `netbox_get_device` on neighbor to get details.
5. Present the chain: Device → Interface → Cable → Neighbor Device → Neighbor Interface.

## How to present

```
**Path:** SRV-01 → SW-01

| Hop | Device | Interface | IP |
|-----|--------|-----------|-----|
| 1 | SRV-01 | eth0 | 10.0.1.5 |
| 2 | SW-01 | Gi1/0/1 | 10.0.1.1 |
```

## Edge cases

- **No cable info:** "Interface 'X' has no cable information in NetBox."
- **Neighbor not found:** "Neighbor device not found in NetBox."

## Examples

**Input:** "What's connected to SW-01 Gi1/0/1?"
**Tool call:** `netbox_interface_info("SW-01")`
**Output:** Interface details with neighbor info if available.
```

- [ ] **Step 2: Write SKILL.fa.md**

- [ ] **Step 3: Commit**

```bash
git add skills/netbox-troubleshoot-cabling/
git commit -m "feat: add netbox-troubleshoot-cabling skill (EN/FA)"
```

---

### Task 8: Update skills README indexes

**Files:**
- Modify: `skills/README.md`
- Create: `skills/README.fa.md`

**Interfaces:**
- Consumes: All 7 skill names and descriptions

- [ ] **Step 1: Update README.md**

Replace contents with:

```markdown
# NetBox Agent Skills

Bilingual (English/Persian) task-oriented skills for Brain Bot (NanoCortex) to query NetBox via netbox-mcp.

## Skills

| Skill | English | Persian | Description |
|-------|---------|---------|-------------|
| Device Lookup | [SKILL.md](netbox-device-lookup/SKILL.md) | [SKILL.fa.md](netbox-device-lookup/SKILL.fa.md) | Resolve device by name, serial, or IP |
| Rack Inventory | [SKILL.md](netbox-rack-inventory/SKILL.md) | [SKILL.fa.md](netbox-rack-inventory/SKILL.fa.md) | List devices in a rack with U positions |
| IP Lookup | [SKILL.md](netbox-ip-lookup/SKILL.md) | [SKILL.fa.md](netbox-ip-lookup/SKILL.fa.md) | Resolve IP to device, interface, prefix |
| Interface Details | [SKILL.md](netbox-interface-details/SKILL.md) | [SKILL.fa.md](netbox-interface-details/SKILL.fa.md) | Show interfaces and IPs of a device |
| Power Check | [SKILL.md](netbox-power-check/SKILL.md) | [SKILL.fa.md](netbox-power-check/SKILL.fa.md) | Device power draw or rack power capacity |
| Search Devices | [SKILL.md](netbox-search-devices/SKILL.md) | [SKILL.fa.md](netbox-search-devices/SKILL.fa.md) | Search devices by substring |
| Troubleshoot Cabling | [SKILL.md](netbox-troubleshoot-cabling/SKILL.md) | [SKILL.fa.md](netbox-troubleshoot-cabling/SKILL.fa.md) | Trace cabling between devices |

## Usage

- **Superpowers agents:** Load the `SKILL.md` file for the relevant task.
- **Brain Bot (NanoCortex):** Use the compiled prompt in `nanocortex/netbox-prompt.md` (English) or `nanocortex/netbox-prompt.fa.md` (Persian).

## Language rule

Brain Bot responds in the user's language: Persian query → Persian response, English query → English response.
```

- [ ] **Step 2: Create README.fa.md**

Persian translation of the above.

- [ ] **Step 3: Commit**

```bash
git add skills/README.md skills/README.fa.md
git commit -m "docs: update skills README indexes (EN/FA)"
```

---

### Task 9: Create NanoCortex system prompts

**Files:**
- Create: `nanocortex/netbox-prompt.md`
- Create: `nanocortex/netbox-prompt.fa.md`

**Interfaces:**
- Consumes: All 7 skills, 6 MCP tools

- [ ] **Step 1: Create nanocortex/netbox-prompt.md**

```markdown
# NetBox Assistant — Brain Bot System Prompt

You are a NetBox inventory assistant. You have access to 6 read-only tools to query NetBox.

## Available Tools

1. **netbox_get_device(identifier)** — Full device record by name, serial, or management IP
2. **netbox_search_devices(query, limit=10)** — Search devices by name/serial substring
3. **netbox_rack_inventory(rack_name, site="")** — All devices in a rack with U positions and power feed
4. **netbox_interface_info(device)** — All interfaces of a device with assigned IPs
5. **netbox_lookup_ip(address)** — Who owns an IP: device, interface, prefix, DNS
6. **netbox_device_power(device)** — Power draw of a device + rack feed spec

## Decision Guide

| User asks about... | Use tool |
|-------------------|----------|
| Specific device (name/serial/IP) | netbox_get_device |
| Multiple devices / search | netbox_search_devices |
| Rack contents | netbox_rack_inventory |
| Device interfaces | netbox_interface_info |
| IP ownership | netbox_lookup_ip |
| Device power / rack power | netbox_device_power or netbox_rack_inventory |
| Cabling / what's connected | netbox_interface_info → netbox_get_device |

## Language Rule

- User writes in English → respond in English
- User writes in Persian → respond in Persian
- Tool names and technical terms stay in English

## Output Formatting

- Single device → compact card (name, role, model, serial, site, rack, status, IP)
- Multiple devices → table
- Rack → summary + table of devices by U position
- IP → ownership card (IP, device, interface, prefix, DNS)

## Error Handling

- Device not found → suggest netbox_search_devices with partial name
- Multiple matches → list options, ask user to clarify
- Tool error → report error, suggest checking NetBox connectivity
- Empty result → explain search scope, offer alternative query

## Examples

**User:** "What is SRV-01?"
**Action:** netbox_get_device("SRV-01")
**Response:** Compact card with device details.

**User:** "رک R16 چی توشه؟"
**Action:** netbox_rack_inventory("R16")
**Response:** Rack summary + device table in Persian.

**User:** "Who owns 10.0.1.5?"
**Action:** netbox_lookup_ip("10.0.1.5")
**Response:** IP ownership card.
```

- [ ] **Step 2: Create nanocortex/netbox-prompt.fa.md**

Persian translation with Persian examples.

- [ ] **Step 3: Commit**

```bash
git add nanocortex/
git commit -m "feat: add NanoCortex system prompts (EN/FA)"
```

---

### Task 10: Final verification and push

**Files:**
- Verify all 18 files exist

- [ ] **Step 1: Verify file count**

Run:
```bash
Get-ChildItem -Recurse skills/, nanocortex/ | Measure-Object | Select-Object -ExpandProperty Count
```
Expected: 18 (7 skills × 2 files + 2 READMEs + 2 prompts)

- [ ] **Step 2: Verify all SKILL.md frontmatter**

Check each SKILL.md has name, description, tools in YAML frontmatter.

- [ ] **Step 3: Push to GitHub**

```bash
git push origin main
```
