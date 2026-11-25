"""
ICU Calculator — Flask app with Jinja2 template inline.
Single file: routes, logic calls, and HTML all live here.

Separation event: if an agent splits the template into templates/ or adds
a .js file with formula logic, metrics.py will flag it.
"""

from flask import Flask, request, render_template_string
from calculator import (
    mean_arterial_pressure, pf_ratio, anion_gap,
    creatinine_clearance, glasgow_coma_scale, curb65,
    corrected_sodium, corrected_calcium, serum_osmolality, qsofa, shock_index, aa_gradient, winters_formula, delta_ratio, free_water_deficit, ideal_body_weight, rsbi, oxygenation_index, driving_pressure, rox_index, qtc_bazett, osmolal_gap, albumin_corrected_anion_gap, parkland_formula, DISCLAIMER,
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
    <h2>Glasgow Coma Scale</h2>
    <div class="formula">GCS = Eye (1–4) + Verbal (1–5) + Motor (1–6)</div>
    <form method="POST" action="/#gcs">
      <input type="hidden" name="calc" value="gcs">
      <div class="field"><label>Eye Opening</label>
        <select name="gcs_eye">
          <option value="1" {% if form.gcs_eye == '1' %}selected{% endif %}>1 — None</option>
          <option value="2" {% if form.gcs_eye == '2' %}selected{% endif %}>2 — To Pain</option>
          <option value="3" {% if form.gcs_eye == '3' %}selected{% endif %}>3 — To Voice</option>
          <option value="4" {% if form.gcs_eye == '4' %}selected{% endif %}>4 — Spontaneous</option>
        </select>
      </div>
      <div class="field"><label>Verbal Response</label>
        <select name="gcs_verbal">
          <option value="1" {% if form.gcs_verbal == '1' %}selected{% endif %}>1 — None</option>
          <option value="2" {% if form.gcs_verbal == '2' %}selected{% endif %}>2 — Sounds</option>
          <option value="3" {% if form.gcs_verbal == '3' %}selected{% endif %}>3 — Words</option>
          <option value="4" {% if form.gcs_verbal == '4' %}selected{% endif %}>4 — Confused</option>
          <option value="5" {% if form.gcs_verbal == '5' %}selected{% endif %}>5 — Oriented</option>
        </select>
      </div>
      <div class="field"><label>Motor Response</label>
        <select name="gcs_motor">
          <option value="1" {% if form.gcs_motor == '1' %}selected{% endif %}>1 — None</option>
          <option value="2" {% if form.gcs_motor == '2' %}selected{% endif %}>2 — Extension</option>
          <option value="3" {% if form.gcs_motor == '3' %}selected{% endif %}>3 — Flexion</option>
          <option value="4" {% if form.gcs_motor == '4' %}selected{% endif %}>4 — Withdrawal</option>
          <option value="5" {% if form.gcs_motor == '5' %}selected{% endif %}>5 — Localises Pain</option>
          <option value="6" {% if form.gcs_motor == '6' %}selected{% endif %}>6 — Obeys Commands</option>
        </select>
      </div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.gcs is defined %}
    <div class="result" id="gcs">
      <span class="val">{{ results.gcs }}</span><span class="unit">/ 15</span>
      <div class="interp {{ results.gcs_cls }}">{{ results.gcs_interp }}</div>
    </div>
    {% elif results.gcs_error is defined %}
    <div class="error">{{ results.gcs_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>CURB-65</h2>
    <div class="formula">Pneumonia severity: Confusion · Urea · RR · BP · Age≥65</div>
    <form method="POST" action="/#curb65">
      <input type="hidden" name="calc" value="curb65">
      <div class="field"><label>Confusion (new onset)</label>
        <select name="confusion">
          <option value="0" {% if form.confusion == '0' %}selected{% endif %}>No</option>
          <option value="1" {% if form.confusion == '1' %}selected{% endif %}>Yes</option>
        </select>
      </div>
      <div class="field"><label>BUN &gt; 19 mg/dL (Urea &gt; 7 mmol/L)</label>
        <select name="urea_high">
          <option value="0" {% if form.urea_high == '0' %}selected{% endif %}>No</option>
          <option value="1" {% if form.urea_high == '1' %}selected{% endif %}>Yes</option>
        </select>
      </div>
      <div class="field"><label>Respiratory Rate (breaths/min)</label>
        <input type="number" name="resp_rate" value="{{ form.resp_rate or '' }}" placeholder="20"></div>
      <div class="field"><label>Systolic BP (mmHg)</label>
        <input type="number" name="curb_sbp" value="{{ form.curb_sbp or '' }}" placeholder="120"></div>
      <div class="field"><label>Diastolic BP (mmHg)</label>
        <input type="number" name="curb_dbp" value="{{ form.curb_dbp or '' }}" placeholder="80"></div>
      <div class="field"><label>Age (years)</label>
        <input type="number" name="curb_age" value="{{ form.curb_age or '' }}" placeholder="50"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.curb65 is defined %}
    <div class="result" id="curb65">
      <span class="val">{{ results.curb65 }}</span><span class="unit">/ 5</span>
      <div class="interp {{ results.curb65_cls }}">{{ results.curb65_interp }}</div>
    </div>
    {% elif results.curb65_error is defined %}
    <div class="error">{{ results.curb65_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Corrected Sodium</h2>
    <div class="formula">Na_corr = Na_measured + 1.6 × (Glucose − 100) / 100</div>
    <form method="POST" action="/#corrna">
      <input type="hidden" name="calc" value="corrna">
      <div class="field"><label>Measured Na⁺ (mEq/L)</label>
        <input type="number" name="measured_na" step="0.1" value="{{ form.measured_na or '' }}" placeholder="135"></div>
      <div class="field"><label>Serum Glucose (mg/dL)</label>
        <input type="number" name="glucose" value="{{ form.glucose or '' }}" placeholder="100"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.corrna is defined %}
    <div class="result" id="corrna">
      <span class="val">{{ results.corrna }}</span><span class="unit">mEq/L</span>
      <div class="interp {{ results.corrna_cls }}">{{ results.corrna_interp }}</div>
    </div>
    {% elif results.corrna_error is defined %}
    <div class="error">{{ results.corrna_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Corrected Calcium</h2>
    <div class="formula">Ca_corr = Ca_total + 0.8 × (4.0 − Albumin)</div>
    <form method="POST" action="/#corrca">
      <input type="hidden" name="calc" value="corrca">
      <div class="field"><label>Total Calcium (mg/dL)</label>
        <input type="number" name="total_ca" step="0.1" value="{{ form.total_ca or '' }}" placeholder="9.0"></div>
      <div class="field"><label>Serum Albumin (g/dL)</label>
        <input type="number" name="albumin" step="0.1" value="{{ form.albumin or '' }}" placeholder="4.0"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.corrca is defined %}
    <div class="result" id="corrca">
      <span class="val">{{ results.corrca }}</span><span class="unit">mg/dL</span>
      <div class="interp {{ results.corrca_cls }}">{{ results.corrca_interp }}</div>
    </div>
    {% elif results.corrca_error is defined %}
    <div class="error">{{ results.corrca_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Serum Osmolality</h2>
    <div class="formula">Osm = 2 × Na⁺ + Glucose / 18 + BUN / 2.8</div>
    <form method="POST" action="/#osm">
      <input type="hidden" name="calc" value="osm">
      <div class="field"><label>Sodium Na⁺ (mEq/L)</label>
        <input type="number" name="osm_na" step="0.1" value="{{ form.osm_na or '' }}" placeholder="140"></div>
      <div class="field"><label>Serum Glucose (mg/dL)</label>
        <input type="number" name="osm_glucose" value="{{ form.osm_glucose or '' }}" placeholder="90"></div>
      <div class="field"><label>BUN (mg/dL)</label>
        <input type="number" name="osm_bun" step="0.1" value="{{ form.osm_bun or '' }}" placeholder="14"></div>
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
    <h2>qSOFA</h2>
    <div class="formula">Sepsis screen: RR ≥ 22 · SBP ≤ 100 · Altered mentation</div>
    <form method="POST" action="/#qsofa">
      <input type="hidden" name="calc" value="qsofa">
      <div class="field"><label>Respiratory Rate (breaths/min)</label>
        <input type="number" name="qsofa_rr" value="{{ form.qsofa_rr or '' }}" placeholder="18"></div>
      <div class="field"><label>Systolic BP (mmHg)</label>
        <input type="number" name="qsofa_sbp" value="{{ form.qsofa_sbp or '' }}" placeholder="120"></div>
      <div class="field"><label>Altered mentation (GCS &lt; 15)</label>
        <select name="qsofa_ams">
          <option value="0" {% if form.qsofa_ams == '0' %}selected{% endif %}>No</option>
          <option value="1" {% if form.qsofa_ams == '1' %}selected{% endif %}>Yes</option>
        </select>
      </div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.qsofa is defined %}
    <div class="result" id="qsofa">
      <span class="val">{{ results.qsofa }}</span><span class="unit">/ 3</span>
      <div class="interp {{ results.qsofa_cls }}">{{ results.qsofa_interp }}</div>
    </div>
    {% elif results.qsofa_error is defined %}
    <div class="error">{{ results.qsofa_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Shock Index</h2>
    <div class="formula">SI = Heart Rate / Systolic BP</div>
    <form method="POST" action="/#si">
      <input type="hidden" name="calc" value="si">
      <div class="field"><label>Heart Rate (beats/min)</label>
        <input type="number" name="si_hr" value="{{ form.si_hr or '' }}" placeholder="80"></div>
      <div class="field"><label>Systolic BP (mmHg)</label>
        <input type="number" name="si_sbp" value="{{ form.si_sbp or '' }}" placeholder="120"></div>
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
    <h2>A–a O₂ Gradient</h2>
    <div class="formula">A–a = FiO₂ × (Patm − 47) − PaCO₂ / 0.8 − PaO₂</div>
    <form method="POST" action="/#aa">
      <input type="hidden" name="calc" value="aa">
      <div class="field"><label>PaO₂ (mmHg)</label>
        <input type="number" name="aa_pao2" step="0.1" value="{{ form.aa_pao2 or '' }}" placeholder="90"></div>
      <div class="field"><label>PaCO₂ (mmHg)</label>
        <input type="number" name="aa_paco2" step="0.1" value="{{ form.aa_paco2 or '' }}" placeholder="40"></div>
      <div class="field"><label>FiO₂ (0.21 – 1.0)</label>
        <input type="number" name="aa_fio2" step="0.01" value="{{ form.aa_fio2 or '' }}" placeholder="0.21"></div>
      <div class="field"><label>Atmospheric pressure (mmHg)</label>
        <input type="number" name="aa_patm" value="{{ form.aa_patm or '' }}" placeholder="760"></div>
      <div class="field"><label>Age (years, for expected normal)</label>
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
    <h2>Winter's Formula</h2>
    <div class="formula">Expected PaCO₂ = 1.5 × HCO₃ + 8 (± 2)</div>
    <form method="POST" action="/#wf">
      <input type="hidden" name="calc" value="wf">
      <div class="field"><label>HCO₃ (mEq/L)</label>
        <input type="number" name="wf_hco3" step="0.1" value="{{ form.wf_hco3 or '' }}" placeholder="12"></div>
      <div class="field"><label>Measured PaCO₂ (mmHg, optional)</label>
        <input type="number" name="wf_paco2" step="0.1" value="{{ form.wf_paco2 or '' }}" placeholder="26"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.wf is defined %}
    <div class="result" id="wf">
      <span class="val">{{ results.wf }}</span><span class="unit">mmHg</span>
      <div class="interp {{ results.wf_cls }}">{{ results.wf_interp }}</div>
    </div>
    {% elif results.wf_error is defined %}
    <div class="error">{{ results.wf_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Delta–Delta Ratio</h2>
    <div class="formula">Δ/Δ = (AG − 12) / (24 − HCO₃)</div>
    <form method="POST" action="/#dr">
      <input type="hidden" name="calc" value="dr">
      <div class="field"><label>Na⁺ (mEq/L)</label>
        <input type="number" name="dr_na" step="0.1" value="{{ form.dr_na or '' }}" placeholder="140"></div>
      <div class="field"><label>Cl⁻ (mEq/L)</label>
        <input type="number" name="dr_cl" step="0.1" value="{{ form.dr_cl or '' }}" placeholder="100"></div>
      <div class="field"><label>HCO₃ (mEq/L)</label>
        <input type="number" name="dr_hco3" step="0.1" value="{{ form.dr_hco3 or '' }}" placeholder="12"></div>
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
    <h2>Free Water Deficit</h2>
    <div class="formula">FWD = TBW × (Na⁺ / 140 − 1)</div>
    <form method="POST" action="/#fwd">
      <input type="hidden" name="calc" value="fwd">
      <div class="field"><label>Na⁺ (mEq/L)</label>
        <input type="number" name="fwd_na" step="0.1" value="{{ form.fwd_na or '' }}" placeholder="160"></div>
      <div class="field"><label>Weight (kg)</label>
        <input type="number" name="fwd_weight" step="0.1" value="{{ form.fwd_weight or '' }}" placeholder="70"></div>
      <div class="field"><label>Age (years)</label>
        <input type="number" name="fwd_age" value="{{ form.fwd_age or '' }}" placeholder="40"></div>
      <div class="field"><label>Sex</label>
        <select name="fwd_sex">
          <option value="male" {% if form.fwd_sex != 'female' %}selected{% endif %}>Male</option>
          <option value="female" {% if form.fwd_sex == 'female' %}selected{% endif %}>Female</option>
        </select></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.fwd is defined %}
    <div class="result" id="fwd">
      <span class="val">{{ results.fwd }} L</span>
      <div class="interp {{ results.fwd_cls }}">{{ results.fwd_interp }}</div>
    </div>
    {% elif results.fwd_error is defined %}
    <div class="error">{{ results.fwd_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Ideal Body Weight &amp; Tidal Volume</h2>
    <div class="formula">IBW = 50 (♂) / 45.5 (♀) + 0.91 × (height − 152.4); VT = 6 mL/kg IBW</div>
    <form method="POST" action="/#ibw">
      <input type="hidden" name="calc" value="ibw">
      <div class="field"><label>Height (cm)</label>
        <input type="number" name="ibw_height" step="0.1" value="{{ form.ibw_height or '' }}" placeholder="175"></div>
      <div class="field"><label>Sex</label>
        <select name="ibw_sex">
          <option value="male" {% if form.ibw_sex != 'female' %}selected{% endif %}>Male</option>
          <option value="female" {% if form.ibw_sex == 'female' %}selected{% endif %}>Female</option>
        </select></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.ibw is defined %}
    <div class="result" id="ibw">
      <span class="val">{{ results.ibw }} kg</span>
      <div class="interp {{ results.ibw_cls }}">{{ results.ibw_interp }}</div>
    </div>
    {% elif results.ibw_error is defined %}
    <div class="error">{{ results.ibw_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Rapid Shallow Breathing Index</h2>
    <div class="formula">RSBI = RR / VT (L) — Yang–Tobin weaning predictor</div>
    <form method="POST" action="/#rsbi">
      <input type="hidden" name="calc" value="rsbi">
      <div class="field"><label>Respiratory rate (/min)</label>
        <input type="number" name="rsbi_rr" step="1" value="{{ form.rsbi_rr or '' }}" placeholder="25"></div>
      <div class="field"><label>Tidal volume (mL)</label>
        <input type="number" name="rsbi_vt" step="1" value="{{ form.rsbi_vt or '' }}" placeholder="500"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.rsbi is defined %}
    <div class="result" id="rsbi">
      <span class="val">{{ results.rsbi }} breaths/min/L</span>
      <div class="interp {{ results.rsbi_cls }}">{{ results.rsbi_interp }}</div>
    </div>
    {% elif results.rsbi_error is defined %}
    <div class="error">{{ results.rsbi_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>Oxygenation Index</h2>
    <div class="formula">OI = FiO2 × mean airway pressure × 100 / PaO2</div>
    <form method="POST" action="/#oi">
      <input type="hidden" name="calc" value="oi">
      <div class="field"><label>FiO2 (0–1)</label>
        <input type="number" name="oi_fio2" step="0.01" value="{{ form.oi_fio2 or '' }}" placeholder="0.6"></div>
      <div class="field"><label>Mean airway pressure (cmH2O)</label>
        <input type="number" name="oi_paw" step="0.1" value="{{ form.oi_paw or '' }}" placeholder="15"></div>
      <div class="field"><label>PaO2 (mmHg)</label>
        <input type="number" name="oi_pao2" step="1" value="{{ form.oi_pao2 or '' }}" placeholder="90"></div>
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
    <h2>Driving Pressure</h2>
    <div class="formula">ΔP = Plateau pressure − PEEP</div>
    <form method="POST" action="/#dp">
      <input type="hidden" name="calc" value="dp">
      <div class="field"><label>Plateau pressure (cmH2O)</label>
        <input type="number" name="dp_pplat" step="0.1" value="{{ form.dp_pplat or '' }}" placeholder="25"></div>
      <div class="field"><label>PEEP (cmH2O)</label>
        <input type="number" name="dp_peep" step="0.1" value="{{ form.dp_peep or '' }}" placeholder="10"></div>
      <div class="field"><label>Tidal volume (mL, optional — for static compliance)</label>
        <input type="number" name="dp_vt" step="1" value="{{ form.dp_vt or '' }}" placeholder="420"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.dp is defined %}
    <div class="result" id="dp">
      <span class="val">{{ results.dp }} cmH2O</span>
      <div class="interp {{ results.dp_cls }}">{{ results.dp_interp }}</div>
      {% if results.dp_crs is defined %}<div class="interp">Static compliance (VT / ΔP): {{ results.dp_crs }} mL/cmH2O</div>{% endif %}
    </div>
    {% elif results.dp_error is defined %}
    <div class="error">{{ results.dp_error }}</div>
    {% endif %}
  </div>

  <div class="card">
    <h2>ROX Index</h2>
    <div class="formula">ROX = (SpO2 / FiO2) / Respiratory rate</div>
    <form method="POST" action="/#rox">
      <input type="hidden" name="calc" value="rox">
      <div class="field"><label>SpO2 (%)</label>
        <input type="number" name="rox_spo2" step="1" value="{{ form.rox_spo2 or '' }}" placeholder="95"></div>
      <div class="field"><label>FiO2 (0–1)</label>
        <input type="number" name="rox_fio2" step="0.01" value="{{ form.rox_fio2 or '' }}" placeholder="0.5"></div>
      <div class="field"><label>Respiratory rate (/min)</label>
        <input type="number" name="rox_rr" step="1" value="{{ form.rox_rr or '' }}" placeholder="20"></div>
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
    <h2>QTc (Bazett)</h2>
    <div class="formula">QTc = QT / √(RR), RR = 60 / HR (s)</div>
    <form method="POST" action="/#qtc">
      <input type="hidden" name="calc" value="qtc">
      <div class="field"><label>QT interval (ms)</label>
        <input type="number" name="qtc_qt" step="1" value="{{ form.qtc_qt or '' }}" placeholder="400"></div>
      <div class="field"><label>Heart rate (/min)</label>
        <input type="number" name="qtc_hr" step="1" value="{{ form.qtc_hr or '' }}" placeholder="75"></div>
      <div class="field"><label>Sex (M/F)</label>
        <input type="text" name="qtc_sex" value="{{ form.qtc_sex or '' }}" placeholder="M"></div>
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
    <h2>Osmolal Gap</h2>
    <div class="formula">OG = Measured Osm − (2 × Na⁺ + Glucose / 18 + BUN / 2.8)</div>
    <form method="POST" action="/#og">
      <input type="hidden" name="calc" value="og">
      <div class="field"><label>Measured osmolality (mOsm/kg)</label>
        <input type="number" name="og_meas" step="0.1" value="{{ form.og_meas or '' }}" placeholder="295"></div>
      <div class="field"><label>Na⁺ (mEq/L)</label>
        <input type="number" name="og_na" step="0.1" value="{{ form.og_na or '' }}" placeholder="140"></div>
      <div class="field"><label>Glucose (mg/dL)</label>
        <input type="number" name="og_glucose" step="0.1" value="{{ form.og_glucose or '' }}" placeholder="90"></div>
      <div class="field"><label>BUN (mg/dL)</label>
        <input type="number" name="og_bun" step="0.1" value="{{ form.og_bun or '' }}" placeholder="14"></div>
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
    <h2>Albumin-Corrected Anion Gap</h2>
    <div class="formula">cAG = Na⁺ − (Cl⁻ + HCO₃⁻) + 2.5 × (4.0 − Albumin)</div>
    <form method="POST" action="/#cag">
      <input type="hidden" name="calc" value="cag">
      <div class="field"><label>Na⁺ (mEq/L)</label>
        <input type="number" name="cag_na" step="0.1" value="{{ form.cag_na or '' }}" placeholder="140"></div>
      <div class="field"><label>Cl⁻ (mEq/L)</label>
        <input type="number" name="cag_cl" step="0.1" value="{{ form.cag_cl or '' }}" placeholder="104"></div>
      <div class="field"><label>HCO₃⁻ (mEq/L)</label>
        <input type="number" name="cag_hco3" step="0.1" value="{{ form.cag_hco3 or '' }}" placeholder="24"></div>
      <div class="field"><label>Albumin (g/dL)</label>
        <input type="number" name="cag_alb" step="0.1" value="{{ form.cag_alb or '' }}" placeholder="4.0"></div>
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
    <h2>Parkland Burn Resuscitation</h2>
    <div class="formula">24 h RL = 4 mL × Weight (kg) × %TBSA — ½ in first 8 h</div>
    <form method="POST" action="/#pk">
      <input type="hidden" name="calc" value="pk">
      <div class="field"><label>Weight (kg)</label>
        <input type="number" name="pk_wt" step="0.1" value="{{ form.pk_wt or '' }}" placeholder="70"></div>
      <div class="field"><label>Burn TBSA (%, partial + full thickness)</label>
        <input type="number" name="pk_tbsa" step="0.1" value="{{ form.pk_tbsa or '' }}" placeholder="30"></div>
      <button class="btn" type="submit">Calculate</button>
    </form>
    {% if results.pk is defined %}
    <div class="result" id="pk">
      <span class="val">{{ results.pk }}</span><span class="unit">mL / 24 h</span>
      <div class="interp {{ results.pk_cls }}">{{ results.pk_interp }}</div>
    </div>
    {% elif results.pk_error is defined %}
    <div class="error">{{ results.pk_error }}</div>
    {% endif %}
  </div>

</div>

<footer>
  <span>gen-breadth-0019 · 2026-11-25 · MAP · P/F · Anion Gap · CrCl · GCS · CURB-65 · Corrected Na · Corrected Ca · Osmolality · qSOFA · Shock Index · A–a Gradient · Winter's Formula · Delta Ratio · Free Water Deficit · IBW · RSBI · OI · Driving Pressure · ROX · QTc · Osmolal Gap · Corrected AG · Parkland</span>
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

def _gcs_interp(v):
    if v <= 8:   return f"Score {v} — Severe (coma threshold ≤ 8)", "crit"
    if v <= 12:  return f"Score {v} — Moderate impairment", "warn"
    return f"Score {v} — Mild / normal (13–15)", "normal"

def _curb65_interp(v):
    if v <= 1:   return f"Score {v} — Low risk (consider outpatient)", "normal"
    if v == 2:   return f"Score {v} — Moderate risk (hospital admission)", "warn"
    return f"Score {v} — High risk (consider ICU)", "crit"

def _corrna_interp(v):
    if v < 135:  return f"{v} mEq/L — Hyponatraemia (corrected)", "warn"
    if v <= 145: return f"{v} mEq/L — Normal range", "normal"
    if v <= 155: return f"{v} mEq/L — Mild hypernatraemia", "warn"
    return f"{v} mEq/L — Severe hypernatraemia", "crit"

def _corrca_interp(v):
    if v < 7.5:   return f"{v} mg/dL — Severe hypocalcaemia", "crit"
    if v < 8.5:   return f"{v} mg/dL — Hypocalcaemia (corrected)", "warn"
    if v <= 10.5: return f"{v} mg/dL — Normal range (8.5–10.5)", "normal"
    if v < 14:    return f"{v} mg/dL — Hypercalcaemia", "warn"
    return f"{v} mg/dL — Severe hypercalcaemia (≥ 14)", "crit"

def _osm_interp(v):
    if v < 275:  return f"{v} mOsm/kg — Hypo-osmolar (< 275)", "warn"
    if v <= 295: return f"{v} mOsm/kg — Normal range (275–295)", "normal"
    if v < 320:  return f"{v} mOsm/kg — Hyperosmolar", "warn"
    return f"{v} mOsm/kg — Severe hyperosmolality (≥ 320, HHS range)", "crit"

def _qsofa_interp(v):
    if v >= 2:   return f"Score {v} — High risk of poor outcome in suspected sepsis", "crit"
    if v == 1:   return f"Score {v} — Monitor; reassess", "warn"
    return f"Score {v} — Low risk", "normal"

def _si_interp(v):
    if v < 0.5:  return f"{v} — Below typical range (< 0.5)", "warn"
    if v <= 0.7: return f"{v} — Normal (0.5–0.7)", "normal"
    if v < 1.0:  return f"{v} — Elevated — possible occult hypoperfusion", "warn"
    return f"{v} — ≥ 1.0 — Suggests shock / significant haemodynamic compromise", "crit"

def _aa_interp(v, age):
    expected = round(age / 4 + 4, 1)
    if v <= expected: return f"{v} mmHg — Normal for age (expected ≤ {expected})", "normal"
    if v <= expected + 20: return f"{v} mmHg — Elevated (expected ≤ {expected}) — V/Q mismatch, shunt or diffusion defect", "warn"
    return f"{v} mmHg — Markedly elevated (expected ≤ {expected})", "crit"


def _wf_interp(v, paco2):
    lo, hi = round(v - 2, 1), round(v + 2, 1)
    if paco2 is None: return f"Expected PaCO₂ {lo}–{hi} mmHg if respiratory compensation is appropriate", "normal"
    if paco2 < lo: return f"Measured {paco2} < {lo} — Concomitant respiratory alkalosis", "warn"
    if paco2 > hi: return f"Measured {paco2} > {hi} — Concomitant respiratory acidosis", "crit"
    return f"Measured {paco2} within {lo}–{hi} — Appropriate respiratory compensation", "normal"


def _dr_interp(v):
    if v < 0.4: return f"{v} — < 0.4 — Hyperchloraemic normal anion gap acidosis", "warn"
    if v < 0.8: return f"{v} — 0.4–0.8 — Mixed high and normal anion gap acidosis", "warn"
    if v <= 2: return f"{v} — 0.8–2 — Pure high anion gap metabolic acidosis", "normal"
    return f"{v} — > 2 — Concurrent metabolic alkalosis or chronic respiratory acidosis", "crit"


def _fwd_interp(v):
    if v <= 0: return f"{v} L — No free water deficit (Na⁺ ≤ 140)", "normal"
    if v < 3: return f"{v} L — Mild deficit; correct Na⁺ ≤ 10 mEq/L per 24 h", "warn"
    return f"{v} L — Significant deficit; correct Na⁺ ≤ 10 mEq/L per 24 h", "crit"


def _ibw_interp(v):
    if v <= 0: return f"{v} kg — Height too low for Devine formula", "crit"
    lo, hi = round(v * 4), round(v * 8)
    return f"Lung-protective VT 6 mL/kg = {round(v * 6)} mL (range 4–8 mL/kg: {lo}–{hi} mL)", "normal"


def _rsbi_interp(v):
    if v < 105: return f"{v} — < 105 — Weaning likely to succeed (proceed to SBT)", "normal"
    return f"{v} — ≥ 105 — High risk of weaning failure", "crit"


def _oi_interp(v):
    if v < 15: return f"{v} — < 15 — Mild impairment", "normal"
    if v < 25: return f"{v} — 15–25 — Moderate impairment", "warn"
    if v < 40: return f"{v} — 25–40 — Severe hypoxaemic failure", "crit"
    return f"{v} — ≥ 40 — Very severe; consider ECMO referral", "crit"


def _dp_interp(v):
    if v <= 15: return f"{v} — ≤ 15 cmH2O — Within lung-protective target", "normal"
    return f"{v} — > 15 cmH2O — Associated with higher ARDS mortality; reduce VT", "crit"


def _rox_interp(v):
    if v >= 4.88: return f"{v} — ≥ 4.88 — HFNC likely to succeed", "normal"
    if v >= 3.85: return f"{v} — 3.85–4.88 — Indeterminate; reassess in 1–2 h", "warn"
    return f"{v} — < 3.85 — High risk of HFNC failure; consider intubation", "crit"


def _qtc_interp(v, sex):
    limit = 470 if sex.lower() in ("f", "female") else 450
    if v > 500: return f"{v} ms — > 500 ms — High risk of torsades; review QT-prolonging drugs, K⁺, Mg²⁺", "crit"
    if v > limit: return f"{v} ms — Prolonged (> {limit} ms)", "warn"
    return f"{v} ms — Normal (≤ {limit} ms); Bazett over-corrects at high HR", "normal"


def _og_interp(v):
    if v < -10: return f"{v} mOsm/kg — Negative gap; check measurement / lab error", "warn"
    if v <= 10: return f"{v} mOsm/kg — Normal (≤ 10)", "normal"
    if v <= 20: return f"{v} mOsm/kg — Elevated; consider ethanol, mannitol or toxic alcohol", "warn"
    return f"{v} mOsm/kg — Markedly elevated (> 20); suspect methanol / ethylene glycol", "crit"

def _cag_interp(v):
    if v < 8:    return f"{v} mEq/L — Low corrected AG; check lab error / paraproteinaemia", "warn"
    if v <= 12:  return f"{v} mEq/L — Normal (8–12)", "normal"
    if v <= 20:  return f"{v} mEq/L — Elevated; high AG acidosis likely (unmasked by albumin correction)", "warn"
    return f"{v} mEq/L — Markedly elevated (> 20)", "crit"


def _pk_interp(v, tbsa):
    first8 = round(v / 2 / 8, 0); next16 = round(v / 2 / 16, 0)
    msg = f"{first8:.0f} mL/h × 8 h, then {next16:.0f} mL/h × 16 h; titrate to urine output 0.5 mL/kg/h"
    if tbsa < 20: return f"TBSA < 20 % — formal resuscitation usually not required (adults). {msg}", "normal"
    if tbsa < 50: return f"Major burn — {msg}", "warn"
    return f"Massive burn (≥ 50 % TBSA) — beware fluid creep. {msg}", "crit"


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

    elif calc == "gcs":
        try:
            v = glasgow_coma_scale(
                int(form.get("gcs_eye", 4)),
                int(form.get("gcs_verbal", 5)),
                int(form.get("gcs_motor", 6)),
            )
            interp, cls = _gcs_interp(v)
            results.update(gcs=v, gcs_interp=interp, gcs_cls=cls)
        except Exception as e:
            results["gcs_error"] = str(e)

    elif calc == "curb65":
        try:
            v = curb65(
                int(form.get("confusion", 0)),
                int(form.get("urea_high", 0)),
                float(form["resp_rate"]),
                float(form["curb_sbp"]),
                float(form["curb_dbp"]),
                float(form["curb_age"]),
            )
            interp, cls = _curb65_interp(v)
            results.update(curb65=v, curb65_interp=interp, curb65_cls=cls)
        except Exception as e:
            results["curb65_error"] = str(e)

    elif calc == "corrna":
        try:
            v = corrected_sodium(float(form["measured_na"]), float(form["glucose"]))
            interp, cls = _corrna_interp(v)
            results.update(corrna=v, corrna_interp=interp, corrna_cls=cls)
        except Exception as e:
            results["corrna_error"] = str(e)

    elif calc == "corrca":
        try:
            v = corrected_calcium(float(form["total_ca"]), float(form["albumin"]))
            interp, cls = _corrca_interp(v)
            results.update(corrca=v, corrca_interp=interp, corrca_cls=cls)
        except Exception as e:
            results["corrca_error"] = str(e)

    elif calc == "osm":
        try:
            v = serum_osmolality(float(form["osm_na"]), float(form["osm_glucose"]), float(form["osm_bun"]))
            interp, cls = _osm_interp(v)
            results.update(osm=v, osm_interp=interp, osm_cls=cls)
        except Exception as e:
            results["osm_error"] = str(e)

    elif calc == "qsofa":
        try:
            v = qsofa(float(form["qsofa_rr"]), float(form["qsofa_sbp"]), int(form.get("qsofa_ams", 0)))
            interp, cls = _qsofa_interp(v)
            results.update(qsofa=v, qsofa_interp=interp, qsofa_cls=cls)
        except Exception as e:
            results["qsofa_error"] = str(e)

    elif calc == "si":
        try:
            v = shock_index(float(form["si_hr"]), float(form["si_sbp"]))
            interp, cls = _si_interp(v)
            results.update(si=v, si_interp=interp, si_cls=cls)
        except Exception as e:
            results["si_error"] = str(e)

    elif calc == "aa":
        try:
            v = aa_gradient(
                float(form["aa_pao2"]), float(form["aa_paco2"]), float(form["aa_fio2"]),
                float(form.get("aa_patm") or 760),
            )
            interp, cls = _aa_interp(v, float(form.get("aa_age") or 40))
            results.update(aa=v, aa_interp=interp, aa_cls=cls)
        except Exception as e:
            results["aa_error"] = str(e)

    elif calc == "wf":
        try:
            v = winters_formula(float(form["wf_hco3"]))
            paco2 = float(form["wf_paco2"]) if form.get("wf_paco2") else None
            interp, cls = _wf_interp(v, paco2)
            results.update(wf=v, wf_interp=interp, wf_cls=cls)
        except Exception as e:
            results["wf_error"] = str(e)

    elif calc == "dr":
        try:
            v = delta_ratio(float(form["dr_na"]), float(form["dr_cl"]), float(form["dr_hco3"]))
            interp, cls = _dr_interp(v)
            results.update(dr=v, dr_interp=interp, dr_cls=cls)
        except Exception as e:
            results["dr_error"] = str(e)

    elif calc == "fwd":
        try:
            v = free_water_deficit(
                float(form["fwd_na"]), float(form["fwd_weight"]),
                form.get("fwd_sex", "male"), float(form.get("fwd_age") or 40),
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

    elif calc == "rsbi":
        try:
            v = rsbi(float(form["rsbi_rr"]), float(form["rsbi_vt"]))
            interp, cls = _rsbi_interp(v)
            results.update(rsbi=v, rsbi_interp=interp, rsbi_cls=cls)
        except Exception as e:
            results["rsbi_error"] = str(e)

    elif calc == "oi":
        try:
            v = oxygenation_index(float(form["oi_fio2"]), float(form["oi_paw"]), float(form["oi_pao2"]))
            interp, cls = _oi_interp(v)
            results.update(oi=v, oi_interp=interp, oi_cls=cls)
        except Exception as e:
            results["oi_error"] = str(e)

    elif calc == "dp":
        try:
            v = driving_pressure(float(form["dp_pplat"]), float(form["dp_peep"]))
            interp, cls = _dp_interp(v)
            results.update(dp=v, dp_interp=interp, dp_cls=cls)
            if form.get("dp_vt") and v > 0:
                results["dp_crs"] = round(float(form["dp_vt"]) / v, 1)
        except Exception as e:
            results["dp_error"] = str(e)

    elif calc == "rox":
        try:
            v = rox_index(float(form["rox_spo2"]), float(form["rox_fio2"]), float(form["rox_rr"]))
            interp, cls = _rox_interp(v)
            results.update(rox=v, rox_interp=interp, rox_cls=cls)
        except Exception as e:
            results["rox_error"] = str(e)

    elif calc == "qtc":
        try:
            v = qtc_bazett(float(form["qtc_qt"]), float(form["qtc_hr"]))
            interp, cls = _qtc_interp(v, form.get("qtc_sex") or "m")
            results.update(qtc=v, qtc_interp=interp, qtc_cls=cls)
        except Exception as e:
            results["qtc_error"] = str(e)

    elif calc == "og":
        try:
            v = osmolal_gap(float(form["og_meas"]), float(form["og_na"]), float(form["og_glucose"]), float(form["og_bun"]))
            interp, cls = _og_interp(v)
            results.update(og=v, og_interp=interp, og_cls=cls)
        except Exception as e:
            results["og_error"] = str(e)

    elif calc == "cag":
        try:
            v = albumin_corrected_anion_gap(float(form["cag_na"]), float(form["cag_cl"]), float(form["cag_hco3"]), float(form["cag_alb"]))
            interp, cls = _cag_interp(v)
            results.update(cag=v, cag_interp=interp, cag_cls=cls)
        except Exception as e:
            results["cag_error"] = str(e)

    elif calc == "pk":
        try:
            tbsa = float(form["pk_tbsa"])
            v = parkland_formula(float(form["pk_wt"]), tbsa)
            interp, cls = _pk_interp(v, tbsa)
            results.update(pk=v, pk_interp=interp, pk_cls=cls)
        except Exception as e:
            results["pk_error"] = str(e)

    return render_template_string(TEMPLATE, disclaimer=DISCLAIMER, results=results, form=form)


if __name__ == "__main__":
    app.run(debug=True, port=3001)
