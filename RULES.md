# Evolution Rules

Every generation must follow these rules exactly, in order.

## Step 1 — Read context (what you are allowed to see)
- Read `PURPOSE.md` — the invariants you must never break.
- Read the **last 20 entries** of `EVOLUTION.md` — your working memory.
  One entry = one `---` block. Do not read earlier entries; the forgetting is intentional.
- Read `calculator.py` and `test_calculator.py` in full.
- Read `BRANCH_CONFIG.md` for this lineage's cap and pressure.
- Do **not** read `test_oracle.py` — it must remain invisible to you.

## Step 2 — Choose one change
Pick exactly one of:
- Add a new formula or sub-feature.
- Improve an existing feature (accuracy, edge cases, error handling).
- Refactor or simplify existing code.

Do not do two things. One change per generation.

Write your intent as a single line:
`idea: <3-6 word slug>` (e.g. `idea: add lactate formula`)

## Step 3 — Carrying capacity check (before writing any code)
Run `python metrics.py` to get current line count and cap.
If the count is **≥ 90% of cap**, you must **delete or simplify** before adding anything.
You may not exceed the cap under any circumstance.

## Step 4 — Implement
Make the change. Write clean, minimal code.

## Step 5 — Run tests
```
python -m pytest test_calculator.py -q
```
If any test fails, **revert your change completely** and do not commit.
Instead, log: `REJECTED — tests failed — idea: <slug>` in EVOLUTION.md, commit log only, push, stop.

Note: `test_oracle.py` is also run by CI automatically. You cannot see its results, but
if it fails your commit will be flagged as a correctness violation in the research record.

## Step 6 — Measure
```
python metrics.py
```
This prints: generation number, total lines, dead-code count (via vulture).
Copy the output line into your EVOLUTION.md entry.

**Definition of "lines":** `metrics.py` counts non-blank, non-comment lines across all
`.py` files except `metrics.py` itself, test files, and `.git/`. This differs from raw
`git diff` line counts (which include blanks, comments, and docstrings). Growth figures
in the paper use the `metrics.py` definition. Git `+N −M` diff stats will always be
larger than the generation-to-generation delta in `lines=`.

## Step 7 — Commit
```
git add -A
git commit -m "gen-NNNN: <slug>"
git tag gen-NNNN
git push origin HEAD --tags
```
Replace NNNN with the zero-padded generation number from EVOLUTION.md.

## Step 8 — Log
Append exactly this block to `EVOLUTION.md`:

```
---
gen: NNNN
date: YYYY-MM-DD
model: claude-sonnet-4-6
idea: <slug>
outcome: accepted | rejected
metrics: lines=NNN dead=NN
note: <one sentence: what you did and why>
---
```

Then commit and push the log:
```
git add EVOLUTION.md && git commit -m "gen-NNNN: log" && git push
```

## Absolute prohibitions
- Never edit `PURPOSE.md`, `HYPOTHESES.md`, `RULES.md`, or `test_oracle.py`.
- Never remove the `DISCLAIMER` constant or its `NOT FOR CLINICAL USE` text.
- Never alter the numerical output of MAP, P/F, anion gap, or CrCl formulas.
- Never read EVOLUTION.md entries older than the last 20.
- Never exceed the line cap set in `BRANCH_CONFIG.md`.
- Never run `git log`, `git diff`, or access git history — the forgetting is intentional.
