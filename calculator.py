"""
ICU Calculator — generation 0 seed.
Four formulas: MAP, P/F ratio, anion gap, creatinine clearance (Cockcroft-Gault).
"""

DISCLAIMER = "EXPERIMENTAL — NOT FOR CLINICAL USE"


def _is_female(sex: str) -> bool:
    """Validate sex ('m', 'male', 'f', 'female'; any case) and return True if female."""
    sex_lower = sex.lower()
    if sex_lower not in ("m", "male", "f", "female"):
        raise ValueError("Sex must be 'm', 'male', 'f', or 'female'")
    return sex_lower in ("f", "female")


def _check_fio2(fio2: float) -> None:
    """Validate FiO2 as a fraction in (0, 1]."""
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")


def mean_arterial_pressure(systolic: float, diastolic: float) -> float:
    """MAP = DBP + 1/3 (SBP - DBP)"""
    if systolic <= 0 or diastolic <= 0:
        raise ValueError("Pressures must be positive")
    if systolic < diastolic:
        raise ValueError("Systolic must be >= diastolic")
    return round(diastolic + (systolic - diastolic) / 3, 1)


def pf_ratio(pao2: float, fio2: float) -> float:
    """P/F ratio = PaO2 / FiO2 (FiO2 as fraction 0-1)"""
    if pao2 <= 0:
        raise ValueError("PaO2 must be positive")
    _check_fio2(fio2)
    return round(pao2 / fio2, 1)


def anion_gap(sodium: float, chloride: float, bicarbonate: float) -> float:
    """AG = Na - (Cl + HCO3)"""
    if sodium <= 0 or chloride <= 0 or bicarbonate <= 0:
        raise ValueError("Electrolytes must be positive")
    return round(sodium - (chloride + bicarbonate), 1)


def corrected_anion_gap(
    sodium: float, chloride: float, bicarbonate: float, albumin: float
) -> float:
    """Albumin-corrected AG = AG + 2.5 * (4.0 - albumin), albumin in g/dL"""
    if albumin <= 0:
        raise ValueError("Albumin must be positive")
    return round(anion_gap(sodium, chloride, bicarbonate) + 2.5 * (4.0 - albumin), 1)


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
    if age <= 0:
        raise ValueError("Age must be positive")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    result = ((140 - age) * weight) / (72 * creatinine)
    if _is_female(sex):
        result *= 0.85
    return round(result, 1)


def shock_index(heart_rate: float, systolic: float) -> float:
    """Shock index = HR / SBP; > 1.0 suggests haemodynamic instability"""
    if heart_rate <= 0 or systolic <= 0:
        raise ValueError("Heart rate and systolic pressure must be positive")
    return round(heart_rate / systolic, 2)


def ards_severity(pao2: float, fio2: float) -> str:
    """Berlin ARDS severity by P/F: severe <=100, moderate <=200, mild <=300"""
    ratio = pf_ratio(pao2, fio2)
    if ratio <= 100:
        return "severe"
    if ratio <= 200:
        return "moderate"
    if ratio <= 300:
        return "mild"
    return "none"


def winters_formula(bicarbonate: float) -> tuple:
    """Expected PaCO2 in metabolic acidosis = 1.5 * HCO3 + 8 (± 2), mmHg"""
    if bicarbonate <= 0:
        raise ValueError("Bicarbonate must be positive")
    expected = 1.5 * bicarbonate + 8
    return (round(expected - 2, 1), round(expected + 2, 1))


def delta_ratio(sodium: float, chloride: float, bicarbonate: float) -> float:
    """Delta ratio = (AG - 12) / (24 - HCO3); <1 mixed NAGMA, >2 concurrent met. alkalosis"""
    if bicarbonate >= 24:
        raise ValueError("Bicarbonate must be below 24 for a delta ratio")
    return round((anion_gap(sodium, chloride, bicarbonate) - 12) / (24 - bicarbonate), 2)


def corrected_sodium(sodium: float, glucose: float) -> float:
    """Katz-corrected Na = Na + 1.6 * (glucose - 100) / 100, glucose in mg/dL"""
    if sodium <= 0 or glucose <= 0:
        raise ValueError("Sodium and glucose must be positive")
    return round(sodium + 1.6 * (glucose - 100) / 100, 1)


def free_water_deficit(sodium: float, weight: float, sex: str) -> float:
    """FWD (L) = TBW * (Na / 140 - 1); TBW = 0.6 * kg (male) or 0.5 * kg (female)"""
    if sodium <= 0 or weight <= 0:
        raise ValueError("Sodium and weight must be positive")
    tbw = (0.5 if _is_female(sex) else 0.6) * weight
    return round(tbw * (sodium / 140 - 1), 1)


