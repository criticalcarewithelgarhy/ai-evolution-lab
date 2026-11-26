"""
ICU Calculator — generation 0 seed.
Four formulas: MAP, P/F ratio, anion gap, creatinine clearance (Cockcroft-Gault).
"""

import math

DISCLAIMER = "EXPERIMENTAL — NOT FOR CLINICAL USE"


def _require_finite(*values: float) -> None:
    """Reject non-numeric types (str, None, bool) and NaN/infinity."""
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
        raise ValueError("Inputs must be numbers")
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Inputs must be finite numbers")


def mean_arterial_pressure(systolic: float, diastolic: float) -> float:
    """MAP = DBP + 1/3 (SBP - DBP)"""
    _require_finite(systolic, diastolic)
    if systolic <= 0 or diastolic < 0:
        raise ValueError("Blood pressure values must be positive")
    if systolic <= diastolic:
        raise ValueError("Systolic must be greater than diastolic")
    if systolic > 300:
        raise ValueError("Systolic above 300 mmHg is physiologically implausible")
    if systolic < 30:
        raise ValueError("Systolic below 30 mmHg is implausible — check for a typo")
    if diastolic < 10:
        raise ValueError("Diastolic below 10 mmHg is implausible — check for a typo")
    if diastolic > 200:
        raise ValueError("Diastolic above 200 mmHg is implausible — check for a typo")
    return round(diastolic + (systolic - diastolic) / 3, 1)


def pf_ratio(pao2: float, fio2: float) -> float:
    """P/F ratio = PaO2 / FiO2 (FiO2 as fraction 0-1)"""
    _require_finite(pao2, fio2)
    if pao2 <= 0:
        raise ValueError("PaO2 must be positive")
    if pao2 < 20:
        raise ValueError("PaO2 below 20 mmHg is implausible — was it entered in kPa?")
    if pao2 > 800:
        raise ValueError("PaO2 above 800 mmHg is implausible — check for a typo or kPa/mmHg mix-up")
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if fio2 < 0.21:
        raise ValueError("FiO2 below 0.21 (room air) is implausible — check for a typo")
    return round(pao2 / fio2, 1)


def anion_gap(sodium: float, chloride: float, bicarbonate: float) -> float:
    """AG = Na - (Cl + HCO3)"""
    _require_finite(sodium, chloride, bicarbonate)
    if sodium <= 0 or chloride <= 0 or bicarbonate < 0:
        raise ValueError("Electrolyte values must be positive")
    if not (90 <= sodium <= 200):
        raise ValueError("Sodium outside 90–200 mEq/L is implausible — check for a typo")
    if not (50 <= chloride <= 160):
        raise ValueError("Chloride outside 50–160 mEq/L is implausible — check for a typo")
    if bicarbonate > 60:
        raise ValueError("Bicarbonate above 60 mEq/L is implausible — check for a typo")
    if bicarbonate < 2:
        raise ValueError("Bicarbonate below 2 mEq/L is implausible — check for a typo")
    return round(sodium - (chloride + bicarbonate), 1)


def creatinine_clearance(
    age: float, weight: float, creatinine: float, sex: str
) -> float:
    """
    Cockcroft-Gault: CrCl = [(140 - age) * weight] / (72 * Cr)
    Multiply by 0.85 for female.
    weight in kg, creatinine in mg/dL.
    """
    _require_finite(age, weight, creatinine)
    if creatinine <= 0:
        raise ValueError("Creatinine must be positive")
    if creatinine < 0.1:
        raise ValueError("Creatinine below 0.1 mg/dL is implausible — check for a misplaced decimal")
    if creatinine > 30:
        raise ValueError("Creatinine above 30 mg/dL is implausible — was it entered in µmol/L?")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if weight < 20:
        raise ValueError("Weight below 20 kg is implausible for an adult — check for a typo")
    if weight > 400:
        raise ValueError("Weight above 400 kg is implausible — was it entered in grams or pounds?")
    if not (0 <= age < 140):
        raise ValueError("Age must be between 0 and 140 years")
    if age < 18:
        raise ValueError("Cockcroft-Gault is validated only for adults (age ≥ 18) — use a paediatric formula")
    sex_key = sex.strip().lower() if isinstance(sex, str) else ""
    if sex_key not in ("m", "male", "f", "female"):
        raise ValueError("Sex must be 'male' or 'female'")
    result = ((140 - age) * weight) / (72 * creatinine)
    if sex_key in ("f", "female"):
        result *= 0.85
    return round(result, 1)
