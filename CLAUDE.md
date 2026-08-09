# CLAUDE.md

## What this repository is

A Claude Code **plugin marketplace** holding one plugin, `claude-teacher`. Nothing here is built,
tested, or deployed — there is no package manager, no test runner, no CI. The artifacts are Markdown
files that a Claude Code runtime loads: skills, agents, and the doctrine they read.

The plugin's subject is **harness development** — teaching Claude to author the pieces a harness is
made of. Skill authoring is the first of them and the only one currently complete; rule authoring is
a declared stub, and other components follow later. When adding a component, add it as its own
skill with its own doctrine, not as a section inside skill authoring.

```
.claude-plugin/marketplace.json          marketplace "claude-teacher"
plugins/claude-teacher/
  .claude-plugin/plugin.json             plugin manifest — holds `version`
  doctrine/                              the normative text; the plugin's shared core
    laws.md  archetypes.md  frontmatter.md  body.md  scripts.md
  skills/skill-authoring/SKILL.md        the procedure that applies the doctrine
  skills/skill-authoring/scripts/validate.py   mechanical checks
  skills/rule-authoring/SKILL.md         stub — says so, and says what not to assume
  agents/skill-walker.md                 read-only reviewer: walks the skill as a caller (fitness)
  agents/skill-fact-checker.md           read-only reviewer: verifies facts (grounding, volatility, ownership)
  agents/skill-conformance-reviewer.md   read-only reviewer: reads the text against the doctrine
knowledge/                               gitignored source material; not shipped
```

## The architecture, and why it is this shape

**One text, many readers.** `doctrine/` is the single source of every rule about how a skill is
written. `skills/skill-authoring` writes against it; the three reviewer agents review against it,
in parallel, each owning one activity and an exclusive set of finding axes. All reach it as
`${CLAUDE_PLUGIN_ROOT}/doctrine/…`, so there is one copy and nothing to drift. Each reviewer
re-reads its subset every run and deliberately states no rule about skills of its own — an agent
body carries only its activity, its doctrine subset, its axes, and the protocol it runs under.
How the review is *orchestrated* — who is spawned, what they are passed, how findings are
adjudicated — is meta the reviewers never read: it lives in `skill-authoring`'s step 6 and
nowhere else.

Consequences that constrain edits:

- **A rule goes in `doctrine/`, never in `SKILL.md` or an agent prompt.** `skill-authoring` is a
  procedure and states no rule about the skill being authored; a reviewer states no rule about
  skills at all. A rule written in either is a rule nothing enforces.
- **A change in behaviour is a doctrine edit.** Changing what is required of skills means editing
  `doctrine/`; every reader picks it up with no other change.
- **Mechanical vs. judgement is a hard split.** Anything a script can decide (YAML parsing, field
  sets, dangling bundled files) belongs in `validate.py`; anything it cannot belongs to the
  reviewers. Neither duplicates the other.
- **Axes are exclusively owned.** Each finding axis belongs to exactly one reviewer, stated in
  that agent's own body and in `skill-authoring`'s step 6 table. A defect class covered by two
  reviewers is a seam both will assume the other holds.

The `skill-authoring` → reviewers hand-off is deliberately narrow: the author passes each reviewer
**only the skill's path and its declared archetype** — classification is the author's job, and no
reviewer re-makes it. Passing the draft's text or the intent behind it is what makes a reviewer
agree with the author, so it is prohibited rather than discouraged.

## Engineering principles

Skills are modules, and we hold ourselves to what we tell others. `doctrine/laws.md` opens with the
mapping from principle to law — Modularity, Encapsulation, Open–closed, Reusability. Apply it in
both directions: when writing guidance **and** when editing anything in this repo.

In practice, for our own files:

- **Encapsulation** — no component reads another's internals. Cross-component sharing goes through
  `${CLAUDE_PLUGIN_ROOT}/doctrine/`, which is the plugin's own shared core, never through a
  sibling skill's directory.
- **Open–closed** — a component's name and the job it owns are its public surface and stay stable;
  the doctrine behind them is free to change.
- **Modularity** — one responsibility each. If a change wants to give `skill-authoring` a second
  job, it is a second skill.
- **Reusability** — components refer to each other by name and outcome (`` the `rule-authoring`
  skill ``, declared as `Skill(claude-teacher:rule-authoring)` in `allowed-tools`), never by path.

## Working in this repository

**Before editing any skill, agent, or doctrine file, read `plugins/claude-teacher/doctrine/` —
all of it, `laws.md` first.** It is normative for our own files too, not only for skills we teach
others to write. Do not restate its rules here or anywhere else; point at it.

Authoring or revising a skill — including one in this repo — runs the `skill-authoring` skill's
procedure end to end, reviewer round included. Do not hand-roll a shortcut version of it.

Validate a skill directory:

```bash
python3 plugins/claude-teacher/skills/skill-authoring/scripts/validate.py <skill-dir> [--portable]
```

Exit status 1 on any ERROR. `--portable` restricts frontmatter to the six fields claude.ai and the
Skills API accept, for skills that must travel outside Claude Code.

**Bump `version` in `plugins/claude-teacher/.claude-plugin/plugin.json` in the same commit as any
change to the plugin.** Without the bump, `claude plugin update` reports "already at the latest
version" and the change reaches nobody who installed it.

`knowledge/` is gitignored source material the doctrine was distilled from. Read it for grounding;
never ship from it, and never point a shipped file at it.
