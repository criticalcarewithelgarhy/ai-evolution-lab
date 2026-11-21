"""
ICU Calculator — generation 0 seed.
Four formulas: MAP, P/F ratio, anion gap, creatinine clearance (Cockcroft-Gault).
"""

DISCLAIMER = "EXPERIMENTAL — NOT FOR CLINICAL USE"


def mean_arterial_pressure(systolic: float, diastolic: float) -> float:
    """MAP = DBP + 1/3 (SBP - DBP)"""
    if diastolic < 0:
        raise ValueError("Diastolic BP cannot be negative")
    if systolic < diastolic:
        raise ValueError("Systolic BP must be greater than or equal to diastolic BP")
    return round(diastolic + (systolic - diastolic) / 3, 1)


def pf_ratio(pao2: float, fio2: float) -> float:
    """P/F ratio = PaO2 / FiO2 (FiO2 as fraction 0-1)"""
    if not (0.21 <= fio2 <= 1.0):
        raise ValueError("FiO2 must be between 0.21 (room air) and 1.0")
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
    if not (1 <= age <= 120):
        raise ValueError("Age must be between 1 and 120 years")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    sex_key = str(sex).strip().lower()
    if sex_key not in ("m", "male", "f", "female"):
        raise ValueError("Sex must be 'male' or 'female'")
    result = ((140 - age) * weight) / (72 * creatinine)
    if sex_key in ("f", "female"):
        result *= 0.85
    return round(result, 1)
