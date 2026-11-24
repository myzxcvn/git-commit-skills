#!/usr/bin/env python3
"""Validate this repository's Skill metadata, local links and eval definitions."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ERRORS = []


def fail(path, message):
    ERRORS.append(f"{path.relative_to(ROOT)}: {message}")


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(path, str(exc))
        return ""


def validate_skill(path):
    raw = read(path)
    # Deliberately support the repository's simple, single-line YAML metadata.
    match = re.match(r"\A---\n(.*?)\n---\n", raw, re.S)
    if not match:
        fail(path, "missing front matter")
        return
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if not sep or key in fields or key not in {"name", "description"}:
            fail(path, f"invalid or duplicate metadata: {line}")
            continue
        value = value.strip()
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError:
                fail(path, f"invalid quoted value: {key}")
                continue
        fields[key] = value
    name = fields.get("name", "")
    if not isinstance(name, str) or name != path.parent.name or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", name
    ) or len(name) > 64:
        fail(path, "invalid name or directory mismatch")
    desc = fields.get("description", "")
    if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
        fail(path, "description must contain 1–1024 characters")


def validate_markdown(path):
    fence = None
    for number, line in enumerate(read(path).splitlines(), 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token, tail = marker.groups()
            if fence is None:
                fence = token
                continue
            if token[0] == fence[0] and len(token) >= len(fence) and not tail.strip():
                fence = None
            continue
        if fence:
            continue
        # Repository-local inline Markdown links; external URLs are not fetched.
        for target in re.findall(r"\]\(([^)\s]+)\)", line):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            local = (path.parent / unquote(url.path)).resolve()
            if not local.is_relative_to(ROOT) or not local.exists():
                fail(path, f"line {number}: invalid local link {target}")
    if fence:
        fail(path, "unclosed Markdown fence")


def validate_evals(skill_names):
    files = sorted((ROOT / "evals").glob("*.json"))
    if {p.stem for p in files} != skill_names:
        fail(ROOT / "evals", "expected one JSON dataset per skill")
    ids = set()
    count = 0
    for path in files:
        try:
            data = json.loads(read(path))
        except ValueError as exc:
            fail(path, str(exc))
            continue
        if not isinstance(data, dict) or data.get("skill") != path.stem:
            fail(path, "skill does not match dataset filename")
            continue
        cases = data.get("cases")
        if not isinstance(cases, list) or not cases:
            fail(path, "cases must be a nonempty array")
            continue
        for case in cases:
            count += 1
            if not isinstance(case, dict):
                fail(path, "case must be an object")
                continue
            ident = case.get("id")
            if not isinstance(ident, str) or not re.fullmatch(r"[A-Z]+-[0-9]{3}", ident) or ident in ids:
                fail(path, f"invalid or duplicate case id: {ident}")
            else:
                ids.add(ident)
            for key in ("task", "fixture"):
                if not isinstance(case.get(key), str) or not case[key].strip():
                    fail(path, f"{ident}: missing {key}")
            for key in ("expect", "forbid"):
                items = case.get(key)
                if not isinstance(items, list) or not items or not all(
                    isinstance(item, str) and item.strip() for item in items
                ):
                    fail(path, f"{ident}: invalid {key}")
    return count


def main():
    names = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    if not names:
        fail(SKILLS, "no skills found")
    for name in sorted(names):
        validate_skill(SKILLS / name / "SKILL.md")
    for path in sorted(SKILLS.rglob("*.md")) + [ROOT / "README.md", ROOT / "AGENTS.md"]:
        validate_markdown(path)
    count = validate_evals(names)
    if ERRORS:
        print("\n".join(ERRORS), file=sys.stderr)
        return 1
    print(f"Validated {len(names)} skills and {count} eval definitions (static only).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
