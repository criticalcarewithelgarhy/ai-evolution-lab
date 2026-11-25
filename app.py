"""
ICU Calculator — Flask app with Jinja2 template inline.
Single file: routes, logic calls, and HTML all live here.

Separation event: if an agent splits the template into templates/ or adds
a .js file with formula logic, metrics.py will flag it.
"""

from flask import Flask, request, render_template_string
from pathlib import Path
from calculator import (
    mean_arterial_pressure, pf_ratio, anion_gap,
    corrected_anion_gap, corrected_sodium, creatinine_clearance, winters_formula,
    delta_ratio, aa_gradient, serum_osmolality, corrected_calcium, predicted_body_weight, shock_index, free_water_deficit, rox_index, qsofa_score, driving_pressure, oxygenation_index, sf_ratio, static_compliance, DISCLAIMER,
)

app = Flask(__name__)


def _current_gen_info():
    try:
        text = Path("EVOLUTION.md").read_text(encoding="utf-8")
        blocks = [b.strip() for b in text.split("---") if b.strip()]
        entries = []
        for b in blocks:
            def _get(k):
                import re
                m = re.search(rf"^{k}:\s*(.+)", b, re.M)
                return m.group(1).strip() if m else None
            g = _get("gen")
            if g and g.isdigit():
                entries.append((int(g), _get("date") or ""))
        if entries:
            g, d = max(entries, key=lambda x: x[0])
            return f"gen-{g:04d} · {d}"
    except Exception:
        pass
    return "gen-0000"

