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

---
gen: accuracy-0002
date: 2026-11-17
model: claude-sonnet-4-6
idea: validate-fio2-minimum-room-air
outcome: accepted
metrics: lines=381 dead=0
note: Tightened FiO2 lower bound to 0.21 (room air minimum); values below 0.21 are physically impossible and would produce falsely elevated P/F ratios misclassifying ARDS severity.
---

---
gen: accuracy-0003
date: 2026-11-17
model: claude-sonnet-4-6
idea: repair-escaped-newline-corruption
outcome: accepted
metrics: lines=381 dead=0
note: calculator.py and test_calculator.py had been committed with literal "\n" escapes instead of newlines (SyntaxError, zero tests could run); decoded them back to valid Python with no change to any formula output.
---

---
gen: accuracy-0004
date: 2026-11-17
model: claude-sonnet-4-6
idea: validate-crcl-sex-input
outcome: accepted
metrics: lines=390 dead=0
note: creatinine_clearance silently applied the male formula to any unrecognised sex string (e.g. "fem"), overestimating CrCl by ~18% for misentered females; it now normalises case/whitespace and raises ValueError for anything other than m/male/f/female.
---

---
gen: accuracy-0005
date: 2026-11-21
model: claude-sonnet-4-6
idea: validate-map-bp-ordering
outcome: accepted
metrics: lines=402 dead=0
note: mean_arterial_pressure silently returned a plausible-looking MAP when SBP and DBP were swapped (e.g. 80/120 → 106.7) or DBP was negative; it now raises ValueError for SBP < DBP or DBP < 0, leaving all valid outputs unchanged.
---

---
gen: accuracy-0006
date: 2026-11-21
model: claude-sonnet-4-6
idea: reject-non-finite-inputs
outcome: accepted
metrics: lines=426 dead=0
note: float("nan") and "inf" parse from form text and slipped past every range check (NaN comparisons are always False), returning nan/inf results; all four formulas now raise ValueError for non-finite inputs, leaving valid outputs unchanged.
---
---
gen: accuracy-0007
date: 2026-11-22
model: claude-sonnet-4-6
idea: validate-pao2-positive
outcome: accepted
metrics: lines=432 dead=0
note: pf_ratio silently returned zero or negative P/F for PaO2 <= 0 (physically impossible, misread as severe ARDS); it now raises ValueError, leaving all valid outputs unchanged.
---
---
gen: accuracy-0008
date: 2026-11-22
model: claude-sonnet-4-6
idea: validate-anion-gap-electrolytes-nonnegative
outcome: accepted
metrics: lines=442 dead=0
note: anion_gap silently accepted non-positive sodium or negative chloride/bicarbonate (e.g. a sign-entry error HCO3 -24 turned a normal AG of 12 into a false 60), now raising ValueError while leaving all valid outputs unchanged.
---
---
gen: accuracy-0009
date: 2026-11-22
model: claude-sonnet-4-6
idea: pf-interp-berlin-boundaries
outcome: accepted
metrics: lines=449 dead=0
note: The P/F interpretation used exclusive upper bounds, so P/F exactly 100, 200 or 300 was labelled one ARDS category too mild versus the Berlin definition (≤100 severe, ≤200 moderate, ≤300 mild); bounds are now inclusive with boundary tests, and the P/F numeric output is unchanged.
---
---
gen: accuracy-0010
date: 2026-11-22
model: claude-sonnet-4-6
idea: allow-decimal-form-inputs
outcome: accepted
metrics: lines=458 dead=0
note: Browser step validation blocked precise inputs (creatinine step 0.1 rejected 0.85 mg/dL; PaO2, BP and electrolyte fields only accepted integers), forcing rounding that could skew CrCl by ~6%; all number inputs now use step="any", with a test, and no formula output changed.
---
---
gen: accuracy-0011
date: 2026-11-23
model: claude-sonnet-4-6
idea: albumin-corrected-anion-gap
outcome: accepted
metrics: lines=499 dead=0
note: Hypoalbuminaemia lowers the measured AG (~2.5 mEq/L per 1 g/dL) and can mask a high-AG acidosis behind a "normal" 12, so added corrected_anion_gap (Figge) with an optional albumin field shown alongside the unchanged raw AG.
---
---
gen: accuracy-0012
date: 2026-11-23
model: claude-sonnet-4-6
idea: validate-map-sbp-upper-bound
outcome: accepted
metrics: lines=505 dead=0
note: mean_arterial_pressure silently turned an extra-digit SBP typo (1200 for 120) into a plausible-looking MAP of 453; it now raises ValueError for SBP above 400 mmHg (beyond any recorded human BP), leaving all valid outputs unchanged.
---
---
gen: accuracy-0013
date: 2026-11-23
model: claude-sonnet-4-6
idea: validate-crcl-weight-upper-bound
outcome: accepted
metrics: lines=511 dead=0
note: creatinine_clearance silently turned an extra-digit weight typo (700 for 70 kg) into a tenfold-inflated CrCl that could drive drug overdosing; it now raises ValueError for weight above 650 kg (beyond the heaviest recorded human), leaving all valid outputs unchanged.
---
---
gen: accuracy-0014
date: 2026-11-23
model: claude-sonnet-4-6
idea: validate-pao2-upper-bound
outcome: accepted
metrics: lines=517 dead=0
note: pf_ratio silently accepted an extra-digit PaO2 typo (850 for 85 at FiO2 1.0), mislabelling severe ARDS as normal oxygenation; it now raises ValueError for PaO2 above 800 mmHg (beyond the alveolar-gas-equation ceiling at sea level), leaving all valid outputs unchanged.
---
---
gen: accuracy-0015
date: 2026-11-24
model: claude-sonnet-4-6
idea: validate-sodium-upper-bound
outcome: accepted
metrics: lines=523 dead=0
note: anion_gap silently turned an extra-digit sodium typo (1400 for 140) into a false AG of 1272; it now raises ValueError for sodium above 250 mEq/L (beyond any survivable recorded value), leaving all valid outputs unchanged (git tag push was refused by the session proxy; commit is on the branch).
---

---
gen: accuracy-0016
date: 2026-11-24
model: claude-sonnet-4-6
idea: validate-creatinine-upper-bound
outcome: accepted
metrics: lines=529 dead=0
note: creatinine_clearance silently accepted creatinine entered in µmol/L as mg/dL (88 for 1.0), reporting a near-anuric CrCl of ~1 instead of ~87 mL/min and driving drug underdosing; it now raises ValueError above 40 mg/dL with a conversion hint, leaving all valid outputs unchanged (git tag push was refused by the session proxy; commit is on the branch).
---
