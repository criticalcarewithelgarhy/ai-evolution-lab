# Purpose

**This file must never be edited by any generation.**

This project is an ICU clinical calculator containing four formulas:
MAP, P/F ratio, anion gap, and creatinine clearance (Cockcroft-Gault).

It is a research artefact for studying AI-directed code evolution.
It is not a production tool.

## Invariants no generation may break

1. The string `DISCLAIMER` in `calculator.py` must always contain `"NOT FOR CLINICAL USE"`.
2. All four original formulas must remain present and correct.
3. All existing tests must pass before a commit is made.
4. This file must not be modified.
5. `HYPOTHESES.md` must not be modified after generation 0.
6. `test_oracle.py` must never be modified. It is the independent correctness reference.
   Any generation that touches `test_oracle.py` invalidates the entire experiment.

## Evolvable vs locked files

| File | Status |
|---|---|
| `calculator.py` | **Evolvable** — agents may refactor, but numerical outputs must stay correct |
| `test_calculator.py` | **Evolvable** — agents may add, modify, or remove tests (this is part of the experiment) |
| `app.py` | **Evolvable** — UI changes permitted |
| `test_oracle.py` | **LOCKED** — never touch, never read as context |
| `PURPOSE.md` | **LOCKED** |
| `HYPOTHESES.md` | **LOCKED** |
| `RULES.md` | **LOCKED** |
