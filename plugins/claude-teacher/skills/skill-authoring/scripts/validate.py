#!/usr/bin/env python3
"""Mechanically validate an Agent Skill directory.

Checks only what inspection misses or gets wrong: frontmatter that fails to parse (which
disables a skill silently, with no error at the point of use), field combinations that cancel
each other out, references to bundled files that are not there, and bundled files nothing
points at.

Judgement calls -- whether a description routes, whether a body earns its length -- are not
here. They belong to the reviewer.

    python3 validate.py <skill-dir> [--portable]

--portable restricts frontmatter to the six fields claude.ai uploads and the Skills API
accept; every other key is a hard error on those paths rather than a warning.

Exit status is 1 if any ERROR was reported, else 0.
"""

import os
import re
import sys

# Claude Code's full field set. A key outside it is not rejected at load time -- it is
# ignored, so a typo looks exactly like the feature not working.
KNOWN_FIELDS = {
    "name", "description", "when_to_use", "argument-hint", "arguments",
    "disable-model-invocation", "user-invocable", "allowed-tools", "disallowed-tools",
    "model", "effort", "context", "agent", "background", "hooks", "paths", "shell",
    "metadata", "license", "compatibility",
}

# The portable subset. Anything else is a hard error on claude.ai / the Skills API.
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

BUNDLE_DIRS = ("references", "scripts", "assets")

# A description is a routing key, not a summary. Past roughly this length it has almost
# always started describing the procedure instead of the trigger.
DESCRIPTION_WORD_BUDGET = 40
BODY_LINE_BUDGET = 500
TOC_LINE_BUDGET = 100

TRUTHY = {"true", "yes", "on", "1"}
FALSY = {"false", "no", "off", "0"}

findings = []


def report(level, path, line, message):
    findings.append((level, path, line, message))


def error(path, line, message):
    report("ERROR", path, line, message)


def warn(path, line, message):
    report("WARN", path, line, message)


