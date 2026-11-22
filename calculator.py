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
