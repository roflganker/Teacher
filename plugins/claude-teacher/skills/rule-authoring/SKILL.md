---
name: rule-authoring
description: Authors .claude/rules/ files — the standing conventions and prohibitions a project loads unbidden, path-scoped or always-on. Use when writing or revising a rule, promoting a learned correction into one, or deciding whether content is a rule at all.
argument-hint: [concept-or-rule-path]
allowed-tools: Skill(claude-teacher:skill-authoring)
---

# Authoring a rule

**The doctrine is `${CLAUDE_PLUGIN_ROOT}/doctrine/rules.md`, and it is normative.** This file is
the procedure that applies it and states no rule of its own; where the two ever seem to disagree,
the doctrine wins. The reviewer at step 4 reads the same file, so what you are held to and what it
checks are one text. Read it **now** — step 1 is its admission table, and nothing starts before
that table has spoken.

**Every step is a gate.** A failed step stops the run; say where and why.

```
- [ ] 1. Admit it — is this content a rule at all?
- [ ] 2. Scope it — one concept, its file, its level, its globs
- [ ] 3. Author it
- [ ] 4. Review    (rule-reviewer subagent → adjudicate → fix; cap 5 rounds)
- [ ] 5. Report
```

## Steps

**1. Admit.** Run the content through the doctrine's admission table. Content that is
a job belongs to the `skill-authoring` skill — hand it over. Content a tool can reject, or that is
a fact for the project's instructions file, gets named as such and stops here; if the operator
wants a rule anyway, that is their call: build it.

**2. Scope.** One concept, named by the filename. Declare the level — project (`.claude/rules/`)
or user (`~/.claude/rules/`) — and the `paths` globs, or the case for always-on, per the
doctrine's scoping section. Read the project's existing rules first: the concept may already have
a file, and revising it beats founding a rival.

**3. Author.** Obey the doctrine. Ground every anchor, path, and example in the real
codebase — read the actual class, run the actual grep — before the rule states it.

**4. Review.** Spawn the `claude-teacher:rule-reviewer` subagent. Pass it exactly one thing: the
path of the rule file. Do not pass the rule's text, your reasoning, or what you intended — it
reads the file and the doctrine itself, and telling it your intent is what makes it agree with
you.

It answers `OK`, or a numbered list of claimed divergences with `file:line` and evidence. Each
item is a **claim**, not a verdict: open the cited line, check the evidence, fix what survives,
and for each item you discard say in one line why it was wrong. Then re-spawn and loop, **capped
at 5 review rounds total**. If round 5 still returns confirmed divergences, apply what you can
and report the residue rather than looping.

**5. Report.** The rule's path and level, its globs or the case made for always-on, what the
review found and what you did with each finding.

**Revising an existing rule** runs the same steps, with step 1 asking whether the content still
belongs in a rule rather than whether it should exist. Deleting is the normal edit.

**What it does not handle.** This is the happy path: a failed step halts and reports where, and
retrying is the caller's. A written rule is also not yet a loaded one — confirming it surfaces in
a fresh session, pointing the project's instructions file at it, and disabling auto memory in the
project's settings are the operator's follow-ups, not steps here.

## Rules

- Steps run in order. Nothing is authored before the admission table has spoken.
- **No rule about rule files is written here.** It belongs in
  `${CLAUDE_PLUGIN_ROOT}/doctrine/rules.md` — the text the reviewer judges against, so a rule
  written here is one nothing enforces. This block governs running the procedure, nothing else.
- **The reviewer is spawned, never impersonated.** You do not review your own draft in its place,
  and you do not skip it because the rule is short.
- **Every finding is adjudicated by opening the file.** Confirmed ones get fixed; discarded ones
  get a reason.
- Invoking this skill authorizes writing the rule file. It does not authorize committing, or
  editing the project's settings or instructions files.
