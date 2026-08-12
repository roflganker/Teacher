# Rules

Normative, like every other file in this directory — and this one is the whole doctrine for
`.claude/rules/` files. The laws in `laws.md` that are not skill-specific apply to a rule
unchanged: the frontier test, *Leave nothing to interpret*, *Match the form to the failure*, and
*Every claim is grounded in something real*. This file states only what is a rule's own.

- [What a rule is](#what-a-rule-is)
- [Admission — is this content a rule](#admission)
- [One rule, one concept](#one-rule-one-concept)
- [Scoping](#scoping)
- [What a rule carries](#what-a-rule-carries)
- [What a rule never carries](#what-a-rule-never-carries)
- [The mechanics the runtime fixes](#the-mechanics-the-runtime-fixes)

## What a rule is

A rule is a standing convention or prohibition that **loads unbidden**. A skill does a job and
hopes to be invoked; a rule holds a line and is simply present — at launch, or the moment the
agent reads a file its globs match. That is its entire power and its entire cost: nothing decides
to consult it, and every line of it is context spent whether or not the task needed it.

It is context, not enforcement. A rule shapes what the model does; it guarantees nothing. Where a
violation must be *impossible* rather than discouraged, that is a hook, a linter, or a schema —
the admission table routes it there.

**The agent always sees the codebase.** The code already shows what is: the current layout, the
existing classes, how the surrounding calls look. What the code cannot show is which of those
shapes are deliberate — what must stay true when the next change is made, what is prohibited
however natural it looks, and why. A rule states exactly that, and nothing the agent could read
off the code itself.

## Admission

One question routes content in or out — asked before writing, because no rewriting moves content
into the right mechanism:

| The content is | It belongs in |
| :--- | :--- |
| a job with steps and a definition of done | a skill — the `skill-authoring` skill |
| a violation a tool can reject | a linter rule, a schema, or a hook — not prose at all |
| a fact or a map every session needs regardless of task — build commands, layout, where things live | the project's `CLAUDE.md` |
| a standing convention or prohibition tied to one concept | a rule |
| a correction learned mid-session, worth keeping | a rule, written now — never left to auto memory |

The last row is a stance, held for reasons: auto memory is machine-local and outside version
control, so it is not shared with the team, not reviewable per change, not observable when the
codebase moves under it, capped in what loads, and not scopeable by path. A correction that
mattered once will matter again on a teammate's machine — promoting it into a rule is what makes
it survive, and projects here disable auto memory outright (`autoMemoryEnabled: false` in
`.claude/settings.json`) so learnings have exactly one place to land.

The boundary with `CLAUDE.md` is growth: `CLAUDE.md` is the map, and a couple of always-true
lines live there fine. The moment a concept needs its examples and its reasons, it is a rule
file, and `CLAUDE.md` at most points at it.

## One rule, one concept

A rule file describes **one concept the project has committed to** — "logging is a `BaseLogger`
subclass", "schema changes are generated migrations", "every failure is the error envelope". The
filename names the concept (`logging.md`, `entities.md`, `messaging.md`), because the filename is
all a maintainer sees when deciding where an edit goes; subdirectories group where volume earns
it. Two concepts in one file cannot be scoped to two sets of paths; a concept split across two
files gives the same line two homes to drift between.

The bound on length is the frontier test applied line by line, same as any body. A rule past
roughly a hundred lines is usually carrying a tour of its domain rather than the convention.

## Scoping

**Path-scoped is the default.** A rule without `paths` frontmatter loads at launch into every
session, with the same priority as `.claude/CLAUDE.md` — a permanent tax on every task, including
the ones nowhere near the concept. That is affordable only for a convention any task can trip
over. A concept whose files have a home gets globs, and costs nothing until those files are read.

Scope the globs to **where the concept surfaces, not where it is implemented**. A path-scoped
rule loads when the agent reads a matching file — so the globs cover every file family the agent
will have open while the concept is in play. A migrations convention matches the entities the
migration mirrors; an events convention matches the subscribers and the outbox, not only the
event classes. A rule whose globs match only the canonical implementation loads after the
mistake, or never.

User-level rules (`~/.claude/rules/`) carry the operator's own preferences across every project,
and load before project rules so the project wins a conflict. The ownership consequence is the
same as a personal skill's: a project's convention written there is misplaced — invisible to the
team and applied to repositories it was never true for. The fix is moving it into the project.

## What a rule carries

- **The convention, as a prohibition or a recipe** — chosen by *Match the form to the failure*.
  The commonest rule failure is the pressure case: the agent knows the convention and abandons it
  when the natural-looking alternative is nearer. That form is a prohibition with the excuses
  named and answered — "hoisting any of the three to the class is a convention violation", not
  "prefer route-level decorators".
- **The stable anchors the convention is built on.** "Logging is a `BaseLogger` subclass" is
  driven by `BaseLogger` — name it, with its path. An anchor is admitted precisely because the
  rule turns on it: renaming it rewrites the rule anyway, so carrying it costs nothing extra, and
  the name is what lets the agent find the real thing instead of inventing a parallel one.
- **One good shape and one bad shape**, real, minimal, and labeled — the bad one by name, as the
  violation it is. A pair anchors the line better than either alone: the good example shows what
  to write, the bad one is what the agent's own draft is matched against.
- **The mechanism** — what actually breaks, drifts, or misleads when the line is crossed. This is
  *Leave nothing to interpret* applied: a bare imperative stops generalizing the moment the
  situation shifts, and a model that knows why a line exists holds it in the case the author
  never anticipated. It is also what the code can least express — the rationale is the part of a
  convention with no representation in the source at all.
- **A sibling rule, referred to by its path** — `.claude/rules/exceptions.md`. Rules have no
  names or namespace; the path is the identity, and one concept speaks for itself rather than
  being restated where it is used.

## What a rule never carries

- **A volatile fact the convention does not turn on.** A schema, a module inventory, the current
  shape of a config — the codebase answers those live, and a snapshot in a rule decays silently
  while still reading as authoritative. Carry the lookup if anything: the path where the live
  answer is.
- **The list of adopters.** Which modules follow the convention is derivable by grep, wrong by
  the next module, and useless for holding the line — the rule binds the code its globs reach,
  not an enumerated membership.
- **What the frontier already knows.** What a class is, how to subclass, what the framework's
  default does — the test is `laws.md`'s: would a competent agent get this wrong without the
  line? The one exception it names applies here in full: the place this project deliberately
  violates the standard convention is exactly what a rule exists to say.
- **What a tool already rejects.** Restating the linter is context spent guarding a line that
  cannot be crossed. The rule states the half no tool sees — the paired convention whose
  violation compiles clean.
- **Anything readable off the code.** Layout, naming as it currently stands, what exists where —
  the agent sees the codebase. If deleting a line loses nothing the code does not show, delete it.

## The mechanics the runtime fixes

- **Discovery.** Every `.md` under the project's `.claude/rules/` is a rule, found recursively —
  subdirectories organize freely. Symlinks resolve, so a shared rule set can be linked in.
- **`paths` frontmatter** is a YAML list of globs. `**/*.ts` matches by extension anywhere,
  `src/api/**/*` by directory, `src/**/*.{ts,tsx}` by brace expansion. No `paths` means
  always-on; matching makes the rule load when a matching file is read.
- **Brace expansion is budgeted** — one rule's whole `paths` list shares a budget of 1,000
  expanded patterns, and a pattern that would exceed it is used unexpanded, its literal braces
  matching nothing. Multiplying brace groups multiplies expansions; keep the list short.
- **`[` opens a bracket expression.** A pattern with a `[` that cannot be read as one is invalid
  and matches nothing — silently; the rule's other patterns keep working. A literal `[` in a
  file name is escaped: `photos \[2024/**`.
- **A rule that fails to parse fails silently**, like any frontmatter: it never loads, and
  nothing at the point of use says so. The check is behavioural — read a matching file in a
  fresh session and see whether the convention surfaces.
- **Compaction does not re-inject path-scoped rules.** After a compaction they return the next
  time a matching file is read, not before — one more reason a rule states standing conventions
  rather than one-time steps.
- **`claudeMdExcludes`** in settings can silence rules by glob — the escape hatch when a
  monorepo's neighbouring rule sets do not concern this work.
