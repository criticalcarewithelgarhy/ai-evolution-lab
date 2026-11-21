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
