"""
ICU Calculator — generation 0 seed.
Four formulas: MAP, P/F ratio, anion gap, creatinine clearance (Cockcroft-Gault).
"""

DISCLAIMER = "EXPERIMENTAL — NOT FOR CLINICAL USE"

import math


def _require_finite(**values: float) -> None:
    """Reject NaN/inf, which slip past every range check (all NaN comparisons are False)."""
    for name, v in values.items():
        if not math.isfinite(v):
            raise ValueError(f"{name} must be a finite number")


def mean_arterial_pressure(systolic: float, diastolic: float) -> float:
    """MAP = DBP + 1/3 (SBP - DBP)"""
    _require_finite(systolic=systolic, diastolic=diastolic)
    if diastolic < 0:
        raise ValueError("Diastolic BP cannot be negative")
    if systolic < diastolic:
        raise ValueError("Systolic BP must be greater than or equal to diastolic BP")
    if systolic > 400:
        # Above any recorded human BP; almost always an extra-digit typo (1200 for 120)
        raise ValueError("Systolic BP must not exceed 400 mmHg")
    return round(diastolic + (systolic - diastolic) / 3, 1)


def pf_ratio(pao2: float, fio2: float) -> float:
    """P/F ratio = PaO2 / FiO2 (FiO2 as fraction 0-1)"""
    _require_finite(pao2=pao2, fio2=fio2)
    if not (0.21 <= fio2 <= 1.0):
        raise ValueError("FiO2 must be between 0.21 (room air) and 1.0")
    if pao2 <= 0:
        raise ValueError("PaO2 must be positive")
    return round(pao2 / fio2, 1)


def anion_gap(sodium: float, chloride: float, bicarbonate: float) -> float:
    """AG = Na - (Cl + HCO3)"""
    _require_finite(sodium=sodium, chloride=chloride, bicarbonate=bicarbonate)
    if sodium <= 0:
        raise ValueError("Sodium must be positive")
    if chloride < 0 or bicarbonate < 0:
        raise ValueError("Chloride and bicarbonate cannot be negative")
    return round(sodium - (chloride + bicarbonate), 1)


def corrected_anion_gap(
    sodium: float, chloride: float, bicarbonate: float, albumin: float
) -> float:
    """
    Albumin-corrected AG (Figge): AG + 2.5 * (4.0 - albumin), albumin in g/dL.
    Hypoalbuminaemia lowers the measured AG and can mask a high-AG acidosis.
    """
    _require_finite(albumin=albumin)
    if not (0 < albumin <= 10):
        raise ValueError("Albumin must be between 0 and 10 g/dL")
    anion_gap(sodium, chloride, bicarbonate)  # reuse electrolyte validation
    ag = sodium - (chloride + bicarbonate)
    return round(ag + 2.5 * (4.0 - albumin), 1)


def creatinine_clearance(
    age: float, weight: float, creatinine: float, sex: str
) -> float:
    """
    Cockcroft-Gault: CrCl = [(140 - age) * weight] / (72 * Cr)
    Multiply by 0.85 for female.
    weight in kg, creatinine in mg/dL.
    """
    _require_finite(age=age, weight=weight, creatinine=creatinine)
    if creatinine <= 0:
        raise ValueError("Creatinine must be positive")
    if not (1 <= age <= 120):
        raise ValueError("Age must be between 1 and 120 years")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if weight > 650:
        # Above the heaviest recorded human; almost always an extra-digit typo (700 for 70)
        raise ValueError("Weight must not exceed 650 kg")
    sex_key = str(sex).strip().lower()
    if sex_key not in ("m", "male", "f", "female"):
        raise ValueError("Sex must be 'male' or 'female'")
    result = ((140 - age) * weight) / (72 * creatinine)
    if sex_key in ("f", "female"):
        result *= 0.85
    return round(result, 1)
