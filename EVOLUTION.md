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
metrics: lines=363 dead=0 cap=2500 headroom=2137
note: Generation 0 seed. MAP, P/F ratio, anion gap, CrCl (Cockcroft-Gault). Experiment begins.
---

---
gen: accuracy-0001
date: 2026-11-17
model: claude-sonnet-4-6
idea: validate-crcl-age-weight-ranges
outcome: accepted
metrics: lines=376 dead=0 cap=2500 headroom=2124
note: Added age (1–120 years) and weight (> 0 kg) validation to creatinine_clearance to prevent silent negative/zero CrCl for physiologically impossible inputs.
---
