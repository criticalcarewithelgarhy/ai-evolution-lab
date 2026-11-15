"""
ICU Calculator — Flask app with Jinja2 template inline.
Single file: routes, logic calls, and HTML all live here.

Separation event: if an agent splits the template into templates/ or adds
a .js file with formula logic, metrics.py will flag it.
"""

from flask import Flask, request, render_template_string
from calculator import (
    mean_arterial_pressure, pf_ratio, anion_gap,
    creatinine_clearance, DISCLAIMER,
)

app = Flask(__name__)

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

<div class="disclaimer">⚠ {{ disclaimer }}</div>

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

</div>

<footer>
  <span>gen-0000 · 2026-11-15 · Seed: MAP · P/F · Anion Gap · CrCl</span>
  <span>{{ disclaimer }}</span>
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

    return render_template_string(TEMPLATE, disclaimer=DISCLAIMER, results=results, form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5010)
