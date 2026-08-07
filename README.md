# Teacher

A Claude Code **plugin marketplace**, not an application — nothing here is deployed.

```
.claude-plugin/marketplace.json     marketplace "claude-teacher"
plugins/claude-teacher/
  .claude-plugin/plugin.json        plugin "claude-teacher"
```

## Install

```bash
/plugin marketplace add roflganker/Teacher
/plugin install claude-teacher@claude-teacher
```

## Adding to the plugin

A plugin's components live beside its manifest, in conventional directories that Claude Code
discovers automatically:

```
plugins/claude-teacher/
  .claude-plugin/plugin.json
  skills/<name>/SKILL.md           skills (YAML frontmatter: name + description)
  commands/<name>.md               slash commands
  agents/<name>.md                 subagents
  hooks/hooks.json                 hooks
```

## Releasing

Bump `version` in `plugins/claude-teacher/.claude-plugin/plugin.json` **in the same commit as the
change**, then push. Without the bump `claude plugin update` reports "already at the latest
version" and does nothing, so the edit never reaches anyone who has it installed.
