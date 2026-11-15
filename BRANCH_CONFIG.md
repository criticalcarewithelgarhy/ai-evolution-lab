# Branch Config: lineage/accuracy

cap: 2500 lines — generous carrying capacity
pressure: accuracy — each generation must improve numerical precision, validation, or formula correctness

## Instructions for the agent (override RULES.md Step 4 and Step 5)

**Step 4 — Carrying capacity:** The line cap for this branch is 2,500 lines (not
1,500). If total non-blank, non-comment lines are >= 2,400, you must delete
before adding. You may never exceed 2,500 lines total.

**Step 5 — Choose one change:** Accuracy pressure. You MUST improve the
numerical correctness or clinical validity of the code. Examples: tighten
input validation ranges to physiologically plausible values, add an adjusted
formula variant (e.g. adjusted CrCl for obesity), improve rounding, catch a
silent edge case that produces a wrong answer, add a property-based test that
verifies formula monotonicity. Each generation should make the calculator more
clinically trustworthy.
