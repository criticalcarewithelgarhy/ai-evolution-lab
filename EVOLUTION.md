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
