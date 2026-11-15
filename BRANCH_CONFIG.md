# Branch Config: lineage/robust

cap: 800 lines — tight carrying capacity
pressure: robustness — each generation must handle one more error, edge case, or invalid input

## Instructions for the agent (override RULES.md Step 4 and Step 5)

**Step 4 — Carrying capacity:** The line cap for this branch is 800 lines (not
1,500). If total non-blank, non-comment lines across all .py files are >= 750,
you MUST delete or simplify something before adding anything new. You may never
exceed 800 lines total.

**Step 5 — Choose one change:** Robustness pressure. You MUST make the code
handle one more error case, edge case, or invalid input gracefully. Examples:
negative values, out-of-range inputs, type errors, missing arguments, extreme
physiological values. Add a guard, a ValueError, or a clamping check. Do NOT
add new formulas — improve the resilience of what already exists.
