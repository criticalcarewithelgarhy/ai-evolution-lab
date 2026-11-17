# Evolution Log

This file is the agent's working memory.
Each generation reads only the **last 20 entries** — intentional forgetting.
The full history is preserved in git tags (gen-0000 through gen-NNNN).

---
gen: 0000
date: 2026-11-15
model: claude-sonnet-4-6
idea: seed — four ICU formulas
outcome: accepted
metrics: lines=363 dead=0 cap=800 headroom=437
note: Generation 0 seed. MAP, P/F ratio, anion gap, CrCl (Cockcroft-Gault). Experiment begins.
---

---
gen: robust-0001
date: 2026-11-17
model: claude-sonnet-4-6
idea: guard-map-sbp-gt-dbp
outcome: accepted
metrics: lines=373 dead=0
note: Added ValueError guards to mean_arterial_pressure for non-positive values and systolic ≤ diastolic, preventing physiologically impossible inputs.
---
