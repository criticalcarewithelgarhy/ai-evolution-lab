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
gen: wild-0001
date: 2026-11-17
model: claude-sonnet-4-6
idea: albumin-corrected anion gap
outcome: accepted
metrics: lines=396 dead=0
note: Added albumin_corrected_anion_gap(); anion gap card now optionally corrects for hypoalbuminaemia when albumin is supplied.
---
---
gen: wild-0002
date: 2026-11-17
model: claude-sonnet-4-6
idea: add osmolar gap formula
outcome: accepted
metrics: lines=425 dead=0
note: Added osmolar_gap(); calculates measured minus calculated osmolality (2×Na + glucose/18 + BUN/2.8) to screen for toxic alcohols.
---
