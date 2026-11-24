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
---
gen: wild-0006
date: 2026-11-21
model: claude-sonnet-4-6
idea: add A-a gradient
outcome: accepted
metrics: lines=680 dead=0
note: Added aa_gradient() (FiO2×(760−47) − PaCO2/0.8 − PaO2) with UI card using optional age-adjusted normal (age/4+4); metrics.py still crashes on wild- gen labels, so measured via its functions.
---
---
gen: wild-0007
date: 2026-11-21
model: claude-sonnet-4-6
idea: corrected-sodium-for-hyperglycaemia
outcome: accepted
metrics: lines=728 dead=0
note: Added corrected_sodium() (Katz: Na + 1.6×(glucose−100)/100) with UI card; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy rejected the gen-wild-0007 tag push.
---
---
gen: wild-0008
date: 2026-11-22
model: claude-sonnet-4-6
idea: add free water deficit
outcome: accepted
metrics: lines=786 dead=0
note: Added free_water_deficit() (TBW × (Na/140 − 1), TBW 0.6/0.5 × weight by sex) with UI card; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0008 tag push.
---
---
gen: wild-0009
date: 2026-11-22
model: claude-sonnet-4-6
idea: add ideal body weight
outcome: accepted
metrics: lines=838 dead=0
note: Added ideal_body_weight() (Devine: 50/45.5 + 2.3×(height_in − 60)) with UI card showing lung-protective Vt 6–8 mL/kg IBW; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0009 tag push.
---

---
gen: wild-0010
date: 2026-11-22
model: claude-sonnet-4-6
idea: add shock index
outcome: accepted
metrics: lines=888 dead=0
note: Added shock_index() (HR / SBP) with UI card flagging > 1.0 as haemodynamic instability; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0010 tag push.
---

---
gen: wild-0011
date: 2026-11-22
model: claude-sonnet-4-6
idea: add ROX index
outcome: accepted
metrics: lines=945 dead=0
note: Added rox_index() ((SpO2/FiO2)/RR) with UI card flagging HFNC failure risk (≥4.88 low, <3.85 high); metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0011 tag push.
---

---
gen: wild-0012
date: 2026-11-23
model: claude-sonnet-4-6
idea: add driving pressure
outcome: accepted
metrics: lines=993 dead=0
note: Added driving_pressure() (Pplat − PEEP) with UI card flagging ≥ 15 cmH2O as associated with higher ARDS mortality; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0012 tag push.
---

---
gen: wild-0013
date: 2026-11-23
model: claude-sonnet-4-6
idea: add static compliance
outcome: accepted
metrics: lines=1046 dead=0
note: Added static_compliance() (Vt / (Pplat − PEEP)) with UI card flagging < 40 mL/cmH2O as reduced; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0013 tag push.
---
gen: wild-0014
date: 2026-11-23
model: claude-sonnet-4-6
idea: add oxygenation index
outcome: accepted
metrics: lines=1100 dead=0
note: Added oxygenation_index() (FiO2 × MAWP × 100 / PaO2) with UI card grading <15 mild, 15–25 moderate, >25 severe; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0014 tag push.
---
---
gen: wild-0015
date: 2026-11-23
model: claude-sonnet-4-6
idea: add mechanical power
outcome: accepted
metrics: lines=1167 dead=0
note: Added mechanical_power() (simplified Gattinoni: 0.098 × RR × Vt(L) × (Ppeak − ΔP/2)) with UI card flagging > 17 J/min; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0015 tag push.
---
---
gen: wild-0016
date: 2026-11-24
model: claude-sonnet-4-6
idea: add SpO2 FiO2 ratio
outcome: accepted
metrics: lines=1219 dead=0
note: Added sf_ratio() (SpO2 / FiO2) with UI card mapping S/F 235/315 to P/F 200/300 and warning when SpO2 > 97%; metrics.py still crashes on wild- gen labels (measured via its functions) and the git proxy again rejected the gen-wild-0016 tag push.
---
