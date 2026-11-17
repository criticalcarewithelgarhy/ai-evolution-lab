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