def corrected_calcium(calcium: float, albumin: float) -> float:
    """Payne-corrected Ca = Ca + 0.8 * (4.0 - albumin); Ca mg/dL, albumin g/dL"""
    if calcium <= 0 or albumin <= 0:
        raise ValueError("Calcium and albumin must be positive")
    return round(calcium + 0.8 * (4.0 - albumin), 1)


def aa_gradient(pao2: float, paco2: float, fio2: float) -> float:
    """A-a gradient = FiO2 * (760 - 47) - PaCO2 / 0.8 - PaO2, mmHg at sea level"""
    if pao2 <= 0 or paco2 <= 0:
        raise ValueError("PaO2 and PaCO2 must be positive")
    _check_fio2(fio2)
    return round(fio2 * (760 - 47) - paco2 / 0.8 - pao2, 1)


def serum_osmolality(sodium: float, glucose: float, bun: float) -> float:
    """Calculated Osm = 2 * Na + glucose / 18 + BUN / 2.8; glucose, BUN in mg/dL"""
    if sodium <= 0 or glucose <= 0 or bun <= 0:
        raise ValueError("Sodium, glucose and BUN must be positive")
    return round(2 * sodium + glucose / 18 + bun / 2.8, 1)


def osmolar_gap(measured: float, sodium: float, glucose: float, bun: float) -> float:
    """Osmolar gap = measured Osm - calculated Osm; > 10 suggests toxic alcohols"""
    if measured <= 0:
        raise ValueError("Measured osmolality must be positive")
    return round(measured - serum_osmolality(sodium, glucose, bun), 1)


def predicted_body_weight(height_cm: float, sex: str) -> float:
    """ARDSNet PBW (kg) = 50 (male) or 45.5 (female) + 0.91 * (height_cm - 152.4)"""
    if height_cm <= 0:
        raise ValueError("Height must be positive")
    base = 45.5 if _is_female(sex) else 50.0
    return round(base + 0.91 * (height_cm - 152.4), 1)


def tidal_volume(height_cm: float, sex: str, ml_per_kg: float = 6.0) -> float:
    """Lung-protective Vt (mL) = ml_per_kg * PBW; ARDSNet target 4-8 mL/kg"""
    if not (4 <= ml_per_kg <= 8):
        raise ValueError("mL/kg must be between 4 and 8")
    return round(ml_per_kg * predicted_body_weight(height_cm, sex))


def driving_pressure(plateau: float, peep: float) -> float:
    """Driving pressure (cmH2O) = Pplat - PEEP; target < 15 in ARDS"""
    if plateau <= 0 or peep < 0:
        raise ValueError("Plateau must be positive and PEEP non-negative")
    if plateau < peep:
        raise ValueError("Plateau must be >= PEEP")
    return round(plateau - peep, 1)


def static_compliance(tidal_volume_ml: float, plateau: float, peep: float) -> float:
    """Static compliance (mL/cmH2O) = Vt / (Pplat - PEEP); normal ~50-100"""
    if tidal_volume_ml <= 0:
        raise ValueError("Tidal volume must be positive")
    dp = driving_pressure(plateau, peep)
    if dp == 0:
        raise ValueError("Plateau must exceed PEEP")
    return round(tidal_volume_ml / dp, 1)


def oxygenation_index(pao2: float, fio2: float, mean_airway_pressure: float) -> float:
    """OI = FiO2 * 100 * mean airway pressure / PaO2; > 25 suggests severe hypoxaemia"""
    if mean_airway_pressure <= 0:
        raise ValueError("Mean airway pressure must be positive")
    pf_ratio(pao2, fio2)  # validates PaO2 and FiO2
    return round(fio2 * 100 * mean_airway_pressure / pao2, 1)


def rox_index(spo2: float, fio2: float, respiratory_rate: float) -> float:
    """ROX = (SpO2 / FiO2) / RR; >= 4.88 at 12 h predicts HFNC success"""
    if not (0 < spo2 <= 100) or respiratory_rate <= 0:
        raise ValueError("SpO2 must be 0-100 and respiratory rate positive")
    _check_fio2(fio2)
    return round(spo2 / fio2 / respiratory_rate, 2)


def qsofa_score(respiratory_rate: float, systolic: float, altered_mentation: bool) -> int:
    """qSOFA: 1 point each for RR >= 22, SBP <= 100, altered mentation; >= 2 flags sepsis risk"""
    if respiratory_rate <= 0 or systolic <= 0:
        raise ValueError("Respiratory rate and systolic pressure must be positive")
    return int(respiratory_rate >= 22) + int(systolic <= 100) + int(bool(altered_mentation))


def rsbi(respiratory_rate: float, tidal_volume_ml: float) -> float:
    """Rapid shallow breathing index = RR / Vt (L); < 105 predicts weaning success"""
    if respiratory_rate <= 0 or tidal_volume_ml <= 0:
        raise ValueError("Respiratory rate and tidal volume must be positive")
    return round(respiratory_rate / (tidal_volume_ml / 1000), 1)
