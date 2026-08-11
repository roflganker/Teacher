---
name: teacher-feedback
description: Reports a flaw in the claude-teacher plugin's guidance — wrong, contradictory, or misleading doctrine, skills, or reviewers — to the maintainer as a GitHub issue. Use when the operator hits a problem with this plugin and wants it fixed upstream.
---

# Reporting a flaw in this plugin's guidance

Feedback goes to the plugin's public repository, `roflganker/Teacher` on GitHub. The maintainer
wants problems, not patches: an issue that proposes edits or replacement wording anchors the fix to
the reporter's framing, so the issue states what happened and what was expected, and stops there.

1. **Pin down the flaw.** Which component — the doctrine file, skill, or reviewer agent, by name —
   and the concrete situation: what the guidance said or led to (observed), and what the operator
   expected instead. Quote the offending line where there is one. Read the installed plugin's
   version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` — the maintainer cannot judge a
   report against an unknown revision.

2. **Draft the issue.**
   - Title: one line naming the component and the flaw.
   - Body, in order: the component and plugin version; the situation the flaw arose in; what was
     observed; what was expected. No proposed fix, edit, or replacement wording anywhere in it.

3. **Show the draft to the operator and apply their corrections.** Filing posts publicly under
   their GitHub account, so it never runs before they have read what will be posted.

4. **File it.** If `gh auth status` succeeds, create the issue —

   ```bash
   gh issue create -R roflganker/Teacher --title "<title>" --body "<body>"
   ```

   — and report the URL it prints. If `gh` is missing or unauthenticated, do not install it or
   start a login flow: hand the operator the drafted title and body together with
   <https://github.com/roflganker/Teacher/issues/new>, to file themselves.

Done when the issue's URL is reported, or the draft and the link are handed to the operator.

## Rules

- The issue describes the problem — situation, observed, expected — and never proposes a fix.
- Never posted unseen: the operator reads the draft before `gh issue create` runs.
- Invocation authorizes drafting and reading `gh` state; filing runs only after step 3, and
  patching the installed plugin around the flaw is never authorized — the fix arrives as a plugin
  update.
- Not handled: fixing the guidance, or tracking the issue after it is filed.
