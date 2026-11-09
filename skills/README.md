# NetBox Agent Skills

This directory holds reusable agent skills for NetBox workflows. Each skill is a
subdirectory containing a `SKILL.md` file with YAML frontmatter:

```
skills/
  netbox-device-onboarding/
    SKILL.md
  netbox-ipam-audit/
    SKILL.md
```

## SKILL.md format

```markdown
---
name: skill-name
description: One-line summary of when to use this skill.
---

# Skill Title

Step-by-step instructions the agent follows when this skill is invoked.
```

Skills are loaded on demand by agents that support the convention (e.g.
[superpowers](https://github.com/obra/superpowers)).
