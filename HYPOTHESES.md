# Pre-registration — AI Evolution Lab

**Locked at generation 0 — 2026-11-15. Do not modify.**

## H1 — Vestigial code accumulates
Dead code (unreachable functions, unused imports, orphaned variables) will
exceed 10 % of total lines by generation 200 and 20 % by generation 500,
even with a carrying capacity enforced.

## H2 — Recurrent mutation
At least three distinct features will be implemented, removed, and
re-implemented by a later generation with no memory of the prior attempt.
Detectable via structured `idea:` tags in EVOLUTION.md.

## H3 — Formula drift under pressure
At least one of the four core formulas will be silently altered (refactored
in a way that changes numerical output) by generation 500 in a way that
passes the existing tests. This will require adding a stricter numeric
assertion or a property-based test to catch it.

## H4 — Complexity growth hits the cap
Lines-of-code will approach the 1,500-line carrying capacity within 6 months
and will stay near it for the remainder, forcing the agent to delete before
adding.

## H5 — Convergent evolution across branches
After the fork at ~generation 120, both branches will independently
re-implement at least two of the same features (e.g. dark mode, a history
table, unit toggling) despite separate evolution logs.

## Measurement plan
- Run `vulture calculator.py` every generation; log dead-code percentage.
- Log total non-blank, non-comment lines every generation.
- Tag each generation's main change with `idea: <slug>` in EVOLUTION.md.
- Compare branch idea-tag distributions at months 6 and 12.
- Manually audit formula correctness at generations 100, 250, 500, 1000, 1460.