TEMPLATE = """{% macro result(key, unit="") %}
  {% if results[key] is defined %}
  <div class="result" id="{{ key }}">
    <span class="val">{{ results[key] }}</span>{% if unit %}<span class="unit">{{ unit }}</span>{% endif %}
    <div class="interp {{ results[key ~ '_cls'] }}">{{ results[key ~ '_interp'] }}</div>
  </div>
  {% elif results[key ~ '_error'] is defined %}
  <div class="error">{{ results[key ~ '_error'] }}</div>
  {% endif %}
{% endmacro -%}
{% macro num(name, label, ph, step=None) %}
      <div class="field"><label>{{ label }}</label>
        <input type="number" name="{{ name }}"{% if step %} step="{{ step }}"{% endif %} value="{{ form[name] or '' }}" placeholder="{{ ph }}"></div>
{% endmacro -%}
{% macro sel(name, label, opts) %}
      <div class="field"><label>{{ label }}</label>
        <select name="{{ name }}">
{%- for v, t in opts %}
          <option value="{{ v }}" {% if form[name] == v %}selected{% endif %}>{{ t }}</option>
{%- endfor %}
        </select>
      </div>
{% endmacro -%}
{% macro card(key, title, formula, unit="") %}
  <div class="card">
    <h2>{{ title|safe }}</h2>
    <div class="formula">{{ formula|safe }}</div>
    <form method="POST" action="/#{{ key }}">
      <input type="hidden" name="calc" value="{{ key }}">
{{ caller() }}      <button class="btn" type="submit">Calculate</button>
    </form>
    {{ result(key, unit) }}
  </div>
{% endmacro -%}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ICU Calculator</title>
<style>
  :root {
    --bg:#0d1117; --surface:#161b22; --border:#30363d;
    --text:#e6edf3; --muted:#8b949e; --blue:#58a6ff;
    --green:#3fb950; --red:#ff7b72; --yellow:#e3b341;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
    background:var(--bg);color:var(--text);padding:32px 20px;
    max-width:860px;margin:0 auto}
  a{color:var(--blue);text-decoration:none}
  header{margin-bottom:24px}
  header h1{font-size:1.3rem;font-weight:600}
  .nav{font-size:.8rem;color:var(--muted);margin-top:8px}
  .disclaimer{background:rgba(227,179,65,.1);border:1px solid rgba(227,179,65,.3);
    border-radius:6px;padding:10px 14px;font-size:.78rem;color:var(--yellow);
    margin:16px 0 24px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  @media(max-width:600px){.grid{grid-template-columns:1fr}}
  .card{background:var(--surface);border:1px solid var(--border);
    border-radius:8px;padding:20px}
  .card h2{font-size:.95rem;font-weight:600;margin-bottom:3px}
  .formula{font-size:.72rem;color:var(--muted);font-family:monospace;margin-bottom:14px}
  .field{margin-bottom:10px}
  .field label{display:block;font-size:.75rem;color:var(--muted);margin-bottom:3px}
  .field input,.field select{width:100%;background:var(--bg);
    border:1px solid var(--border);border-radius:6px;padding:8px 10px;
    color:var(--text);font-size:.875rem}
  .btn{width:100%;margin-top:14px;background:var(--blue);color:#000;
    border:none;border-radius:6px;padding:9px;font-size:.875rem;
    font-weight:600;cursor:pointer}
  .btn:hover{opacity:.9}
  .result{margin-top:12px;background:var(--bg);border-radius:6px;padding:12px 14px}
  .result .val{font-size:1.8rem;font-weight:700;color:var(--blue);
    font-variant-numeric:tabular-nums}
  .result .unit{font-size:.8rem;color:var(--muted);margin-left:6px}
  .interp{font-size:.78rem;margin-top:4px}
  .normal{color:var(--green)} .warn{color:var(--yellow)} .crit{color:var(--red)}
  .error{color:var(--red);font-size:.8rem;margin-top:8px}
  footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--border);
    font-size:.72rem;color:var(--muted);display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px}
</style>
</head>
<body>
<header>
  <h1>ICU Calculator</h1>
  <div class="nav">
    <a href="https://criticalcarewithelgarhy.github.io/ai-evolution-lab/">← Evolution Dashboard</a> ·
    <a href="https://github.com/criticalcarewithelgarhy/ai-evolution-lab" target="_blank">GitHub</a>
  </div>
</header>

<div class="disclaimer">⚠ NOT FOR CLINICAL USE · AI-modified experiment ·
  <a href="https://github.com/criticalcarewithelgarhy/ai-evolution-lab" style="color:var(--yellow);">See the experiment →</a>
</div>

<div class="grid">

  {% call card("map", "Mean Arterial Pressure", "MAP = DBP + (SBP − DBP) / 3", "mmHg") %}
      {{ num("sbp", "Systolic BP (mmHg)", "120") }}
      {{ num("dbp", "Diastolic BP (mmHg)", "80") }}
  {% endcall %}

  {% call card("pf", "P/F Ratio", "P/F = PaO₂ / FiO₂", "mmHg") %}
      {{ num("pao2", "PaO₂ (mmHg)", "100") }}
      {{ num("fio2", "FiO₂ (0.21 – 1.0)", "0.21", "0.01") }}
  {% endcall %}

  {% call card("ag", "Anion Gap", "AG = Na⁺ − (Cl⁻ + HCO₃⁻)", "mEq/L") %}
      {{ num("na", "Sodium Na⁺ (mEq/L)", "140") }}
      {{ num("cl", "Chloride Cl⁻ (mEq/L)", "104") }}
      {{ num("hco3", "Bicarbonate HCO₃⁻ (mEq/L)", "24") }}
  {% endcall %}

  {% call card("crcl", "Creatinine Clearance", "Cockcroft-Gault", "mL/min") %}
      {{ num("age", "Age (years)", "50") }}
      {{ num("weight", "Weight (kg)", "70") }}
      {{ num("creatinine", "Serum Creatinine (mg/dL)", "1.0", "0.1") }}
      {{ sel("sex", "Sex", [("male", "Male"), ("female", "Female")]) }}
  {% endcall %}

  {% call card("cag", "Corrected Anion Gap", "AG<sub>corr</sub> = AG + 2.5 × (4 − Albumin)", "mEq/L") %}
      {{ num("cag_na", "Sodium Na⁺ (mEq/L)", "140") }}
      {{ num("cag_cl", "Chloride Cl⁻ (mEq/L)", "104") }}
      {{ num("cag_hco3", "Bicarbonate HCO₃⁻ (mEq/L)", "24") }}
      {{ num("albumin", "Albumin (g/dL)", "4.0", "0.1") }}
  {% endcall %}

  {% call card("cna", "Corrected Sodium", "Na<sub>corr</sub> = Na<sub>meas</sub> + 1.6 × (Glucose − 100) / 100", "mEq/L") %}
      {{ num("cna_na", "Measured Sodium Na⁺ (mEq/L)", "135") }}
      {{ num("glucose", "Blood Glucose (mg/dL)", "100") }}
  {% endcall %}

  {% call card("win", "Winter's Formula", "Expected PaCO₂ = 1.5 × HCO₃⁻ + 8 ± 2", "mmHg (± 2)") %}
      {{ num("win_hco3", "Bicarbonate HCO₃⁻ (mEq/L)", "12", "0.1") }}
      {{ num("win_paco2", "Measured PaCO₂ (mmHg, optional)", "26", "0.1") }}
  {% endcall %}

  {% call card("dr", "Delta Ratio", "Δ/Δ = (AG − 12) / (24 − HCO₃⁻)") %}
      {{ num("dr_na", "Sodium Na⁺ (mEq/L)", "138") }}
      {{ num("dr_cl", "Chloride Cl⁻ (mEq/L)", "98") }}
      {{ num("dr_hco3", "Bicarbonate HCO₃⁻ (mEq/L)", "10", "0.1") }}
  {% endcall %}

  {% call card("aa", "A–a Gradient", "A–a = FiO₂ × (760 − 47) − PaCO₂ / 0.8 − PaO₂", "mmHg") %}
      {{ num("aa_pao2", "PaO₂ (mmHg)", "90") }}
      {{ num("aa_paco2", "PaCO₂ (mmHg)", "40") }}
      {{ num("aa_fio2", "FiO₂ (0.21 – 1.0)", "0.21", "0.01") }}
      {{ num("aa_age", "Age (years, optional)", "50") }}
  {% endcall %}

  {% call card("osm", "Serum Osmolality", "Osm = 2 × Na⁺ + Glucose / 18 + BUN / 2.8", "mOsm/kg") %}
      {{ num("osm_na", "Sodium Na⁺ (mEq/L)", "140") }}
      {{ num("osm_glu", "Glucose (mg/dL)", "90") }}
      {{ num("osm_bun", "BUN (mg/dL)", "14") }}
      {{ num("osm_meas", "Measured Osmolality (mOsm/kg, optional)", "300") }}
  {% endcall %}

  {% call card("cca", "Corrected Calcium", "Ca<sub>corr</sub> = Ca + 0.8 × (4 − Albumin)", "mg/dL") %}
      {{ num("cca_ca", "Total Calcium (mg/dL)", "8.0", "0.1") }}
      {{ num("cca_alb", "Albumin (g/dL)", "4.0", "0.1") }}
  {% endcall %}

  {% call card("pbw", "Predicted Body Weight &amp; Tidal Volume", "PBW = 50 (♂) / 45.5 (♀) + 0.91 × (Height − 152.4); V<sub>T</sub> 6–8 mL/kg", "kg") %}
      {{ num("pbw_ht", "Height (cm)", "170", "0.1") }}
      {{ sel("pbw_sex", "Sex", [("male", "Male"), ("female", "Female")]) }}
  {% endcall %}

  {% call card("si", "Shock Index", "SI = HR / SBP") %}
      {{ num("si_hr", "Heart Rate (bpm)", "80") }}
      {{ num("si_sbp", "Systolic BP (mmHg)", "120") }}
  {% endcall %}

  {% call card("fwd", "Free Water Deficit", "FWD = TBW × (Na⁺ / 140 − 1); TBW = 0.6 (♂) / 0.5 (♀) × Weight", "L") %}
      {{ num("fwd_na", "Sodium Na⁺ (mEq/L)", "160") }}
      {{ num("fwd_wt", "Weight (kg)", "70", "0.1") }}
      {{ sel("fwd_sex", "Sex", [("male", "Male"), ("female", "Female")]) }}
  {% endcall %}

  {% call card("rox", "ROX Index", "ROX = (SpO₂ / FiO₂) / RR") %}
      {{ num("rox_spo2", "SpO₂ (%)", "95") }}
      {{ num("rox_fio2", "FiO₂ (0.21 – 1.0)", "0.5", "0.01") }}
      {{ num("rox_rr", "Respiratory Rate (breaths/min)", "20") }}
  {% endcall %}

  {% call card("qsofa", "qSOFA", "1 pt each: RR ≥ 22 · SBP ≤ 100 · altered mentation", "/ 3") %}
      {{ num("qs_rr", "Respiratory Rate (breaths/min)", "18") }}
      {{ num("qs_sbp", "Systolic BP (mmHg)", "120") }}
      {{ sel("qs_ams", "Altered mentation (GCS < 15)", [("no", "No"), ("yes", "Yes")]) }}
  {% endcall %}

  {% call card("dp", "Driving Pressure", "ΔP = P<sub>plat</sub> − PEEP", "cmH₂O") %}
      {{ num("dp_pplat", "Plateau Pressure (cmH₂O)", "25", "0.1") }}
      {{ num("dp_peep", "PEEP (cmH₂O)", "10", "0.1") }}
  {% endcall %}

  {% call card("oi", "Oxygenation Index", "OI = FiO₂ × mPaw × 100 / PaO₂") %}
      {{ num("oi_fio2", "FiO₂ (0.21 – 1.0)", "0.6", "0.01") }}
      {{ num("oi_mpaw", "Mean Airway Pressure (cmH₂O)", "15", "0.1") }}
      {{ num("oi_pao2", "PaO₂ (mmHg)", "75") }}
  {% endcall %}

  {% call card("sf", "SpO₂/FiO₂ Ratio", "S/F = SpO₂ / FiO₂ (valid if SpO₂ ≤ 97%)") %}
      {{ num("sf_spo2", "SpO₂ (%)", "92") }}
      {{ num("sf_fio2", "FiO₂ (0.21 – 1.0)", "0.4", "0.01") }}
  {% endcall %}

  {% call card("cst", "Static Compliance", "C<sub>stat</sub> = V<sub>T</sub> / (P<sub>plat</sub> − PEEP)", "mL/cmH₂O") %}
      {{ num("cst_vt", "Tidal Volume (mL)", "450") }}
      {{ num("cst_pplat", "Plateau Pressure (cmH₂O)", "25", "0.1") }}
      {{ num("cst_peep", "PEEP (cmH₂O)", "10", "0.1") }}
  {% endcall %}

</div>

<footer>
  <span>{{ gen_info }} · Seed: MAP · P/F · Anion Gap · CrCl · Corr AG · Corr Na · Winter's · Δ/Δ · A–a · Osm · Corr Ca · PBW · SI · FWD · ROX · qSOFA · ΔP · OI · S/F · C<sub>stat</sub></span>
  <span><a href="https://criticalcarewithelgarhy.github.io/ai-evolution-lab/" style="color:var(--muted)">Evolution Dashboard →</a></span>
</footer>
</body>
</html>"""


