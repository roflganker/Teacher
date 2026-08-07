# Teacher

A Claude Code **plugin marketplace**, not an application — nothing here is deployed.

```
.claude-plugin/marketplace.json     marketplace "teacher"
plugins/meoty/
  .claude-plugin/plugin.json        plugin "meoty"
```

## Install

```bash
/plugin marketplace add roflganker/Teacher
/plugin install meoty@teacher
```

## Adding to the plugin

A plugin's components live beside its manifest, in conventional directories that Claude Code
discovers automatically:

```
plugins/meoty/
  .claude-plugin/plugin.json
  skills/<name>/SKILL.md           skills (YAML frontmatter: name + description)
  commands/<name>.md               slash commands
  agents/<name>.md                 subagents
  hooks/hooks.json                 hooks
```

## Releasing

Bump `version` in `plugins/meoty/.claude-plugin/plugin.json` **in the same commit as the
change**, then push. Without the bump `claude plugin update` reports "already at the latest
version" and does nothing, so the edit never reaches anyone who has it installed.
