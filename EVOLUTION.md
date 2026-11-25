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
---
gen: 0008
date: 2026-11-22
model: claude-sonnet-4-6
idea: shock-index
outcome: accepted
metrics: lines=129 dead=-1 cap=1500 headroom=1371
note: Added shockIndex (HR/SBP, rounded to 2 dp) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0009
date: 2026-11-23
model: claude-sonnet-4-6
idea: corrected-calcium
outcome: accepted
metrics: lines=138 dead=-1 cap=1500 headroom=1362
note: Added correctedCalcium (Payne: Ca + 0.8×(4.0−albumin)) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0010
date: 2026-11-23
model: claude-sonnet-4-6
idea: free-water-deficit
outcome: accepted
metrics: lines=149 dead=-1 cap=1500 headroom=1351
note: Added freeWaterDeficit (TBW × (Na/140 − 1), TBW 0.6/0.5 × weight by sex) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0011
date: 2026-11-23
model: claude-sonnet-4-6
idea: rox-index
outcome: accepted
metrics: lines=160 dead=-1 cap=1500 headroom=1340
note: Added roxIndex ((SpO2/FiO2)/RR, rounded to 2 dp) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0012
date: 2026-11-24
model: claude-sonnet-4-6
idea: oxygenation-index
outcome: accepted
metrics: lines=171 dead=-1 cap=1500 headroom=1329
note: Added oxygenationIndex ((FiO2×100×mPaw)/PaO2, rounded to 1 dp) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0013
date: 2026-11-24
model: claude-sonnet-4-6
idea: ideal-body-weight
outcome: accepted
metrics: lines=182 dead=-1 cap=1500 headroom=1318
note: Added idealBodyWeight (Devine: 50/45.5 + 2.3 × (height[in] − 60), height in cm) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0014
date: 2026-11-24
model: claude-sonnet-4-6
idea: protective-tidal-volume
outcome: accepted
metrics: lines=200 dead=-1 cap=1500 headroom=1300
note: Added protectiveTidalVolume (mL/kg [4–8, default 6] × Devine IBW, rounded to mL) reusing idealBodyWeight, with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0015
date: 2026-11-24
model: claude-sonnet-4-6
idea: driving-pressure
outcome: accepted
metrics: lines=202 dead=-1 cap=1500 headroom=1298
note: Added drivingPressure (Pplat − PEEP, cmH2O, throws if Pplat < PEEP) with two tests; four original formulas untouched, oracle 16/16 passing (lines = non-blank, non-comment in both files; prior-gen count methodology may differ slightly).
---
gen: 0016
date: 2026-11-25
model: claude-sonnet-4-6
idea: static-compliance
outcome: accepted
metrics: lines=212 dead=-1 cap=1500 headroom=1288
note: Added staticCompliance (Vt / (Pplat − PEEP), mL/cmH2O, throws if Pplat <= PEEP) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0017
date: 2026-11-25
model: claude-sonnet-4-6
idea: mechanical-power
outcome: accepted
metrics: lines=223 dead=-1 cap=1500 headroom=1277
note: Added mechanicalPower (Gattinoni simplified: 0.098 × RR × Vt[L] × (Ppeak − ½·ΔP), J/min, throws if Pplat < PEEP or Ppeak < Pplat) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0018
date: 2026-11-25
model: claude-sonnet-4-6
idea: sf-ratio
outcome: accepted
metrics: lines=233 dead=-1 cap=1500 headroom=1267
note: Added sfRatio (SpO2/FiO2, rounded to 1 dp, throws if FiO2 outside (0, 1]) with two tests; four original formulas untouched, oracle 16/16 passing.
---
gen: 0019
date: 2026-11-25
model: claude-sonnet-4-6
idea: ventilatory-ratio
outcome: accepted
metrics: lines=243 dead=-1 cap=1500 headroom=1257
note: Added ventilatoryRatio (Sinha: VE[mL/min] × PaCO2 / (PBW × 100 × 37.5), rounded to 2 dp, throws if PBW <= 0) with two tests; four original formulas untouched, oracle 16/16 passing.
