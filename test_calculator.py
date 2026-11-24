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


def test_map_sbp_must_exceed_dbp():
    with pytest.raises(ValueError):
        mean_arterial_pressure(80, 90)


def test_map_nonpositive_sbp():
    with pytest.raises(ValueError):
        mean_arterial_pressure(0, 0)


def test_map_implausible_systolic():
    with pytest.raises(ValueError):
        mean_arterial_pressure(400, 80)
    assert mean_arterial_pressure(300, 100) == 166.7


def test_pf_ratio_normal():
    assert pf_ratio(100, 1.0) == 100.0


def test_pf_ratio_ards():
    # PaO2 60, FiO2 0.8 → 75 (severe ARDS)
    assert pf_ratio(60, 0.8) == 75.0


def test_pf_ratio_bad_fio2():
    with pytest.raises(ValueError):
        pf_ratio(100, 0)


def test_pf_ratio_subatmospheric_fio2():
    with pytest.raises(ValueError):
        pf_ratio(100, 0.05)  # typo for 0.5
    assert pf_ratio(84, 0.21) == 400.0


def test_pf_ratio_nonpositive_pao2():
    with pytest.raises(ValueError):
        pf_ratio(0, 0.5)


def test_pf_ratio_implausible_pao2():
    with pytest.raises(ValueError):
        pf_ratio(1000, 1.0)  # typo for 100
    assert pf_ratio(800, 1.0) == 800.0


def test_anion_gap_normal():
    # Na 140, Cl 104, HCO3 24 → 12
    assert anion_gap(140, 104, 24) == 12.0


def test_anion_gap_elevated():
    # DKA-like: Na 138, Cl 98, HCO3 10 → 30
    assert anion_gap(138, 98, 10) == 30.0


def test_anion_gap_negative_input():
    with pytest.raises(ValueError):
        anion_gap(140, -104, 24)


def test_anion_gap_implausible_sodium():
    with pytest.raises(ValueError):
        anion_gap(14, 104, 24)  # typo for 140
    with pytest.raises(ValueError):
        anion_gap(250, 104, 24)
    assert anion_gap(200, 104, 24) == 72.0


def test_anion_gap_implausible_chloride():
    with pytest.raises(ValueError):
        anion_gap(140, 10, 24)  # typo for 104
    with pytest.raises(ValueError):
        anion_gap(140, 1040, 24)
    assert anion_gap(140, 50, 24) == 66.0
    assert anion_gap(200, 160, 24) == 16.0


def test_anion_gap_implausible_bicarbonate():
    with pytest.raises(ValueError):
        anion_gap(140, 104, 240)  # typo for 24
    assert anion_gap(140, 70, 60) == 10.0


def test_crcl_male():
    # 50yo, 70kg, Cr 1.0 → 87.5  (Cockcroft-Gault: (90×70)/72)
    assert creatinine_clearance(50, 70, 1.0, "male") == 87.5


def test_crcl_female():
    # Same but female → 74.4  (87.5 × 0.85)
    assert creatinine_clearance(50, 70, 1.0, "female") == 74.4


def test_crcl_bad_creatinine():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 0, "male")


def test_crcl_creatinine_unit_confusion():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 88, "male")  # µmol/L typed as mg/dL
    assert creatinine_clearance(50, 70, 30, "male") == 2.9


def test_crcl_nonpositive_weight():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 0, 1.0, "male")


def test_crcl_implausible_weight():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70000, 1.0, "male")  # grams typed as kg
    assert creatinine_clearance(50, 400, 1.0, "male") == 500.0


def test_crcl_age_out_of_range():
    with pytest.raises(ValueError):
        creatinine_clearance(150, 70, 1.0, "male")


@pytest.mark.parametrize("sex", ["", "xyz", None, 1])
def test_crcl_invalid_sex_rejected(sex):
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 1.0, sex)


def test_crcl_sex_case_and_whitespace():
    assert creatinine_clearance(50, 70, 1.0, " Female ") == 74.4
    assert creatinine_clearance(50, 70, 1.0, "M") == 87.5


@pytest.mark.parametrize("call", [
    lambda: mean_arterial_pressure(float("nan"), 80),
    lambda: pf_ratio(float("inf"), 0.5),
    lambda: anion_gap(140, float("nan"), 24),
    lambda: creatinine_clearance(50, float("inf"), 1.0, "male"),
])
def test_nonfinite_inputs_rejected(call):
    with pytest.raises(ValueError):
        call()


@pytest.mark.parametrize("call", [
    lambda: mean_arterial_pressure("120", 80),
    lambda: pf_ratio(None, 0.5),
    lambda: anion_gap(140, 104, True),
    lambda: creatinine_clearance(50, [70], 1.0, "male"),
])
def test_non_numeric_inputs_rejected(call):
    with pytest.raises(ValueError):
        call()


def test_disclaimer_present():
    assert "NOT FOR CLINICAL USE" in DISCLAIMER


def test_app_crcl_missing_sex_not_defaulted_to_male():
    from app import app
    client = app.test_client()
    data = {"calc": "crcl", "age": "50", "weight": "70", "creatinine": "1.0"}
    html = client.post("/", data=data).get_data(as_text=True)
    assert "Sex must be" in html and "87.5" not in html
    html = client.post("/", data={**data, "sex": "female"}).get_data(as_text=True)
    assert "74.4" in html
