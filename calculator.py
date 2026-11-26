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
    if pao2 > 800:
        # Alveolar gas equation caps PaO2 near 670 mmHg on 100% O2 at sea level;
        # higher values are almost always an extra-digit typo (850 for 85)
        raise ValueError("PaO2 must not exceed 800 mmHg")
    return round(pao2 / fio2, 1)


def anion_gap(sodium: float, chloride: float, bicarbonate: float) -> float:
    """AG = Na - (Cl + HCO3)"""
    _require_finite(sodium=sodium, chloride=chloride, bicarbonate=bicarbonate)
    if sodium <= 0:
        raise ValueError("Sodium must be positive")
    if sodium < 80:
        # Below any survivable recorded value (~85); almost always a dropped-digit typo
        # (14 for 140 reports a false AG of -114, masking a real high-AG acidosis)
        raise ValueError("Sodium must be at least 80 mEq/L")
    if sodium > 250:
        # Above any survivable recorded value (~255); almost always an extra-digit typo (1400 for 140)
        raise ValueError("Sodium must not exceed 250 mEq/L")
    if chloride < 0 or bicarbonate < 0:
        raise ValueError("Chloride and bicarbonate cannot be negative")
    if chloride > 200 or bicarbonate > 100:
        # Far beyond any survivable recorded value; almost always an extra-digit typo
        # (1040 for 104 reports a false AG of -928, masking a real high-AG acidosis)
        raise ValueError("Chloride must not exceed 200 and bicarbonate 100 mEq/L")
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
    if creatinine < 0.1:
        # Below any physiological value in mg/dL; almost always mmol/L entered as mg/dL
        # (0.088 mmol/L read as mg/dL reports CrCl ~994 instead of ~87 mL/min -> overdosing)
        raise ValueError("Creatinine must be at least 0.1 mg/dL (convert mmol/L × 11.31)")
    if creatinine > 40:
        # Above any recorded value in mg/dL; almost always µmol/L entered as mg/dL
        # (88 µmol/L read as 88 mg/dL reports CrCl ~1 instead of ~87 mL/min)
        raise ValueError("Creatinine must not exceed 40 mg/dL (convert µmol/L ÷ 88.4)")
    if not (18 <= age <= 120):
        # Cockcroft-Gault was derived and validated in adults only; in children it
        # misestimates clearance (paediatric dosing uses the bedside Schwartz equation)
        raise ValueError("Age must be between 18 and 120 years (Cockcroft-Gault is adult-only)")
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


def crcl_dosing_weight(weight: float, height_cm: float, sex: str) -> tuple:
    """
    Weight for Cockcroft-Gault (actual-weight CG overestimates CrCl in obesity).
    IBW (Devine): 50 kg male / 45.5 kg female + 2.3 kg per inch over 60 in
    (no subtraction below 5 ft). Use actual weight if below IBW, adjusted weight
    IBW + 0.4 * (actual - IBW) if above 120% of IBW, otherwise IBW.
    Returns (kg, basis).
    """
    _require_finite(weight=weight, height_cm=height_cm)
    if not (0 < weight <= 650):
        # Same bounds as creatinine_clearance; a negative/zero or extra-digit weight
        # was otherwise returned as a plausible "actual"/"adjusted" dosing weight
        raise ValueError("Weight must be positive and not exceed 650 kg")
    if not (100 <= height_cm <= 250):
        raise ValueError("Height must be between 100 and 250 cm")
    sex_key = str(sex).strip().lower()
    if sex_key not in ("m", "male", "f", "female"):
        raise ValueError("Sex must be 'male' or 'female'")
    base = 50.0 if sex_key in ("m", "male") else 45.5
    ibw = base + 2.3 * max(0.0, height_cm / 2.54 - 60)
    if weight < ibw:
        return weight, "actual"
    if weight > 1.2 * ibw:
        return round(ibw + 0.4 * (weight - ibw), 1), "adjusted"
    return round(ibw, 1), "ideal"