def _map_interp(v):
    if v < 65:   return "Below target — vasopressor threshold", "crit"
    if v < 70:   return "Low — monitor closely", "warn"
    if v <= 100: return "Normal (65–100 mmHg)", "normal"
    return "Elevated", "warn"

def _pf_interp(v):
    if v < 100:  return "Severe ARDS (< 100)", "crit"
    if v < 200:  return "Moderate ARDS (100–200)", "warn"
    if v < 300:  return "Mild ARDS (200–300)", "warn"
    return "Normal (≥ 300)", "normal"

def _ag_interp(v):
    if v < 8:    return "Low (< 8) — hypoalbuminaemia?", "warn"
    if v <= 12:  return "Normal (8–12 mEq/L)", "normal"
    if v <= 20:  return "Elevated — high AG acidosis", "warn"
    return "Markedly elevated", "crit"

def _cag_interp(v):
    if v < 8:    return "Low corrected AG — check albumin", "warn"
    if v <= 12:  return "Normal corrected AG (8–12 mEq/L)", "normal"
    if v <= 20:  return "Elevated — high AG acidosis", "warn"
    return "Markedly elevated", "crit"

def _cna_interp(v):
    if v < 135:  return "Hyponatraemia (< 135 mEq/L)", "warn"
    if v <= 145: return "Normal (135–145 mEq/L)", "normal"
    if v <= 150: return "Mild hypernatraemia", "warn"
    return "Severe hypernatraemia (> 150 mEq/L)", "crit"

