---
name: feedback-sweep
description: Interactive triage of this repository's open GitHub issues — user feedback on the plugin's guidance — to an operator-ruled outcome for each.
disable-model-invocation: true
allowed-tools: Skill(claude-teacher:skill-authoring), Bash(gh issue list*), Bash(gh issue view*)
---

# Sweeping the feedback issues

An interactive triage: every action on an issue follows an explicit ruling from the operator, made
against a brief — never against the raw issue list, and never inferred.

1. **Collect.** `gh issue list` in this repository — open issues only, which is its default. None
   open: report that and stop.

2. **Brief.** Read each with `gh issue view <number> --comments`. Where several report the same
   flaw, group them and pick the best-stated one as the original. Present one brief per issue or
   group: the component named, the claimed flaw, and a one-line assessment of whether the claim
   holds against the doctrine.

3. **Rule.** The operator rules on each brief: **discard**, **fix**, or **leave open**. A ruling
   on a group covers every issue in it. A brief without a ruling is left open and listed as such
   in the report.

4. **Act**, per ruling — on the issue itself, or on a group's original:

   | Ruling | Action |
   | :--- | :--- |
   | Discard | `gh issue close <number> --reason "not planned" --comment "<why>"` |
   | Fix | Apply it — a change to a skill runs the `skill-authoring` skill — and commit. Then `gh issue close <number> --reason completed --comment "<what changed, and the plugin version carrying it>"` |
   | Leave open | nothing |

   A discarded or fixed group's other members each close with
   `gh issue close <number> --duplicate-of <original>` — the reason needs no comment. A group left
   open stays open whole.

Done when every open issue was briefed and either acted on per its ruling or left open, and the
report lists each issue's outcome.

## Rules

- **Issue comments are one or two sentences.** A discard states why; a resolution states what
  changed and the version carrying it. The record is for the reporter, not a changelog.
- **A fixed issue closes only after its fix is committed.** A close citing an uncommitted change
  tells the reporter it shipped when nothing did.
- Invocation authorizes querying and briefing. Each comment, close, and fix runs only under the
  operator's ruling on that issue; pushing is never authorized by this skill.
- Not handled: deciding the rulings — an issue nobody ruled on stays open, however clear-cut it
  looks.
