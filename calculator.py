"""
ICU Calculator — generation 0 seed.
Four formulas: MAP, P/F ratio, anion gap, creatinine clearance (Cockcroft-Gault).
"""

DISCLAIMER = "EXPERIMENTAL — NOT FOR CLINICAL USE"


def mean_arterial_pressure(systolic: float, diastolic: float) -> float:
    """MAP = DBP + 1/3 (SBP - DBP)"""
    return round(diastolic + (systolic - diastolic) / 3, 1)


def pf_ratio(pao2: float, fio2: float) -> float:
    """P/F ratio = PaO2 / FiO2 (FiO2 as fraction 0-1)"""
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    return round(pao2 / fio2, 1)


def anion_gap(sodium: float, chloride: float, bicarbonate: float) -> float:
    """AG = Na - (Cl + HCO3)"""
    return round(sodium - (chloride + bicarbonate), 1)


def creatinine_clearance(
    age: float, weight: float, creatinine: float, sex: str
) -> float:
    """
    Cockcroft-Gault: CrCl = [(140 - age) * weight] / (72 * Cr)
    Multiply by 0.85 for female.
    weight in kg, creatinine in mg/dL.
    """
    if creatinine <= 0:
        raise ValueError("Creatinine must be positive")
    result = ((140 - age) * weight) / (72 * creatinine)
    if sex.lower() in ("f", "female"):
        result *= 0.85
    return round(result, 1)


def glasgow_coma_scale(eye: int, verbal: int, motor: int) -> int:
    """
    Glasgow Coma Scale: total score 3–15.
    eye: 1–4 (none=1, to pain=2, to voice=3, spontaneous=4)
    verbal: 1–5 (none=1, sounds=2, words=3, confused=4, oriented=5)
    motor: 1–6 (none=1, extension=2, flexion=3, withdrawal=4, localises=5, obeys=6)
    """
    if not (1 <= eye <= 4):
        raise ValueError("Eye response must be between 1 and 4")
    if not (1 <= verbal <= 5):
        raise ValueError("Verbal response must be between 1 and 5")
    if not (1 <= motor <= 6):
        raise ValueError("Motor response must be between 1 and 6")
    return eye + verbal + motor


def corrected_sodium(measured_na: float, glucose: float) -> float:
    """
    Corrected serum sodium for hyperglycemia (Katz formula).
    corrected_Na = measured_Na + 1.6 × (glucose − 100) / 100
    glucose in mg/dL, sodium in mEq/L.
    """
    if glucose < 0:
        raise ValueError("Glucose must be non-negative")
    return round(measured_na + 1.6 * (glucose - 100) / 100, 1)


def curb65(confusion: int, urea_high: int, resp_rate: float, sbp: float, dbp: float, age: float) -> int:
    """
    CURB-65 pneumonia severity score (0–5).
    confusion/urea_high: 1=present, 0=absent.
    resp_rate >= 30, SBP < 90 or DBP <= 60, age >= 65 each score 1 point.
    """
    score = int(bool(confusion)) + int(bool(urea_high))
    score += 1 if resp_rate >= 30 else 0
    score += 1 if (sbp < 90 or dbp <= 60) else 0
    score += 1 if age >= 65 else 0
    return score


def corrected_calcium(total_ca: float, albumin: float) -> float:
    """
    Albumin-corrected calcium (Payne formula).
    corrected_Ca = total_Ca + 0.8 × (4.0 − albumin)
    calcium in mg/dL, albumin in g/dL.
    """
    if total_ca < 0:
        raise ValueError("Calcium must be non-negative")
    if albumin < 0:
        raise ValueError("Albumin must be non-negative")
    return round(total_ca + 0.8 * (4.0 - albumin), 1)


def serum_osmolality(sodium: float, glucose: float, bun: float) -> float:
    """
    Calculated serum osmolality.
    Osm = 2 × Na + glucose / 18 + BUN / 2.8
    sodium in mEq/L, glucose and BUN in mg/dL; result in mOsm/kg.
    """
    if sodium < 0 or glucose < 0 or bun < 0:
        raise ValueError("Sodium, glucose and BUN must be non-negative")
    return round(2 * sodium + glucose / 18 + bun / 2.8, 1)


