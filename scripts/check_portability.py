#!/usr/bin/env python3
"""Check skills for host- and OS-portability problems.

    python3 scripts/check_portability.py

Enforces the mechanical rules from ARCHITECTURE.md#portability-rules.
Errors fail the run; warnings are printed for review.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

errors = []
warnings = []


def rel(path):
    return path.relative_to(ROOT)


def check_frontmatter(skill_md):
    match = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(), re.S)
    if not match:
        errors.append(f"{rel(skill_md)}: missing frontmatter")
        return
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{rel(skill_md)}: frontmatter is not valid YAML ({str(exc).splitlines()[0]})")
        return
    if not isinstance(frontmatter, dict) or not frontmatter.get("description"):
        errors.append(f"{rel(skill_md)}: frontmatter has no description")
        return
    description = frontmatter["description"]
    if len(description) > 1024:
        errors.append(f"{rel(skill_md)}: description is {len(description)} chars (Agent Skills limit is 1024)")


def check_file(path):
    text = path.read_text()
    for n, line in enumerate(text.splitlines(), 1):
        where = f"{rel(path)}:{n}"
        if re.search(r"(~|\$HOME)/\.claude/memory", line):
            errors.append(f"{where}: ~/.claude/memory path; use the agent's memory or $MAKERSKILLS_MEMORY")
        if "mcp__" in line:
            errors.append(f"{where}: Claude Code MCP tool name; describe the tool instead")
        if "Skill({" in line:
            errors.append(f"{where}: Claude Code Skill() call syntax; say 'run the <name> skill'")
        if re.search(r"\b(WebFetch|WebSearch)\b", line) and not re.search(r"e\.g\.|Claude Code", line):
            warnings.append(f"{where}: bare {re.search(r'WebFetch|WebSearch', line).group()}; prefer the capability")
    if re.search(r"\bpb(copy|paste)\b", text) and not re.search(r"wl-(copy|paste)|xclip", text):
        errors.append(f"{rel(path)}: pbcopy/pbpaste without a Linux fallback")
    if "CLAUDE.md" in text and "AGENTS.md" not in text:
        errors.append(f"{rel(path)}: reads CLAUDE.md without also accepting AGENTS.md")


for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
    check_frontmatter(skill_md)
for path in sorted(SKILLS.rglob("*")):
    if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
        check_file(path)

for w in warnings:
    print(f"warning: {w}")
for e in errors:
    print(f"error: {e}")
if errors:
    sys.exit(1)
print(f"portability check passed ({len(list(SKILLS.glob('*/SKILL.md')))} skills, {len(warnings)} warnings)")
