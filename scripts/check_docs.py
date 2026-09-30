#!/usr/bin/env python3
"""Mechanical docs checks (stdlib only). Stub: diagram boxes only; rule checks arrive in M1."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTEXTS = ("Purchase", "Payment", "Access")


def check_diagrams():
    errors = []
    for path in sorted((ROOT / "diagrams").glob("*.mmd")):
        text = path.read_text()
        seq = text.lstrip().startswith("sequenceDiagram")
        for ctx in CONTEXTS:
            pattern = rf"^\s*box\b.*\b{ctx}\b" if seq else rf"^\s*(subgraph|state)\s+\"?{ctx}\b"
            if not re.search(pattern, text, re.M):
                errors.append(f"{path.name}: missing {ctx} box")
    return errors


def main():
    errors = check_diagrams()
    for e in errors:
        print("ERROR", e)
    print(f"check_docs: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