def _win_interp(expected, measured):
    if measured is None: return f"Expected range {expected - 2:.1f}–{expected + 2:.1f} mmHg", "normal"
    if measured > expected + 2: return "PaCO₂ above expected — concomitant respiratory acidosis", "crit"
    if measured < expected - 2: return "PaCO₂ below expected — concomitant respiratory alkalosis", "warn"
    return "Appropriate respiratory compensation", "normal"

def _dr_interp(v):
    if v < 0.4:  return "< 0.4 — hyperchloraemic normal-AG acidosis", "warn"
    if v < 1:    return "0.4–1 — mixed high-AG + normal-AG acidosis", "warn"
    if v <= 2:   return "1–2 — pure high-AG metabolic acidosis", "normal"
    return "> 2 — concurrent metabolic alkalosis", "crit"

def _aa_interp(v, age):
    limit = age / 4 + 4 if age is not None else 15
    if v <= limit: return f"Normal (≤ {limit:.0f} mmHg expected)", "normal"
    return f"Elevated (> {limit:.0f}) — V/Q mismatch, shunt or diffusion defect", "warn"

def _osm_interp(v, measured):
    if measured is not None:
        gap = measured - v
        if gap > 10: return f"Osmolar gap {gap:.1f} (> 10) — consider toxic alcohols", "crit"
        return f"Osmolar gap {gap:.1f} — normal (≤ 10)", "normal"
    if v < 275:  return "Low (< 275 mOsm/kg)", "warn"
    if v <= 295: return "Normal (275–295 mOsm/kg)", "normal"
    if v <= 320: return "Elevated (> 295 mOsm/kg)", "warn"
    return "Markedly elevated (> 320) — hyperosmolar state", "crit"

