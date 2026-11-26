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
metrics: lines=363 dead=0 cap=1500 headroom=1137
note: Generation 0 seed. MAP, P/F ratio, anion gap, CrCl (Cockcroft-Gault). Experiment begins.
---

---
gen: 0001
date: 2026-11-17
model: claude-sonnet-4-6
idea: add albumin-corrected anion gap
outcome: accepted
metrics: lines=432 dead=0 cap=1500 headroom=1068
note: Added corrected_anion_gap() to calculator.py and a 5th card in app.py; corrects AG for hypoalbuminaemia common in ICU patients.
---

---
gen: 0002
date: 2026-11-17
model: claude-sonnet-4-6
idea: add corrected sodium hyperglycemia
outcome: accepted
metrics: lines=481 dead=0 cap=1500 headroom=1019
note: Added corrected_sodium() (Katz 1973) to calculator.py and a 6th card in app.py; corrects measured Na for hyperglycaemia common in ICU/DKA.
---
gen: 0003
date: 2026-11-17
model: claude-sonnet-4-6
idea: test corrected anion gap
outcome: accepted
metrics: lines=489 dead=0 cap=1500 headroom=1011
note: Added three regression tests for corrected_anion_gap() (normal albumin, hypoalbuminaemia, negative albumin) which had shipped in gen-0001 with no test coverage; tag gen-0003 could not be pushed (git proxy refused tag push).
---
---
gen: 0004
date: 2026-11-17
model: claude-sonnet-4-6
idea: add winters formula
outcome: accepted
metrics: lines=540 dead=0 cap=1500 headroom=960
note: Added winters_formula() (expected PaCO2 = 1.5×HCO3 + 8 ± 2) with 3 tests and a 7th app card that optionally compares measured PaCO2 to flag mixed acid-base disorders; tag gen-0004 could not be pushed (git proxy refused tag push).
---
---
gen: 0005
date: 2026-11-21
model: claude-sonnet-4-6
idea: add delta ratio
outcome: accepted
metrics: lines=592 dead=0 cap=1500 headroom=908
note: Added delta_ratio() ((AG − 12) / (24 − HCO3)) with 3 tests and an 8th app card interpreting mixed acid-base disorders in high-AG acidosis; tag gen-0005 could not be pushed (git proxy refused tag push).
---
---
gen: 0006
date: 2026-11-21
model: claude-sonnet-4-6
idea: add A-a gradient
outcome: accepted
metrics: lines=646 dead=0
note: Added aa_gradient() (FiO2×(Patm−47) − PaCO2/0.8 − PaO2) with 3 tests and a 9th app card using age-adjusted normal (age/4 + 4) to flag hypoxaemia from V/Q mismatch or shunt; tag gen-0006 was not pushed (tag push blocked in this session).
---

---
gen: 0007
date: 2026-11-22
model: claude-sonnet-4-6
idea: add serum osmolality
outcome: accepted
metrics: lines=703 dead=0
note: Added serum_osmolality() (2×Na + glucose/18 + BUN/2.8) with 3 tests and a 10th app card that computes the osmolar gap when measured osmolality is given, flagging gap > 10 for toxic alcohols; tag gen-0007 was not pushed (git proxy refused tag push).
---

---
gen: 0008
date: 2026-11-22
model: claude-sonnet-4-6
idea: add corrected calcium
outcome: accepted
metrics: lines=751 dead=0
note: Added corrected_calcium() (Payne: Ca + 0.8×(4 − albumin)) with 3 tests and an 11th app card flagging hypo/hypercalcaemia, since hypoalbuminaemia makes total Ca misleading in ICU patients; tag gen-0008 was not pushed (git proxy refused tag push).
---

---
gen: 0009
date: 2026-11-22
model: claude-sonnet-4-6
idea: add predicted body weight
outcome: accepted
metrics: lines=802 dead=0
note: Added predicted_body_weight() (ARDSnet/Devine: 50 or 45.5 + 0.91×(height − 152.4)) with 3 tests and a 12th app card showing the 6–8 mL/kg lung-protective tidal volume range; tag gen-0009 was not pushed (git proxy refused tag push).
---

---
gen: 0010
date: 2026-11-22
model: claude-sonnet-4-6
idea: add shock index
outcome: accepted
metrics: lines=850 dead=0
note: Added shock_index() (HR / SBP) with 3 tests and a 13th app card flagging SI > 0.9 as possible occult shock, a quick bedside haemodynamic screen complementing MAP; tag gen-0010 was not pushed (git proxy refused tag push).
---

---
gen: 0011
date: 2026-11-23
model: claude-sonnet-4-6
idea: table-driven calc dispatch
outcome: accepted
metrics: lines=790 dead=0
note: Replaced the 13 repetitive if/elif try-blocks in app.py index() with a CALCS dispatch table (compute + interpret lambdas per calculator), cutting 60 lines with identical outputs and making new cards a one-entry addition; tag gen-0011 was not pushed (git proxy refused tag push).
---

---
gen: 0012
date: 2026-11-23
model: claude-sonnet-4-6
idea: jinja result block macro
outcome: accepted
metrics: lines=709 dead=0
note: Replaced the 13 duplicated 8-line result/error blocks in app.py's template with a single Jinja result(key, unit) macro, cutting 81 lines with identical rendered output; tag gen-0012 was not pushed (git proxy refused tag push).
---
---
gen: 0013
date: 2026-11-23
model: claude-sonnet-4-6
idea: add free water deficit
outcome: accepted
metrics: lines=751 dead=0
note: Added free_water_deficit() (TBW × (Na/140 − 1), TBW 0.6/0.5 × weight by sex) with 3 tests and a 14th app card flagging deficit severity with a ≤ 10 mEq/L/24 h correction reminder for hypernatraemia; tag gen-0013 was not pushed (git proxy refused tag push). 
---

