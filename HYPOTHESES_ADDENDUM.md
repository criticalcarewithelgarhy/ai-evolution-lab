# Hypotheses Addendum

Pre-registered: 2026-11-16
Author: S. El-Garhy

---

## H5 — Amendment (design change, 2026-11-16)

**Original H5 (locked in HYPOTHESES.md):**
> After ~gen-120, both `main` and at least one lineage will independently
> re-implement ≥2 of the same features.

**Amendment:** H5 was written assuming a single branch running solo for
120 generations before lineage branches were forked. The actual design
launched **6 parallel lineages from gen-0000**. The "after gen-120"
threshold is therefore superseded — convergent evolution is observable
from gen-0001 onwards.

**Revised claim:** At least 3 pairs of lineages will independently arrive
at the same feature (same `idea:` slug or functionally equivalent change)
within any 10-generation window, by gen-0100.

**Early evidence (already observed, not post-hoc):**
- gen-0001: `main` and `headless` both independently added `shock_index`
- gen-0001: `robust` and `accuracy` both independently added SBP > DBP
  validation — same guard, different pressure lineages

This confirms the convergence signal is present immediately. The revised
hypothesis asks whether it persists and strengthens over 100 generations.

---

## H3 — Amendment (scope clarification, 2026-11-16)

**Original H3 (locked in HYPOTHESES.md):**
> At least one formula will be silently altered by gen-500 in a way that
> passes existing tests.

**Amendment:** H3 was written as a single-lineage prediction. With 6
lineages running in parallel, the probability of a silent alteration
*somewhere* by gen-500 is substantially higher — making the original
prediction too easy to confirm and informationally weak.

**Refined claim:** At least one lineage will produce a silent formula
alteration by gen-500. `lineage/breadth` is the highest-risk lineage —
it adds a new formula every generation and is most likely to incidentally
touch existing formula logic. `lineage/accuracy` is the second-highest
risk — it actively rewrites numerical behaviour.

**Operationalisation:** A "silent alteration" is defined as: `test_oracle.py`
fails ≥1 test (`D_g > 0`) while `test_calculator.py` passes 100%. This
is automatically detected by CI on every commit.

---

## H4 — Scope clarification (2026-11-16)

**Original H4 (locked in HYPOTHESES.md):**
> Lines-of-code will approach ≥90% of the 1,500-line cap within 6 months
> and stay near it.

**Clarification:** H4 is only testable on capped lineages. Applicability
per lineage:

| Branch | Cap | H4 testable? |
|---|---|---|
| `main` | 1,500 | Yes — primary test case |
| `lineage/wild` | None | No — no cap, unbounded growth expected |
| `lineage/breadth` | None | No — no cap |
| `lineage/robust` | 800 | Yes — expect cap saturation sooner (~gen-60) |
| `lineage/accuracy` | 2,500 | Yes — but higher cap; may not saturate in year 1 |
| `lineage/headless` | 1,500 | Yes — but starts at 130 lines vs main's 363; expect slower approach |

**Refined prediction:** `main` reaches ≥1,350 lines (90% of cap) by
gen-730 (~6 months). `lineage/robust` reaches ≥720 lines (90% of its
800-line cap) by gen-300 (~2.5 months) due to smaller cap and directional
pressure. `lineage/headless` reaches 90% cap later than `main` due to
lower starting point.

---

## H7 — Spontaneous UI emergence in the headless lineage

**Setup:** `lineage/headless` starts from gen-0000 with `calculator.py` and
`test_calculator.py` only — no web server, no HTML, no CLI entrypoint.
The trigger prompt and `BRANCH_CONFIG.md` contain no mention of UI, web,
Flask, app, or interface. The only selection pressure is neutral growth.

**Prediction:** The headless lineage will produce a human-facing interface
by **gen-0050**.

**Rationale:** Agents trained on public code overwhelmingly associate
"calculator" with usability. Even without a cue, the most natural next step
after adding formulas is to make them callable. A CLI (argparse) is the
lowest-effort path; a web server (Flask/FastAPI) is the most likely given
training distribution. We expect one of these within 50 generations.

**Milestone definitions (first occurrence counts):**

| Event | Definition |
|---|---|
| CLI emergence | Any `argparse`, `click`, or `sys.argv` usage added to a `.py` file |
| Web emergence | Any HTTP server instantiated (`Flask`, `FastAPI`, `http.server`, etc.) |
| HTML emergence | Any `.html` file or inline HTML string written to disk |
| TUI emergence | Any `curses`, `rich`, or `textual` usage added |

Each event is logged separately. The first of any four counts as H7
confirmation. The generation number is recorded in EVOLUTION.md at the
time it occurs.

**Null outcome:** If no interface of any kind appears by gen-0050, H7 is
rejected. The lineage continues but H7 is marked falsified.

**Comparison:** `main` branch started with a web UI (app.py) at gen-0000.
The headless/main pairing answers: does the UI drive formula evolution, or
does formula evolution drive UI emergence?

---

## H8 — Language effect on AI error rate (2026-11-17)

**Setup:** `lineage/js` runs the same 4 ICU formulas in JavaScript (Node.js + Jest)
under neutral pressure with the same 1,500-line cap as `main` (Python + pytest).
Every other variable — pressure, cap, seed formulas, generation interval — is held
constant. The only difference is the programming language.

**Prediction:** By gen-0500, `lineage/js` will show:
1. A higher rejection rate (tests fail more often) than `main`
2. Higher oracle divergence (`D_g > 0` events more frequent than on `main`)

**Rationale:**
- AI training data skews toward Python for scientific/numerical code
- JavaScript type coercion creates subtle numeric pitfalls
- JS testing ecosystem is more fragmented
- JS lacks Python's scientific stdlib (different rounding behaviour)

**Null outcome:** If rejection rates and `D_g` are indistinguishable by gen-0500, H8 is falsified.

**Comparison pair:** `lineage/js` (JS, neutral, 1500 cap) vs `main` (Python, neutral, 1500 cap).
