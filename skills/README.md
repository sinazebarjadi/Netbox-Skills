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
| IPAM Prefixes | [SKILL.md](netbox-ipam-prefixes/SKILL.md) | [SKILL.fa.md](netbox-ipam-prefixes/SKILL.fa.md) | List prefixes and find free IPs |
| VLAN Lookup | [SKILL.md](netbox-vlan-lookup/SKILL.md) | [SKILL.fa.md](netbox-vlan-lookup/SKILL.fa.md) | Look up VLANs and associated prefixes |
| VRF List | [SKILL.md](netbox-vrf-list/SKILL.md) | [SKILL.fa.md](netbox-vrf-list/SKILL.fa.md) | List VRFs |
| Cable Inventory | [SKILL.md](netbox-cable-inventory/SKILL.md) | [SKILL.fa.md](netbox-cable-inventory/SKILL.fa.md) | List cables and trace connections |
| Site Overview | [SKILL.md](netbox-site-overview/SKILL.md) | [SKILL.fa.md](netbox-site-overview/SKILL.fa.md) | List sites and show site details |
| Rack List | [SKILL.md](netbox-rack-list/SKILL.md) | [SKILL.fa.md](netbox-rack-list/SKILL.fa.md) | List all racks with optional site filter |
| Device Full | [SKILL.md](netbox-device-full/SKILL.md) | [SKILL.fa.md](netbox-device-full/SKILL.fa.md) | Complete device context in one call |
| Rack Full | [SKILL.md](netbox-rack-full/SKILL.md) | [SKILL.fa.md](netbox-rack-full/SKILL.fa.md) | Complete rack context in one call |
| IP Full | [SKILL.md](netbox-ip-full/SKILL.md) | [SKILL.fa.md](netbox-ip-full/SKILL.fa.md) | Complete IP context in one call |
| Prefix Full | [SKILL.md](netbox-prefix-full/SKILL.md) | [SKILL.fa.md](netbox-prefix-full/SKILL.fa.md) | Complete prefix context in one call |
| Site Full | [SKILL.md](netbox-site-full/SKILL.md) | [SKILL.fa.md](netbox-site-full/SKILL.fa.md) | Complete site context in one call |
| Device Neighbors | [SKILL.md](netbox-device-neighbors/SKILL.md) | [SKILL.fa.md](netbox-device-neighbors/SKILL.fa.md) | Directly connected devices |
| Find Free IPs | [SKILL.md](netbox-find-free-ips/SKILL.md) | [SKILL.fa.md](netbox-find-free-ips/SKILL.fa.md) | Quick free IP finder |
| Device By Role | [SKILL.md](netbox-device-by-role/SKILL.md) | [SKILL.fa.md](netbox-device-by-role/SKILL.fa.md) | Devices filtered by role |

## Usage

- **Superpowers agents:** Load the `SKILL.md` file for the relevant task.
- **Brain Bot (NanoCortex):** Use the compiled prompt in `nanocortex/netbox-prompt.md` (English) or `nanocortex/netbox-prompt.fa.md` (Persian).

## Language rule

Brain Bot responds in the user's language: Persian query → Persian response, English query → English response.
