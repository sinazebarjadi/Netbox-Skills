# Netbox-Skills

A collection of reusable agent skills, tools, and reference material for working with [NetBox](https://netbox.dev/) — the open-source DCIM/IPAM platform.

## What's inside

| Path | Description |
|------|-------------|
| `skills/` | Agent skills (SKILL.md format) for NetBox workflows |
| `netbox-mcp/` | Read-only MCP server exposing NetBox inventory to AI agents |
| `docs/` | Design specs and implementation plans for NetBox integrations |

## netbox-mcp

A read-only [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes NetBox inventory to AI agents (Brain Bot / NanoCortex).

**Tools provided:**

| Tool | Description |
|------|-------------|
| `netbox_get_device` | Full device record by name / serial / management IP |
| `netbox_search_devices` | Substring search across name + serial |
| `netbox_rack_inventory` | All devices in a rack with U positions + power feed |
| `netbox_interface_info` | Interfaces of a device + assigned IPs |
| `netbox_lookup_ip` | Who owns an IP: device, interface, prefix, DNS |
| `netbox_device_power` | Live PSU draw + rack feed electrical spec |

See [`netbox-mcp/README.md`](netbox-mcp/README.md) for setup and deployment.

## Skills

Agent skills follow the [SKILL.md convention](https://github.com/obra/superpowers) — a markdown file with frontmatter that teaches an AI agent how to perform a specific NetBox task.

## License

MIT
