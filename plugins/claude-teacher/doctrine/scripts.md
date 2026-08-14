# Bundled scripts

- [Two kinds of script](#two-kinds-of-script)
- [Whether to bundle one at all](#whether-to-bundle-one-at-all)
- [A wrapper hands the primitive back](#a-wrapper-hands-the-primitive-back)
- [Invocation](#invocation)
- [The interface](#the-interface)
- [Never blocks, never lies about failing](#never-blocks-never-lies-about-failing)
- [Output is the whole return channel](#output-is-the-whole-return-channel)
- [Errors](#errors)
- [Portability](#portability)
- [State](#state)
- [What the body must not say about the script](#what-the-body-must-not-say-about-the-script)

## Two kinds of script

Decide which one you are writing before anything else. Most rules below fork on it.

| | **Wrapper** | **Owned** |
| :--- | :--- | :--- |
| It is | an established CLI — `curl`, `kubectl`, `psql`, `glab` — fronted with preconfiguration, credentials, or a preflight | an operation the skill implements itself, with no CLI underneath |
| Its interface | the CLI's, passed through verbatim, plus only what the preconfiguration needs | yours, and minimal |
| Its output | the CLI's conventions, unchanged | whatever the next step needs |
| Its errors | the CLI's stderr and exit code, unchanged | yours to write |

A wrapper that reshapes what it wraps has quietly become an owned script with an inherited bug
surface — and the agent already knows the CLI, so every reshaping is one more fact it has to
unlearn at the point of use.

## Whether to bundle one at all

**The default is no script.** A command with a couple of flags belongs in the body, where the agent
can see it, adapt it, and compose the next one from it. A script is a second interface to maintain, a
permission grant to justify, and a thing the body can drift from — so it has to buy its way in.

It buys its way in when the agent cannot reliably do the thing from prose. Three conditions do that,
and each is mechanical rather than a matter of taste:

| Condition | Why prose cannot cover it |
| :--- | :--- |
| **Something must survive between tool calls.** A bearer token, a session or cookie, a resolved endpoint, a fetched document, a created account's handle — anything obtained once and used again later | Each Bash call is a fresh shell: exported variables are gone by the next call, and so is the working directory. A value captured in one call does not reach the next, and an instruction to stash it in a file must then be obeyed correctly on every call for the rest of the session. **Test it rather than assuming** — export a variable in one call and read it in another. This condition is the one most often missed, because it never bites the author, who holds the value in context while writing; it bites the caller, on the second call |
| **A step is conditional on the previous step's result, and getting it wrong is silent** | Refresh-then-retry, resolve-then-call, check-then-write. Written as prose it is a branch the agent must remember mid-task, and the failure looks like a normal error rather than a missed step |
| **The real call needs resolution first** — a credential read, an endpoint discovered, an environment picked | The preflight is where the mistakes are, and it is identical every time. See *The interface* below |

Repetition alone is not one of them. The same simple call made twenty times is fine in the body; what
justifies a script is that composing it correctly is hard, not that it happens often.

Its advantage is that the source never enters context, only the output. A script the agent has to
*read* in order to use has forfeited exactly that, so say which you mean: run it, or read it.

### A wrapper hands the primitive back

This is what makes a wrapper safe to write, and it is why covering the awkward part costs the caller
nothing. A wrapper owns the stateful or conditional part and **hands the primitive back** — a
`--token`, a `--url`, a resolved connection string, printed to stdout for the caller to use with the
real tool directly. The body says both paths exist and when each is right.

With that, a wrapper takes nothing away: everything the underlying tool could do, the caller can
still do. Without it, the script becomes the only way in, and a caller needing something it does not
expose — a response header, a streamed body, a deliberately malformed request — is stuck choosing
between a lie and giving up. That is the reshaping failure above wearing a different hat, and it is
the *absence* of the escape hatch that causes it, not the wrapper itself.

Note also what the wrapper is *not* hiding. The plumbing it owns — authenticating, resolving a host,
refreshing a token — is not the thing the caller is investigating. Wrapping a stable mechanism does
not obscure the subject under test; it removes the part that was never in question.

## Invocation

Bash unless the job makes it wrong. It is present on every machine without exception, and it is
the language the frontier writes most fluently, so the script is both runnable and reviewable
anywhere. Node, Python, or anything else the job genuinely needs is equally fine — this is the
job's choice, not a house style.

Invoke by absolute path with the interpreter named, and grant that exact string, interpreter
included. `<SKILL_DIR>` below stands in for the CLAUDE_SKILL_DIR template variable, written out in
shell form — an example may not contain it literally, because it would substitute:

```
bash <SKILL_DIR>/scripts/deploy.bash --env staging
```

```yaml
allowed-tools: Bash(bash <SKILL_DIR>/scripts/deploy.bash *)
```

A grant written without the `bash ` prefix does not match the command, so every call prompts.

The `*` is a prefix match: everything after it is accepted, and the agent composes that tail from
the operator's words. The script is therefore the boundary — `"$@"`, quoted expansions, no `eval`,
and never an argument interpolated into a shell string.

## The interface

Minimal. Every flag is one more thing that can be passed wrong and one more line the body spends
explaining it. A wrapper is the exception: it inherits the CLI's surface whole, because
re-deriving a subset of it is how a wrapper turns into an owned script.

- **Preflight lives in the script.** Missing binary, unset credential, wrong directory — the
  script checks and exits. The same check written into the body as an instruction costs a turn
  and gets skipped under pressure.
- **`--help` is how the agent learns an owned script.** Keep it short; it enters context. A
  wrapper's `--help` states what it preconfigures and leaves the rest to the real CLI's help.
- **Every hardcoded constant carries its reason** — a timeout, a retry count, a page size. If you
  cannot say why that value, the agent inheriting it cannot either.

## Never blocks, never lies about failing

**No interactive prompt, ever.** The agent's shell has no TTY. A `read`, a `sudo` password, a
confirmation menu, an auth flow that wants a browser, or a pager (`less` behind `git log`, `gh`,
`kubectl`) blocks until the harness kills the call — and a killed call discards the output it had
already produced, which is worse than any error. Take input from flags, environment, or stdin; set
`--no-pager` or `PAGER=cat` on anything that might page; exit with a usage error where a human
would have been asked a question.

**Bound anything that waits.** `curl --max-time`, a ceiling on every retry loop. The agent cannot
interrupt a hang; only the harness can, and it takes the output with it.

**Exit non-zero when it failed.** The exit code is the agent's control flow — a script that prints
an error and exits 0 makes it proceed on a failure it cannot see. `set -euo pipefail` in bash.
Distinct codes only where the agent should branch differently, documented in `--help`.

**Idempotent where the operation allows it.** Agents retry. Create-if-not-exists beats
create-and-fail-on-duplicate.

## Output is the whole return channel

The body is paid for once per session; the script's output is paid for on every call.

- **Data to stdout, progress and diagnostics to stderr**, so one can be filtered without dragging
  in the other.
- **Bounded.** Harnesses truncate past roughly 10–30K characters *silently*, and a truncated
  result reads as a complete one. Default an owned script to a summary with a `--limit`, or write
  the full result to a file the agent reads in pieces.
- **Shaped for what happens next.** An owned script emits JSON or TSV where the agent will filter
  or aggregate, plain lines where it will only read. A wrapper emits what the CLI emits.

## Errors

An owned script's error text is the agent's next attempt, so it states what was wrong, what was
expected, and what to try:

```
Error: --env is required. Options: development, staging, production.
```

A wrapper writes almost none of its own. The CLI's message is the best available one and the agent
reads it correctly — catching it to reword it only destroys information.

Neither kind explains what a status code means.

**What a script prints is prose the agent reads on the same terms as the body** — deferred, and
only on failure, but arriving at the moment it is deciding what to do next, so a wrong claim there
is acted on immediately. Every law governing the body governs it unchanged: one term for one
thing, nothing the agent already knows, and a sibling named as a skill and never as the binary
behind it. "The `kubernetes` skill lists them" survives that skill swapping `kubectl` for an MCP
server; "the kubectl skill lists them" was already false the day it was written.

## Portability

Bash is everywhere; the utilities a bash script reaches for are not. `sed -i`, `date -d`,
`grep -P` and `readlink -f` differ between GNU and BSD, and the failure surfaces as a flag error
that never mentions coreutils. Stay on POSIX-portable invocations, or detect and fail clearly.

A script in Python or Node declares its dependencies in the file itself — PEP 723 run with
`uv run` — rather than in a manifest the agent must install first.

## State

Prefer stateless. `kubectl config use-context` is the shape to avoid: it mutates a selector every
concurrent session reads, so two agents working at once silently fight over which cluster the next
command reaches. Pass the target per call instead.

Where state is genuinely needed, isolate it per session: the harness exports
`CLAUDE_CODE_SESSION_ID` into every Bash call, so the script reads it from its own environment and
keys the state directory on it — `/tmp/<skill>/$CLAUDE_CODE_SESSION_ID/`, exiting with a clear
error if it is unset. It is not one of the three template variables (`frontmatter.md`, path
substitution), so the body has nothing to pass in and never writes it.

## What the body must not say about the script

Do not narrate its failures. "If it returns 404 the resource does not exist", "if it returns 401
run `glab login`" — the agent reads those correctly unaided, and the lines spend session-long
context restating what it already knows.

Two things earn the space:

- an outcome whose cause is genuinely not derivable from what the script prints, and
- custom logic the script performs that nothing in its output reveals.

Nor should the body describe how the script behaves. The two drift, and the body loses: a sentence
saying the script falls back to a default when a flag is omitted survives long after the script
started refusing outright, and the agent believes the sentence. State what the skill is for; let
the script state what the script does.

The line between this rule and *A wrapper hands the primitive back* is interface versus mechanism.
That both paths exist and when each is right is the wrapper's **interface** — the caller cannot use
a path it was never told about, so the body must say it. How the script conducts either path — what
it preconfigures, checks, retries, or falls back to along the way — is **mechanism**, and that is
what this rule keeps out. A sentence that survives the script being rewritten with the same
interface is on the right side of the line; one that would become false is on the wrong side.
