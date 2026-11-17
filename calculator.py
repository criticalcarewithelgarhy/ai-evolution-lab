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


def albumin_corrected_anion_gap(
    sodium: float, chloride: float, bicarbonate: float, albumin: float
) -> float:
    """
    Albumin-corrected AG = AG + 2.5 × (4.0 − albumin_g_dL).
    Corrects for hypoalbuminaemia which lowers the apparent anion gap.
    """
    if albumin < 0:
        raise ValueError("Albumin must be non-negative")
    ag = sodium - (chloride + bicarbonate)
    return round(ag + 2.5 * (4.0 - albumin), 1)


def osmolar_gap(
    measured_osmolality: float,
    sodium: float,
    glucose: float,
    bun: float,
) -> float:
    """
    Osmolar gap = measured osmolality − calculated osmolality.
    Calculated osmolality = 2×Na + glucose/18 + BUN/2.8
    glucose and BUN in mg/dL, osmolality in mOsm/kg.
    Normal OG < 10 mOsm/kg; elevated OG suggests toxic alcohols.
    """
    if glucose < 0:
        raise ValueError("Glucose must be non-negative")
    if bun < 0:
        raise ValueError("BUN must be non-negative")
    calc = 2 * sodium + glucose / 18 + bun / 2.8
    return round(measured_osmolality - calc, 1)


def corrected_calcium(calcium: float, albumin: float) -> float:
    """
    Corrected calcium for hypoalbuminaemia.
    Corrected Ca = measured Ca + 0.8 × (4.0 − albumin)
    calcium and result in mg/dL, albumin in g/dL.
    """
    if calcium < 0:
        raise ValueError("Calcium must be non-negative")
    if albumin < 0:
        raise ValueError("Albumin must be non-negative")
    return round(calcium + 0.8 * (4.0 - albumin), 1)


def winters_formula(bicarbonate: float) -> tuple:
    """
    Winter's formula: expected PaCO2 = 1.5 × HCO3 + 8 (± 2) mmHg.
    Returns (low, high) expected PaCO2 range for compensated metabolic acidosis.
    """
    if bicarbonate <= 0:
        raise ValueError("Bicarbonate must be positive")
    centre = 1.5 * bicarbonate + 8
    return round(centre - 2, 1), round(centre + 2, 1)


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
