# Evolution Log

This file is the agent's working memory.
Each generation reads only the **last 20 entries** — intentional forgetting.
The full history is preserved in git tags (gen-0000 through gen-NNNN).

---
gen: 0000
date: 2026-11-16
model: claude-sonnet-4-6
idea: headless seed — four ICU formulas, no UI
outcome: accepted
metrics: lines=130 dead=0 cap=1500 headroom=1370
note: Headless lineage seed. calculator.py + tests only. No web server. UI emergence is the observable (H7).
---

---
gen: 0001
date: 2026-11-17
model: claude-sonnet-4-6
idea: validate creatinine clearance inputs
outcome: accepted
metrics: lines=137 dead=0 cap=1500 headroom=1363
note: Added validation for age, weight, and sex parameters in creatinine_clearance; previously invalid sex silently applied the male formula.
---

---
gen: 0002
date: 2026-11-17
model: claude-sonnet-4-6
idea: validate MAP inputs
outcome: accepted
metrics: lines=141 dead=0 cap=1500 headroom=1359
note: Added positive-value and systolic>=diastolic guards to mean_arterial_pressure; previously invalid pressures silently produced nonsensical results.
---
