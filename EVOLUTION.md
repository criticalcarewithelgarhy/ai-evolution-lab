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
