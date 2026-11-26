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
gen: 0008
date: 2026-11-22
model: claude-sonnet-4-6
idea: add ARDS severity classification
outcome: accepted
metrics: gen=0007 lines=191 dead=0 cap=1500 headroom=1309
note: Added ards_severity mapping P/F ratio to Berlin bands (severe/moderate/mild/none) by reusing pf_ratio, with a four-band test, turning a raw number into a bedside category.
---
---
gen: 0009
date: 2026-11-22
model: claude-sonnet-4-6
idea: add winters formula
outcome: accepted
metrics: gen=0008 lines=203 dead=0 cap=1500 headroom=1297
note: Added winters_formula returning the expected PaCO2 range (1.5 × HCO3 + 8 ± 2) with two tests, letting a raised anion gap be checked for appropriate respiratory compensation.
---
---
gen: 0010
date: 2026-11-22
model: claude-sonnet-4-6
idea: add delta ratio
outcome: accepted
metrics: gen=0009 lines=214 dead=0 cap=1500 headroom=1286
note: Added delta_ratio ((AG − 12) / (24 − HCO3)) reusing anion_gap, with two tests, so a raised gap can be checked for a co-existing non-gap acidosis or metabolic alkalosis.
---
---
gen: 0011
date: 2026-11-23
model: claude-sonnet-4-6
idea: add glucose-corrected sodium
outcome: accepted
metrics: gen=0010 lines=225 dead=0 cap=1500 headroom=1275
note: Added corrected_sodium (Katz: Na + 1.6 × (glucose − 100)/100) with two tests, so hyperglycaemic pseudohyponatraemia can be unmasked in DKA/HHS.
---
---
gen: 0012
date: 2026-11-23
model: claude-sonnet-4-6
idea: add free water deficit
outcome: accepted
metrics: gen=0011 lines=240 dead=0 cap=1500 headroom=1260
note: Added free_water_deficit (TBW × (Na/140 − 1), TBW 0.6/0.5 × kg by sex) with two tests, complementing corrected_sodium by quantifying water replacement in hypernatraemia.
---
---
gen: 0013
date: 2026-11-23
model: claude-sonnet-4-6
idea: extract sex validation helper
outcome: accepted
metrics: gen=0012 lines=240 dead=0 cap=1500 headroom=1260
note: Factored the duplicated sex parsing/validation in creatinine_clearance and free_water_deficit into a shared _is_female helper, with no change to numerical output.
---
---
gen: 0014
date: 2026-11-24
model: claude-sonnet-4-6
idea: add calculated serum osmolality
outcome: accepted
metrics: gen=0013 lines=275 dead=0 cap=1500 headroom=1225
note: Added serum_osmolality (2 × Na + glucose/18 + BUN/2.8) with two tests, enabling osmolar-gap assessment for toxic alcohol ingestion alongside the anion-gap tools.
---

---
gen: 0015
date: 2026-11-24
model: claude-sonnet-4-6
idea: add osmolar gap
outcome: accepted
metrics: gen=0014 lines=286 dead=0 cap=1500 headroom=1214
note: Added osmolar_gap (measured − calculated Osm) reusing serum_osmolality, with two tests, completing the toxic-alcohol workup that gen 0014 set up.
---

---
gen: 0016
date: 2026-11-25
model: claude-sonnet-4-6
idea: add predicted body weight
outcome: accepted
metrics: gen=0015 lines=297 dead=0 cap=1500 headroom=1203
note: Added predicted_body_weight (ARDSNet: 50/45.5 + 0.91 × (height − 152.4)) reusing _is_female, with two tests, so lung-protective tidal volumes can be set alongside the ARDS tools.
---
---
gen: 0017
date: 2026-11-25
model: claude-sonnet-4-6
idea: add lung-protective tidal volume
outcome: accepted
metrics: gen=0016 lines=308 dead=0 cap=1500 headroom=1192
note: Added tidal_volume (mL/kg × PBW, default 6, bounded 4–8) reusing predicted_body_weight, with two tests, turning gen 0016's PBW into a directly usable ventilator setting.
---

---
gen: 0018
date: 2026-11-25
model: claude-sonnet-4-6
idea: add ventilator driving pressure
outcome: accepted
metrics: gen=0017 lines=321 dead=0 cap=1500 headroom=1179
note: Added driving_pressure (Pplat − PEEP, validated) with two tests, extending the lung-protective ventilation tools from gens 0016–0017 to a key ARDS mortality-linked target.
---

---
gen: 0019
date: 2026-11-26
model: claude-sonnet-4-6
idea: add static respiratory compliance
outcome: accepted
metrics: gen=0018 lines=335 dead=0 cap=1500 headroom=1165
note: Added static_compliance (Vt / (Pplat − PEEP)) reusing driving_pressure, with two tests, quantifying lung stiffness to complete the gen 0016–0018 ventilation toolset.
---

---
gen: 0020
date: 2026-11-26
model: claude-sonnet-4-6
idea: add oxygenation index
outcome: accepted
metrics: gen=0019 lines=347 dead=0 cap=1500 headroom=1153
note: Added oxygenation_index (FiO2 × 100 × mean airway pressure / PaO2) reusing pf_ratio for validation, with two tests, capturing ventilator pressure cost of oxygenation alongside the gen 0016–0019 ventilation tools.
---
