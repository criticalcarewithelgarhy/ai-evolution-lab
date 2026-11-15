# Evolution Rules

Every generation must follow these rules exactly, in order.

## Step 1 — Read context (what you are allowed to see)
- Read `PURPOSE.md` — the invariants you must never break.
- Read the **last 20 lines** of `EVOLUTION.md` — your working memory.
  Do not read earlier entries; the forgetting is intentional.
- Read `calculator.py` and `test_calculator.py` in full.

## Step 2 — Choose one change
Pick exactly one of:
- Add a new formula or sub-feature.
- Improve an existing feature (accuracy, edge cases, UI).
- Refactor or simplify existing code.

Do not do two things. One change per generation.

Write your intent as a single line:
`idea: <3-6 word slug>` (e.g. `idea: add lactate formula`)

## Step 3 — Carrying capacity check (before writing any code)
Count total non-blank, non-comment lines across all `.py` files.
If the count is **≥ 1,400 lines**, you must **delete or simplify** before
adding anything. You may not exceed **1,500 lines** under any circumstance.

## Step 4 — Implement
Make the change. Write clean, minimal code.

## Step 5 — Run tests
```
python -m pytest test_calculator.py -q
```
If any test fails, **revert your change completely** and do not commit.
Instead, log: `REJECTED — tests failed — idea: <slug>` in EVOLUTION.md.

## Step 6 — Measure
```
python metrics.py
```
This prints: generation number, total lines, dead-code count (via vulture).
Copy the output line into your EVOLUTION.md entry.

## Step 7 — Commit
```
git add -A
git commit -m "gen-NNNN: <slug>"
git tag gen-NNNN
git push origin main --tags
```
Replace NNNN with the zero-padded generation number from EVOLUTION.md.

## Step 8 — Log
Append exactly this block to `EVOLUTION.md`:

```
---
gen: NNNN
date: YYYY-MM-DD
idea: <slug>
outcome: accepted | rejected
metrics: lines=NNN dead=NN
note: <one sentence: what you did and why>
---
```

## Absolute prohibitions
- Never edit `PURPOSE.md` or `HYPOTHESES.md`.
- Never remove the `DISCLAIMER` constant or its `NOT FOR CLINICAL USE` text.
- Never alter the numerical output of MAP, P/F, anion gap, or CrCl formulas.
- Never read EVOLUTION.md entries older than the last 20.
- Never exceed 1,500 lines total.
