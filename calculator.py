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


def delta_ratio(sodium: float, chloride: float, bicarbonate: float) -> float:
    """
    Delta ratio (delta-delta) = (AG − 12) / (24 − HCO3).
    Identifies mixed disorders in high anion gap metabolic acidosis.
    <0.4 hyperchloraemic NAGMA; 0.4–0.8 mixed HAGMA + NAGMA;
    0.8–2 pure HAGMA; >2 concurrent metabolic alkalosis.
    """
    if bicarbonate >= 24:
        raise ValueError("Bicarbonate must be below 24 for delta ratio")
    ag = sodium - (chloride + bicarbonate)
    return round((ag - 12) / (24 - bicarbonate), 2)


def aa_gradient(
    pao2: float, paco2: float, fio2: float, patm: float = 760, rq: float = 0.8
) -> float:
    """
    Alveolar-arterial O2 gradient = PAO2 − PaO2.
    PAO2 = FiO2 × (Patm − 47) − PaCO2 / RQ  (PH2O 47 mmHg, RQ 0.8).
    Normal ≈ age/4 + 4 mmHg on room air.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if paco2 < 0:
        raise ValueError("PaCO2 must be non-negative")
    alveolar = fio2 * (patm - 47) - paco2 / rq
    return round(alveolar - pao2, 1)


def corrected_sodium(sodium: float, glucose: float) -> float:
    """
    Sodium corrected for hyperglycaemia (Katz).
    Corrected Na = Na + 1.6 × (glucose − 100) / 100
    sodium in mEq/L, glucose in mg/dL.
    """
    if glucose < 0:
        raise ValueError("Glucose must be non-negative")
    return round(sodium + 1.6 * (glucose - 100) / 100, 1)


def free_water_deficit(sodium: float, weight: float, sex: str, target: float = 140) -> float:
    """
    Free water deficit (L) = TBW × (Na / target − 1).
    TBW = weight × 0.6 (male) or 0.5 (female). weight in kg, sodium in mEq/L.
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if sodium <= 0 or target <= 0:
        raise ValueError("Sodium must be positive")
    tbw = weight * (0.5 if sex.lower() in ("f", "female") else 0.6)
    return round(tbw * (sodium / target - 1), 1)


def ideal_body_weight(height_cm: float, sex: str) -> float:
    """
    Ideal body weight (Devine): 50 kg (male) or 45.5 kg (female)
    + 2.3 kg per inch of height over 60 in. height in cm, result in kg.
    Used for lung-protective tidal volume (6–8 mL/kg IBW).
    """
    if height_cm <= 0:
        raise ValueError("Height must be positive")
    base = 45.5 if sex.lower() in ("f", "female") else 50.0
    return round(base + 2.3 * (height_cm / 2.54 - 60), 1)


def shock_index(heart_rate: float, systolic: float) -> float:
    """
    Shock index = heart rate / systolic BP.
    Normal 0.5–0.7; > 1.0 suggests haemodynamic instability / occult shock.
    """
    if heart_rate < 0:
        raise ValueError("Heart rate must be non-negative")
    if systolic <= 0:
        raise ValueError("Systolic BP must be positive")
    return round(heart_rate / systolic, 2)


def rox_index(spo2: float, fio2: float, resp_rate: float) -> float:
    """
    ROX index = (SpO2 / FiO2) / respiratory rate.
    SpO2 in %, FiO2 as fraction 0-1, RR in breaths/min.
    On high-flow nasal oxygen, ≥ 4.88 predicts HFNC success; < 3.85 high risk of intubation.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if not (0 <= spo2 <= 100):
        raise ValueError("SpO2 must be between 0 and 100")
    if resp_rate <= 0:
        raise ValueError("Respiratory rate must be positive")
    return round((spo2 / fio2) / resp_rate, 2)


def driving_pressure(plateau: float, peep: float) -> float:
    """
    Driving pressure (ΔP) = plateau pressure − PEEP (cmH2O).
    In ARDS, ΔP ≥ 15 cmH2O is associated with increased mortality.
    """
    if peep < 0:
        raise ValueError("PEEP must be non-negative")
    if plateau < peep:
        raise ValueError("Plateau pressure must be at least PEEP")
    return round(plateau - peep, 1)


def static_compliance(tidal_volume: float, plateau: float, peep: float) -> float:
    """
    Static respiratory system compliance (mL/cmH2O) = Vt / (Pplat − PEEP).
    tidal_volume in mL, pressures in cmH2O. Normal ≈ 50–100 mL/cmH2O; < 40 suggests stiff lungs (ARDS).
    """
    if tidal_volume <= 0:
        raise ValueError("Tidal volume must be positive")
    if peep < 0:
        raise ValueError("PEEP must be non-negative")
    if plateau <= peep:
        raise ValueError("Plateau pressure must exceed PEEP")
    return round(tidal_volume / (plateau - peep), 1)


def oxygenation_index(fio2: float, mean_airway_pressure: float, pao2: float) -> float:
    """
    Oxygenation index (OI) = (FiO2 × mean airway pressure × 100) / PaO2.
    FiO2 as fraction 0-1, mean airway pressure in cmH2O, PaO2 in mmHg.
    Higher OI = worse oxygenation; > 25 severe hypoxaemic respiratory failure.
    """
    if not (0 < fio2 <= 1):
        raise ValueError("FiO2 must be between 0 and 1")
    if mean_airway_pressure < 0:
        raise ValueError("Mean airway pressure must be non-negative")
    if pao2 <= 0:
        raise ValueError("PaO2 must be positive")
    return round(fio2 * mean_airway_pressure * 100 / pao2, 1)


def mechanical_power(
    resp_rate: float, tidal_volume: float, peak: float, plateau: float, peep: float
) -> float:
    """
    Mechanical power (simplified Gattinoni), J/min =
    0.098 × RR × Vt(L) × (Ppeak − ½ × (Pplat − PEEP)).
    tidal_volume in mL, pressures in cmH2O. > 17 J/min associated with higher ARDS mortality.
    """
    if resp_rate <= 0:
        raise ValueError("Respiratory rate must be positive")
    if tidal_volume <= 0:
        raise ValueError("Tidal volume must be positive")
    if peep < 0:
        raise ValueError("PEEP must be non-negative")
    if plateau < peep:
        raise ValueError("Plateau pressure must be at least PEEP")
    if peak < plateau:
        raise ValueError("Peak pressure must be at least plateau pressure")
    return round(0.098 * resp_rate * tidal_volume / 1000 * (peak - (plateau - peep) / 2), 1)


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
