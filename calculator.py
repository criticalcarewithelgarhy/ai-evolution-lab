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


def corrected_anion_gap(
    sodium: float, chloride: float, bicarbonate: float, albumin: float
) -> float:
    """
    Albumin-corrected anion gap: AG + 2.5 * (4.0 - albumin)
    Corrects for hypoalbuminaemia, common in ICU patients.
    albumin in g/dL (normal ~4.0).
    """
    if albumin < 0:
        raise ValueError("Albumin must be non-negative")
    ag = sodium - (chloride + bicarbonate)
    return round(ag + 2.5 * (4.0 - albumin), 1)


def corrected_sodium(sodium: float, glucose: float) -> float:
    """
    Corrected sodium for hyperglycaemia (Katz, 1973).
    corrected Na = measured Na + 1.6 × (glucose − 100) / 100
    sodium in mEq/L, glucose in mg/dL.
    """
    if glucose < 0:
        raise ValueError("Glucose must be non-negative")
    return round(sodium + 1.6 * (glucose - 100) / 100, 1)


def winters_formula(bicarbonate: float) -> float:
    """
    Winter's formula: expected PaCO2 = 1.5 × HCO3 + 8 (± 2 mmHg).
    Assesses respiratory compensation in metabolic acidosis.
    bicarbonate in mEq/L.
    """
    if bicarbonate < 0:
        raise ValueError("Bicarbonate must be non-negative")
    return round(1.5 * bicarbonate + 8, 1)


def delta_ratio(sodium: float, chloride: float, bicarbonate: float) -> float:
    """
    Delta ratio (delta-delta) = (AG − 12) / (24 − HCO3).
    Detects mixed disorders in high-AG metabolic acidosis.
    All inputs in mEq/L.
    """
    if bicarbonate == 24:
        raise ValueError("Bicarbonate must differ from 24 mEq/L")
    ag = sodium - (chloride + bicarbonate)
    return round((ag - 12) / (24 - bicarbonate), 2)


def aa_gradient(pao2: float, paco2: float, fio2: float, patm: float = 760) -> float:
    """
    Alveolar-arterial O2 gradient = PAO2 − PaO2,
    where PAO2 = FiO2 × (Patm − 47) − PaCO2 / 0.8.
    Pressures in mmHg, FiO2 as fraction 0-1.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    alveolar = fio2 * (patm - 47) - paco2 / 0.8
    return round(alveolar - pao2, 1)


def serum_osmolality(sodium: float, glucose: float, bun: float) -> float:
    """
    Calculated serum osmolality = 2 × Na + glucose / 18 + BUN / 2.8.
    sodium in mEq/L, glucose and BUN in mg/dL; result in mOsm/kg.
    """
    if glucose < 0 or bun < 0:
        raise ValueError("Glucose and BUN must be non-negative")
    return round(2 * sodium + glucose / 18 + bun / 2.8, 1)


def corrected_calcium(calcium: float, albumin: float) -> float:
    """
    Albumin-corrected calcium (Payne, 1973) = Ca + 0.8 × (4.0 − albumin).
    calcium in mg/dL, albumin in g/dL.
    """
    if calcium < 0 or albumin < 0:
        raise ValueError("Calcium and albumin must be non-negative")
    return round(calcium + 0.8 * (4.0 - albumin), 1)


def predicted_body_weight(height_cm: float, sex: str) -> float:
    """
    ARDSnet predicted body weight (Devine):
    male 50 + 0.91 × (height − 152.4); female 45.5 + 0.91 × (height − 152.4).
    height in cm; result in kg. Used to set lung-protective tidal volume (6 mL/kg).
    """
    if height_cm <= 0:
        raise ValueError("Height must be positive")
    base = 45.5 if sex.lower() in ("f", "female") else 50.0
    return round(base + 0.91 * (height_cm - 152.4), 1)


def shock_index(heart_rate: float, systolic: float) -> float:
    """
    Shock index = HR / SBP. Normal 0.5–0.7; > 0.9 suggests occult shock.
    heart_rate in bpm, systolic in mmHg.
    """
    if systolic <= 0 or heart_rate < 0:
        raise ValueError("SBP must be positive and HR non-negative")
    return round(heart_rate / systolic, 2)


def free_water_deficit(sodium: float, weight: float, sex: str) -> float:
    """
    Free water deficit = TBW × (Na / 140 − 1), TBW = 0.6 × weight (male) or 0.5 × weight (female).
    sodium in mEq/L, weight in kg; result in litres. Negative means no deficit.
    """
    if sodium <= 0 or weight <= 0:
        raise ValueError("Sodium and weight must be positive")
    tbw = weight * (0.5 if sex.lower() in ("f", "female") else 0.6)
    return round(tbw * (sodium / 140 - 1), 1)


def rox_index(spo2: float, fio2: float, resp_rate: float) -> float:
    """
    ROX index = (SpO2 / FiO2) / RR (Roca, 2016). Predicts high-flow nasal cannula success.
    spo2 in %, FiO2 as fraction 0-1, resp_rate in breaths/min. >= 4.88 suggests HFNC success.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if resp_rate <= 0 or not (0 <= spo2 <= 100):
        raise ValueError("RR must be positive and SpO2 between 0 and 100")
    return round(spo2 / fio2 / resp_rate, 2)


