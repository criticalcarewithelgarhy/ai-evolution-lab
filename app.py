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
    delta_ratio, aa_gradient, serum_osmolality, corrected_calcium, DISCLAIMER,
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

TEMPLATE = """<!DOCTYPE html>
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

  <div class="card">
    <h2>Mean Arterial Pressure</h2>
    <div class="formula">MAP = DBP + (SBP − DBP) / 3</div>
    <form method="POST" action="/#map">
      <input type="hidden" name="calc" value="map">
      <div class="field"><label>Systolic BP (mmHg)</label>
        <input type="number" name="sbp" value="{{ form.sbp or '' }}" placeholder="120"></div>
      <div class="field"><label>Diastolic BP (mmHg)</label>
        <input type="number" name="dbp" value="{{ form.dbp or '' }}" placeholder="80"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.map is defined %}
    <div class="result" id="map">
      <span class="val">{{ results.map }}</span><span class="unit">mmHg</span>
      <div class="interp {{ results.map_cls }}">{{ results.map_interp }}</div>
    </div>
    {% elif results.map_error is defined %}
    <div class="error">{{ results.map_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>P/F Ratio</h2>
    <div class="formula">P/F = PaO₂ / FiO₂</div>
    <form method="POST" action="/#pf">
      <input type="hidden" name="calc" value="pf">
      <div class="field"><label>PaO₂ (mmHg)</label>
        <input type="number" name="pao2" value="{{ form.pao2 or '' }}" placeholder="100"></div>
      <div class="field"><label>FiO₂ (0.21 – 1.0)</label>
        <input type="number" name="fio2" step="0.01" value="{{ form.fio2 or '' }}" placeholder="0.21"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.pf is defined %}
    <div class="result" id="pf">
      <span class="val">{{ results.pf }}</span><span class="unit">mmHg</span>
      <div class="interp {{ results.pf_cls }}">{{ results.pf_interp }}</div>
    </div>
    {% elif results.pf_error is defined %}
    <div class="error">{{ results.pf_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Anion Gap</h2>
    <div class="formula">AG = Na⁺ − (Cl⁻ + HCO₃⁻)</div>
    <form method="POST" action="/#ag">
      <input type="hidden" name="calc" value="ag">
      <div class="field"><label>Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="na" value="{{ form.na or '' }}" placeholder="140"></div>
      <div class="field"><label>Chloride Cl⁻ (mEq/L)</label>
        <input type="number" name="cl" value="{{ form.cl or '' }}" placeholder="104"></div>
      <div class="field"><label>Bicarbonate HCO₃⁻ (mEq/L)</label>
        <input type="number" name="hco3" value="{{ form.hco3 or '' }}" placeholder="24"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.ag is defined %}
    <div class="result" id="ag">
      <span class="val">{{ results.ag }}</span><span class="unit">mEq/L</span>
      <div class="interp {{ results.ag_cls }}">{{ results.ag_interp }}</div>
    </div>
    {% elif results.ag_error is defined %}
    <div class="error">{{ results.ag_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Creatinine Clearance</h2>
    <div class="formula">Cockcroft-Gault</div>
    <form method="POST" action="/#crcl">
      <input type="hidden" name="calc" value="crcl">
      <div class="field"><label>Age (years)</label>
        <input type="number" name="age" value="{{ form.age or '' }}" placeholder="50"></div>
      <div class="field"><label>Weight (kg)</label>
        <input type="number" name="weight" value="{{ form.weight or '' }}" placeholder="70"></div>
      <div class="field"><label>Serum Creatinine (mg/dL)</label>
        <input type="number" name="creatinine" step="0.1" value="{{ form.creatinine or '' }}" placeholder="1.0"></div>
      <div class="field"><label>Sex</label>
        <select name="sex">
          <option value="male" {% if form.sex == 'male' %}selected{% endif %}>Male</option>
          <option value="female" {% if form.sex == 'female' %}selected{% endif %}>Female</option>
        </select>
      </div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.crcl is defined %}
    <div class="result" id="crcl">
      <span class="val">{{ results.crcl }}</span><span class="unit">mL/min</span>
      <div class="interp {{ results.crcl_cls }}">{{ results.crcl_interp }}</div>
    </div>
    {% elif results.crcl_error is defined %}
    <div class="error">{{ results.crcl_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Corrected Anion Gap</h2>
    <div class="formula">AG<sub>corr</sub> = AG + 2.5 × (4 − Albumin)</div>
    <form method="POST" action="/#cag">
      <input type="hidden" name="calc" value="cag">
      <div class="field"><label>Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="cag_na" value="{{ form.cag_na or '' }}" placeholder="140"></div>
      <div class="field"><label>Chloride Cl⁻ (mEq/L)</label>
        <input type="number" name="cag_cl" value="{{ form.cag_cl or '' }}" placeholder="104"></div>
      <div class="field"><label>Bicarbonate HCO₃⁻ (mEq/L)</label>
        <input type="number" name="cag_hco3" value="{{ form.cag_hco3 or '' }}" placeholder="24"></div>
      <div class="field"><label>Albumin (g/dL)</label>
        <input type="number" name="albumin" step="0.1" value="{{ form.albumin or '' }}" placeholder="4.0"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.cag is defined %}
    <div class="result" id="cag">
      <span class="val">{{ results.cag }}</span><span class="unit">mEq/L</span>
      <div class="interp {{ results.cag_cls }}">{{ results.cag_interp }}</div>
    </div>
    {% elif results.cag_error is defined %}
    <div class="error">{{ results.cag_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Corrected Sodium</h2>
    <div class="formula">Na<sub>corr</sub> = Na<sub>meas</sub> + 1.6 × (Glucose − 100) / 100</div>
    <form method="POST" action="/#cna">
      <input type="hidden" name="calc" value="cna">
      <div class="field"><label>Measured Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="cna_na" value="{{ form.cna_na or '' }}" placeholder="135"></div>
      <div class="field"><label>Blood Glucose (mg/dL)</label>
        <input type="number" name="glucose" value="{{ form.glucose or '' }}" placeholder="100"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.cna is defined %}
    <div class="result" id="cna">
      <span class="val">{{ results.cna }}</span><span class="unit">mEq/L</span>
      <div class="interp {{ results.cna_cls }}">{{ results.cna_interp }}</div>
    </div>
    {% elif results.cna_error is defined %}
    <div class="error">{{ results.cna_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Winter's Formula</h2>
    <div class="formula">Expected PaCO₂ = 1.5 × HCO₃⁻ + 8 ± 2</div>
    <form method="POST" action="/#win">
      <input type="hidden" name="calc" value="win">
      <div class="field"><label>Bicarbonate HCO₃⁻ (mEq/L)</label>
        <input type="number" name="win_hco3" step="0.1" value="{{ form.win_hco3 or '' }}" placeholder="12"></div>
      <div class="field"><label>Measured PaCO₂ (mmHg, optional)</label>
        <input type="number" name="win_paco2" step="0.1" value="{{ form.win_paco2 or '' }}" placeholder="26"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.win is defined %}
    <div class="result" id="win">
      <span class="val">{{ results.win }}</span><span class="unit">mmHg (± 2)</span>
      <div class="interp {{ results.win_cls }}">{{ results.win_interp }}</div>
    </div>
    {% elif results.win_error is defined %}
    <div class="error">{{ results.win_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Delta Ratio</h2>
    <div class="formula">Δ/Δ = (AG − 12) / (24 − HCO₃⁻)</div>
    <form method="POST" action="/#dr">
      <input type="hidden" name="calc" value="dr">
      <div class="field"><label>Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="dr_na" value="{{ form.dr_na or '' }}" placeholder="138"></div>
      <div class="field"><label>Chloride Cl⁻ (mEq/L)</label>
        <input type="number" name="dr_cl" value="{{ form.dr_cl or '' }}" placeholder="98"></div>
      <div class="field"><label>Bicarbonate HCO₃⁻ (mEq/L)</label>
        <input type="number" name="dr_hco3" step="0.1" value="{{ form.dr_hco3 or '' }}" placeholder="10"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.dr is defined %}
    <div class="result" id="dr">
      <span class="val">{{ results.dr }}</span>
      <div class="interp {{ results.dr_cls }}">{{ results.dr_interp }}</div>
    </div>
    {% elif results.dr_error is defined %}
    <div class="error">{{ results.dr_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>A–a Gradient</h2>
    <div class="formula">A–a = FiO₂ × (760 − 47) − PaCO₂ / 0.8 − PaO₂</div>
    <form method="POST" action="/#aa">
      <input type="hidden" name="calc" value="aa">
      <div class="field"><label>PaO₂ (mmHg)</label>
        <input type="number" name="aa_pao2" value="{{ form.aa_pao2 or '' }}" placeholder="90"></div>
      <div class="field"><label>PaCO₂ (mmHg)</label>
        <input type="number" name="aa_paco2" value="{{ form.aa_paco2 or '' }}" placeholder="40"></div>
      <div class="field"><label>FiO₂ (0.21 – 1.0)</label>
        <input type="number" name="aa_fio2" step="0.01" value="{{ form.aa_fio2 or '' }}" placeholder="0.21"></div>
      <div class="field"><label>Age (years, optional)</label>
        <input type="number" name="aa_age" value="{{ form.aa_age or '' }}" placeholder="50"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.aa is defined %}
    <div class="result" id="aa">
      <span class="val">{{ results.aa }}</span><span class="unit">mmHg</span>
      <div class="interp {{ results.aa_cls }}">{{ results.aa_interp }}</div>
    </div>
    {% elif results.aa_error is defined %}
    <div class="error">{{ results.aa_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Serum Osmolality</h2>
    <div class="formula">Osm = 2 × Na⁺ + Glucose / 18 + BUN / 2.8</div>
    <form method="POST" action="/#osm">
      <input type="hidden" name="calc" value="osm">
      <div class="field"><label>Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="osm_na" value="{{ form.osm_na or '' }}" placeholder="140"></div>
      <div class="field"><label>Glucose (mg/dL)</label>
        <input type="number" name="osm_glu" value="{{ form.osm_glu or '' }}" placeholder="90"></div>
      <div class="field"><label>BUN (mg/dL)</label>
        <input type="number" name="osm_bun" value="{{ form.osm_bun or '' }}" placeholder="14"></div>
      <div class="field"><label>Measured Osmolality (mOsm/kg, optional)</label>
        <input type="number" name="osm_meas" value="{{ form.osm_meas or '' }}" placeholder="300"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.osm is defined %}
    <div class="result" id="osm">
      <span class="val">{{ results.osm }}</span><span class="unit">mOsm/kg</span>
      <div class="interp {{ results.osm_cls }}">{{ results.osm_interp }}</div>
    </div>
    {% elif results.osm_error is defined %}
    <div class="error">{{ results.osm_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Corrected Calcium</h2>
    <div class="formula">Ca<sub>corr</sub> = Ca + 0.8 × (4 − Albumin)</div>
    <form method="POST" action="/#cca">
      <input type="hidden" name="calc" value="cca">
      <div class="field"><label>Total Calcium (mg/dL)</label>
        <input type="number" name="cca_ca" step="0.1" value="{{ form.cca_ca or '' }}" placeholder="8.0"></div>
      <div class="field"><label>Albumin (g/dL)</label>
        <input type="number" name="cca_alb" step="0.1" value="{{ form.cca_alb or '' }}" placeholder="4.0"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.cca is defined %}
    <div class="result" id="cca">
      <span class="val">{{ results.cca }}</span><span class="unit">mg/dL</span>
      <div class="interp {{ results.cca_cls }}">{{ results.cca_interp }}</div>
    </div>
    {% elif results.cca_error is defined %}
    <div class="error">{{ results.cca_error }}</div>
    {% endif %}
  </div>

</div>

<footer>
  <span>{{ gen_info }} · Seed: MAP · P/F · Anion Gap · CrCl · Corr AG · Corr Na · Winter's · Δ/Δ · A–a · Osm · Corr Ca</span>
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

def _crcl_interp(v):
    if v < 15:   return "Stage 5 CKD — dialysis range", "crit"
    if v < 30:   return "Stage 4 CKD — severe", "crit"
    if v < 60:   return "Stage 3 CKD — moderate", "warn"
    if v < 90:   return "Stage 2 CKD — mild", "warn"
    return "Normal (≥ 90 mL/min)", "normal"


@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    form = request.form if request.method == "POST" else {}
    calc = form.get("calc")

    if calc == "map":
        try:
            v = mean_arterial_pressure(float(form["sbp"]), float(form["dbp"]))
            interp, cls = _map_interp(v)
            results.update(map=v, map_interp=interp, map_cls=cls)
        except Exception as e:
            results["map_error"] = str(e)

    elif calc == "pf":
        try:
            v = pf_ratio(float(form["pao2"]), float(form["fio2"]))
            interp, cls = _pf_interp(v)
            results.update(pf=v, pf_interp=interp, pf_cls=cls)
        except Exception as e:
            results["pf_error"] = str(e)

    elif calc == "ag":
        try:
            v = anion_gap(float(form["na"]), float(form["cl"]), float(form["hco3"]))
            interp, cls = _ag_interp(v)
            results.update(ag=v, ag_interp=interp, ag_cls=cls)
        except Exception as e:
            results["ag_error"] = str(e)

    elif calc == "cag":
        try:
            v = corrected_anion_gap(
                float(form["cag_na"]), float(form["cag_cl"]),
                float(form["cag_hco3"]), float(form["albumin"]),
            )
            interp, cls = _cag_interp(v)
            results.update(cag=v, cag_interp=interp, cag_cls=cls)
        except Exception as e:
            results["cag_error"] = str(e)

    elif calc == "cna":
        try:
            v = corrected_sodium(float(form["cna_na"]), float(form["glucose"]))
            interp, cls = _cna_interp(v)
            results.update(cna=v, cna_interp=interp, cna_cls=cls)
        except Exception as e:
            results["cna_error"] = str(e)

    elif calc == "win":
        try:
            v = winters_formula(float(form["win_hco3"]))
            measured = float(form["win_paco2"]) if form.get("win_paco2") else None
            interp, cls = _win_interp(v, measured)
            results.update(win=v, win_interp=interp, win_cls=cls)
        except Exception as e:
            results["win_error"] = str(e)

    elif calc == "dr":
        try:
            v = delta_ratio(float(form["dr_na"]), float(form["dr_cl"]), float(form["dr_hco3"]))
            interp, cls = _dr_interp(v)
            results.update(dr=v, dr_interp=interp, dr_cls=cls)
        except Exception as e:
            results["dr_error"] = str(e)

    elif calc == "aa":
        try:
            v = aa_gradient(float(form["aa_pao2"]), float(form["aa_paco2"]), float(form["aa_fio2"]))
            age = float(form["aa_age"]) if form.get("aa_age") else None
            interp, cls = _aa_interp(v, age)
            results.update(aa=v, aa_interp=interp, aa_cls=cls)
        except Exception as e:
            results["aa_error"] = str(e)

    elif calc == "osm":
        try:
            v = serum_osmolality(float(form["osm_na"]), float(form["osm_glu"]), float(form["osm_bun"]))
            measured = float(form["osm_meas"]) if form.get("osm_meas") else None
            interp, cls = _osm_interp(v, measured)
            results.update(osm=v, osm_interp=interp, osm_cls=cls)
        except Exception as e:
            results["osm_error"] = str(e)

    elif calc == "cca":
        try:
            v = corrected_calcium(float(form["cca_ca"]), float(form["cca_alb"]))
            interp, cls = _cca_interp(v)
            results.update(cca=v, cca_interp=interp, cca_cls=cls)
        except Exception as e:
            results["cca_error"] = str(e)

    elif calc == "crcl":
        try:
            v = creatinine_clearance(
                float(form["age"]), float(form["weight"]),
                float(form["creatinine"]), form.get("sex", "male"),
            )
            interp, cls = _crcl_interp(v)
            results.update(crcl=v, crcl_interp=interp, crcl_cls=cls)
        except Exception as e:
            results["crcl_error"] = str(e)

    return render_template_string(TEMPLATE, disclaimer=DISCLAIMER,
                                   gen_info=_current_gen_info(), results=results, form=form)


if __name__ == "__main__":
    app.run(debug=True, port=3001)
