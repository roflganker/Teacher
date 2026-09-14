---
name: rule-authoring
description: Authors .claude/rules/ files — standing conventions and prohibitions, path-scoped or always-on, project-level or user-level. Covers writing or revising a rule, promoting a correction or preference into one, and deciding whether content is a rule at all.
argument-hint: [concept-or-rule-path]
---

# Authoring a rule

**The doctrine is `${CLAUDE_PLUGIN_ROOT}/doctrine/rules.md`, and it is normative.** This file is
the procedure that applies it. Read it **now** — step 1 is its admission table.

**Every step is a gate.** A failed step stops the run; say where and why.

## Steps

**1. Admit.** Run the content through the doctrine's admission table. Content the table routes
anywhere but a rule is named as such, with the row that rejects it, and the run stops here.

**2. Scope.** One concept, named by the filename. Declare the level — project (`.claude/rules/`)
or user (`~/.claude/rules/`) — and the `paths` globs, or the case for always-on, per the
doctrine's scoping section. Read the existing rules at the declared level first: the concept may
already have a file, and revising it beats founding a rival.

**3. Author.** Obey the doctrine.

**4. Review.** Spawn the `claude-teacher:rule-reviewer` subagent. Pass it exactly one thing: the
path of the rule file. Do not pass the rule's text, your reasoning, or what you intended — it
reads the file and the doctrine itself, and telling it your intent is what makes it agree with
you.

It answers `OK`, or a numbered list of claimed divergences with `file:line` and evidence. Each
item is a **claim**, not a verdict: open the cited line, check the evidence, fix what survives,
and for each item you discard say in one line why it was wrong. If every finding was discarded,
go to step 5: nothing changed, so another round reads the same file. If any was fixed, re-spawn,
**capped at 5 review rounds total**. Fixes applied in round 5 are not reviewed again; step 5
reports them as such.

**5. Report.** The rule's path and level, its globs or the case made for always-on, what the
review found and what you did with each finding.

**Revising an existing rule** runs the same steps, with step 1 re-running admission on the
content as it now stands.

**What it does not handle.** This is the happy path: retrying a halted step is the caller's. It
does not confirm the rule loads — a written rule surfaces only in a later session, at launch or on
reading a matching file, and this run never observes one.

## Rules

- **The reviewer is spawned, never impersonated.** You do not review your own draft in its place,
  and you do not skip it because the rule is short.
- Invoking this skill authorizes writing the rule file. It does not authorize committing, or
  editing the project's settings or instructions files.
