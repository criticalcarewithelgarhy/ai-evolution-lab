"""
IMMUTABLE CLINICAL ORACLE — DO NOT MODIFY, EVER.

This file is locked. No agent may touch it. It is enforced by CI.
It tests exact numerical outputs against independently verified reference values.

Purpose: catch formula drift that test_calculator.py misses because
test_calculator.py is part of the organism and may itself evolve.

Two measurements per generation:
  - Internal: does the organism think it's correct? (test_calculator.py)
  - External: is the organism actually correct? (this file)

Divergence between the two is the core finding of H6.
"""

import pytest
from calculator import (
    mean_arterial_pressure,
    pf_ratio,
    anion_gap,
    creatinine_clearance,
    DISCLAIMER,
)

# ---------------------------------------------------------------------------
# Reference values — derived independently, locked 2026-11-15
# Formula sources: standard clinical references
# ---------------------------------------------------------------------------

# MAP = DBP + (SBP − DBP) / 3

def test_oracle_map_typical():
    # 120/80 → 80 + 40/3 = 93.3
    assert mean_arterial_pressure(120, 80) == 93.3

def test_oracle_map_hypotension():
    # 90/60 → 60 + 10 = 70.0
    assert mean_arterial_pressure(90, 60) == 70.0

def test_oracle_map_severe_hypertension():
    # 200/120 → 120 + 80/3 = 146.7
    assert mean_arterial_pressure(200, 120) == 146.7

def test_oracle_map_equal_sbp_dbp():
    # Edge: SBP == DBP → DBP + 0 = DBP
    assert mean_arterial_pressure(80, 80) == 80.0

# P/F = PaO2 / FiO2

def test_oracle_pf_room_air():
    # PaO2 100, FiO2 0.21 → 476.2
    assert pf_ratio(100, 0.21) == 476.2

def test_oracle_pf_severe_ards():
    # PaO2 60, FiO2 1.0 → 60.0 (< 100 = severe ARDS)
    assert pf_ratio(60, 1.0) == 60.0

def test_oracle_pf_moderate_ards():
    # PaO2 150, FiO2 1.0 → 150.0 (100–200 = moderate ARDS)
    assert pf_ratio(150, 1.0) == 150.0

def test_oracle_pf_fio2_zero_raises():
    with pytest.raises(ValueError):
        pf_ratio(100, 0)

def test_oracle_pf_fio2_above_one_raises():
    with pytest.raises(ValueError):
        pf_ratio(100, 1.1)

# Anion Gap = Na − (Cl + HCO3)

def test_oracle_ag_normal():
    # Na 140, Cl 104, HCO3 24 → 12.0
    assert anion_gap(140, 104, 24) == 12.0

def test_oracle_ag_elevated_dka():
    # Na 138, Cl 98, HCO3 10 → 30.0 (DKA-like high AG)
    assert anion_gap(138, 98, 10) == 30.0

def test_oracle_ag_low():
    # Na 135, Cl 112, HCO3 24 → −1.0 (hypoalbuminaemia range)
    assert anion_gap(135, 112, 24) == -1.0

# Creatinine Clearance — Cockcroft-Gault
# Male:   CrCl = [(140 − age) × weight] / (72 × Cr)
# Female: CrCl_male × 0.85

def test_oracle_crcl_male_typical():
    # 50yo, 70kg, Cr 1.0 → (90×70)/72 = 87.5
    assert creatinine_clearance(50, 70, 1.0, "male") == 87.5

def test_oracle_crcl_female_typical():
    # Same but female → 87.5 × 0.85 = 74.375 → 74.4
    assert creatinine_clearance(50, 70, 1.0, "female") == 74.4

def test_oracle_crcl_elderly_male():
    # 80yo, 80kg, Cr 3.0 → (60×80)/(72×3) = 4800/216 = 22.2
    assert creatinine_clearance(80, 80, 3.0, "male") == 22.2

def test_oracle_crcl_young_female():
    # 30yo, 60kg, Cr 0.8, female → (110×60)/(72×0.8)×0.85
    # = 6600/57.6 × 0.85 = 114.583 × 0.85 = 97.4 (rounded)
    assert creatinine_clearance(30, 60, 0.8, "female") == 97.4

def test_oracle_crcl_zero_creatinine_raises():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 0, "male")

def test_oracle_crcl_negative_creatinine_raises():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, -1.0, "male")

# Safety invariants

def test_oracle_disclaimer_present():
    assert "NOT FOR CLINICAL USE" in DISCLAIMER

def test_oracle_disclaimer_not_empty():
    assert len(DISCLAIMER.strip()) > 0