def _cca_interp(v):
    if v < 8.5:   return "Hypocalcaemia (< 8.5 mg/dL) — check ionised Ca", "warn"
    if v <= 10.5: return "Normal (8.5–10.5 mg/dL)", "normal"
    if v <= 12:   return "Mild hypercalcaemia", "warn"
    return "Severe hypercalcaemia (> 12 mg/dL)", "crit"

def _pbw_interp(v):
    return f"Lung-protective VT: {6 * v:.0f} mL (6 mL/kg) – {8 * v:.0f} mL (8 mL/kg)", "normal"

def _si_interp(v):
    if v < 0.5:  return "Low (< 0.5)", "normal"
    if v <= 0.7: return "Normal (0.5–0.7)", "normal"
    if v <= 0.9: return "Borderline (0.7–0.9) — reassess", "warn"
    return "Elevated (> 0.9) — possible occult shock", "crit"

def _fwd_interp(v):
    if v <= 0:  return "No free water deficit (Na ≤ 140)", "normal"
    if v <= 3:  return "Mild deficit — correct Na ≤ 10 mEq/L per 24 h", "warn"
    return "Significant deficit — correct Na ≤ 10 mEq/L per 24 h", "crit"

def _rox_interp(v):
    if v >= 4.88: return "≥ 4.88 — HFNC success likely", "normal"
    if v >= 3.85: return "3.85–4.88 — indeterminate, reassess in 1–2 h", "warn"
    return "< 3.85 — high risk of HFNC failure, consider intubation", "crit"

def _qsofa_interp(v):
    if v >= 2: return "≥ 2 — high risk of poor outcome, assess for sepsis/organ dysfunction", "crit"
    return "< 2 — low risk, but does not exclude sepsis", "normal"

def _dp_interp(v):
    if v <= 15: return "≤ 15 cmH₂O — within lung-protective target", "normal"
    return "> 15 cmH₂O — associated with higher ARDS mortality, consider lowering VT", "crit"

def _oi_interp(v):
    if v < 15:  return "< 15 — mild oxygenation impairment", "normal"
    if v <= 25: return "15–25 — moderate impairment", "warn"
    if v <= 40: return "25–40 — severe impairment", "crit"
    return "> 40 — very severe, consider ECMO referral", "crit"

def _sf_interp(v, spo2):
    note = " (SpO₂ > 97% — unreliable)" if spo2 > 97 else ""
    if v < 235: return "< 235 — ≈ P/F < 200, moderate–severe hypoxaemia" + note, "crit"
    if v < 315: return "235–315 — ≈ P/F 200–300, mild hypoxaemia" + note, "warn"
    return "≥ 315 — ≈ P/F ≥ 300" + note, "normal"

def _cst_interp(v):
    if v < 20: return "< 20 — very stiff respiratory system, severe ARDS/restriction", "crit"
    if v < 40: return "20–40 — reduced compliance (e.g. ARDS, oedema, fibrosis)", "warn"
    return "≥ 40 — normal or near-normal compliance", "normal"

def _crcl_interp(v):
    if v < 15:   return "Stage 5 CKD — dialysis range", "crit"
    if v < 30:   return "Stage 4 CKD — severe", "crit"
    if v < 60:   return "Stage 3 CKD — moderate", "warn"
    if v < 90:   return "Stage 2 CKD — mild", "warn"
    return "Normal (≥ 90 mL/min)", "normal"


def _n(f, k):
    return float(f[k])

def _opt(f, k):
    return float(f[k]) if f.get(k) else None


