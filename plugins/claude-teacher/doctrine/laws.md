# Laws

Normative. So is every other file in this directory.

- [Assume the frontier](#assume-the-frontier)
- [The description is a routing key, not a summary](#the-description-is-a-routing-key-not-a-summary)
- [A skill's public surface is its name and the job it owns](#a-skills-public-surface-is-its-name-and-the-job-it-owns)
- [Leave nothing to interpret](#leave-nothing-to-interpret)
- [Match the form to the failure](#match-the-form-to-the-failure)
- [Let the runtime do it](#let-the-runtime-do-it)
- [Every claim is grounded in something real](#every-claim-is-grounded-in-something-real)


A skill is never alone. A real system has many — capabilities, drivers, workflows, bodies of
knowledge — and they are the building blocks everything else is assembled from. So they answer to
the principles any other module answers to, and every law below is an application of one:

| Principle | For a skill | Carried by |
| :--- | :--- | :--- |
| **Modularity** | one responsibility, one owned area, scoped like a function | the admission test's fourth clause |
| **Encapsulation** | internals are unreachable from outside — no sibling runs its scripts, names its CLI, or repeats its rules | the public-surface law |
| **Open–closed** | the name and the job it owns are stable; everything behind them is free to change | the public-surface law, and naming |
| **Reusability** | another skill can route to it by name and outcome, and get the capability without knowing how | the referral form, and declared hand-offs |

Where a rule below seems arbitrary, it is one of these four made concrete.

### Assume the frontier

The test for every line is: **would a competent agent get this wrong without it?** If no, cut it.
This retires whole classes of content that skills habitually carry:

| Cut — the agent already has it                       | Keep — it cannot be derived                                             |
| ------------------------------------------------------ | ------------------------------------------------------------------------- |
| What the format is, why the tool exists, what a 404 means | That this service answers `404` for a route that exists but is not deployed |
| "If the CLI is not installed, install it"             | That an HTML body instead of a JSON error means a proxy answered, not the app |
| Restating what a linter, compiler, or type checker rejects | The paired rule no tool enforces, where moving one half silently breaks the other |
| Standard language and framework convention            | The one place this project deliberately violates it, and why                |

The mirror failure is real and costs more: **over-trimming**. Cutting the *reason* leaves a bare
imperative that stops generalizing the moment the situation shifts. Cut duplication and derivable
facts; never cut the mechanism that explains a rule.

### The description is a routing key, not a summary

It is the only thing loaded before the skill is chosen, and the only thing that decides whether it is
chosen. Three consequences:

- **It carries triggers, not procedure.** The words, tools, symptoms, and product names that should
  fire it. Third person, about the skill.
- **It must not un-black-box the body.** A description that summarizes the workflow gets acted on
  *instead of* the body — the agent takes the summary as the instruction and never loads the file it
  is summarizing. Name the domain and the outcome; never enumerate the steps.
- **Its length is independent of the body's.** A body that triples earns no extra description. Aim
  for the shortest description that still routes correctly — around twenty words for most skills.
- **Under-triggering is the default failure.** A skill is consulted when the task looks like more
  than the agent can already do, so a description that reads as ordinary work never fires. Say
  where it applies, including the cases where the operator will not name the domain.
- **Carry the words a request would actually contain** — the error strings, the symptoms, the
  product and tool names, the file types. That is what it is matched against. This pulls against
  the twenty words, so spend them on the highest-signal terms rather than listing every synonym.

### A skill's public surface is its name and the job it owns

Everything else is private: the CLI it shells out to, its subcommands and flags, its script paths,
its env vars, its config files, the identifiers it hardcodes. Those are free to change the day it
swaps its CLI for an MCP server. The law reaches wherever the skill speaks — the body,
`references/`, and whatever its scripts print.

**Private surface is free, and it is the point.** This law constrains who may reach in, never
whether you may have internals — so a script's flags, its token store, its cache cost nothing to
own. Moving a rule the caller must remember into an internal the caller cannot reach is the trade
this law exists to enable, the same one behind preferring a field the runtime enforces over a
paragraph asking for the same thing. Reading it as a reason to keep a skill thin inverts it.

The name is half that surface, so it names the job and never the tooling — `kubernetes`, not
`kubectl`; `deliver`, not `trigger-gitlab-pipeline`. Verb-first or gerund where the skill does
something, the domain's own noun where it answers questions about one. Never `helper`, `utils`,
`tools`, or any name whose scope you cannot state in a sentence: a name that vague cannot route,
and it invites the skill to accrete a second job.

So a skill that needs another skill's capability **names the skill and states the outcome in domain
terms**, and lets the owner supply the command:

| ✗ Reaching in                                | ✓ Referring                                        |
| ---------------------------------------------- | ---------------------------------------------------- |
| `bash <other-skill>/scripts/api.bash send …`  | "send it — the `telegram` skill"                    |
| "needs the `cloud` skill's `xyzctl` auth"     | "needs cloud access — the `cloud` skill"            |
| Copying a sibling's context names into an example | "`-c <context>`, which the `kubernetes` skill lists" |

Two clauses that are easy to miss:

- **Restating a sibling's invariant is also a violation** — "the `commit` skill never pushes". That
  is a second copy of a claim with one owner. Say what *this* skill does and let the other speak for
  itself.
- **No path form crosses a skill boundary; only the name does.** The CLAUDE_SKILL_DIR template
  variable is the one that looks like an exception and is not — `frontmatter.md` says why.
  CLAUDE_PLUGIN_ROOT genuinely can address a sibling skill's directory, and that is the one place
  this law needs stating rather than deriving: use it for what the plugin shares between its own
  components, never to reach into a sibling skill's files.
- **Not every path leaving the skill is a boundary crossing.** A binary on the operator's `PATH`,
  or a project-scoped entry point like `npm run test`, is ordinary use of the environment. Reaching
  into a sibling's directory — `<this-skill>/../database/scripts/psql.bash` — is the violation,
  and no skill ever runs another skill's script.
- **Name a sibling in the fixed form** — `` the `kubernetes` skill ``. This is grammar, not style:
  a reference written that way can be checked against the installed set, and one written any other
  way cannot be found at all. A name in that position that is not a skill is either somebody's
  internal or a rename left behind, and both are broken today rather than eventually.

Declare a hand-off you rely on in `allowed-tools`, **always namespaced** — `Skill(plugin:commit)`,
never bare `Skill(commit)`. A bare name is a name, not an identity: a project or personal skill of
the same name overrides the one you meant and inherits a grant never intended for it. The list
doubles as the skill's dependency list, so a name there the body never routes to is a stale
dependency.

A sentence cannot be namespaced — "the `commit` skill" means whichever `commit` the operator has
installed. The grant is what fixes the identity, so every sibling the body routes to is declared,
and the pair is read together: the sentence says what is wanted, the grant says which skill.

### Leave nothing to interpret

- **One term for one thing**, throughout. Synonyms read as distinctions.
- **A default, not a menu.** "Use X; for the OCR case, Y instead" — never "you could use X, or Y, or
  Z".
- **No nuance clauses.** "Don't do X unless it matters" reopens the negotiation you just closed. A
  genuine exception is its own conditional on an observable predicate: "if a design doc exists, cite
  it".
- **Exemptions do not scope.** "This limit does not apply to code blocks" still suppresses code
  blocks. If part of the output must be exempt, restructure so the rule cannot reach it.
- **State the rule and its mechanism in the same breath** — what actually breaks, which tool
  misbehaves, what drifts. A rule with its reason attached survives the case you did not anticipate.

### Match the form to the failure

Classify what actually goes wrong *before* choosing how to write it. The form that fixes one failure
measurably worsens another.

| The failure                                               | The form that works                                              | The form that backfires             |
| ----------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------- |
| Knows the rule, skips it under pressure                    | Prohibition, plus the specific excuses named and answered         | Soft guidance — "prefer", "consider" |
| Complies, but the output has the wrong shape               | A positive recipe: state what the output **is**, its parts in order | A list of prohibitions              |
| Omits an element from something it already produces        | Structural — a required slot in the template it fills             | A prose reminder near the template  |
| Behaviour should depend on a condition                     | A conditional keyed to an observable predicate                    | An unconditional rule with exemptions |

### Let the runtime do it

Anything the frontmatter, a script, or a hook can enforce should not be prose asking nicely. Prose
shapes behaviour; it does not guarantee it. `frontmatter.md` maps each intent to the field
that carries it — restricting tools, blocking auto-invocation, scoping activation to file patterns,
forking to a subagent, injecting live command output. A skill that spends a paragraph asking for
something a field enforces has chosen the weaker of two available mechanisms.

### Every claim is grounded in something real

**Never invent a flag, path, field, subcommand, endpoint, or API.** Read the real thing — the CLI's
`--help`, the actual config, the repository — or leave it out. An invented detail stated confidently
is the most expensive defect a skill can carry: it reads as authoritative and is wrong, and the
agent has no way to tell it from the parts that are true.

**An absence is a claim in the same way** — "there is no such endpoint", "the tool has no such
flag", "that document is not served anywhere". It needs the same grounding before anything is built
on it, because what gets built on an unverified absence is a workaround: a scraper, a snapshot, a
hardcoded copy of something the system would have answered for itself.

The same test applies to the skill as a whole. **What it teaches must come from something that
actually happened** — a task run, a correction made, a real config or spec read, a real incident.
Content generated from priors alone can only restate what the agent already knows, which is by
construction the content that fails the frontier test.

