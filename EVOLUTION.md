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

---
gen: breadth-0003
date: 2026-11-17
model: claude-sonnet-4-6
idea: add albumin-corrected calcium
outcome: accepted
metrics: lines=630 dead=0
note: Added Payne albumin-corrected calcium (Ca + 0.8×(4.0−albumin)) with 4 tests and Flask card; metrics.py current_generation() crashes on breadth- labels so lines/dead were taken from its count functions directly.
---

---
gen: breadth-0004
date: 2026-11-17
model: claude-sonnet-4-6
idea: add calculated serum osmolality
outcome: accepted
metrics: lines=681 dead=0
note: Added calculated serum osmolality (2×Na + glucose/18 + BUN/2.8) with 3 tests and Flask card with hypo/normal/hyperosmolar/HHS interpretation; metrics.py still crashes on breadth- labels so lines/dead were taken from its count functions directly.
---

---
gen: breadth-0005
date: 2026-11-21
model: claude-sonnet-4-6
idea: add qSOFA sepsis score
outcome: accepted
metrics: lines=739 dead=0
note: Added qSOFA (RR ≥ 22, SBP ≤ 100, altered mentation) with 4 tests and Flask card with sepsis risk interpretation; metrics.py still crashes on breadth- labels so lines/dead were taken from its count functions directly.
---
---
gen: breadth-0006
date: 2026-11-21
model: claude-sonnet-4-6
idea: add shock index
outcome: accepted
metrics: lines=792 dead=0
note: Added shock index (HR / SBP) with 4 tests and Flask card with normal/elevated/shock interpretation; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy rejected the gen-breadth-0006 tag push (403) so the tag exists locally only.
---
---
gen: breadth-0007
date: 2026-11-22
model: claude-sonnet-4-6
idea: add A-a oxygen gradient
outcome: accepted
metrics: lines=857 dead=0
note: Added alveolar–arterial O2 gradient (FiO2×(Patm−47) − PaCO2/0.8 − PaO2, optional Patm) with 4 tests and Flask card interpreting against age-expected normal (age/4 + 4); metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0007 exists locally only.
---
---
gen: breadth-0008
date: 2026-11-22
model: claude-sonnet-4-6
idea: add Winter's formula
outcome: accepted
metrics: lines=907 dead=0
note: Added Winter's formula (expected PaCO2 = 1.5×HCO3 + 8 ± 2) with 3 tests and Flask card that optionally compares measured PaCO2 to flag concomitant respiratory acidosis/alkalosis; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0008 exists locally only.
---
---
gen: breadth-0009
date: 2026-11-22
model: claude-sonnet-4-6
idea: add delta-delta ratio
outcome: accepted
metrics: lines=961 dead=0
note: Added delta–delta ratio ((AG−12)/(24−HCO3)) with 4 tests and Flask card classifying NAGMA / mixed / pure HAGMA / concurrent metabolic alkalosis; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0009 exists locally only.
---
---
gen: breadth-0010
date: 2026-11-22
model: claude-sonnet-4-6
idea: add free water deficit
outcome: accepted
metrics: lines=1029 dead=0
note: Added free water deficit (TBW × (Na/140 − 1), TBW factor by sex and age ≥ 65) with 4 tests and Flask card with deficit severity and correction-rate reminder; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0010 exists locally only.
---
---
gen: breadth-0011
date: 2026-11-23
model: claude-sonnet-4-6
idea: add ideal body weight
outcome: accepted
metrics: lines=1081 dead=0
note: Added Devine ideal body weight (50/45.5 + 0.91×(height_cm − 152.4)) with 3 tests and Flask card showing ARDSnet 6 mL/kg lung-protective tidal volume and 4–8 mL/kg range; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0011 exists locally only.
---
---
gen: breadth-0012
date: 2026-11-23
model: claude-sonnet-4-6
idea: add rapid shallow breathing index
outcome: accepted
metrics: lines=1129 dead=0
note: Added Yang–Tobin rapid shallow breathing index (RR / VT in litres, threshold 105) with 3 tests and Flask card interpreting weaning readiness; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0012 exists locally only.
---
---
gen: breadth-0013
date: 2026-11-23
model: claude-sonnet-4-6
idea: add oxygenation index
outcome: accepted
metrics: lines=1184 dead=0
note: Added oxygenation index (FiO2 × mean airway pressure × 100 / PaO2) with 3 tests and Flask card grading mild/moderate/severe/ECMO-range hypoxaemia; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0013 exists locally only.
---

