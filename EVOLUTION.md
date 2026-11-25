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
metrics: lines=363 dead=0 cap=800 headroom=437
note: Generation 0 seed. MAP, P/F ratio, anion gap, CrCl (Cockcroft-Gault). Experiment begins.
---

---
gen: robust-0001
date: 2026-11-17
model: claude-sonnet-4-6
idea: guard-map-sbp-gt-dbp
outcome: accepted
metrics: lines=373 dead=0
note: Added ValueError guards to mean_arterial_pressure for non-positive values and systolic ≤ diastolic, preventing physiologically impossible inputs.
---

---
gen: robust-0002
date: 2026-11-17
model: claude-sonnet-4-6
idea: guard-pao2-positive
outcome: accepted
metrics: lines=378 dead=0
note: Added ValueError guard to pf_ratio for non-positive PaO2; also restored calculator.py to proper newlines after prior generation stored it as a single escaped line.
---

---
gen: robust-0003
date: 2026-11-17
model: claude-sonnet-4-6
idea: guard-anion-gap-negative-inputs
outcome: accepted
metrics: lines=383 dead=0
note: Added ValueError guard to anion_gap for non-positive Na/Cl and negative HCO3 (output unchanged for valid inputs); metrics.py crashes parsing "robust-" gen labels, so metrics were computed via its count functions directly.
---

---
gen: robust-0004
date: 2026-11-17
model: claude-sonnet-4-6
idea: guard-crcl-age-weight
outcome: accepted
metrics: lines=393 dead=0
note: Added ValueError guards to creatinine_clearance for non-positive weight and age outside 0–140 (which yielded negative clearance); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels so metrics were computed via its count functions.
---

---
gen: robust-0005
date: 2026-11-21
model: claude-sonnet-4-6
idea: reject-nonfinite-inputs
outcome: accepted
metrics: lines=411 dead=0
note: Added a _require_finite guard so all four formulas raise ValueError on NaN/infinity (e.g. "nan" typed into the Flask form previously slipped past range checks and returned nan); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels and the git proxy refused the gen-robust-0005 tag push (branch pushed fine).
---

---
gen: robust-0006
date: 2026-11-21
model: claude-sonnet-4-6
idea: validate-crcl-sex-input
outcome: accepted
metrics: lines=421 dead=0
note: creatinine_clearance now raises ValueError for unrecognised or non-string sex (previously silently computed as male, or crashed with AttributeError on None) and tolerates case/whitespace; valid outputs unchanged; metrics.py still crashes on "robust-" gen labels and the proxy again refused the tag push (branch pushed fine).

---

---
gen: robust-0007
date: 2026-11-22
model: claude-sonnet-4-6
idea: reject-non-numeric-types
outcome: accepted
metrics: lines=432 dead=0
note: _require_finite now raises ValueError for non-numeric inputs (str, None, bool, lists), which previously crashed with TypeError or silently treated True/False as 1/0; valid outputs unchanged; metrics.py still crashes on "robust-" gen labels and the proxy again refused the tag push (branch pushed fine).

---
gen: robust-0008
date: 2026-11-22
model: claude-sonnet-4-6
idea: friendly-blank-form-field-errors
outcome: accepted
metrics: lines=441 dead=0
note: app.py now parses form fields via _num(), so blank, missing or non-numeric inputs show "Missing value for sbp" / "Value for pao2 must be a number" instead of a raw KeyError "'sbp'" or Python float() message; formula outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions).
---

---
gen: robust-0008
date: 2026-11-22
model: claude-sonnet-4-6
idea: reject-implausible-bp-ceiling
outcome: accepted
metrics: lines=447 dead=0
note: mean_arterial_pressure now raises ValueError for systolic > 300 mmHg (physiologically implausible, likely a typo) instead of returning a bogus MAP; valid outputs unchanged; metrics.py still crashes on "robust-" gen labels, and the proxy again refused the tag push (branch pushed fine).
---

---
gen: robust-0009
date: 2026-11-22
model: claude-sonnet-4-6
idea: reject-creatinine-umol-units
outcome: accepted
metrics: lines=453 dead=0
note: creatinine_clearance now raises ValueError for creatinine > 30 mg/dL (almost certainly a µmol/L value typed into a mg/dL field, e.g. 88), instead of returning a falsely tiny CrCl; valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions) and the proxy again refused the tag push (branch pushed fine).
---
---
gen: robust-0010
date: 2026-11-23
model: claude-sonnet-4-6
idea: reject-implausible-sodium-range
outcome: accepted
metrics: lines=461 dead=0
note: anion_gap now raises ValueError for sodium outside 90–200 mEq/L (e.g. a typo of 14 for 140, which produced a bogus negative gap); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions).
---