def qsofa(resp_rate: float, sbp: float, altered_mentation: int) -> int:
    """
    qSOFA (quick Sepsis-related Organ Failure Assessment), score 0–3.
    1 point each: RR >= 22/min, SBP <= 100 mmHg, altered mentation (GCS < 15).
    """
    if resp_rate < 0 or sbp < 0:
        raise ValueError("Respiratory rate and SBP must be non-negative")
    score = 1 if resp_rate >= 22 else 0
    score += 1 if sbp <= 100 else 0
    score += int(bool(altered_mentation))
    return score


def shock_index(heart_rate: float, sbp: float) -> float:
    """
    Shock index = heart rate / systolic BP.
    heart rate in beats/min, SBP in mmHg. Normal ~0.5–0.7.
    """
    if heart_rate < 0:
        raise ValueError("Heart rate must be non-negative")
    if sbp <= 0:
        raise ValueError("Systolic BP must be positive")
    return round(heart_rate / sbp, 2)


def aa_gradient(pao2: float, paco2: float, fio2: float, patm: float = 760.0) -> float:
    """
    Alveolar–arterial (A–a) oxygen gradient.
    PAO2 = FiO2 × (Patm − 47) − PaCO2 / 0.8 ; A–a = PAO2 − PaO2
    pressures in mmHg, FiO2 as fraction 0–1. Expected normal ≈ age/4 + 4.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if pao2 < 0 or paco2 < 0:
        raise ValueError("PaO2 and PaCO2 must be non-negative")
    if patm <= 47:
        raise ValueError("Atmospheric pressure must exceed water vapour pressure (47 mmHg)")
    alveolar = fio2 * (patm - 47) - paco2 / 0.8
    return round(alveolar - pao2, 1)


def winters_formula(bicarbonate: float) -> float:
    """
    Winter's formula — expected PaCO2 in primary metabolic acidosis.
    expected PaCO2 = 1.5 × HCO3 + 8 (± 2), HCO3 in mEq/L, result in mmHg.
    """
    if bicarbonate < 0:
        raise ValueError("Bicarbonate must be non-negative")
    return round(1.5 * bicarbonate + 8, 1)


def delta_ratio(sodium: float, chloride: float, bicarbonate: float) -> float:
    """
    Delta–delta ratio = (AG − 12) / (24 − HCO3), AG = Na − (Cl + HCO3).
    Detects mixed acid–base disorders in high anion gap metabolic acidosis.
    <0.4 hyperchloraemic NAGMA; 0.4–0.8 mixed; 0.8–2 pure HAGMA; >2 concurrent metabolic alkalosis.
    """
    if bicarbonate >= 24:
        raise ValueError("Bicarbonate must be below 24 mEq/L for delta ratio")
    ag = sodium - (chloride + bicarbonate)
    return round((ag - 12) / (24 - bicarbonate), 2)


def free_water_deficit(sodium: float, weight: float, sex: str, age: float = 40) -> float:
    """
    Free water deficit in hypernatraemia.
    FWD = TBW × (Na / 140 − 1), TBW = weight × factor.
    factor: male 0.6 (0.5 if age ≥ 65), female 0.5 (0.45 if age ≥ 65).
    sodium in mEq/L, weight in kg; result in litres.
    """
    if sodium <= 0:
        raise ValueError("Sodium must be positive")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    female = sex.lower() in ("f", "female")
    if age >= 65:
        factor = 0.45 if female else 0.5
    else:
        factor = 0.5 if female else 0.6
    return round(weight * factor * (sodium / 140 - 1), 1)


def ideal_body_weight(height_cm: float, sex: str) -> float:
    """
    Ideal (predicted) body weight — Devine formula, as used by ARDSnet.
    male: 50 + 0.91 × (height_cm − 152.4); female: 45.5 + 0.91 × (height_cm − 152.4).
    height in cm; result in kg. Lung-protective tidal volume = 6 mL/kg IBW.
    """
    if height_cm <= 0:
        raise ValueError("Height must be positive")
    base = 45.5 if sex.lower() in ("f", "female") else 50.0
    return round(base + 0.91 * (height_cm - 152.4), 1)


def rsbi(resp_rate: float, tidal_volume_ml: float) -> float:
    """
    Rapid Shallow Breathing Index (Yang–Tobin) = RR / VT (litres).
    resp_rate in breaths/min, tidal volume in mL. < 105 predicts weaning success.
    """
    if resp_rate < 0:
        raise ValueError("Respiratory rate must be non-negative")
    if tidal_volume_ml <= 0:
        raise ValueError("Tidal volume must be positive")
    return round(resp_rate / (tidal_volume_ml / 1000), 1)


def oxygenation_index(fio2: float, mean_airway_pressure: float, pao2: float) -> float:
    """
    Oxygenation index = FiO2 × mean airway pressure × 100 / PaO2.
    FiO2 as fraction 0–1, mean airway pressure in cmH2O, PaO2 in mmHg.
    Higher = worse oxygenation; > 25 severe, ≥ 40 consider ECMO referral.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if mean_airway_pressure < 0:
        raise ValueError("Mean airway pressure must be non-negative")
    if pao2 <= 0:
        raise ValueError("PaO2 must be positive")
    return round(fio2 * mean_airway_pressure * 100 / pao2, 1)