def qsofa_score(resp_rate: float, systolic: float, altered_mentation: bool) -> int:
    """
    qSOFA (Seymour, 2016): 1 point each for RR >= 22, SBP <= 100, altered mentation (GCS < 15).
    Score >= 2 flags higher risk of poor outcome in suspected infection.
    """
    if resp_rate < 0 or systolic < 0:
        raise ValueError("RR and SBP must be non-negative")
    return int(resp_rate >= 22) + int(systolic <= 100) + int(bool(altered_mentation))


def driving_pressure(plateau: float, peep: float) -> float:
    """
    Driving pressure = Pplat − PEEP (Amato, 2015). cmH2O; <= 15 associated with lower ARDS mortality.
    """
    if peep < 0 or plateau < peep:
        raise ValueError("PEEP must be non-negative and Pplat >= PEEP")
    return round(plateau - peep, 1)


def oxygenation_index(fio2: float, mean_airway_pressure: float, pao2: float) -> float:
    """
    Oxygenation index = FiO2 × mPaw × 100 / PaO2. FiO2 as fraction 0-1, mPaw in cmH2O, PaO2 in mmHg.
    Higher is worse; > 40 is a common threshold for considering ECMO.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if pao2 <= 0 or mean_airway_pressure < 0:
        raise ValueError("PaO2 must be positive and mPaw non-negative")
    return round(fio2 * mean_airway_pressure * 100 / pao2, 1)


def sf_ratio(spo2: float, fio2: float) -> float:
    """
    S/F ratio = SpO2 / FiO2 (Rice, 2007). Non-invasive P/F surrogate; S/F 235 ≈ P/F 200, 315 ≈ P/F 300.
    spo2 in %, FiO2 as fraction 0-1. Valid only when SpO2 <= 97%.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if not (0 <= spo2 <= 100):
        raise ValueError("SpO2 must be between 0 and 100")
    return round(spo2 / fio2, 1)


def static_compliance(tidal_volume: float, plateau: float, peep: float) -> float:
    """
    Static respiratory system compliance = VT / (Pplat − PEEP). VT in mL, pressures in cmH2O; result mL/cmH2O.
    Normal ~50–100 in ventilated adults; < 40 suggests stiff lungs (e.g. ARDS).
    """
    if tidal_volume <= 0 or peep < 0 or plateau <= peep:
        raise ValueError("VT must be positive, PEEP non-negative and Pplat > PEEP")
    return round(tidal_volume / (plateau - peep), 1)


def rsbi(resp_rate: float, tidal_volume: float) -> float:
    """
    Rapid shallow breathing index (Yang & Tobin, 1991) = RR / VT(L). RR in breaths/min, VT in mL.
    < 105 breaths/min/L during a spontaneous breathing trial predicts weaning success.
    """
    if resp_rate < 0 or tidal_volume <= 0:
        raise ValueError("RR must be non-negative and VT positive")
    return round(resp_rate / (tidal_volume / 1000), 1)


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
