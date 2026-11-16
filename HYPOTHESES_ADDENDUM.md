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
