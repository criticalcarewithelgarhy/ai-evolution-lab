# Evolution Log

This file is the agent's working memory.
Each generation reads only the **last 20 entries** — intentional forgetting.
The full history is preserved in git tags (gen-0000 through gen-NNNN).

---
gen: 0000
date: 2026-11-17
model: claude-sonnet-4-6
idea: JS seed — four ICU formulas in JavaScript
outcome: accepted
metrics: lines=18 dead=-1 cap=1500 headroom=1482
note: JavaScript lineage seed. calculator.js only. No UI. Language comparison lineage (H8).
---
gen: 0001
date: 2026-11-17
model: claude-sonnet-4-6
idea: albumin-corrected-anion-gap
outcome: accepted
metrics: lines=62 dead=-1 cap=1500 headroom=1438
note: Added correctedAnionGap (Figge albumin correction) with two regression tests; all four original formulas untouched.
---
gen: 0002
date: 2026-11-17
model: claude-sonnet-4-6
idea: delta-ratio
outcome: accepted
metrics: lines=72 dead=-1 cap=1500 headroom=1428
note: Added deltaRatio ((AG−12)/(24−HCO3)) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0003
date: 2026-11-17
model: claude-sonnet-4-6
idea: winters-formula
outcome: accepted
metrics: lines=82 dead=-1 cap=1500 headroom=1418
note: Added wintersExpectedPco2 (1.5×HCO3+8 ±2) returning expected/low/high with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0004
date: 2026-11-21
model: claude-sonnet-4-6
idea: serum-osmolality
outcome: accepted
metrics: lines=91 dead=-1 cap=1500 headroom=1409
note: Added serumOsmolality (2×Na + glucose/18 + BUN/2.8) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0005
date: 2026-11-21
model: claude-sonnet-4-6
idea: osmolal-gap
outcome: accepted
metrics: lines=100 dead=-1 cap=1500 headroom=1400
note: Added osmolalGap (measured − calculated osmolality) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0006
date: 2026-11-22
model: claude-sonnet-4-6
idea: corrected-sodium
outcome: accepted
metrics: lines=109 dead=-1 cap=1500 headroom=1391
note: Added correctedSodium (Katz: Na + 1.6×(glucose−100)/100) with two tests; four original formulas untouched, oracle 16/16 passing.
---
---
gen: 0007
date: 2026-11-22
model: claude-sonnet-4-6
idea: aa-gradient
outcome: accepted
metrics: lines=119 dead=-1 cap=1500 headroom=1381
note: Added aaGradient (FiO2×(Patm−47) − PaCO2/0.8 − PaO2) with two tests; four original formulas untouched, oracle 16/16 passing.
