# Admission and archetypes

- [Admission — should this exist at all](#admission)
- [Choosing the archetype](#choosing-the-archetype)
- [Anatomy — driver, procedure, knowledge](#anatomy)
- [Bundled files](#bundled-files)

## Admission

A skill earns its place only if all four hold. Any one failing means the content belongs somewhere
else, and no amount of rewriting changes that.

Admission is judged against a **declared placement** — personal, project, or plugin — because
placement fixes which siblings surround the skill and which facts are its own to carry
(`frontmatter.md`, placement). Declare it before testing; the fourth test cannot run without it.

1. **The agent gets it wrong without it.** Run the task without the skill first, at least in your
   head and preferably for real. If the unaided attempt is fine, the skill adds cost and no capability.
2. **It is a procedure or a body of situated knowledge, not a fact.** A fact every session needs is
   cheaper in the project's instructions file, which is always loaded. A skill's body loads only when
   invoked — that is exactly what makes long reference material affordable and single facts wasteful.
3. **Nothing loads it for you.** Of the three mechanisms, a skill is the weakest: a hook *denies*, a
   rule file *loads unbidden*, a skill only hopes to be invoked — and the model deciding to invoke it
   is the same model about to get this wrong. So if a linter, type checker, formatter, schema, or
   hook can reject the violation, use that. If it is a standing rule to hold rather than a job to do,
   it belongs in `.claude/rules/`. Skills do a job; they are not where a line is held.
4. **It is one coherent unit.** Scope it like a function. Too narrow and several skills must load to
   do one job, each contradicting the others at the seams. Too broad and it cannot be triggered
   precisely, so it fires on the wrong tasks and gets ignored on the right ones. And the boundary is
   drawn within the surrounding set the placement fixes, not in a vacuum: a job or body of knowledge
   an installed sibling already owns is not this skill's to take. Extend the owner, or route to it by
   name — a second owner is a seam nothing arbitrates, because skills loaded together share one
   scope and the runtime does not rank them (`frontmatter.md`, traps). Where the placement makes
   the surrounding set unenumerable, the test cannot run — `frontmatter.md` states what the
   operator gets instead.

Where rejected content goes:

| Fails on | It belongs in |
| :--- | :--- |
| 1 — the agent already does it | nowhere; drop it |
| 2 — it is a fact, not a procedure | the project's instructions file (`CLAUDE.md` or equivalent) |
| 3 — a tool can reject it | a linter rule, a schema, or a hook |
| 3 — it is a rule to hold, not a job to do | `.claude/rules/` — the `rule-authoring` skill |
| 4 — it is two jobs | two skills |
| 4 — an installed sibling owns it | that sibling, extended — or a referral to it by name |

**The generated-skill trap.** A skill produced from an LLM's own priors with no grounding in real
material can only restate what the model already knows — which is by construction the content that
fails test 1. Grounding means: a task actually performed, corrections actually made, a real config or
API spec read, a real incident. That material is the skill; the writing is transcription.

## Choosing the archetype

Pick exactly one. Two archetypes means two skills. None means re-run admission — it is usually a fact
or a rule.

There are three, and one question separates them: **is there a thing to drive, a job to run, or a
domain to answer about?**

| Archetype     | It exists to                                                  | Tell by                                                                       |
| :------------ | :------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| **Driver**    | operate something with its own interface, outside the conversation | there is a CLI, an API, a store, or a corpus of files behind a wrapper       |
| **Procedure** | carry one job to a stated end                                  | it has steps and a definition of done                                          |
| **Knowledge** | answer questions about a domain the agent knows imprecisely     | it answers "what is X here" rather than "do X"                                 |

Two categories that look like archetypes and are not:

- **Delegation.** A skill whose steps are other skills' names is a Procedure, not a fourth thing.
  Drivers delegate too — to an access skill, a secrets skill, a sibling gateway — so delegation is a
  property any archetype can have, and no archetype is defined by it.
- **A failure mode.** "The agent knows this and abandons it under pressure" describes a problem, not
  a job. What fixes a failure mode is a mechanism that fires without being chosen — a rule or a hook.
  A skill that is only a line to hold has no archetype because it should not be a skill.

## Anatomy

Each archetype's required parts. Missing a required part is a defect the reviewer reports.

### Driver

The thing driven need not be remote. A deployed cluster, a hosted API, a live database — but equally
a corpus of files the project owns that may only be touched through a wrapper. What makes it a Driver
is that the thing has **its own interface**, and getting the interface wrong is the failure.

Named after **the thing driven, not the CLI that drives it** — the CLI is an implementation detail
that may be swapped for an MCP server tomorrow without the name becoming a lie, and a name that leaks
the binary invites siblings to reach for the binary.

Required:

- **A command table or a small set of worked invocations** — the shape of a call, not a manual. Push
  the flag-by-flag detail to `--help` and say so.
- **The operating model**: which operations are safe to run freely, and which are outward-facing,
  irreversible, or destructive and need confirmation first. Reads and writes are not the same
  authorization.
- **Authentication**, only where it is not an ordinary login. An ordinary login needs no words. An
  interactive flow only a human can complete, a credential that must be injected out-of-band, or a
  token that must never be printed — those need words.
- **A failure table, only for symptoms whose cause is not derivable from the error text.** A row
  states the **cause** — the mechanism this skill knows and the reader does not. Where to go next is
  the operator's judgement, made with context the table does not have, so a row ends at the cause and
  never prescribes the remedy tool.

| Cut — the message already says it | Keep — the message actively misleads |
| :--- | :--- |
| `command not found` → install it | `404` on a route that exists in the source → it is not deployed |
| `authentication failed` → log in | HTML where an error envelope was expected → a proxy answered; the app never saw the request |
| `permission denied` → get access | `429` on one route family only → it is throttled far below the documented limit |

**Say how to tell the call reached the right thing.** An unreachable system announces itself and
needs no words. The failure worth writing down is the one that is reachable and answers *plausibly
for the wrong target* — a base path served by the marketing site, a staging cluster returning valid
rows, a default context nobody chose. Nothing about such an answer looks wrong, which makes it worse
than an error. So a skill spanning several environments must not default to one — require the target
explicitly — and wherever a wrong target still answers, name the tell that gives it away.

### Procedure

Required:

- **The steps**, in the order they run — numbered where the order is fixed, keyed to an observable
  condition where the job branches by situation rather than sequence. A technique set for one class
  of job is still a Procedure; what it may not be is a menu.
- **The gate** — what must be true to proceed, and what stops the run. "Done" stated concretely
  enough to be checked, and **satisfiable with the authority the skill itself declares**: a
  completion condition resting on a step the `## Rules` block does not authorize, or on another
  skill succeeding afterwards, is a procedure with no completion condition of its own. A failed step
  halts and reports where; it does not continue degraded.
- **A `## Rules` block** ending the body: the load-bearing invariants, the "never" list, and what
  the invocation does and does not authorize. Where the procedure runs stages the operator would
  otherwise approve one by one, say which of them the invocation authorizes and which it never does.
- **What it does not handle.** A happy-path procedure should say it is the happy path, so a caller
  wrapping it in a retry loop knows the failure handling is theirs.

Anything the procedure needs about the surrounding project — branch names, hosts, layering rules,
domain values — is **read at runtime from the project's own files**, never baked in. A skill that
hardcodes a project's value is a skill that works in one repository.

**Where a step is another skill's job, name the skill and stop.** It invokes; it does not inline,
pre-empt, or paraphrase what the invoked skill does. Naming a sub-skill's flags or restating its
rules is the boundary violation a delegating procedure is most prone to. And where such a procedure
spans a whole pipeline, its highest-value stage is usually the **cheap moment to be wrong** — a stage
before any artifact exists, where intent is stated concretely enough to be contradicted. After that,
every downstream stage only checks that the built thing is coherent, never that it was the right thing.

### Knowledge

Only where **the domain names itself in the work** — the package, import, product, tool, error string
or file type appears in the task, so the skill can be reached. Knowledge the agent needs *before* it
knows the domain is in play cannot be routed to by any description, and belongs in always-loaded
content instead. This is the archetype deferred loading exists for: bulky, needed sometimes, and
named when needed.

Required:

- **A pointer into `references/`, with the condition that triggers each file.** The body is a table
  of contents; the knowledge is in the files, costing nothing until read.
- **A scope boundary, stated as a pair.** Structure versus current state; breadth versus depth. Say
  which one this skill is and name where the other lives.
- **What it describes, and as of when** — the library version, the API revision, the date the map was
  true. Reference material about a moving target rots silently, and stale material reads exactly as
  authoritative as fresh material.
- **A discover-on-miss path.** Any map goes stale; say what to do when the thing asked about is not
  in it, so the gap produces a lookup rather than a guess.

## Bundled files

`references/` for documentation read on demand, `scripts/` for executables, `assets/` for templates
and data. Only `SKILL.md` is required; the rest are conventions.

- **One level deep.** `SKILL.md` → `references/x.md`. A chain `SKILL.md` → `a.md` → `b.md` gets read
  partially, and partial reference material is worse than none because it reads as complete.
- **Say when to read each file, not that it exists.** "Read `references/errors.md` when the API
  returns a non-2xx status" beats "see `references/` for details".
- **Any reference file over ~100 lines opens with its own table of contents**, so a partial read
  still reveals the full scope.
- **A prewritten script beats generated code**: its source never enters context, only its output.
  State whether the agent should *run* it or *read* it.
- **A bundled file nothing points at is dead weight.** Delete it or reference it.
- **Watching the skill in use outranks re-reading it.** A reference file opened on every run
  belongs in `SKILL.md`; one never opened is unnecessary or badly signposted. Removal is the usual
  outcome of both.