# calc key -> (compute(form) -> value, interpret(value, form) -> (text, css class))
CALCS = {
    "map": (lambda f: mean_arterial_pressure(_n(f, "sbp"), _n(f, "dbp")),
            lambda v, f: _map_interp(v)),
    "pf": (lambda f: pf_ratio(_n(f, "pao2"), _n(f, "fio2")),
           lambda v, f: _pf_interp(v)),
    "ag": (lambda f: anion_gap(_n(f, "na"), _n(f, "cl"), _n(f, "hco3")),
           lambda v, f: _ag_interp(v)),
    "cag": (lambda f: corrected_anion_gap(_n(f, "cag_na"), _n(f, "cag_cl"), _n(f, "cag_hco3"), _n(f, "albumin")),
            lambda v, f: _cag_interp(v)),
    "cna": (lambda f: corrected_sodium(_n(f, "cna_na"), _n(f, "glucose")),
            lambda v, f: _cna_interp(v)),
    "win": (lambda f: winters_formula(_n(f, "win_hco3")),
            lambda v, f: _win_interp(v, _opt(f, "win_paco2"))),
    "dr": (lambda f: delta_ratio(_n(f, "dr_na"), _n(f, "dr_cl"), _n(f, "dr_hco3")),
           lambda v, f: _dr_interp(v)),
    "aa": (lambda f: aa_gradient(_n(f, "aa_pao2"), _n(f, "aa_paco2"), _n(f, "aa_fio2")),
           lambda v, f: _aa_interp(v, _opt(f, "aa_age"))),
    "osm": (lambda f: serum_osmolality(_n(f, "osm_na"), _n(f, "osm_glu"), _n(f, "osm_bun")),
            lambda v, f: _osm_interp(v, _opt(f, "osm_meas"))),
    "cca": (lambda f: corrected_calcium(_n(f, "cca_ca"), _n(f, "cca_alb")),
            lambda v, f: _cca_interp(v)),
    "pbw": (lambda f: predicted_body_weight(_n(f, "pbw_ht"), f.get("pbw_sex", "male")),
            lambda v, f: _pbw_interp(v)),
    "si": (lambda f: shock_index(_n(f, "si_hr"), _n(f, "si_sbp")),
           lambda v, f: _si_interp(v)),
    "fwd": (lambda f: free_water_deficit(_n(f, "fwd_na"), _n(f, "fwd_wt"), f.get("fwd_sex", "male")),
            lambda v, f: _fwd_interp(v)),
    "rox": (lambda f: rox_index(_n(f, "rox_spo2"), _n(f, "rox_fio2"), _n(f, "rox_rr")),
            lambda v, f: _rox_interp(v)),
    "qsofa": (lambda f: qsofa_score(_n(f, "qs_rr"), _n(f, "qs_sbp"), f.get("qs_ams") == "yes"),
              lambda v, f: _qsofa_interp(v)),
    "dp": (lambda f: driving_pressure(_n(f, "dp_pplat"), _n(f, "dp_peep")),
           lambda v, f: _dp_interp(v)),
    "oi": (lambda f: oxygenation_index(_n(f, "oi_fio2"), _n(f, "oi_mpaw"), _n(f, "oi_pao2")),
           lambda v, f: _oi_interp(v)),
    "sf": (lambda f: sf_ratio(_n(f, "sf_spo2"), _n(f, "sf_fio2")),
           lambda v, f: _sf_interp(v, _n(f, "sf_spo2"))),
    "cst": (lambda f: static_compliance(_n(f, "cst_vt"), _n(f, "cst_pplat"), _n(f, "cst_peep")),
            lambda v, f: _cst_interp(v)),
    "crcl": (lambda f: creatinine_clearance(_n(f, "age"), _n(f, "weight"), _n(f, "creatinine"), f.get("sex", "male")),
             lambda v, f: _crcl_interp(v)),
}


@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    form = request.form if request.method == "POST" else {}
    calc = form.get("calc")

    if calc in CALCS:
        compute, interpret = CALCS[calc]
        try:
            v = compute(form)
            interp, cls = interpret(v, form)
            results.update({calc: v, f"{calc}_interp": interp, f"{calc}_cls": cls})
        except Exception as e:
            results[f"{calc}_error"] = str(e)

    return render_template_string(TEMPLATE, disclaimer=DISCLAIMER,
                                   gen_info=_current_gen_info(), results=results, form=form)


if __name__ == "__main__":
    app.run(debug=True, port=3001)
