"""
ICU Calculator — generation 0 seed.
Four formulas: MAP, P/F ratio, anion gap, creatinine clearance (Cockcroft-Gault).
"""

DISCLAIMER = "EXPERIMENTAL — NOT FOR CLINICAL USE"


def mean_arterial_pressure(systolic: float, diastolic: float) -> float:
    """MAP = DBP + 1/3 (SBP - DBP)"""
    if systolic <= 0 or diastolic < 0:
        raise ValueError("Blood pressure values must be positive")
    if systolic <= diastolic:
        raise ValueError("Systolic must be greater than diastolic")
    return round(diastolic + (systolic - diastolic) / 3, 1)


def pf_ratio(pao2: float, fio2: float) -> float:
    """P/F ratio = PaO2 / FiO2 (FiO2 as fraction 0-1)"""
    if pao2 <= 0:
        raise ValueError("PaO2 must be positive")
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    return round(pao2 / fio2, 1)


def anion_gap(sodium: float, chloride: float, bicarbonate: float) -> float:
    """AG = Na - (Cl + HCO3)"""
    if sodium <= 0 or chloride <= 0 or bicarbonate < 0:
        raise ValueError("Electrolyte values must be positive")
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
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if not (0 <= age < 140):
        raise ValueError("Age must be between 0 and 140 years")
    result = ((140 - age) * weight) / (72 * creatinine)
    if sex.lower() in ("f", "female"):
        result *= 0.85
    return round(result, 1)
