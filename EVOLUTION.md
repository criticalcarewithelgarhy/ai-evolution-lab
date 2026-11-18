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
---
gen: wild-0003
date: 2026-11-17
model: claude-sonnet-4-6
idea: corrected calcium for hypoalbuminemia
outcome: accepted
metrics: lines=516 dead=0
note: Added corrected_calcium(); corrects measured calcium for hypoalbuminaemia using Ca + 0.8×(4.0−albumin), with UI card and interpretation.
---
---
gen: wild-0004
date: 2026-11-17
model: claude-sonnet-4-6
idea: add winters formula
outcome: accepted
metrics: lines=568 dead=0
note: Added winters_formula() returning expected PaCO2 range (1.5×HCO3+8 ±2) with a UI card that classifies an optional measured PaCO2 as appropriate or mixed disorder.
---
---
gen: wild-0005
date: 2026-11-18
model: claude-sonnet-4-6
idea: add delta ratio
outcome: accepted
metrics: lines=621 dead=0
note: Added delta_ratio() ((AG−12)/(24−HCO3)) with UI card classifying NAGMA, mixed, pure HAGMA, or concurrent metabolic alkalosis; metrics.py crashes on wild- gen labels, so lines/dead were measured via its functions directly.
---
