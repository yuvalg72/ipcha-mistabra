#!/usr/bin/env python3
"""Reproducibly package this one-folder ChatGPT Skill using Python stdlib only."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from validate_skill import validate

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 25 * 1024 * 1024
EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv"}
EXCLUDE_FILES = {"skill.zip", ".DS_Store"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".bak", ".tmp", ".swp"}


def package(destination: Path) -> Path:
    errors = validate(ROOT)
    if errors:
        raise ValueError("Cannot package invalid Skill: " + "; ".join(errors))
    destination = destination.resolve()
    paths = []
    for candidate in sorted(ROOT.rglob("*")):
        relative = candidate.relative_to(ROOT)
        if (not candidate.is_file() or candidate.resolve() == destination or
                any(part in EXCLUDE_DIRS for part in relative.parts) or
                candidate.name in EXCLUDE_FILES or candidate.suffix in EXCLUDE_SUFFIXES or
                candidate.name.startswith(".env")):
            continue
        paths.append((candidate, relative.as_posix()))
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_suffix(".tmp")
    try:
        with ZipFile(temp, "w", ZIP_DEFLATED) as bundle:
            for candidate, relative in paths:
                # Fixed timestamps and permissions make repeat packages reproducible.
                payload = candidate.read_bytes()
                from zipfile import ZipInfo
                info = ZipInfo(filename=f"{ROOT.name}/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = (0o644 & 0xFFFF) << 16
                bundle.writestr(info, payload)
        if temp.stat().st_size > MAX_BYTES:
            raise ValueError("skill.zip exceeds 25 MiB")
        with ZipFile(temp) as bundle:
            names = bundle.namelist()
            if (not names or {name.split("/")[0] for name in names} != {ROOT.name} or
                    f"{ROOT.name}/SKILL.md" not in names):
                raise ValueError("The package must have exactly one Skill root and SKILL.md")
        os.replace(temp, destination)
    finally:
        temp.unlink(missing_ok=True)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "skill.zip")
    args = parser.parse_args()
    try:
        path = package(args.output)
    except (OSError, ValueError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1
    print(f"VALID: {path} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
