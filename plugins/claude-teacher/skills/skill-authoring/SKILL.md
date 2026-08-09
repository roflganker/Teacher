---
name: skill-authoring
description: Authors and revises Agent Skills — SKILL.md, its frontmatter, its bundled files, and where it installs. Use when creating a skill, editing one, or judging whether one is well built.
argument-hint: [skill-name-or-path]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py *) Skill(claude-teacher:rule-authoring)
---

# Authoring an Agent Skill

**The doctrine is `${CLAUDE_PLUGIN_ROOT}/doctrine/`, and every file in it is normative.** This file
is the procedure that applies it and states no rule of its own; where the two ever seem to disagree,
the doctrine wins. The reviewers at step 6 read the same directory, so what you are held to and what
they check are one text.

Read `${CLAUDE_PLUGIN_ROOT}/doctrine/archetypes.md` **now** — the admission test and the anatomy your
draft owes both live there, and steps 1 and 2 cannot start without it. Then, on reaching each step:

| At | Read | For |
| :--- | :--- | :--- |
| step 3 | `${CLAUDE_PLUGIN_ROOT}/doctrine/frontmatter.md` | placement, fields, and what the runtime enforces for you |
| step 4 | `${CLAUDE_PLUGIN_ROOT}/doctrine/laws.md` | the laws every line of the draft answers to |
| step 4 | `${CLAUDE_PLUGIN_ROOT}/doctrine/body.md` | how each part of the body is shaped |
| step 4 | `${CLAUDE_PLUGIN_ROOT}/doctrine/scripts.md` | only if it bundles a script |

**Every step is a gate.** A failed step stops the run; say where and why.

```
- [ ] 1. Admit it — is this a skill at all, and one coherent unit?
- [ ] 2. Classify the archetype, and take its anatomy
- [ ] 3. Place it, and pick the frontmatter that does the work
- [ ] 4. Author it
- [ ] 5. Validate  (scripts/validate.py)
- [ ] 6. Review    (3 reviewer subagents in parallel → adjudicate → fix; cap 2 rounds)
- [ ] 7. Report
```

## Steps

**1. Admit it.** Run the admission test in `doctrine/archetypes.md`. A skill that fails it is not
made good by better writing — say so and stop. If the operator wants it anyway, that is their call:
say what fails and build it.

**2. Classify.** Pick exactly one archetype and take its required anatomy verbatim. A skill needing
two archetypes is two skills; a skill matching none is usually a fact or a standing rule belonging in
the consuming project's own instructions and rules, not a skill.

**3. Place and configure.** Where it installs — personal, project, or plugin — decides which
frontmatter fields exist and who can reach it. Then choose fields by what each one *does*, per
`doctrine/frontmatter.md`. A field the runtime enforces beats a sentence in the body asking for the
same thing, every time.

**4. Author.** Obey `doctrine/laws.md` and the archetype's anatomy.

**5. Validate.** `python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py <skill-dir>` — it catches the
mechanical failures that are invisible by inspection, chiefly frontmatter that does not parse, which
disables a skill **silently**. Add `--portable` when the skill must also load on claude.ai or
through the Skills API, where a Claude Code field is a hard error rather than an ignored key. Fix
every error before step 6. Judge each warning; a warning you overrule, say why.

**6. Review.** Spawn the three reviewer subagents **in parallel, in one message**. Each owns one
activity and an exclusive set of finding axes — none covers another's ground:

| Subagent | Activity | Axes it emits |
| :--- | :--- | :--- |
| `claude-teacher:skill-walker` | carries the skill's job end to end as a caller | `fitness` |
| `claude-teacher:skill-fact-checker` | verifies every stated fact against something real, holds each to the fact-admission test | `grounding`, `volatility` |
| `claude-teacher:skill-conformance-reviewer` | reads the skill as a text against the doctrine | `admission`, `anatomy`, `description`, `boundary`, `bundling`, `economy`, `form`, `ambiguity` |

Pass each exactly one thing: the path of the skill under review. They find the doctrine themselves, at a location nothing in your prompt can move. Do
not pass the skill's text, your reasoning, or what you intended; each reads the files itself, and
telling a reviewer your intent is what makes it agree with you.

Each answers `OK`, or a numbered list of claimed divergences with `file:line` and evidence. Merge
the lists; a defect reported by more than one reviewer is adjudicated once.

| The merged result is | You do                                                                                                                                                                            |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Three `OK`s          | Report clean. Stop.                                                                                                                                                               |
| Any findings         | Each item is a **claim**, not a verdict. Open the cited `file:line` and check the evidence yourself. Fix what survives; for each item you discard, say in one line why it was wrong. |

Then re-spawn all three and loop, **capped at 2 review rounds total**. If round 2 still returns
confirmed divergences, apply what you can and report the residue rather than looping. Never forward
a finding you did not open, and never re-run a reviewer's pass yourself before it runs — you would
only be grading your own work twice.

**7. Report.** The skill's path, its archetype, what the validator said, what the review found and
what you did with each finding, and — if it landed in a plugin — that the plugin's `version` still
needs bumping for the change to reach anyone who installed it.

**Revising an existing skill** runs the same steps, with step 1 asking whether it still passes
admission rather than whether it should exist. Two signals from watching it in use outrank another
reading: a reference file opened on every run belongs in `SKILL.md`, and one never opened is either
unnecessary or badly signposted. Removal is the usual outcome of both.

## Rules

- Steps run in order. Nothing is authored before the archetype is chosen.
- **No rule about the skill being authored is written in this file.** A rule belongs in
  `${CLAUDE_PLUGIN_ROOT}/doctrine/` — that is the only text the reviewers read, so a rule written
  here is one nothing enforces. This block governs running the procedure, nothing else.
- **The reviewers are spawned, never impersonated.** You do not review your own draft in place of
  them, you do not tell them what you meant, and you do not skip one of the three because its
  ground looks clean.
- **Every finding is adjudicated by opening the file.** Confirmed ones get fixed; discarded ones get
  a reason. Cap the loop at 2 rounds and report the residue.
- **Deleting is the normal edit.** Revising a skill removes more often than it adds.
- Invoking this skill authorizes writing the skill's files and running its validator. It does not
  authorize committing, publishing, or bumping a plugin version.