def driving_pressure(plateau_pressure: float, peep: float) -> float:
    """
    Driving pressure (ΔP) = plateau pressure − PEEP, both in cmH2O.
    ΔP > 15 cmH2O is associated with increased mortality in ARDS (Amato 2015).
    """
    if peep < 0:
        raise ValueError("PEEP must be non-negative")
    if plateau_pressure < peep:
        raise ValueError("Plateau pressure must be at least PEEP")
    return round(plateau_pressure - peep, 1)


def rox_index(spo2: float, fio2: float, resp_rate: float) -> float:
    """
    ROX index (Roca 2016) = (SpO2 / FiO2) / respiratory rate.
    SpO2 in %, FiO2 as fraction 0–1, RR in breaths/min.
    On high-flow nasal cannula: ≥ 4.88 predicts HFNC success; < 3.85 high risk of intubation.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if not (0 <= spo2 <= 100):
        raise ValueError("SpO2 must be between 0 and 100")
    if resp_rate <= 0:
        raise ValueError("Respiratory rate must be positive")
    return round(spo2 / fio2 / resp_rate, 2)


def qtc_bazett(qt_ms: float, heart_rate: float) -> float:
    """
    Corrected QT interval (Bazett) = QT / sqrt(RR), RR = 60 / HR in seconds.
    QT in ms, heart rate in beats/min; result in ms.
    Prolonged: > 450 ms (male) / > 470 ms (female); > 500 ms high torsades risk.
    """
    if qt_ms <= 0:
        raise ValueError("QT interval must be positive")
    if heart_rate <= 0:
        raise ValueError("Heart rate must be positive")
    return round(qt_ms / (60 / heart_rate) ** 0.5, 1)


def osmolal_gap(measured_osm: float, sodium: float, glucose: float, bun: float) -> float:
    """
    Osmolal gap = measured osmolality − calculated osmolality.
    calculated = 2 × Na + glucose / 18 + BUN / 2.8 (mOsm/kg).
    > 10 mOsm/kg suggests unmeasured osmoles (toxic alcohols, mannitol).
    """
    if measured_osm <= 0:
        raise ValueError("Measured osmolality must be positive")
    if sodium < 0 or glucose < 0 or bun < 0:
        raise ValueError("Sodium, glucose and BUN must be non-negative")
    return round(measured_osm - (2 * sodium + glucose / 18 + bun / 2.8), 1)


def albumin_corrected_anion_gap(sodium: float, chloride: float, bicarbonate: float, albumin: float) -> float:
    """
    Albumin-corrected anion gap (Figge) = AG + 2.5 × (4.0 − albumin).
    AG = Na − (Cl + HCO3) in mEq/L, albumin in g/dL.
    Unmasks a high anion gap acidosis hidden by hypoalbuminaemia; normal ≈ 8–12.
    """
    if albumin < 0:
        raise ValueError("Albumin must be non-negative")
    return round(sodium - (chloride + bicarbonate) + 2.5 * (4.0 - albumin), 1)


def parkland_formula(weight: float, tbsa_percent: float) -> float:
    """
    Parkland formula — 24 h crystalloid (Ringer's lactate) for burn resuscitation.
    volume = 4 mL × weight (kg) × %TBSA (partial + full thickness burns); result in mL.
    Give half in the first 8 h from time of burn, the remainder over the next 16 h.
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if not (0 <= tbsa_percent <= 100):
        raise ValueError("TBSA must be between 0 and 100 %")
    return round(4 * weight * tbsa_percent, 1)


def body_surface_area(height_cm: float, weight: float) -> float:
    """
    Body surface area — Mosteller formula.
    BSA = sqrt(height_cm × weight_kg / 3600); result in m².
    Used for cardiac index, chemotherapy and some drug dosing. Typical adult ≈ 1.7–2.0 m².
    """
    if height_cm <= 0:
        raise ValueError("Height must be positive")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    return round((height_cm * weight / 3600) ** 0.5, 2)


def egfr_ckd_epi_2021(creatinine: float, age: float, sex: str) -> float:
    """
    eGFR — CKD-EPI 2021 race-free creatinine equation.
    eGFR = 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^−1.200 × 0.9938^age × 1.012 [female]
    κ = 0.7 (F) / 0.9 (M); α = −0.241 (F) / −0.302 (M).
    creatinine in mg/dL, age in years; result in mL/min/1.73 m². Assumes steady-state creatinine.
    """
    if creatinine <= 0:
        raise ValueError("Creatinine must be positive")
    if age < 18:
        raise ValueError("CKD-EPI is validated for adults (age ≥ 18)")
    female = sex.lower() in ("f", "female")
    kappa, alpha = (0.7, -0.241) if female else (0.9, -0.302)
    ratio = creatinine / kappa
    result = 142 * min(ratio, 1) ** alpha * max(ratio, 1) ** -1.2 * 0.9938 ** age
    if female:
        result *= 1.012
    return round(result, 1)


def wells_pe(dvt_signs: int, pe_most_likely: int, heart_rate: float, immobilisation: int,
             prior_vte: int, haemoptysis: int, malignancy: int) -> float:
    """
    Wells score for pulmonary embolism (0–12.5).
    Clinical signs of DVT 3; PE the most likely diagnosis 3; HR > 100 1.5;
    immobilisation ≥ 3 days or surgery in past 4 weeks 1.5; prior DVT/PE 1.5;
    haemoptysis 1; active malignancy 1. Flags: 1 = present, 0 = absent.
    Two-tier: ≤ 4 PE unlikely (D-dimer), > 4 PE likely (CTPA).
    """
    if heart_rate < 0:
        raise ValueError("Heart rate must be non-negative")
    score = 3.0 * bool(dvt_signs) + 3.0 * bool(pe_most_likely)
    score += 1.5 if heart_rate > 100 else 0
    score += 1.5 * bool(immobilisation) + 1.5 * bool(prior_vte)
    score += 1.0 * bool(haemoptysis) + 1.0 * bool(malignancy)
    return score


def cha2ds2_vasc(chf: int, hypertension: int, age: float, diabetes: int, stroke_tia: int,
                 vascular_disease: int, sex: str) -> int:
    """
    CHA2DS2-VASc stroke risk score in atrial fibrillation (0–9).
    CHF 1; hypertension 1; age ≥ 75 2 (65–74 1); diabetes 1; prior stroke/TIA/thromboembolism 2;
    vascular disease (MI, PAD, aortic plaque) 1; female sex 1. Flags: 1 = present, 0 = absent.
    Anticoagulation generally recommended at ≥ 2 (male) / ≥ 3 (female).
    """
    if age < 0:
        raise ValueError("Age must be non-negative")
    score = int(bool(chf)) + int(bool(hypertension)) + int(bool(diabetes)) + int(bool(vascular_disease))
    score += 2 * int(bool(stroke_tia))
    score += 2 if age >= 75 else (1 if age >= 65 else 0)
    score += 1 if sex.lower() in ("f", "female") else 0
    return score
