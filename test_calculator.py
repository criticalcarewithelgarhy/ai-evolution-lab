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
    DISCLAIMER,
)


def test_map_typical():
    assert mean_arterial_pressure(120, 80) == 93.3


def test_map_hypotension():
    assert mean_arterial_pressure(90, 60) == 70.0


def test_map_swapped_sbp_dbp():
    # SBP < DBP (fields swapped) must not silently return a plausible MAP
    with pytest.raises(ValueError):
        mean_arterial_pressure(80, 120)


def test_map_negative_dbp():
    with pytest.raises(ValueError):
        mean_arterial_pressure(120, -10)


def test_map_equal_sbp_dbp():
    assert mean_arterial_pressure(80, 80) == 80.0


def test_pf_ratio_normal():
    assert pf_ratio(100, 1.0) == 100.0


def test_pf_ratio_ards():
    # PaO2 60, FiO2 0.8 → 75 (severe ARDS)
    assert pf_ratio(60, 0.8) == 75.0


def test_pf_ratio_bad_fio2():
    with pytest.raises(ValueError):
        pf_ratio(100, 0)


def test_pf_ratio_below_room_air():
    with pytest.raises(ValueError):
        pf_ratio(100, 0.20)


@pytest.mark.parametrize("pao2", [0, -50])
def test_pf_ratio_non_positive_pao2(pao2):
    # Non-positive PaO2 is impossible and would return a zero/negative P/F
    with pytest.raises(ValueError):
        pf_ratio(pao2, 0.5)


def test_pf_ratio_room_air():
    # FiO2 0.21 is the minimum valid value (room air)
    assert pf_ratio(100, 0.21) == 476.2


def test_anion_gap_normal():
    # Na 140, Cl 104, HCO3 24 → 12
    assert anion_gap(140, 104, 24) == 12.0


def test_anion_gap_elevated():
    # DKA-like: Na 138, Cl 98, HCO3 10 → 30
    assert anion_gap(138, 98, 10) == 30.0


@pytest.mark.parametrize("na,cl,hco3", [(0, 104, 24), (-140, 104, 24), (140, -104, 24), (140, 104, -24)])
def test_anion_gap_negative_electrolytes(na, cl, hco3):
    # A sign-entry error (e.g. HCO3 -24) silently inflates the AG into a false high-AG acidosis
    with pytest.raises(ValueError):
        anion_gap(na, cl, hco3)


def test_anion_gap_zero_bicarbonate():
    # HCO3 of 0 is extreme but measurable; must still compute
    assert anion_gap(140, 100, 0) == 40.0


def test_crcl_male():
    # 50yo, 70kg, Cr 1.0 → 87.5  (Cockcroft-Gault: (90×70)/72)
    assert creatinine_clearance(50, 70, 1.0, "male") == 87.5


def test_crcl_female():
    # Same but female → 74.4  (87.5 × 0.85)
    assert creatinine_clearance(50, 70, 1.0, "female") == 74.4


def test_crcl_bad_creatinine():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 0, "male")


def test_crcl_bad_age_zero():
    with pytest.raises(ValueError):
        creatinine_clearance(0, 70, 1.0, "male")


def test_crcl_bad_age_over_120():
    with pytest.raises(ValueError):
        creatinine_clearance(150, 70, 1.0, "male")


def test_crcl_bad_weight_zero():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 0, 1.0, "male")


def test_crcl_sex_case_and_whitespace():
    assert creatinine_clearance(50, 70, 1.0, " Female ") == 74.4
    assert creatinine_clearance(50, 70, 1.0, "M") == 87.5


def test_crcl_bad_sex():
    # Unknown sex must not silently default to the male formula
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 1.0, "fem")


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_inputs_rejected(bad):
    # float("nan") parses from form text and passes every range check silently
    for call in (
        lambda: mean_arterial_pressure(bad, 80),
        lambda: mean_arterial_pressure(120, bad),
        lambda: pf_ratio(bad, 0.5),
        lambda: pf_ratio(100, bad),
        lambda: anion_gap(bad, 104, 24),
        lambda: anion_gap(140, 104, bad),
        lambda: creatinine_clearance(50, bad, 1.0, "male"),
        lambda: creatinine_clearance(50, 70, bad, "male"),
    ):
        with pytest.raises(ValueError):
            call()


@pytest.mark.parametrize("pf,label", [
    (100.0, "Severe"), (100.1, "Moderate"), (200.0, "Moderate"),
    (200.1, "Mild"), (300.0, "Mild"), (300.1, "Normal"),
])
def test_pf_interp_berlin_inclusive_boundaries(pf, label):
    # Berlin ARDS: P/F exactly 100/200/300 belongs to the more severe category
    from app import _pf_interp
    assert _pf_interp(pf)[0].startswith(label)


def test_disclaimer_present():
    assert "NOT FOR CLINICAL USE" in DISCLAIMER