def split_frontmatter(text):
    """Return (frontmatter_text, body_text, body_start_line) or (None, text, 1)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text, 1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:]), i + 2
    return None, text, 1


def parse_frontmatter(fm_text, path):
    """Parse with PyYAML when available, otherwise a strict subset parser.

    Either way, run the subset scan first: it names the specific line that breaks, which a
    YAML error message usually does not.
    """
    subset = subset_scan(fm_text, path)
    try:
        import yaml
    except ImportError:
        return subset
    try:
        data = yaml.safe_load(fm_text)
    except Exception as exc:  # noqa: BLE001 -- any parse failure is the same defect
        first = str(exc).strip().split("\n")[0]
        error(path, 2, "frontmatter is not valid YAML, so the skill loads as nothing: %s" % first)
        return subset if isinstance(subset, dict) else {}
    if data is None:
        error(path, 2, "frontmatter is empty")
        return {}
    if not isinstance(data, dict):
        error(path, 2, "frontmatter must be a mapping of fields, got %s" % type(data).__name__)
        return {}
    return data


def subset_scan(fm_text, path):
    """Flag the hazards that silently break frontmatter, and return what parsed.

    Only top-level `key: value` pairs are returned; block scalars and nested structures are
    recognized and skipped rather than parsed.
    """
    data = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        raw = lines[i]
        lineno = i + 2  # +1 for the opening `---`, +1 for 1-indexing
        i += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            error(path, lineno, "leading tab -- YAML forbids tabs for indentation")
            continue
        if raw[0] in " -":
            continue  # continuation of a block scalar, nested map, or list item
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:(.*)$", raw)
        if not match:
            error(path, lineno, "not a `key: value` line: %s" % raw.strip()[:60])
            continue
        key, value = match.group(1), match.group(2).strip()
        if value in (">", "|", ">-", "|-", ">+", "|+"):
            block = []
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                block.append(lines[i].strip())
                i += 1
            data[key] = " ".join(p for p in block if p)
            continue
        if value == "":
            data[key] = ""
            continue
        if value[0] in "\"'":
            quote = value[0]
            if not value.endswith(quote) or len(value) < 2:
                error(path, lineno, "`%s` opens a quote it never closes" % key)
            data[key] = value[1:-1] if len(value) >= 2 else value
            continue
        # The common silent killer: an unquoted scalar containing `: `, which YAML reads as a
        # nested mapping rather than as text.
        if re.search(r":\s", value):
            error(
                path, lineno,
                "`%s` is unquoted and contains a colon followed by a space, so YAML reads it "
                "as a nested mapping -- quote the value or use a `>` block" % key,
            )
        if value[0] in "&*!%@`":
            error(path, lineno, "`%s` starts with `%s`, which is YAML syntax -- quote the value"
                  % (key, value[0]))
        data[key] = value
    return data


def as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        low = value.strip().lower()
        if low in TRUTHY:
            return True
        if low in FALSY:
            return False
    return None


def strip_fences(text):
    """Blank out fenced code blocks, keeping line numbering intact.

    Paths inside a fence are illustrative -- an example of what a reference looks like, not a
    reference. Scanning them produces false missing-file reports.
    """
    out, fenced = [], False
    for line in text.split("\n"):
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
            out.append("")
        else:
            out.append("" if fenced else line)
    return "\n".join(out)


# Asserted patterns: a path in one of these forms is a claim that the file is there, so its
# absence is an error.
REF_PATTERNS = (
    # An explicit skill-directory path.
    re.compile(r"\$\{CLAUDE_SKILL_DIR\}/([A-Za-z0-9_./-]+)"),
    # A markdown link to a relative path.
    re.compile(r"\]\((?!https?:|#|mailto:)([A-Za-z0-9_./-]+)\)"),
)

# A bare bundle path mentioned in prose or a command line. Enough to show a file is not
# orphaned, but too loose to treat its absence as a defect -- documentation about skills
# writes paths like these as examples.
LOOSE_REF_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_./-])((?:%s)/[A-Za-z0-9_./-]+)" % "|".join(BUNDLE_DIRS)
)


def find_references(text):
    """Yield (path, line, asserted) for each reference to a bundled file.

    `asserted` is False for a path inside a fenced code block. Those are illustrative -- an
    example of what a reference looks like -- so their absence is not a defect. They still
    count as pointing at a file, which is what orphan detection asks.
    """
    fenced_blanked = strip_fences(text).split("\n")
    for lineno, line in enumerate(text.split("\n"), start=1):
        asserted = fenced_blanked[lineno - 1] != "" if lineno <= len(fenced_blanked) else True
        for pattern in REF_PATTERNS:
            for match in pattern.finditer(line):
                target = match.group(1).lstrip("./")
                if target and target != "SKILL.md":
                    yield target, lineno, asserted
        for match in LOOSE_REF_PATTERN.finditer(line):
            yield match.group(1), lineno, False


def check_frontmatter(fm, skill_dir, skill_md, portable):
    name = fm.get("name")
    dirname = os.path.basename(os.path.abspath(skill_dir))
    if name is None:
        warn(skill_md, 2, "no `name` -- it defaults to the directory name, which is fragile for a "
                          "plugin installed from a marketplace, where that name is a version string")
    else:
        name = str(name)
        if name != dirname:
            error(skill_md, 2, "`name: %s` does not match the directory `%s`, so the skill does "
                               "not load" % (name, dirname))
        if len(name) > 64:
            error(skill_md, 2, "`name` is %d characters, over the 64 limit" % len(name))
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            error(skill_md, 2, "`name` must be lowercase letters, digits and single hyphens, with "
                               "no leading, trailing or doubled hyphen")
        if name in ("anthropic", "claude") or "anthropic" in name or "claude" in name:
            warn(skill_md, 2, "`name` contains a reserved word (`anthropic` / `claude`), which is "
                              "rejected on Anthropic's own surfaces")

    desc = fm.get("description")
    if not desc or not str(desc).strip():
        error(skill_md, 2, "no `description` -- it is the only thing that decides whether the "
                           "skill is ever chosen")
    else:
        desc = str(desc).strip()
        if len(desc) > 1024:
            error(skill_md, 2, "`description` is %d characters, over the 1024 limit" % len(desc))
        if "<" in desc or ">" in desc:
            error(skill_md, 2, "`description` contains `<` or `>`; it lands in the system prompt "
                               "and angle brackets can inject unintended structure")
        words = len(desc.split())
        if words > DESCRIPTION_WORD_BUDGET:
            warn(skill_md, 2, "`description` is %d words -- past roughly %d it is usually "
                              "summarizing the procedure, which the model then follows instead of "
                              "loading the body" % (words, DESCRIPTION_WORD_BUDGET))
        # Only the point of view that actually hurts discovery: the skill speaking as "I", or
        # addressing the reader as the actor. "Use when you need X" is an ordinary trigger
        # phrasing and is not flagged.
        if re.search(r"^\s*(I|You)\b", desc) or re.search(r"\bI (can|will|'ll) help\b", desc):
            warn(skill_md, 2, "`description` is written in first or second person; it is injected "
                              "into the system prompt, and mixed point of view hurts discovery. "
                              "Write it in third person, about the skill")

    for key in fm:
        if key not in KNOWN_FIELDS:
            (error if portable else warn)(
                skill_md, 2,
                "unknown frontmatter field `%s`%s" % (
                    key,
                    " -- only %s are accepted on claude.ai and the Skills API, and anything else "
                    "is a hard error there" % ", ".join(sorted(SPEC_FIELDS)) if portable
                    else " -- it is ignored silently, so a typo here looks like the feature not working",
                ),
            )
        elif portable and key not in SPEC_FIELDS:
            error(skill_md, 2, "`%s` is a Claude Code extension and is rejected outright by "
                               "claude.ai uploads and the Skills API" % key)

    no_model = as_bool(fm.get("disable-model-invocation")) is True
    no_user = as_bool(fm.get("user-invocable")) is False
    if no_model and no_user:
        error(skill_md, 2, "`disable-model-invocation: true` with `user-invocable: false` leaves "
                           "the skill unreachable by anyone -- pick one")

    forked = str(fm.get("context", "")).strip() == "fork"
    for field in ("agent", "background"):
        if field in fm and not forked:
            warn(skill_md, 2, "`%s` only has an effect with `context: fork`; here it does nothing"
                 % field)

    allowed = fm.get("allowed-tools")
    if allowed is not None:
        text = " ".join(allowed) if isinstance(allowed, list) else str(allowed)
        for skill_ref in re.findall(r"Skill\(([^)]*)\)", text):
            target = skill_ref.strip().split()[0] if skill_ref.strip() else ""
            if target and ":" not in target:
                warn(skill_md, 2, "`Skill(%s)` is not namespaced -- a bare name is a name, not an "
                                  "identity, so a project or personal skill of the same name "
                                  "inherits a grant never meant for it" % target)
    return fm


def check_body(body, body_start, skill_md, fm):
    lines = body.split("\n")
    if len(lines) > BODY_LINE_BUDGET:
        warn(skill_md, body_start, "body is %d lines, over the ~%d guideline; it enters the "
                                   "conversation once and stays for the session, so every line is "
                                   "a recurring cost" % (len(lines), BODY_LINE_BUDGET))

    allowed = fm.get("allowed-tools")
    allowed_text = " ".join(allowed) if isinstance(allowed, list) else str(allowed or "")
    scannable = strip_fences(body)
    for script in set(re.findall(r"\$\{CLAUDE_SKILL_DIR\}/(scripts/[A-Za-z0-9_./-]+)", scannable)):
        if script not in allowed_text:
            warn(skill_md, body_start, "`%s` is invoked but not pre-approved in `allowed-tools`, "
                                       "so running it prompts; grant the command exactly as the "
                                       "body invokes it, interpreter included" % script)


def check_bundle(skill_dir, skill_md):
    """Referenced-but-absent, present-but-orphaned, chain depth, and missing tables of contents."""
    bundled = []
    for sub in BUNDLE_DIRS:
        base = os.path.join(skill_dir, sub)
        for root, _dirs, files in os.walk(base):
            for filename in files:
                if filename.startswith("."):
                    continue
                full = os.path.join(root, filename)
                bundled.append(os.path.relpath(full, skill_dir).replace(os.sep, "/"))

    markdown = {"SKILL.md": skill_md}
    for rel in bundled:
        if rel.endswith(".md"):
            markdown[rel] = os.path.join(skill_dir, rel)

    referenced = set()
    for rel, full in markdown.items():
        try:
            with open(full, encoding="utf-8") as handle:
                text = handle.read()
        except OSError as exc:
            error(full, 1, "cannot read: %s" % exc)
            continue
        for target, lineno, asserted in find_references(text):
            # A relative link resolves against the file that wrote it, not the skill root.
            here = os.path.dirname(rel)
            candidates = [os.path.normpath(os.path.join(here, target)) if here else target, target]
            resolved = next((c for c in candidates if os.path.exists(os.path.join(skill_dir, c))),
                            None)
            referenced.add(resolved or target)
            if resolved is None:
                if asserted:
                    error(full, lineno, "references `%s`, which does not exist" % target)
            elif rel != "SKILL.md" and resolved.endswith(".md"):
                warn(full, lineno, "`%s` points at `%s`, making a two-hop documentation chain from "
                                   "SKILL.md; files reached through a chain get read partially, and "
                                   "partial reference material reads as complete" % (rel, resolved))

    for rel in sorted(bundled):
        if rel not in referenced:
            warn(skill_md, 2, "`%s` is bundled but nothing points at it -- reference it or delete "
                              "it" % rel)

    for rel, full in markdown.items():
        if rel == "SKILL.md":
            continue
        with open(full, encoding="utf-8") as handle:
            head = [next(handle, "") for _ in range(20)]
            handle.seek(0)
            total = sum(1 for _ in handle)
        if total > TOC_LINE_BUDGET and not any(re.match(r"^\s*[-*]\s*\[", line) for line in head):
            warn(full, 1, "%d lines with no table of contents in the first 20; a partial read of a "
                          "long reference hides the rest of its scope" % total)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    unknown = flags - {"--portable"}
    if unknown or len(args) != 1:
        print("usage: validate.py <skill-dir> [--portable]", file=sys.stderr)
        return 2
    skill_dir = args[0]
    portable = "--portable" in flags

    if not os.path.isdir(skill_dir):
        print("ERROR %s: not a directory" % skill_dir, file=sys.stderr)
        return 1
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        print("ERROR %s: no SKILL.md -- a skill is a directory containing one" % skill_dir,
              file=sys.stderr)
        return 1

    with open(skill_md, encoding="utf-8") as handle:
        text = handle.read()

    fm_text, body, body_start = split_frontmatter(text)
    if fm_text is None:
        error(skill_md, 1, "no YAML frontmatter delimited by `---`; without it there is no "
                           "description, and the skill is never chosen")
        fm = {}
    else:
        fm = parse_frontmatter(fm_text, skill_md)

    check_frontmatter(fm, skill_dir, skill_md, portable)
    check_body(body, body_start, skill_md, fm)
    check_bundle(skill_dir, skill_md)

    errors = [f for f in findings if f[0] == "ERROR"]
    for level, path, line, message in findings:
        print("%-5s %s:%d  %s" % (level, path, line, message))
    if not findings:
        print("OK")
    else:
        print("\n%d error(s), %d warning(s)" % (len(errors), len(findings) - len(errors)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
