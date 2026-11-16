"""
Run once per generation. Prints a metrics line and flags separation events.
"""

import subprocess
import sys
from pathlib import Path


def count_code_lines() -> int:
    skip_dirs = {".git", "__pycache__", "venv", "node_modules"}
    comment_prefixes = ("#", "//", "*", "/*", "*/")
    total = 0
    for pattern in ("**/*.py", "**/*.js"):
        for f in Path(".").glob(pattern):
            if f.name in ("metrics.py",):
                continue
            if f.name.endswith(".test.js") or f.name.startswith("test_"):
                continue
            if any(p in f.parts for p in skip_dirs):
                continue
            for line in f.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped and not any(stripped.startswith(p) for p in comment_prefixes):
                    total += 1
    return total


def count_dead_code() -> int:
    # JS lineage: no vulture; dead code detection not available for JS
    return -1


def current_generation() -> int:
    log = Path("EVOLUTION.md").read_text(encoding="utf-8")
    gens = [int(l.split(":")[1].strip()) for l in log.splitlines() if l.startswith("gen:")]
    return max(gens) if gens else 0


def detect_separation() -> list[str]:
    """Flag architectural separation events (JS lineage variant)."""
    events = []
    # Static HTML calculator
    for html in Path(".").glob("*.html"):
        events.append(f"SEPARATION: standalone HTML file found — {html}")
    return events


if __name__ == "__main__":
    gen = current_generation()
    lines = count_code_lines()
    dead = count_dead_code()

    # Read cap from BRANCH_CONFIG.md if it exists
    cap = 1500
    cfg = Path("BRANCH_CONFIG.md")
    if cfg.exists():
        for line in cfg.read_text().splitlines():
            if line.startswith("cap:") and "none" in line.lower():
                cap = 999999
                break
            if line.startswith("cap:"):
                import re
                m = re.search(r"(\d+)", line)
                if m:
                    cap = int(m.group(1))
                break

    headroom = cap - lines if cap < 999999 else "∞"
    cap_label = str(cap) if cap < 999999 else "none"

    print(f"gen={gen:04d} lines={lines} dead={dead} cap={cap_label} headroom={headroom}")

    sep = detect_separation()
    for s in sep:
        print(f"⚠ {s}")

    if cap < 999999 and lines >= int(cap * 0.93):
        print(f"WARNING: approaching carrying capacity ({lines}/{cap}) — must delete before adding")
    if cap < 999999 and lines > cap:
        print(f"ERROR: carrying capacity exceeded ({lines}/{cap})", file=sys.stderr)
        sys.exit(1)
