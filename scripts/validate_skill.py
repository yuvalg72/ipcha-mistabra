#!/usr/bin/env python3
"""Offline repository contract validator for the standalone Ipcha Mistabra Skill."""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = ROOT.name
REQUIRED_SECTIONS = (
    "## What this Skill does", "## Use this Skill when", "## Core capabilities",
    "## Typical workflow", "## Expected output", "## Guardrails and boundaries",
    "## Example prompts", "## Related Skills", "## Skill files", "## Repository navigation",
)
LINK_PATTERN = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skill_file = root / "SKILL.md"
    metadata_file = root / "agents/openai.yaml"
    icon_file = root / "assets/icon.svg"
    readme_file = root / "README.md"
    for path in (skill_file, metadata_file, icon_file, readme_file):
        if not path.is_file():
            errors.append("Missing required file: " + str(path.relative_to(root)))
    if errors:
        return errors
    skill, metadata, readme = (x.read_text(encoding="utf-8") for x in
                               (skill_file, metadata_file, readme_file))
    fm = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    if not fm:
        errors.append("SKILL.md missing frontmatter")
    else:
        keys = re.findall(r"^([a-z][a-z_]*):", fm.group(1), re.M)
        if sorted(keys) != ["description", "name"]:
            errors.append("Frontmatter must contain exactly name and description")
        if f"name: {root.name}\n" not in fm.group(0):
            errors.append("Skill slug mismatches directory name")
        if len(fm.group(1)) < 120 or not re.search(r"\bUse (?:when|to)\b", fm.group(1)):
            errors.append("Description lacks clear purpose or invocation conditions")
    if "display_name: Ipcha Mistabra" not in metadata:
        errors.append("Metadata lacks display name")
    for key in ("icon_small", "icon_large"):
        if f"{key}: ./assets/icon.svg" not in metadata:
            errors.append(f"Metadata lacks {key} icon path")
    try:
        ET.parse(icon_file)
    except ET.ParseError as error:
        errors.append("Icon SVG invalid: " + str(error))
    for heading in REQUIRED_SECTIONS:
        if heading not in readme:
            errors.append("README missing section: " + heading)
    if "@ipcha-mistabra" not in readme:
        errors.append("README lacks exact invocation example")
    if "SKILL.md" not in readme or "authoritative" not in readme:
        errors.append("README must distinguish execution contract from documentation")
    for file in (skill_file, readme_file):
        for target in LINK_PATTERN.findall(file.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = (file.parent / target.split("#", 1)[0]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                errors.append(f"Broken or escaping link in {file.name}: {target}")
    for path in root.rglob("*"):
        if path.is_file() and (path.suffix == ".pyc" or "__pycache__" in path.parts):
            errors.append(f"Cache file or directory in source: {path.relative_to(root)}")
    return sorted(set(errors))


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print("ERROR: " + error, file=sys.stderr)
        return 1
    print("VALID: Skill structure, metadata, README and local links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
