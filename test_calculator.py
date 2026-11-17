"""
Regression tests — clinical correctness is the selection pressure.
Known inputs must always produce known outputs.
A generation that breaks any test is rejected entirely.
"""

import pytest
from calculator import (
    mean_arterial_pressure,
    pf_ratio,
    anion_gap,
    creatinine_clearance,
    glasgow_coma_scale,
    curb65,
    DISCLAIMER,
)


def test_map_typical():
    assert mean_arterial_pressure(120, 80) == 93.3


def test_map_hypotension():
    assert mean_arterial_pressure(90, 60) == 70.0


def test_pf_ratio_normal():
    assert pf_ratio(100, 1.0) == 100.0


def test_pf_ratio_ards():
    # PaO2 60, FiO2 0.8 → 75 (severe ARDS)
    assert pf_ratio(60, 0.8) == 75.0


def test_pf_ratio_bad_fio2():
    with pytest.raises(ValueError):
        pf_ratio(100, 0)


def test_anion_gap_normal():
    # Na 140, Cl 104, HCO3 24 → 12
    assert anion_gap(140, 104, 24) == 12.0


def test_anion_gap_elevated():
    # DKA-like: Na 138, Cl 98, HCO3 10 → 30
    assert anion_gap(138, 98, 10) == 30.0


def test_crcl_male():
    # 50yo, 70kg, Cr 1.0 → 87.5  (Cockcroft-Gault: (90×70)/72)
    assert creatinine_clearance(50, 70, 1.0, "male") == 87.5


def test_crcl_female():
    # Same but female → 74.4  (87.5 × 0.85)
    assert creatinine_clearance(50, 70, 1.0, "female") == 74.4


def test_crcl_bad_creatinine():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 0, "male")


def test_disclaimer_present():
    assert "NOT FOR CLINICAL USE" in DISCLAIMER


def test_gcs_max():
    assert glasgow_coma_scale(4, 5, 6) == 15


def test_gcs_min():
    assert glasgow_coma_scale(1, 1, 1) == 3


def test_gcs_typical_coma():
    # E2V2M4 = 8, severe TBI threshold
    assert glasgow_coma_scale(2, 2, 4) == 8


def test_gcs_bad_eye():
    with pytest.raises(ValueError):
        glasgow_coma_scale(5, 5, 6)


def test_gcs_bad_motor():
    with pytest.raises(ValueError):
        glasgow_coma_scale(4, 5, 7)


def test_curb65_zero():
    # No risk factors → 0
    assert curb65(0, 0, 18, 120, 80, 50) == 0


def test_curb65_max():
    # All five criteria met → 5
    assert curb65(1, 1, 32, 85, 55, 70) == 5


def test_curb65_resp_threshold():
    # Resp rate exactly 30 scores a point
    assert curb65(0, 0, 30, 120, 80, 50) == 1


def test_curb65_age_threshold():
    # Age exactly 65 scores a point
    assert curb65(0, 0, 18, 120, 80, 65) == 1


def test_curb65_bp_criterion():
    # SBP < 90 triggers BP criterion
    assert curb65(0, 0, 18, 89, 80, 50) == 1
