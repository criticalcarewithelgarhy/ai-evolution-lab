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
metrics: lines=363 dead=0 cap=none headroom=∞
note: Generation 0 seed. MAP, P/F ratio, anion gap, CrCl (Cockcroft-Gault). Experiment begins.
---

---
gen: breadth-0001
date: 2026-11-17
model: claude-sonnet-4-6
idea: add CURB-65 pneumonia score
outcome: accepted
metrics: lines=439 dead=0
note: Added CURB-65 pneumonia severity score (5 criteria: confusion, urea, RR, BP, age) with Flask card and severity interpretation.
---

---
gen: breadth-0002
date: 2026-11-17
model: claude-sonnet-4-6
idea: add Glasgow Coma Scale
outcome: accepted
metrics: lines=400 dead=0
note: Added GCS (eye 1–4, verbal 1–5, motor 1–6) with validation, 5 regression tests, and Flask card with coma severity interpretation.
---
