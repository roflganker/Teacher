# claude-teacher

A Claude Code plugin that teaches Claude how to **build the pieces a harness is made of** — starting
with Agent Skills. It gives Claude a written doctrine of what a good skill is, a procedure that
applies it, and an independent reviewer that checks the result against the same text.

You install it, then ask Claude to write or fix a skill. What comes back has been admitted or
rejected on stated grounds, classified, validated mechanically, and reviewed by a subagent that
never saw your intent.

## What you get

| Component | What it does |
| :--- | :--- |
| `skill-authoring` skill | The procedure: admit → classify → place → author → validate → review → report. Every step is a gate; a failed step stops the run and says why. |
| `skill-reviewer` agent | Read-only. Re-reads the doctrine every run, walks the skill as a caller before reading it as a text, and answers with proven divergences (`file:line` + evidence) or exactly `OK`. |
| `doctrine/` | The normative text both of them read — laws, archetypes, frontmatter, body, scripts. One copy, two readers, nothing to drift. |
| `validate.py` | Mechanical checks the eye misses — chiefly frontmatter that does not parse, which disables a skill *silently*. `--portable` mode restricts fields to what claude.ai and the Skills API accept. |
| `rule-authoring` skill | A declared stub for `.claude/rules/` authoring. It exists to say the doctrine is not written yet and to stop skill doctrine being borrowed for a job it does not fit. |

## Why it exists

The obvious alternative is Anthropic's bundled `skill-creator`. In practice it is a scaffolder: it
will happily produce a well-formed `SKILL.md` for anything you name, because it has no opinion about
what belongs in a skill and no independent check on what it wrote. The failure mode is not malformed
files — it is confidently formatted skills that make the agent worse:

- **No admission test.** A fact, a standing convention, or something a linter already rejects gets
  turned into a skill instead of being sent to `CLAUDE.md`, `.claude/rules/`, or the linter. A skill
  is the weakest of those mechanisms: the model deciding to invoke it is the same model about to get
  the thing wrong.
- **Content generated from priors.** A skill written from what a model already knows can only
  restate what a model already knows — the exact content that adds tokens and no capability.
  claude-teacher's frontier test cuts that class outright, and its grounding law forbids inventing a
  flag, path or endpoint that nothing real confirms.
- **Descriptions that summarize the body.** A description that lists the steps gets acted on
  *instead of* the skill; the agent reads the summary and never loads the file. Here the description
  is treated as a routing key — triggers, not procedure.
- **The author reviews its own draft.** claude-teacher spawns a separate reviewer and passes it
  **one thing: a path.** Not the draft's text, not the reasoning, not what you meant — because
  telling a reviewer your intent is what makes it agree with you.
- **No shared standard.** Rules baked into a generator's prompt cannot be read, argued with, or
  changed. Here every rule lives in `doctrine/`; if a rule is not written there, it is not a rule.

It is also stricter about deletion than any generator is willing to be. Revising a skill removes
more often than it adds, and the reviewer flags over-trimming too — a bare imperative whose reason
was cut is a defect in the same way padding is.

## Install

```
/plugin marketplace add roflganker/Teacher
/plugin install claude-teacher@claude-teacher
```

Both are typed in Claude Code. Update later with `/plugin` (or `claude plugin update claude-teacher`).

## Use

Nothing to configure. Ask for the work in ordinary words — the skill routes itself:

```
Write a skill for our deploy process
Is .claude/skills/kubernetes any good?
Trim this skill down, it's bloated
```

Or invoke it directly, optionally with a path:

```
/claude-teacher:skill-authoring .claude/skills/deploy
```

You can also run the mechanical checks on their own:

```bash
python3 <plugin-root>/skills/skill-authoring/scripts/validate.py <skill-dir> [--portable]
```

Exit status is 1 on any error.

Expect it to push back. If what you asked for fails admission, it says which clause failed and where
the content belongs instead — and builds it anyway if you still want it.

## Scope

Harness development is the subject; skill authoring is the first component of it and the only one
currently complete. Rule authoring is a stub. Other components follow as their doctrine gets
written, each as its own skill with its own doctrine — never as a section bolted onto skill
authoring.
