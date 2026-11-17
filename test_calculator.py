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
    corrected_sodium,
    creatinine_clearance,
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


def test_corrected_sodium_normoglycaemia():
    # Glucose = 100 → no correction
    assert corrected_sodium(140, 100) == 140.0


def test_corrected_sodium_hyperglycaemia():
    # Glucose 500: 140 + 1.6 * (500-100)/100 = 140 + 6.4 = 146.4
    assert corrected_sodium(140, 500) == 146.4


def test_corrected_sodium_bad_glucose():
    with pytest.raises(ValueError):
        corrected_sodium(140, -1)


def test_disclaimer_present():
    assert "NOT FOR CLINICAL USE" in DISCLAIMER
