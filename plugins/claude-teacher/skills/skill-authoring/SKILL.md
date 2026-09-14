---
name: skill-authoring
description: Authors, revises, and judges Agent Skills — SKILL.md, its frontmatter, bundled scripts, and where it installs. Covers a new skill or slash command, and one that never fires or ignores its frontmatter.
argument-hint: [skill-name-or-path]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py *)
---

# Authoring an Agent Skill

**The doctrine is `${CLAUDE_PLUGIN_ROOT}/doctrine/`, and every file in it is normative.** This file
is the procedure that applies it.

Read `${CLAUDE_PLUGIN_ROOT}/doctrine/archetypes.md` **now** — the admission test and the anatomy your
draft owes both live there, and steps 1 and 2 cannot start without it. Then, on reaching each step:

| At | Read | For |
| :--- | :--- | :--- |
| step 1 | `${CLAUDE_PLUGIN_ROOT}/doctrine/frontmatter.md`, its *Placement* section | the surfaces the admission test is judged against |
| step 3 | `${CLAUDE_PLUGIN_ROOT}/doctrine/frontmatter.md`, the rest | the fields, and what the runtime enforces for you |
| step 4 | `${CLAUDE_PLUGIN_ROOT}/doctrine/laws.md` | the laws every line of the draft answers to |
| step 4 | `${CLAUDE_PLUGIN_ROOT}/doctrine/body.md` | how each part of the body is shaped |
| step 4 | `${CLAUDE_PLUGIN_ROOT}/doctrine/scripts.md` | the moment bundling a script comes up — whether to bundle is itself decided against this file, so it is read before that decision, not after it |

**Every step is a gate.** A failed step stops the run; say where and why.

## Steps

**1. Admit it.** Declare where the skill will install — personal, project, or plugin — then run the
admission test against that placement's surfaces. A skill that fails it: say what fails, with the
row that rejects it, and stop.

**2. Classify.** Pick the archetype and take its required anatomy.

**3. Configure.** The placement declared at step 1 decides which frontmatter fields exist and who
can reach the skill. Choose fields by what each one *does*.

**4. Author.** Obey the doctrine and the archetype's anatomy.

**5. Validate.** `python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py <skill-dir>`, with `--portable`
for a skill that must also load on claude.ai or through the Skills API. Fix every error before
step 6. Judge each warning; a warning you overrule, say why.

**6. Review.** Spawn the three reviewer subagents **in parallel, in one message**. Each owns an
exclusive set of finding axes — none covers another's ground:

| Subagent | Axes it emits |
| :--- | :--- |
| `claude-teacher:skill-walker` | `fitness` |
| `claude-teacher:skill-fact-checker` | `grounding`, `volatility`, `ownership` |
| `claude-teacher:skill-conformance-reviewer` | `admission`, `anatomy`, `description`, `boundary`, `orchestration`, `bundling`, `economy`, `form`, `ambiguity` |

Pass each exactly two things: the path of the skill under review, and the archetype chosen at
step 2. Classification is the author's call and part of the record under review. Do not pass the
skill's text, your reasoning, or what you intended; telling a reviewer your intent is what makes
it agree with you.

Each answers `OK`, or a numbered list of claimed divergences with `file:line` and evidence, each
tagged with an axis. Merge the lists; a defect reported by more than one reviewer is adjudicated
once. A finding whose axis is not in its reviewer's column is off its ground: discard it, since
the reviewer that owns the axis reports it if it holds.

| The merged result is | You do                                                                                                                                                                            |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Three `OK`s          | Go to step 7.                                                                                                                                                                     |
| Any findings         | Each item is a **claim**, not a verdict. Open the cited `file:line` and check the evidence yourself. Fix what survives; for each item you discard, say in one line why it was wrong. |

If every finding was discarded, go to step 7: nothing changed, so another round reads the same
files. If any was fixed, re-run step 5 on the edited files — a fix can break what the validator
checks, and the reviewers do not run it — and re-spawn all three, **capped at 5 review rounds
total**. Fixes applied in round 5 are not reviewed again; step 7 reports them as such.

**7. Report.** The skill's path, its archetype, what the validator said, what the review found and
what you did with each finding.

**Revising an existing skill** runs the same steps, with step 1 re-running admission on the skill
as it now stands, and with the usage signals in `${CLAUDE_PLUGIN_ROOT}/doctrine/archetypes.md`,
*Bundled files*, weighed before another reading.

**Judging a skill without a mandate to change it** runs steps 1, 2, 5, one round of 6, and 7 with
every fix replaced by reporting: a validator error is reported and step 6 runs regardless, and
findings are adjudicated as usual and reported rather than applied. Nothing in the skill's
directory is written.

**What it does not handle.** This is the happy path: retrying a halted step is the caller's. It
does not watch the skill in use — the usage signals weighed on revision are whatever the operator
brings — and it does not install the skill or make it reach anyone.

## Rules

- **The reviewers are spawned, never impersonated.** You do not review your own draft in place of
  them, you do not tell them what you meant, you do not skip one of the three because its ground
  looks clean, and you do not re-run a reviewer's pass yourself before it runs — that is grading
  your own work twice.
- Invoking this skill authorizes writing the skill's files and running its validator. It does not
  authorize committing, publishing, or bumping a plugin version.