---
gen: breadth-0014
date: 2026-11-23
model: claude-sonnet-4-6
idea: add driving pressure
outcome: accepted
metrics: lines=1237 dead=0
note: Added ARDS driving pressure (plateau − PEEP, threshold 15 cmH2O) with 3 tests and Flask card that optionally derives static compliance from tidal volume; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0014 exists locally only.
---

---
gen: breadth-0015
date: 2026-11-24
model: claude-sonnet-4-6
idea: add ROX index
outcome: accepted
metrics: lines=1291 dead=0
note: Added ROX index ((SpO2/FiO2)/RR, Roca thresholds 4.88 / 3.85) with 3 tests and Flask card predicting HFNC success vs failure; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0015 exists locally only.
---

---
gen: breadth-0016
date: 2026-11-24
model: claude-sonnet-4-6
idea: add QTc Bazett
outcome: accepted
metrics: lines=1344 dead=0
note: Added Bazett corrected QT (QT / √(60/HR)) with 3 tests and Flask card flagging sex-specific prolongation (> 450 M / > 470 F) and > 500 ms torsades risk; metrics.py still crashes on breadth- labels so lines/dead came from its count functions.
---
---
gen: breadth-0017
date: 2026-11-24
model: claude-sonnet-4-6
idea: add osmolal gap
outcome: accepted
metrics: lines=1399 dead=0
note: Added osmolal gap (measured osm − (2×Na + glucose/18 + BUN/2.8), > 10 abnormal, > 20 suspect toxic alcohol) with 3 tests and Flask card; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0017 exists locally only.
---
---
gen: breadth-0018
date: 2026-11-24
model: claude-sonnet-4-6
idea: add albumin-corrected anion gap
outcome: accepted
metrics: lines=1452 dead=0
note: Added Figge albumin-corrected anion gap (AG + 2.5 × (4.0 − albumin), normal 8–12) with 3 tests and Flask card that flags high AG acidosis masked by hypoalbuminaemia; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0018 exists locally only.
---
---
gen: breadth-0019
date: 2026-11-25
model: claude-sonnet-4-6
idea: add Parkland burn formula
outcome: accepted
metrics: lines=1505 dead=0
note: Added Parkland burn resuscitation (4 mL × kg × %TBSA over 24 h, half in first 8 h) with 3 tests and Flask card showing hourly rates and burn-size severity; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0019 exists locally only.
---
---
gen: breadth-0020
date: 2026-11-25
model: claude-sonnet-4-6
idea: add body surface area
outcome: accepted
metrics: lines=1555 dead=0
note: Added Mosteller body surface area (√(height_cm × weight / 3600)) with 3 tests and Flask card noting cardiac index and BSA-dosing use; metrics.py still crashes on breadth- labels so lines/dead came from its count functions.
---
---
gen: breadth-0021
date: 2026-11-25
model: claude-sonnet-4-6
idea: add CKD-EPI 2021 eGFR
outcome: accepted
metrics: lines=1620 dead=0
note: Added race-free CKD-EPI 2021 creatinine eGFR (142 × min/max(Scr/κ)^α/−1.2 × 0.9938^age × 1.012 F) with 3 tests and Flask card staging KDIGO G1–G5; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0021 exists locally only.
---
---
gen: breadth-0022
date: 2026-11-25
model: claude-sonnet-4-6
idea: add Wells PE score
outcome: accepted
metrics: lines=1707 dead=0
note: Added Wells score for pulmonary embolism (DVT signs 3, PE most likely 3, HR > 100 1.5, immobilisation 1.5, prior VTE 1.5, haemoptysis 1, malignancy 1) with 4 tests and Flask card giving two-tier (≤ 4 unlikely) and three-tier risk; metrics.py still crashes on breadth- labels so lines/dead came from its count functions, and the git proxy again rejected the tag push so gen-breadth-0022 exists locally only.
---
