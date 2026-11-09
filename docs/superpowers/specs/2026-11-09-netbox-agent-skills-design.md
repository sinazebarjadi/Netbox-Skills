# NetBox Agent Skills for Brain Bot — Design Spec

**Date:** 2026-11-09
**Status:** Approved (brainstorming complete, pending implementation plan)
**Scope:** Create bilingual (English + Persian) task-oriented agent skills for Brain Bot (NanoCortex) covering NetBox device lookup, rack inventory, IPAM queries, interface details, power checks, device search, and cabling troubleshooting. All skills are read-only, consuming the existing netbox-mcp tools.

---

## 1. Decisions (locked during brainstorming)

| Question | Decision |
|----------|----------|
| Target agent | Brain Bot (NanoCortex) |
| Primary use cases | Device lookup, IPAM queries, troubleshooting/cabling, full coverage |
| Read/write mode | Read-only only |
| Skill organization | Task-oriented (Approach A) |
| Bilingual | English + Persian; SKILL.md = English canonical, SKILL.fa.md = Persian |
| Response language | Match user language (Persian query → Persian response) |

## 2. Architecture

| Path | Purpose |
|------|---------|
| `skills/netbox-*/SKILL.md` | English skill definition (canonical, agent-loadable) |
| `skills/netbox-*/SKILL.fa.md` | Persian translation for documentation/human review |
| `skills/README.md` | English index of all skills |
| `skills/README.fa.md` | Persian index |
| `nanocortex/netbox-prompt.md` | Compiled Brain Bot system prompt (English) |
| `nanocortex/netbox-prompt.fa.md` | Compiled Brain Bot system prompt (Persian) |

## 3. Skill Set

| Skill | Trigger Examples | Tools | Output |
|-------|-----------------|-------|--------|
| `netbox-device-lookup` | "What is SRV-01?", "Show serial ABC123" | `netbox_get_device` → `netbox_search_devices` | Compact device card |
| `netbox-rack-inventory` | "What's in rack R16?", "Show rack at SiteA" | `netbox_rack_inventory` | U-position table + power feed |
| `netbox-ip-lookup` | "Who owns 10.0.1.5?", "What device has this IP?" | `netbox_lookup_ip` | IP → device → interface → prefix |
| `netbox-interface-details` | "Show interfaces on SW-01", "IPs on Gi1/0/1" | `netbox_interface_info` | Interface table with IPs |
| `netbox-power-check` | "Power draw of SRV-01", "Rack R16 power capacity" | `netbox_device_power` / `netbox_rack_inventory` | PSU draw + feed spec + utilization |
| `netbox-search-devices` | "Find all Cisco switches", "List servers at SiteA" | `netbox_search_devices` | Filtered device table |
| `netbox-troubleshoot-cabling` | "What's connected to SW-01 Gi1/0/1?" | `netbox_interface_info` → `netbox_get_device` → `netbox_lookup_ip` | Device → interface → cable → neighbor chain |

## 4. SKILL.md Format

Each `SKILL.md` contains YAML frontmatter and structured markdown:

```yaml
---
name: netbox-device-lookup
description: Resolve a device by name, serial, or IP and present its full inventory record
tools: [netbox_get_device, netbox_search_devices]
---
```

Body sections:
1. **When to use** — trigger phrases (EN + FA examples)
2. **How to resolve** — tool call sequence with parameters
3. **How to present** — output format templates (EN + FA)
4. **Edge cases** — not found, multiple matches, tool errors
5. **Examples** — 2–3 user queries with expected tool calls and outputs (EN + FA)

## 5. NanoCortex Prompt Files

`nanocortex/netbox-prompt.md` structure:
- Tool reference (6 tools, signatures, when to use)
- Decision tree mapping user questions to tools
- Output formatting rules (tables for lists, cards for single devices)
- Language rule: detect user language, respond in same language
- Error handling patterns

`nanocortex/netbox-prompt.fa.md` is the Persian translation with Persian output examples.

## 6. Error Handling Standards

| Scenario | Pattern |
|----------|---------|
| Device not found | Suggest `netbox_search_devices` with partial name |
| Multiple matches | List options, ask user to clarify |
| Tool error | Report error, suggest checking NetBox connectivity |
| Empty result | Explain search scope, offer alternative query |

All error messages and suggestions appear in the user's language (EN or FA).

## 7. Testing

Each SKILL.md includes **Examples** with:
- Input: user query (EN or FA)
- Expected tool call(s) with parameters
- Expected output format

NanoCortex prompt files are validated by feeding to Brain Bot and running the example queries.

## 8. File Manifest

```
skills/
  netbox-device-lookup/
    SKILL.md
    SKILL.fa.md
  netbox-rack-inventory/
    SKILL.md
    SKILL.fa.md
  netbox-ip-lookup/
    SKILL.md
    SKILL.fa.md
  netbox-interface-details/
    SKILL.md
    SKILL.fa.md
  netbox-power-check/
    SKILL.md
    SKILL.fa.md
  netbox-search-devices/
    SKILL.md
    SKILL.fa.md
  netbox-troubleshoot-cabling/
    SKILL.md
    SKILL.fa.md
  README.md
  README.fa.md
nanocortex/
  netbox-prompt.md
  netbox-prompt.fa.md
```

**Total:** 18 files (7 skills × 2 languages + 2 indexes + 2 prompts)