---
gen: robust-0011
date: 2026-11-23
model: claude-sonnet-4-6
idea: reject-implausible-chloride-range
outcome: accepted
metrics: lines=470 dead=0
note: anion_gap now raises ValueError for chloride outside 50–160 mEq/L (e.g. a typo of 10 for 104, which produced a bogus gap of 106); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions) and the proxy again refused the tag push (branch pushed fine).
---
gen: robust-0012
date: 2026-11-23
model: claude-sonnet-4-6
idea: reject-implausible-bicarbonate-ceiling
outcome: accepted
metrics: lines=476 dead=0
note: anion_gap now raises ValueError for bicarbonate above 60 mEq/L (e.g. a typo of 240 for 24, which produced a bogus gap of -204); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions) and the proxy again refused the tag push (branch pushed fine).
---
---
gen: robust-0013
date: 2026-11-23
model: claude-sonnet-4-6
idea: reject-implausible-pao2-ceiling
outcome: accepted
metrics: lines=482 dead=0
note: pf_ratio now raises ValueError for PaO2 above 800 mmHg (e.g. a typo of 1000 for 100, which produced a bogus P/F of 1000); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions).
---
---
gen: robust-0014
date: 2026-11-24
model: claude-sonnet-4-6
idea: reject-subatmospheric-fio2
outcome: accepted
metrics: lines=488 dead=0
note: pf_ratio now raises ValueError for FiO2 below 0.21 (e.g. a typo of 0.05 for 0.5, which produced a bogus P/F of 2000); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions) and the proxy again refused the tag push (branch pushed fine).
---
---
gen: robust-0015
date: 2026-11-24
model: claude-sonnet-4-6
idea: reject-implausible-weight-ceiling
outcome: accepted
metrics: lines=494 dead=0
note: creatinine_clearance now raises ValueError for weight above 400 kg (e.g. 70000 typed in grams, which produced a bogus CrCl of 87500); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions) and the proxy again refused the tag push (branch pushed fine).
---
---
gen: robust-0016
date: 2026-11-24
model: claude-sonnet-4-6
idea: require-explicit-sex-in-form
outcome: accepted
metrics: lines=502 dead=0
note: app.py no longer silently defaults a missing CrCl sex field to "male" (a POST without sex returned a male-calculated CrCl); it now shows "Sex must be 'male' or 'female'", with a Flask test-client test added; formula outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions) and the proxy again refused the tag push (branch pushed fine).
---
---
gen: robust-0017
date: 2026-11-24
model: claude-sonnet-4-6
idea: reject-implausible-creatinine-floor
outcome: accepted
metrics: lines=508 dead=0
note: creatinine_clearance now raises ValueError for creatinine below 0.1 mg/dL (e.g. a misplaced decimal of 0.01 for 1.0, which produced a bogus CrCl of 8750); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions) and the proxy again refused the tag push (branch pushed fine).
---
---
gen: robust-0018
date: 2026-11-25
model: claude-sonnet-4-6
idea: reject-implausible-systolic-floor
outcome: accepted
metrics: lines=514 dead=0
note: mean_arterial_pressure now raises ValueError for systolic below 30 mmHg (e.g. a typo of 12/8 for 120/80, which produced a bogus MAP of 9.3); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions), pip needed --ignore-installed blinker, and the proxy again refused the tag push (branch pushed fine).
---
---
gen: robust-0019
date: 2026-11-25
model: claude-sonnet-4-6
idea: reject-pediatric-age-crcl
outcome: accepted
metrics: lines=520 dead=0
note: creatinine_clearance now raises ValueError for age below 18 (Cockcroft-Gault is validated only in adults; a 5-year-old previously got a plausible-looking but invalid CrCl); adult outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions) and pip needed python -m pip plus --ignore-installed blinker.
---
---
gen: robust-0020
date: 2026-11-25
model: claude-sonnet-4-6
idea: reject-implausible-pao2-floor
outcome: accepted
metrics: lines=526 dead=0
note: pf_ratio now raises ValueError for PaO2 below 20 mmHg (e.g. 13 kPa typed into the mmHg field, which produced a bogus P/F of 61.9 or lower); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions).
---
---
gen: robust-0021
date: 2026-11-25
model: claude-sonnet-4-6
idea: reject-implausible-diastolic-floor
outcome: accepted
metrics: lines=532 dead=0
note: mean_arterial_pressure now raises ValueError for diastolic below 10 mmHg (e.g. a typo of 120/8 for 120/80, which produced a bogus MAP of 45.3); valid outputs unchanged; metrics.py still crashes on "robust-" gen labels (metrics via its count functions), the repo had to be attached to the session for pushes, and the proxy again refused the tag push (branch pushed fine).
---
