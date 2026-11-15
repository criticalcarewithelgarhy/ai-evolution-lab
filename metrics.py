"""
Run once per generation. Prints a single metrics line to stdout.
Used in RULES.md Step 6.
"""

import subprocess
import sys
from pathlib import Path


def count_code_lines() -> int:
    total = 0
    for f in Path(".").glob("**/*.py"):
        if f.name == "metrics.py":
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                total += 1
    return total


def count_dead_code() -> int:
    try:
        result = subprocess.run(
            ["vulture", ".", "--min-confidence", "80"],
            capture_output=True, text=True
        )
        return len([l for l in result.stdout.splitlines() if l.strip()])
    except FileNotFoundError:
        return -1  # vulture not installed


def current_generation() -> int:
    log = Path("EVOLUTION.md").read_text(encoding="utf-8")
    gens = [int(l.split(":")[1].strip()) for l in log.splitlines()
            if l.startswith("gen:")]
    return max(gens) if gens else 0


if __name__ == "__main__":
    gen = current_generation()
    lines = count_code_lines()
    dead = count_dead_code()
    cap = 1500
    print(f"gen={gen:04d} lines={lines} dead={dead} cap={cap} headroom={cap - lines}")
    if lines >= 1400:
        print("WARNING: approaching carrying capacity — must delete before adding")
    if lines > cap:
        print("ERROR: carrying capacity exceeded", file=sys.stderr)
        sys.exit(1)
