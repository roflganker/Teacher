# Writing the body

- [Degrees of freedom](#degrees-of-freedom)
- [Where a fact goes](#where-a-fact-goes)
- [Shapes that carry better than prose](#shapes-that-carry-better-than-prose)
- [Loops that raise the output's quality](#loops-that-raise-the-outputs-quality)
- [What the runtime needs spelled out](#what-the-runtime-needs-spelled-out)
- [Shapes that fail](#shapes-that-fail)

The body enters the session once and stays. Five hundred lines is the outer bound, but the bound
that matters is the frontier test applied line by line — most bodies that reach four hundred are
carrying a tour of the domain rather than the skill.

## Degrees of freedom

A different axis from matching the form to the failure. That one asks which rhetoric fixes a
failure; this one asks how much room to leave.

| Room | When | Form |
| :--- | :--- | :--- |
| **High** | several valid approaches, and the right one depends on context | prose and heuristics, with the reason stated — an agent that knows why chooses better than one following a rule |
| **Medium** | a preferred pattern exists, variation is tolerable | a worked example, or a command with parameters |
| **Low** | fragile, irreversible, or order-dependent | the exact command, and the instruction not to vary it |

Most skills need all three in different parts. Calibrate each part on its own: a skill written at
one setting throughout is over-constrained where judgment was needed, or vague where it wasn't. The
tell in use is an agent that tries two or three approaches before starting (too loose), or one that
refuses an obvious adaptation (too tight).

## Where a fact goes

Progressive disclosure has one exception, and it is the highest-value content most skills carry.

**A correction the agent needs *before* it meets the situation belongs in `SKILL.md`, not in
`references/`.** It cannot recognize the trigger to open a file about a hazard it does not yet know
exists. Rows that are soft-deleted so every query needs a predicate; an identifier that changes name
across three services; a health check that stays green while the database is down — those stay
inline even though they read as reference material.

Placement follows retrieval, not tidiness. A correct fact in a file nobody opens loses to the same
fact where it is read.

## Shapes that carry better than prose

- **A template beats a description of a template.** Structure is matched against directly. Inline
  the short ones; put long or conditional ones in `assets/` and name the condition that selects them.
- **One excellent example beats five.** Complete, runnable, drawn from something real, commented
  only where the reason isn't visible in the code. Not a fill-in-the-blank skeleton, and not the
  same example in three languages — porting is free, and maintaining three copies is not.

## Loops that raise the output's quality

- **Produce, check, fix, repeat.** The checker can be a script or a document the output is read
  against. Say that it repeats until clean; a single check pass reads as optional.
- **Plan, validate, execute** — for anything batch or destructive. Write the intended changes to a
  file, verify that file against the source of truth, then apply it. The intermediate is
  inspectable and cheap to redo; the applied change is neither.

## What the runtime needs spelled out

- **MCP tools go by qualified name** — `Linear:list_issues`, never bare `list_issues`. With several
  servers connected, a bare name resolves to nothing, or to another server's tool of the same name.
- **Name a prerequisite that isn't ordinary** — a binary, a runtime version, network access.
  `compatibility` carries a genuine environment requirement; a package the operator obviously has
  needs no words.
- **Write nothing that dates.** No "before August, use v1". Current practice in the body; anything
  retired goes into a block marked retired, or goes away. A skill has no release cycle to hang a
  cutover on.

## Shapes that fail

- **The story.** "In the June incident we found an empty `projectDir`…" A skill is a standing
  instruction, not an account of the day you learned something. Keep the finding, drop the day.
- **The flowchart.** Worth it only where a decision has non-obvious branches. Linear steps are
  shorter and more reliably followed as a numbered list; lookups belong in a table.
- **The tour.** A body that explains the domain before instructing spends its whole budget on what
  the agent already brought.
