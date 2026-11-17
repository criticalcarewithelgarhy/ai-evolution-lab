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
