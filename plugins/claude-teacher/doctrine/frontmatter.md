# Frontmatter, placement, and the runtime features worth reaching for

- [Placement decides what is available](#placement-decides-what-is-available)
- [Intent to field](#intent-to-field)
- [Field reference](#field-reference)
- [Invocation control](#invocation-control)
- [Path substitution](#path-substitution)
- [Traps](#traps)

Prose asks; the runtime enforces. Every intent below has a field that carries it, and a field always
beats a paragraph requesting the same behaviour.

## Placement decides what is available

| Location | Path | Reaches |
| :--- | :--- | :--- |
| Personal | `~/.claude/skills/<name>/SKILL.md` | all your projects |
| Project | `.claude/skills/<name>/SKILL.md` | that project, and it is shared through version control |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | wherever the plugin is enabled |

Precedence on a name collision is enterprise, then personal, then project; any of them overrides a
bundled skill of the same name. Plugin skills are namespaced `plugin-name:skill-name` and cannot
collide — which is also why a grant to a plugin skill must be written namespaced, while a project
or personal target, listed bare by the runtime, can only be granted bare.

Placement is not an install-time detail — it is declared before admission, because it fixes the two
surfaces every later decision is judged against: **which siblings surround the skill**, whose owned
jobs and knowledge are not this skill's to take (`archetypes.md`, admission), and **which facts are
its own to carry** (`body.md`, *Where a fact goes*).

| Placement | The surrounding siblings | The facts that are its own |
| :--- | :--- | :--- |
| **Project** | the project's own skills plus every plugin the project installs — an enumerable set, so enumerate it before claiming a job | the project's stable facts |
| **Plugin** | inside the plugin, its own components, sharing through the plugin root; outside, the consumer's installed set, unknowable at authoring time — so the ownership boundary is carried entirely by the name, the description, and namespaced grants | its own domain — the thing it drives or teaches — and no project's |
| **Personal** | every project the operator opens — unenumerable, so the overlap test cannot run and no rule stands in for it. What the operator gets instead is the mechanism: precedence makes a personal skill *shadow* a project skill of the same name, in every repository, silently — a risk only they can weigh | the operator's own environment — machine, accounts, where credentials live. A personal skill built on one project's facts is misplaced rather than wrong: the fix is moving it into that project |

Two more consequences worth designing around:

- **A plugin skill is a product used inside someone else's repository.** It may not hardcode a branch
  name, a host, a layout rule, or a domain value. Anything project-specific is read at runtime from
  the consuming project's own files, and asked for only as a last resort.
- **A skill shipped in a plugin only reaches an installed user after the plugin's `version` is
  bumped.** An unbumped change is a change nobody receives.

Portability is the second axis. Claude Code accepts every field below; **claude.ai uploads and the
Skills API accept only six** — `name`, `description`, `license`, `compatibility`, `metadata`,
`allowed-tools` — and reject anything else as a hard error rather than a warning. Enabling a personal
skill for cloud sessions uploads it and applies the same restriction. Write to the six-field set when
the skill must travel; use the full set when it is Claude Code's.

## Intent to field

| You want | Use | Not |
| :--- | :--- | :--- |
| The skill never to fire on its own — it has side effects and the operator must ask for it | `disable-model-invocation: true` | a sentence saying "only run this when asked" |
| Background knowledge with no meaningful `/command` behind it | `user-invocable: false` | a note explaining it is not really a command |
| A bundled script to run without a permission prompt | `allowed-tools: Bash(python3 <SKILL_DIR>/scripts/validate.py *)` — interpreter included, or it never matches | telling the operator to approve it |
| A hand-off to a sibling skill not to stall on a prompt | `allowed-tools: Skill(plugin:sibling)` | asking the operator to pre-approve |
| A tool kept out of reach while the skill is active | `disallowed-tools` | "do not use Write here" |
| The skill kept out of consideration unless particular files are in play | `paths` | "only relevant for TypeScript files" |
| The work done in a clean context that will not pollute the conversation | `context: fork` (+ `agent`) | asking the model to summarize afterwards |
| The result back in this turn rather than in the background | `background: false` (only with `context: fork`) | polling |
| Live state in the skill's text at load time | `` !`command` `` in the body | instructing the agent to run the command first |
| Autocomplete to show what the skill takes | `argument-hint` | explaining the arguments in the description |
| Positional arguments addressable by name | `arguments` + `$name` | parsing `$ARGUMENTS` in prose |

`model` and `effort` also exist and apply for the rest of the turn. Set them only when the skill's
work genuinely demands a tier the session may not be on — in a skill shipped to other people, both
spend the consumer's budget on a choice they did not make, so the bar is high.

## Field reference

Only `name` and `description` are required. This table is the set worth reaching for, not an
inventory of everything the runtime parses — the validator recognizes a few more that no skill here
should need, and says nothing about them.

| Field | Meaning |
| :--- | :--- |
| `name` | Must be lowercase letters, digits and hyphens; no leading or trailing hyphen, no `--`; at most 64 characters; **must match the directory name** or the skill does not load. Reserved words `anthropic` and `claude` are rejected on Anthropic's own surfaces. |
| `description` | 1–1024 characters. What it covers and when to reach for it. Loaded for every installed skill at startup, so this is where the token budget is genuinely scarce. |
| `when_to_use` | Extra trigger phrases, appended to `description`. Both together are truncated at 1,536 characters in the listing — put the deciding case first. |
| `argument-hint` | Autocomplete hint such as `[issue-number]`. Display only. |
| `arguments` | Named positional arguments for `$name` substitution, mapped by position. |
| `disable-model-invocation` | `true` keeps the model from auto-loading it; manual invocation only. Also keeps its description out of context entirely. |
| `user-invocable` | `false` hides it from the `/` menu. Does **not** stop the model from invoking it. |
| `allowed-tools` | Tools pre-approved **for the turn that invoked the skill**. Grants; never restricts. Clears on the next message. |
| `disallowed-tools` | Tools removed from the pool while the skill is active. |
| `model` | Model while the skill is active. Same values as `/model`, or `inherit`. |
| `effort` | `low` \| `medium` \| `high` \| `xhigh` \| `max`. Overrides session effort. |
| `context` | `fork` runs the skill in a forked subagent context. |
| `agent` | The subagent type when `context: fork`. Defaults to `general-purpose`. |
| `background` | Only meaningful with `context: fork`. `false` waits for the result in the invoking turn. |
| `hooks` | Hooks scoped to this skill's lifecycle. |
| `paths` | Glob patterns limiting auto-activation to work touching matching files. Accepts a comma-separated string or a YAML list. **It narrows; it does not trigger** — a matching file makes the skill eligible to be chosen, it does not load it. A rule file with the same globs would load unbidden; this does not. |
| `metadata` | Free-form map for your own tooling; the runtime ignores its contents. Skill *versioning* is not a runtime concept — if you want one, it lives here. |
| `license`, `compatibility` | Spec fields. Accepted; not acted on. `compatibility` is for genuine environment requirements only, which most skills do not have. |

## Invocation control

| Frontmatter | Operator can invoke | Model can invoke | Description in context |
| :--- | :--- | :--- | :--- |
| neither field | yes | yes | yes |
| `disable-model-invocation: true` | yes | no | **no** |
| `user-invocable: false` | no | yes | yes |

Setting both makes the skill unreachable. Pick one.

## Path substitution

Three template variables exist, all written in shell form: a dollar sign, then the name in braces.

| Variable | Resolves to | Available |
| :--- | :--- | :--- |
| **CLAUDE_SKILL_DIR** | the directory holding this `SKILL.md` — for a plugin skill, the skill's own subdirectory, not the plugin root | any placement |
| **CLAUDE_PROJECT_DIR** | the project root | any placement |
| **CLAUDE_PLUGIN_ROOT** | the installed plugin's root directory | plugin placement only |

All three substitute in the body **and** in `Bash(...)` rules in `allowed-tools`. Write the same
string in both places so a bundled script runs without a prompt — here with `<SKILL_DIR>` standing in
for the written-out variable:

```yaml
---
name: render-chart
description: Renders a chart from a CSV file.
allowed-tools: Bash(bash <SKILL_DIR>/scripts/render.sh *)
---
Run `bash <SKILL_DIR>/scripts/render.sh <csv-file>`.
```

**Substitution has no escape, so a skill cannot show the variable and use it in the same file.** Any
occurrence in the body is replaced before the model reads a word — including one inside a code fence,
where an example meant to teach the syntax instead displays an absolute path into the skill that
wrote it. A skill that documents these variables names them in prose, as above; only a skill that
*uses* one writes it out.

**Substitution happens only in content the runtime injects** — the skill body, an agent body, a
command body, and `allowed-tools`. A file under `references/` is opened with `Read`, which returns
it verbatim, so a variable written there reaches the model as literal text. Anything a reference
file must say about these variables it says in prose.

CLAUDE_SKILL_DIR resolves to the *referencing* skill's directory, so it can never address another
skill's files. There is no path form that legitimately crosses a skill boundary; only the skill's
name does.

CLAUDE_PLUGIN_ROOT is the exception that proves it, and it is what a plugin uses to share one file
between its own components: a skill body and an agent body both addressing
`<PLUGIN_ROOT>/doctrine/laws.md` read the same file with no second copy to drift. Plain `Read`
reaches it; only a `Bash(...)` invocation of a plugin-root script needs the matching grant. What it
must not do is reach into a sibling *skill's* directory — the boundary law is unchanged by the
variable's existence.

## Traps

- **Frontmatter that does not parse disables the skill silently.** There is no error at the point of
  use — it simply never fires. A colon-space inside an unquoted value is the usual cause: write
  `description: Ships the change: staging first` and the parser sees a mapping. Quote it, or use a
  `>` block. Run the validator rather than trusting inspection.
- **`allowed-tools` grants, it never restricts.** Tools absent from the list still follow normal
  permissions. To actually block something, use `disallowed-tools` or a deny rule.
- **A skill declaring `allowed-tools` or `hooks` is an elevated-permission request** and needs
  approval before first use. In a project's `.claude/skills/`, those grants take effect only after
  the workspace trust dialog is accepted — which is also why an untrusted repository's skills are
  worth reading before trusting it.
- **`context: fork` with reference-only content returns nothing.** The subagent receives knowledge and
  no task, then succeeds silently having done nothing. Fork only skills whose body is an instruction.
- **A backgrounded fork runs with the narrower background tool set**, and its file edits fall outside
  session checkpoints. If the steps need a tool outside that set, set `background: false`.
- **Skill content enters the conversation once and stays for the session.** It is not re-read on
  later turns, so write standing instructions rather than one-time steps — and treat every line as a
  recurring cost, not a one-off.
- **Skills loaded together share one scope, and the runtime does not rank them.** Two skills whose
  instructions conflict are not resolved by precedence; the model picks. That is the argument
  against splitting one job across several narrow skills — the seams have no arbiter.
- **Auto-compaction keeps only the most recent invocation of each skill**, the first 5,000 tokens
  of each, within a combined 25,000-token budget filled most-recent-first — so an earlier skill can
  be dropped entirely. A long session does not preserve what it loaded.
- **`` !`command` `` substitutes once, before the content reaches the model.** Its output is not
  rescanned, so a command cannot emit a placeholder for a later pass. Note also that a policy setting
  can disable shell execution in skills entirely, replacing each command with a notice.
- **A skill and a `.claude/commands/` file of the same name collide**; the skill wins.
- **Unknown keys are ignored, not reported.** A typo in a field name means the field silently does
  nothing — which looks exactly like the feature not working.
