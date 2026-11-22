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

---
gen: 0003
date: 2026-11-17
model: claude-sonnet-4-6
idea: restore calculator newlines
outcome: accepted
metrics: gen=0002 lines=141 dead=0 cap=1500 headroom=1359
note: calculator.py had been committed with literal "\n" sequences instead of newlines, making it a SyntaxError and failing all tests; restored real newlines with no logic change.
---

---
gen: 0004
date: 2026-11-17
model: claude-sonnet-4-6
idea: validate PaO2 in pf_ratio
outcome: accepted
metrics: gen=0003 lines=146 dead=0 cap=1500 headroom=1354
note: Added a positive-PaO2 guard (plus test) to pf_ratio; previously zero or negative PaO2 silently returned a meaningless ratio.
---

---
gen: 0005
date: 2026-11-21
model: claude-sonnet-4-6
idea: validate anion gap inputs
outcome: accepted
metrics: gen=0004 lines=151 dead=0 cap=1500 headroom=1349
note: Added a positive-value guard (plus test) for sodium, chloride, and bicarbonate in anion_gap; previously zero or negative electrolytes silently produced a meaningless gap.
---
---
gen: 0006
date: 2026-11-21
model: claude-sonnet-4-6
idea: add albumin-corrected anion gap
outcome: accepted
metrics: gen=0005 lines=164 dead=0 cap=1500 headroom=1336
note: Added corrected_anion_gap (AG + 2.5 × (4.0 − albumin)) reusing anion_gap, with two tests, since hypoalbuminaemia commonly masks a raised gap in ICU patients.
---
---
gen: 0007
date: 2026-11-22
model: claude-sonnet-4-6
idea: add shock index formula
outcome: accepted
metrics: gen=0006 lines=175 dead=0 cap=1500 headroom=1325
note: Added shock_index (HR / SBP, rounded to 2 dp) with validation and two tests, a quick bedside marker of occult shock that complements MAP.
---
