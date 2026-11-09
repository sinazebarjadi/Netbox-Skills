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