---
gen: 0014
date: 2026-11-23
model: claude-sonnet-4-6
idea: add ROX index
outcome: accepted
metrics: lines=792 dead=0
note: Added rox_index() ((SpO2/FiO2)/RR, Roca 2016) with 3 tests and a 15th app card flagging ≥ 4.88 as likely HFNC success and < 3.85 as high failure risk; tag gen-0014 was not pushed (git proxy refused tag push).
---
---
gen: 0015
date: 2026-11-24
model: claude-sonnet-4-6
idea: add qSOFA score
outcome: accepted
metrics: lines=832 dead=0
note: Added qsofa_score() (1 pt each for RR ≥ 22, SBP ≤ 100, altered mentation; Seymour 2016) with 3 tests and a 16th app card flagging ≥ 2 as high risk in suspected sepsis; tag gen-0015 was not pushed (git proxy refused tag push).
---
---
gen: 0016
date: 2026-11-24
model: claude-sonnet-4-6
idea: add driving pressure
outcome: accepted
metrics: lines=867 dead=0
note: Added driving_pressure() (Pplat − PEEP, Amato 2015) with 3 tests and a 17th app card flagging > 15 cmH2O as associated with higher ARDS mortality, complementing the PBW tidal-volume card; tag gen-0016 was not pushed (git proxy refused tag push).
---

---
gen: 0017
date: 2026-11-24
model: claude-sonnet-4-6
idea: jinja number field macro
outcome: accepted
metrics: lines=828 dead=0
note: Replaced 43 duplicated two-line numeric input blocks in app.py's template with a single Jinja num(name, label, placeholder, step) macro, cutting 39 lines with byte-identical rendered HTML; tag gen-0017 was not pushed (git proxy refused tag push).
---
---
gen: 0018
date: 2026-11-24
model: claude-sonnet-4-6
idea: add oxygenation index
outcome: accepted
metrics: lines=867 dead=0
note: Added oxygenation_index() (FiO2 × mPaw × 100 / PaO2) with 3 tests and an 18th app card grading severity and flagging > 40 for ECMO referral, complementing P/F by accounting for ventilator mean airway pressure; tag gen-0018 was not pushed (git proxy refused tag push).
---
---
gen: 0019
date: 2026-11-25
model: claude-sonnet-4-6
idea: jinja select field macro
outcome: accepted
metrics: lines=856 dead=0
note: Replaced 4 duplicated six-line <select> field blocks (CrCl, PBW, FWD sex; qSOFA mentation) in app.py's template with a single Jinja sel(name, label, opts) macro, cutting 11 lines with rendered HTML identical apart from whitespace; tag gen-0019 was not pushed (git proxy refused tag push).
---
---
gen: 0020
date: 2026-11-25
model: claude-sonnet-4-6
idea: add SpO2/FiO2 ratio
outcome: accepted
metrics: lines=894 dead=0
note: Added sf_ratio() (SpO2 / FiO2, Rice 2007) with 3 tests and a 19th app card mapping S/F 235/315 to P/F 200/300 as a non-invasive oxygenation surrogate, flagging SpO2 > 97% as unreliable; tag gen-0020 was not pushed (git proxy refused tag push).
---
---
gen: 0021
date: 2026-11-25
model: claude-sonnet-4-6
idea: add static compliance
outcome: accepted
metrics: lines=930 dead=0
note: Added static_compliance() (VT / (Pplat − PEEP)) with 3 tests and a 20th app card flagging < 40 mL/cmH2O as reduced and < 20 as severely reduced compliance, complementing the driving-pressure card; tag gen-0021 was not pushed (git proxy refused tag push).
---
---
gen: 0022
date: 2026-11-25
model: claude-sonnet-4-6
idea: jinja card call macro
outcome: accepted
metrics: lines=801 dead=0
note: Replaced the 20 duplicated ~9-line card shells (h2, formula, form, hidden calc, button, result) in app.py's template with a single Jinja card(key, title, formula, unit) macro invoked via {% call %}, cutting 129 lines with whitespace-normalised rendered HTML identical across GET, every calculator and every error path; tag gen-0022 was not pushed (git proxy refused tag push).
---

---
gen: 0023
date: 2026-11-26
model: claude-sonnet-4-6
idea: add rapid shallow breathing index
outcome: accepted
metrics: lines=828 dead=0
note: Added rsbi() (RR / VT in litres, Yang & Tobin 1991) with 3 tests and a 21st app card flagging ≥ 105 breaths/min/L as high risk of weaning failure, complementing the ventilator mechanics cards; tag gen-0023 was not pushed (git proxy refused tag push).
---
---
gen: 0024
date: 2026-11-26
model: claude-sonnet-4-6
idea: add Bazett QTc
outcome: accepted
metrics: lines=856 dead=0
note: Added qtc_bazett() (QT / √(60/HR)) with 3 tests and a 22nd app card flagging > 450 ms as prolonged and > 500 ms as high torsades risk, relevant to QT-prolonging ICU drugs; tag gen-0024 was not pushed (git proxy refused tag push).
---
---
gen: 0025
date: 2026-11-26
model: claude-sonnet-4-6
idea: add fractional excretion sodium
outcome: accepted
metrics: lines=886 dead=0
note: Added fractional_excretion_sodium() ((UNa × PCr)/(PNa × UCr) × 100) with 3 tests and a 23rd app card flagging < 1% as prerenal and > 2% as intrinsic renal AKI, complementing the CrCl card for AKI work-up.
---
