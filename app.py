"""
ICU Calculator — Flask app with Jinja2 template inline.
Single file: routes, logic calls, and HTML all live here.

Separation event: if an agent splits the template into templates/ or adds
a .js file with formula logic, metrics.py will flag it.
"""

from flask import Flask, request, render_template_string
from calculator import (
    mean_arterial_pressure, pf_ratio, anion_gap,
    albumin_corrected_anion_gap, osmolar_gap, corrected_calcium, winters_formula,
    delta_ratio, aa_gradient, corrected_sodium, free_water_deficit, ideal_body_weight, shock_index, rox_index, sf_ratio, driving_pressure, static_compliance, oxygenation_index, mechanical_power, fractional_excretion_sodium, fractional_excretion_urea, qtc_bazett, creatinine_clearance, DISCLAIMER,
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

<div style="background:rgba(255,123,114,.12);border:1px solid rgba(255,123,114,.4);border-radius:6px;padding:10px 14px;font-size:.8rem;color:#ff7b72;margin-bottom:10px;font-weight:600;">
  🤖 EXPERIMENTAL — This calculator is being autonomously modified by an AI agent every 6 hours with no human review.
  Code changes may be incorrect. Do not use for clinical decisions.
  <a href="https://github.com/criticalcarewithelgarhy/ai-evolution-lab" style="color:#ff7b72;text-decoration:underline;">See the experiment →</a>
</div>
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
      <div class="field"><label>Albumin (g/dL, optional — for correction)</label>
        <input type="number" name="albumin" step="0.1" value="{{ form.albumin or '' }}" placeholder="4.0"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.ag is defined %}
    <div class="result" id="ag">
      <span class="val">{{ results.ag }}</span><span class="unit">mEq/L</span>
      <div class="interp {{ results.ag_cls }}">{{ results.ag_interp }}</div>
      {% if results.ag_corrected is defined %}
      <div style="margin-top:8px;font-size:.8rem;color:var(--muted)">
        Albumin-corrected: <strong style="color:var(--blue)">{{ results.ag_corrected }}</strong> mEq/L
        <span class="interp {{ results.ag_corrected_cls }}">{{ results.ag_corrected_interp }}</span>
      </div>
      {% endif %}
    </div>
    {% elif results.ag_error is defined %}
    <div class="error">{{ results.ag_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Osmolar Gap</h2>
    <div class="formula">OG = Osm_measured − (2×Na + glucose/18 + BUN/2.8)</div>
    <form method="POST" action="/#og">
      <input type="hidden" name="calc" value="og">
      <div class="field"><label>Measured Osmolality (mOsm/kg)</label>
        <input type="number" name="osm" value="{{ form.osm or '' }}" placeholder="290"></div>
      <div class="field"><label>Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="og_na" value="{{ form.og_na or '' }}" placeholder="140"></div>
      <div class="field"><label>Glucose (mg/dL)</label>
        <input type="number" name="og_glucose" value="{{ form.og_glucose or '' }}" placeholder="90"></div>
      <div class="field"><label>BUN (mg/dL)</label>
        <input type="number" name="og_bun" value="{{ form.og_bun or '' }}" placeholder="14"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.og is defined %}
    <div class="result" id="og">
      <span class="val">{{ results.og }}</span><span class="unit">mOsm/kg</span>
      <div class="interp {{ results.og_cls }}">{{ results.og_interp }}</div>
    </div>
    {% elif results.og_error is defined %}
    <div class="error">{{ results.og_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Corrected Calcium</h2>
    <div class="formula">Ca_corr = Ca + 0.8 × (4.0 − albumin)</div>
    <form method="POST" action="/#ca">
      <input type="hidden" name="calc" value="ca">
      <div class="field"><label>Measured Calcium (mg/dL)</label>
        <input type="number" name="calcium" step="0.1" value="{{ form.calcium or '' }}" placeholder="8.5"></div>
      <div class="field"><label>Albumin (g/dL)</label>
        <input type="number" name="ca_albumin" step="0.1" value="{{ form.ca_albumin or '' }}" placeholder="4.0"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.ca is defined %}
    <div class="result" id="ca">
      <span class="val">{{ results.ca }}</span><span class="unit">mg/dL</span>
      <div class="interp {{ results.ca_cls }}">{{ results.ca_interp }}</div>
    </div>
    {% elif results.ca_error is defined %}
    <div class="error">{{ results.ca_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Winter's Formula</h2>
    <div class="formula">Expected PaCO₂ = 1.5 × HCO₃⁻ + 8 (± 2)</div>
    <form method="POST" action="/#wf">
      <input type="hidden" name="calc" value="wf">
      <div class="field"><label>Bicarbonate HCO₃⁻ (mEq/L)</label>
        <input type="number" name="wf_hco3" step="0.1" value="{{ form.wf_hco3 or '' }}" placeholder="12"></div>
      <div class="field"><label>Measured PaCO₂ (mmHg, optional)</label>
        <input type="number" name="wf_paco2" step="0.1" value="{{ form.wf_paco2 or '' }}" placeholder="26"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.wf is defined %}
    <div class="result" id="wf">
      <span class="val">{{ results.wf }}</span><span class="unit">mmHg expected</span>
      {% if results.wf_interp is defined %}
      <div class="interp {{ results.wf_cls }}">{{ results.wf_interp }}</div>
      {% endif %}
    </div>
    {% elif results.wf_error is defined %}
    <div class="error">{{ results.wf_error }}</div>
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
      <div class="field"><label>Bicarbonate HCO₃⁻ (mEq/L, &lt; 24)</label>
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
    <div class="formula">A–a = FiO₂ × (760 − 47) − PaCO₂/0.8 − PaO₂</div>
    <form method="POST" action="/#aa">
      <input type="hidden" name="calc" value="aa">
      <div class="field"><label>PaO₂ (mmHg)</label>
        <input type="number" name="aa_pao2" value="{{ form.aa_pao2 or '' }}" placeholder="90"></div>
      <div class="field"><label>PaCO₂ (mmHg)</label>
        <input type="number" name="aa_paco2" value="{{ form.aa_paco2 or '' }}" placeholder="40"></div>
      <div class="field"><label>FiO₂ (0.21 – 1.0)</label>
        <input type="number" name="aa_fio2" step="0.01" value="{{ form.aa_fio2 or '' }}" placeholder="0.21"></div>
      <div class="field"><label>Age (years, optional — for expected normal)</label>
        <input type="number" name="aa_age" value="{{ form.aa_age or '' }}" placeholder="40"></div>
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
    <h2>Corrected Sodium</h2>
    <div class="formula">Na_corr = Na⁺ + 1.6 × (glucose − 100) / 100</div>
    <form method="POST" action="/#cna">
      <input type="hidden" name="calc" value="cna">
      <div class="field"><label>Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="cna_na" value="{{ form.cna_na or '' }}" placeholder="130"></div>
      <div class="field"><label>Glucose (mg/dL)</label>
        <input type="number" name="cna_glucose" value="{{ form.cna_glucose or '' }}" placeholder="600"></div>
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
    <h2>Free Water Deficit</h2>
    <div class="formula">FWD = TBW × (Na⁺ / 140 − 1), TBW = wt × 0.6 (M) / 0.5 (F)</div>
    <form method="POST" action="/#fwd">
      <input type="hidden" name="calc" value="fwd">
      <div class="field"><label>Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="fwd_na" value="{{ form.fwd_na or '' }}" placeholder="160"></div>
      <div class="field"><label>Weight (kg)</label>
        <input type="number" name="fwd_weight" value="{{ form.fwd_weight or '' }}" placeholder="70"></div>
      <div class="field"><label>Sex</label>
        <select name="fwd_sex">
          <option value="male" {% if form.fwd_sex == 'male' %}selected{% endif %}>Male</option>
          <option value="female" {% if form.fwd_sex == 'female' %}selected{% endif %}>Female</option>
        </select>
      </div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.fwd is defined %}
    <div class="result" id="fwd">
      <span class="val">{{ results.fwd }}</span><span class="unit">L</span>
      <div class="interp {{ results.fwd_cls }}">{{ results.fwd_interp }}</div>
    </div>
    {% elif results.fwd_error is defined %}
    <div class="error">{{ results.fwd_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Ideal Body Weight &amp; Tidal Volume</h2>
    <div class="formula">IBW = 50 (M) / 45.5 (F) + 2.3 × (height_in − 60); Vt 6–8 mL/kg IBW</div>
    <form method="POST" action="/#ibw">
      <input type="hidden" name="calc" value="ibw">
      <div class="field"><label>Height (cm)</label>
        <input type="number" name="ibw_height" step="0.1" value="{{ form.ibw_height or '' }}" placeholder="175"></div>
      <div class="field"><label>Sex</label>
        <select name="ibw_sex">
          <option value="male" {% if form.ibw_sex == 'male' %}selected{% endif %}>Male</option>
          <option value="female" {% if form.ibw_sex == 'female' %}selected{% endif %}>Female</option>
        </select>
      </div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.ibw is defined %}
    <div class="result" id="ibw">
      <span class="val">{{ results.ibw }}</span><span class="unit">kg</span>
      <div class="interp {{ results.ibw_cls }}">{{ results.ibw_interp }}</div>
    </div>
    {% elif results.ibw_error is defined %}
    <div class="error">{{ results.ibw_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Shock Index</h2>
    <div class="formula">SI = HR / SBP</div>
    <form method="POST" action="/#si">
      <input type="hidden" name="calc" value="si">
      <div class="field"><label>Heart Rate (bpm)</label>
        <input type="number" name="si_hr" value="{{ form.si_hr or '' }}" placeholder="110"></div>
      <div class="field"><label>Systolic BP (mmHg)</label>
        <input type="number" name="si_sbp" value="{{ form.si_sbp or '' }}" placeholder="100"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.si is defined %}
    <div class="result" id="si">
      <span class="val">{{ results.si }}</span>
      <div class="interp {{ results.si_cls }}">{{ results.si_interp }}</div>
    </div>
    {% elif results.si_error is defined %}
    <div class="error">{{ results.si_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>ROX Index</h2>
    <div class="formula">ROX = (SpO₂ / FiO₂) / RR</div>
    <form method="POST" action="/#rox">
      <input type="hidden" name="calc" value="rox">
      <div class="field"><label>SpO₂ (%)</label>
        <input type="number" name="rox_spo2" value="{{ form.rox_spo2 or '' }}" placeholder="92"></div>
      <div class="field"><label>FiO₂ (0.21 – 1.0)</label>
        <input type="number" name="rox_fio2" step="0.01" value="{{ form.rox_fio2 or '' }}" placeholder="0.5"></div>
      <div class="field"><label>Respiratory Rate (breaths/min)</label>
        <input type="number" name="rox_rr" value="{{ form.rox_rr or '' }}" placeholder="24"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.rox is defined %}
    <div class="result" id="rox">
      <span class="val">{{ results.rox }}</span>
      <div class="interp {{ results.rox_cls }}">{{ results.rox_interp }}</div>
    </div>
    {% elif results.rox_error is defined %}
    <div class="error">{{ results.rox_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Driving Pressure</h2>
    <div class="formula">ΔP = Pplat − PEEP</div>
    <form method="POST" action="/#dp">
      <input type="hidden" name="calc" value="dp">
      <div class="field"><label>Plateau Pressure (cmH₂O)</label>
        <input type="number" name="dp_pplat" step="0.5" value="{{ form.dp_pplat or '' }}" placeholder="25"></div>
      <div class="field"><label>PEEP (cmH₂O)</label>
        <input type="number" name="dp_peep" step="0.5" value="{{ form.dp_peep or '' }}" placeholder="10"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.dp is defined %}
    <div class="result" id="dp">
      <span class="val">{{ results.dp }}</span><span class="unit">cmH₂O</span>
      <div class="interp {{ results.dp_cls }}">{{ results.dp_interp }}</div>
    </div>
    {% elif results.dp_error is defined %}
    <div class="error">{{ results.dp_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Static Compliance</h2>
    <div class="formula">Cstat = Vt / (Pplat − PEEP)</div>
    <form method="POST" action="/#cs">
      <input type="hidden" name="calc" value="cs">
      <div class="field"><label>Tidal Volume (mL)</label>
        <input type="number" name="cs_vt" value="{{ form.cs_vt or '' }}" placeholder="450"></div>
      <div class="field"><label>Plateau Pressure (cmH₂O)</label>
        <input type="number" name="cs_pplat" step="0.5" value="{{ form.cs_pplat or '' }}" placeholder="22"></div>
      <div class="field"><label>PEEP (cmH₂O)</label>
        <input type="number" name="cs_peep" step="0.5" value="{{ form.cs_peep or '' }}" placeholder="10"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.cs is defined %}
    <div class="result" id="cs">
      <span class="val">{{ results.cs }}</span><span class="unit">mL/cmH₂O</span>
      <div class="interp {{ results.cs_cls }}">{{ results.cs_interp }}</div>
    </div>
    {% elif results.cs_error is defined %}
    <div class="error">{{ results.cs_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Oxygenation Index</h2>
    <div class="formula">OI = FiO₂ × MAWP × 100 / PaO₂</div>
    <form method="POST" action="/#oi">
      <input type="hidden" name="calc" value="oi">
      <div class="field"><label>FiO₂ (0.21 – 1.0)</label>
        <input type="number" name="oi_fio2" step="0.01" value="{{ form.oi_fio2 or '' }}" placeholder="0.6"></div>
      <div class="field"><label>Mean Airway Pressure (cmH₂O)</label>
        <input type="number" name="oi_mawp" step="0.5" value="{{ form.oi_mawp or '' }}" placeholder="15"></div>
      <div class="field"><label>PaO₂ (mmHg)</label>
        <input type="number" name="oi_pao2" value="{{ form.oi_pao2 or '' }}" placeholder="80"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.oi is defined %}
    <div class="result" id="oi">
      <span class="val">{{ results.oi }}</span>
      <div class="interp {{ results.oi_cls }}">{{ results.oi_interp }}</div>
    </div>
    {% elif results.oi_error is defined %}
    <div class="error">{{ results.oi_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>S/F Ratio</h2>
    <div class="formula">S/F = SpO₂ / FiO₂</div>
    <form method="POST" action="/#sf">
      <input type="hidden" name="calc" value="sf">
      <div class="field"><label>SpO₂ (%)</label>
        <input type="number" name="sf_spo2" value="{{ form.sf_spo2 or '' }}" placeholder="92"></div>
      <div class="field"><label>FiO₂ (0.21 – 1.0)</label>
        <input type="number" name="sf_fio2" step="0.01" value="{{ form.sf_fio2 or '' }}" placeholder="0.5"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.sf is defined %}
    <div class="result" id="sf">
      <span class="val">{{ results.sf }}</span>
      <div class="interp {{ results.sf_cls }}">{{ results.sf_interp }}</div>
    </div>
    {% elif results.sf_error is defined %}
    <div class="error">{{ results.sf_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Mechanical Power</h2>
    <div class="formula">MP = 0.098 × RR × Vt(L) × (Ppeak − ΔP/2)</div>
    <form method="POST" action="/#mp">
      <input type="hidden" name="calc" value="mp">
      <div class="field"><label>Respiratory Rate (breaths/min)</label>
        <input type="number" name="mp_rr" value="{{ form.mp_rr or '' }}" placeholder="20"></div>
      <div class="field"><label>Tidal Volume (mL)</label>
        <input type="number" name="mp_vt" value="{{ form.mp_vt or '' }}" placeholder="450"></div>
      <div class="field"><label>Peak Pressure (cmH₂O)</label>
        <input type="number" name="mp_ppeak" step="0.5" value="{{ form.mp_ppeak or '' }}" placeholder="28"></div>
      <div class="field"><label>Plateau Pressure (cmH₂O)</label>
        <input type="number" name="mp_pplat" step="0.5" value="{{ form.mp_pplat or '' }}" placeholder="22"></div>
      <div class="field"><label>PEEP (cmH₂O)</label>
        <input type="number" name="mp_peep" step="0.5" value="{{ form.mp_peep or '' }}" placeholder="10"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.mp is defined %}
    <div class="result" id="mp">
      <span class="val">{{ results.mp }}</span><span class="unit">J/min</span>
      <div class="interp {{ results.mp_cls }}">{{ results.mp_interp }}</div>
    </div>
    {% elif results.mp_error is defined %}
    <div class="error">{{ results.mp_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Fractional Excretion of Sodium</h2>
    <div class="formula">FENa = (U_Na × P_Cr) / (P_Na × U_Cr) × 100</div>
    <form method="POST" action="/#fena">
      <input type="hidden" name="calc" value="fena">
      <div class="field"><label>Urine Sodium (mEq/L)</label>
        <input type="number" name="fena_una" value="{{ form.fena_una or '' }}" placeholder="20"></div>
      <div class="field"><label>Plasma Sodium (mEq/L)</label>
        <input type="number" name="fena_pna" value="{{ form.fena_pna or '' }}" placeholder="140"></div>
      <div class="field"><label>Urine Creatinine (mg/dL)</label>
        <input type="number" name="fena_ucr" step="0.1" value="{{ form.fena_ucr or '' }}" placeholder="100"></div>
      <div class="field"><label>Plasma Creatinine (mg/dL)</label>
        <input type="number" name="fena_pcr" step="0.1" value="{{ form.fena_pcr or '' }}" placeholder="2.0"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.fena is defined %}
    <div class="result" id="fena">
      <span class="val">{{ results.fena }}</span><span class="unit">%</span>
      <div class="interp {{ results.fena_cls }}">{{ results.fena_interp }}</div>
    </div>
    {% elif results.fena_error is defined %}
    <div class="error">{{ results.fena_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Fractional Excretion of Urea</h2>
    <div class="formula">FEUrea = (U_urea × P_Cr) / (P_urea × U_Cr) × 100</div>
    <form method="POST" action="/#feu">
      <input type="hidden" name="calc" value="feu">
      <div class="field"><label>Urine Urea Nitrogen (mg/dL)</label>
        <input type="number" name="feu_uurea" value="{{ form.feu_uurea or '' }}" placeholder="300"></div>
      <div class="field"><label>Plasma BUN (mg/dL)</label>
        <input type="number" name="feu_purea" value="{{ form.feu_purea or '' }}" placeholder="40"></div>
      <div class="field"><label>Urine Creatinine (mg/dL)</label>
        <input type="number" name="feu_ucr" step="0.1" value="{{ form.feu_ucr or '' }}" placeholder="100"></div>
      <div class="field"><label>Plasma Creatinine (mg/dL)</label>
        <input type="number" name="feu_pcr" step="0.1" value="{{ form.feu_pcr or '' }}" placeholder="2.0"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.feu is defined %}
    <div class="result" id="feu">
      <span class="val">{{ results.feu }}</span><span class="unit">%</span>
      <div class="interp {{ results.feu_cls }}">{{ results.feu_interp }}</div>
    </div>
    {% elif results.feu_error is defined %}
    <div class="error">{{ results.feu_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Corrected QT (Bazett)</h2>
    <div class="formula">QTc = QT / √(60 / HR)</div>
    <form method="POST" action="/#qtc">
      <input type="hidden" name="calc" value="qtc">
      <div class="field"><label>QT Interval (ms)</label>
        <input type="number" name="qtc_qt" value="{{ form.qtc_qt or '' }}" placeholder="400"></div>
      <div class="field"><label>Heart Rate (bpm)</label>
        <input type="number" name="qtc_hr" value="{{ form.qtc_hr or '' }}" placeholder="80"></div>
      <div class="field"><label>Sex</label>
        <select name="qtc_sex">
          <option value="male" {% if form.qtc_sex == 'male' %}selected{% endif %}>Male</option>
          <option value="female" {% if form.qtc_sex == 'female' %}selected{% endif %}>Female</option>
        </select>
      </div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.qtc is defined %}
    <div class="result" id="qtc">
      <span class="val">{{ results.qtc }}</span><span class="unit">ms</span>
      <div class="interp {{ results.qtc_cls }}">{{ results.qtc_interp }}</div>
    </div>
    {% elif results.qtc_error is defined %}
    <div class="error">{{ results.qtc_error }}</div>
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
  <span>gen-wild-0019 · 2026-11-24 · Added: QTc (Bazett)</span>
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

def _og_interp(v):
    if v < 10:   return "Normal (< 10 mOsm/kg)", "normal"
    if v < 20:   return "Borderline elevated (10–20)", "warn"
    return "Elevated — consider toxic alcohol", "crit"

def _ca_interp(v):
    if v < 8.5:  return "Low — hypocalcaemia", "warn"
    if v <= 10.5: return "Normal (8.5–10.5 mg/dL)", "normal"
    return "Elevated — hypercalcaemia", "warn"

def _wf_interp(paco2, low, high):
    if paco2 < low:  return "Below expected — concomitant respiratory alkalosis", "warn"
    if paco2 > high: return "Above expected — concomitant respiratory acidosis", "crit"
    return "Appropriate respiratory compensation", "normal"

def _dr_interp(v):
    if v < 0.4:  return "< 0.4 — hyperchloraemic normal AG acidosis", "warn"
    if v < 0.8:  return "0.4–0.8 — mixed high AG + normal AG acidosis", "warn"
    if v <= 2:   return "0.8–2 — pure high AG acidosis", "normal"
    return "> 2 — concurrent metabolic alkalosis", "crit"

def _aa_interp(v, age=None):
    upper = age / 4 + 4 if age is not None else 15
    if v <= upper: return f"Normal (≤ {upper:g} mmHg expected)", "normal"
    if v <= upper * 2: return "Elevated — V/Q mismatch, shunt or diffusion defect", "warn"
    return "Markedly elevated — significant shunt or V/Q mismatch", "crit"

def _cna_interp(v):
    if v < 135:  return "Low — true hyponatraemia", "warn"
    if v <= 145: return "Normal (135–145 mEq/L)", "normal"
    return "Elevated — hypernatraemia / free water deficit", "warn"

def _fwd_interp(v):
    if v <= 0:   return "No free water deficit (Na ≤ 140)", "normal"
    if v < 4:    return "Mild deficit — correct Na ≤ 10 mEq/L per 24 h", "warn"
    return "Significant deficit — correct Na ≤ 10 mEq/L per 24 h", "crit"

def _ibw_interp(v):
    if v <= 0: return "Height too low for Devine formula", "warn"
    return f"Lung-protective Vt: {round(v * 6)}–{round(v * 8)} mL (6–8 mL/kg IBW)", "normal"

def _si_interp(v):
    if v < 0.5:  return "Low (< 0.5)", "warn"
    if v <= 0.7: return "Normal (0.5–0.7)", "normal"
    if v <= 1.0: return "Elevated (0.7–1.0) — monitor closely", "warn"
    return "> 1.0 — haemodynamic instability / occult shock", "crit"

def _rox_interp(v):
    if v >= 4.88: return "≥ 4.88 — low risk of HFNC failure", "normal"
    if v >= 3.85: return "3.85–4.88 — intermediate, reassess in 1–2 h", "warn"
    return "< 3.85 — high risk of HFNC failure / intubation", "crit"

def _dp_interp(v):
    if v < 15:   return "< 15 cmH₂O — within lung-protective target", "normal"
    return "≥ 15 cmH₂O — associated with higher ARDS mortality", "crit"

def _cs_interp(v):
    if v < 40:   return "< 40 mL/cmH₂O — reduced compliance (ARDS, fibrosis, oedema)", "crit"
    if v < 50:   return "40–50 mL/cmH₂O — mildly reduced", "warn"
    return "≥ 50 mL/cmH₂O — normal", "normal"

def _oi_interp(v):
    if v < 15:   return "< 15 — mild hypoxaemia", "normal"
    if v <= 25:  return "15–25 — moderate hypoxaemic respiratory failure", "warn"
    return "> 25 — severe; consider rescue therapies (prone, ECMO referral)", "crit"

def _sf_interp(v, spo2):
    note = " (SpO₂ > 97% — S/F unreliable, titrate FiO₂ down)" if spo2 > 97 else ""
    if v <= 235: return "≤ 235 — ≈ P/F ≤ 200, moderate–severe hypoxaemia" + note, "crit"
    if v <= 315: return "236–315 — ≈ P/F 200–300, mild hypoxaemia" + note, "warn"
    return "> 315 — ≈ P/F > 300" + note, "normal"

def _mp_interp(v):
    if v <= 12:  return "≤ 12 J/min — within commonly cited safe range", "normal"
    if v <= 17:  return "12–17 J/min — moderate; consider lowering RR / Vt", "warn"
    return "> 17 J/min — associated with higher ARDS mortality", "crit"

def _fena_interp(v):
    if v < 1:    return "< 1% — suggests prerenal AKI (unreliable on diuretics)", "warn"
    if v <= 2:   return "1–2% — indeterminate", "warn"
    return "> 2% — suggests intrinsic renal injury (ATN)", "crit"

def _feu_interp(v):
    if v < 35:   return "< 35% — suggests prerenal AKI (reliable on diuretics)", "warn"
    if v <= 50:  return "35–50% — indeterminate", "warn"
    return "> 50% — suggests intrinsic renal injury (ATN)", "crit"

def _qtc_interp(v, sex):
    upper = 470 if sex == "female" else 450
    if v > 500:   return "> 500 ms — high risk of torsades; review QT-prolonging drugs, K⁺, Mg²⁺", "crit"
    if v > upper: return f"> {upper} ms — prolonged QTc", "warn"
    return f"≤ {upper} ms — normal (Bazett overcorrects at high HR)", "normal"

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
            na, cl, hco3 = float(form["na"]), float(form["cl"]), float(form["hco3"])
            v = anion_gap(na, cl, hco3)
            interp, cls = _ag_interp(v)
            results.update(ag=v, ag_interp=interp, ag_cls=cls)
            albumin_str = form.get("albumin", "").strip()
            if albumin_str:
                vc = albumin_corrected_anion_gap(na, cl, hco3, float(albumin_str))
                interpc, clsc = _ag_interp(vc)
                results.update(ag_corrected=vc, ag_corrected_interp=interpc, ag_corrected_cls=clsc)
        except Exception as e:
            results["ag_error"] = str(e)

    elif calc == "og":
        try:
            v = osmolar_gap(
                float(form["osm"]), float(form["og_na"]),
                float(form["og_glucose"]), float(form["og_bun"]),
            )
            interp, cls = _og_interp(v)
            results.update(og=v, og_interp=interp, og_cls=cls)
        except Exception as e:
            results["og_error"] = str(e)

    elif calc == "ca":
        try:
            v = corrected_calcium(float(form["calcium"]), float(form["ca_albumin"]))
            interp, cls = _ca_interp(v)
            results.update(ca=v, ca_interp=interp, ca_cls=cls)
        except Exception as e:
            results["ca_error"] = str(e)

    elif calc == "wf":
        try:
            low, high = winters_formula(float(form["wf_hco3"]))
            results["wf"] = f"{low}–{high}"
            paco2_str = form.get("wf_paco2", "").strip()
            if paco2_str:
                interp, cls = _wf_interp(float(paco2_str), low, high)
                results.update(wf_interp=interp, wf_cls=cls)
        except Exception as e:
            results["wf_error"] = str(e)

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
            age_str = form.get("aa_age", "").strip()
            interp, cls = _aa_interp(v, float(age_str) if age_str else None)
            results.update(aa=v, aa_interp=interp, aa_cls=cls)
        except Exception as e:
            results["aa_error"] = str(e)

    elif calc == "cna":
        try:
            v = corrected_sodium(float(form["cna_na"]), float(form["cna_glucose"]))
            interp, cls = _cna_interp(v)
            results.update(cna=v, cna_interp=interp, cna_cls=cls)
        except Exception as e:
            results["cna_error"] = str(e)

    elif calc == "fwd":
        try:
            v = free_water_deficit(
                float(form["fwd_na"]), float(form["fwd_weight"]), form.get("fwd_sex", "male"),
            )
            interp, cls = _fwd_interp(v)
            results.update(fwd=v, fwd_interp=interp, fwd_cls=cls)
        except Exception as e:
            results["fwd_error"] = str(e)

    elif calc == "ibw":
        try:
            v = ideal_body_weight(float(form["ibw_height"]), form.get("ibw_sex", "male"))
            interp, cls = _ibw_interp(v)
            results.update(ibw=v, ibw_interp=interp, ibw_cls=cls)
        except Exception as e:
            results["ibw_error"] = str(e)

    elif calc == "si":
        try:
            v = shock_index(float(form["si_hr"]), float(form["si_sbp"]))
            interp, cls = _si_interp(v)
            results.update(si=v, si_interp=interp, si_cls=cls)
        except Exception as e:
            results["si_error"] = str(e)

    elif calc == "rox":
        try:
            v = rox_index(float(form["rox_spo2"]), float(form["rox_fio2"]), float(form["rox_rr"]))
            interp, cls = _rox_interp(v)
            results.update(rox=v, rox_interp=interp, rox_cls=cls)
        except Exception as e:
            results["rox_error"] = str(e)

    elif calc == "dp":
        try:
            v = driving_pressure(float(form["dp_pplat"]), float(form["dp_peep"]))
            interp, cls = _dp_interp(v)
            results.update(dp=v, dp_interp=interp, dp_cls=cls)
        except Exception as e:
            results["dp_error"] = str(e)

    elif calc == "cs":
        try:
            v = static_compliance(float(form["cs_vt"]), float(form["cs_pplat"]), float(form["cs_peep"]))
            interp, cls = _cs_interp(v)
            results.update(cs=v, cs_interp=interp, cs_cls=cls)
        except Exception as e:
            results["cs_error"] = str(e)

    elif calc == "oi":
        try:
            v = oxygenation_index(float(form["oi_fio2"]), float(form["oi_mawp"]), float(form["oi_pao2"]))
            interp, cls = _oi_interp(v)
            results.update(oi=v, oi_interp=interp, oi_cls=cls)
        except Exception as e:
            results["oi_error"] = str(e)

    elif calc == "sf":
        try:
            spo2 = float(form["sf_spo2"])
            v = sf_ratio(spo2, float(form["sf_fio2"]))
            interp, cls = _sf_interp(v, spo2)
            results.update(sf=v, sf_interp=interp, sf_cls=cls)
        except Exception as e:
            results["sf_error"] = str(e)

    elif calc == "mp":
        try:
            v = mechanical_power(
                float(form["mp_rr"]), float(form["mp_vt"]), float(form["mp_ppeak"]),
                float(form["mp_pplat"]), float(form["mp_peep"]),
            )
            interp, cls = _mp_interp(v)
            results.update(mp=v, mp_interp=interp, mp_cls=cls)
        except Exception as e:
            results["mp_error"] = str(e)

    elif calc == "fena":
        try:
            v = fractional_excretion_sodium(
                float(form["fena_una"]), float(form["fena_pna"]),
                float(form["fena_ucr"]), float(form["fena_pcr"]),
            )
            interp, cls = _fena_interp(v)
            results.update(fena=v, fena_interp=interp, fena_cls=cls)
        except Exception as e:
            results["fena_error"] = str(e)

    elif calc == "feu":
        try:
            v = fractional_excretion_urea(
                float(form["feu_uurea"]), float(form["feu_purea"]),
                float(form["feu_ucr"]), float(form["feu_pcr"]),
            )
            interp, cls = _feu_interp(v)
            results.update(feu=v, feu_interp=interp, feu_cls=cls)
        except Exception as e:
            results["feu_error"] = str(e)

    elif calc == "qtc":
        try:
            v = qtc_bazett(float(form["qtc_qt"]), float(form["qtc_hr"]))
            interp, cls = _qtc_interp(v, form.get("qtc_sex", "male"))
            results.update(qtc=v, qtc_interp=interp, qtc_cls=cls)
        except Exception as e:
            results["qtc_error"] = str(e)

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
    app.run(debug=True, port=3001)
