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
    corrected_anion_gap,
    creatinine_clearance,
    shock_index,
    ards_severity,
    winters_formula,
    delta_ratio,
    corrected_sodium,
    free_water_deficit,
    corrected_calcium,
    aa_gradient,
    serum_osmolality,
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


def test_pf_ratio_bad_pao2():
    with pytest.raises(ValueError):
        pf_ratio(0, 0.5)


def test_anion_gap_normal():
    # Na 140, Cl 104, HCO3 24 → 12
    assert anion_gap(140, 104, 24) == 12.0


def test_anion_gap_elevated():
    # DKA-like: Na 138, Cl 98, HCO3 10 → 30
    assert anion_gap(138, 98, 10) == 30.0


def test_anion_gap_bad_electrolytes():
    with pytest.raises(ValueError):
        anion_gap(140, 0, 24)


def test_corrected_anion_gap_low_albumin():
    # AG 12, albumin 2.0 → 12 + 2.5 × 2 = 17
    assert corrected_anion_gap(140, 104, 24, 2.0) == 17.0


def test_corrected_anion_gap_bad_albumin():
    with pytest.raises(ValueError):
        corrected_anion_gap(140, 104, 24, 0)


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


def test_shock_index_elevated():
    # HR 120, SBP 100 → 1.2
    assert shock_index(120, 100) == 1.2


def test_shock_index_bad_input():
    with pytest.raises(ValueError):
        shock_index(80, 0)


def test_ards_severity_bands():
    assert ards_severity(60, 0.8) == "severe"      # P/F 75
    assert ards_severity(150, 1.0) == "moderate"   # P/F 150
    assert ards_severity(125, 0.5) == "mild"       # P/F 250
    assert ards_severity(95, 0.21) == "none"       # P/F 452.4


def test_winters_formula_dka():
    # HCO3 10 → 1.5×10 + 8 = 23, range 21–25
    assert winters_formula(10) == (21.0, 25.0)


def test_winters_formula_bad_input():
    with pytest.raises(ValueError):
        winters_formula(0)


def test_delta_ratio_pure_hagma():
    # Na 138, Cl 98, HCO3 10 → AG 30; (30-12)/(24-10) = 1.29
    assert delta_ratio(138, 98, 10) == 1.29


def test_delta_ratio_bad_bicarbonate():
    with pytest.raises(ValueError):
        delta_ratio(140, 104, 24)


def test_corrected_sodium_hyperglycaemia():
    # Na 130, glucose 600 → 130 + 1.6 × 5 = 138
    assert corrected_sodium(130, 600) == 138.0


def test_corrected_sodium_bad_input():
    with pytest.raises(ValueError):
        corrected_sodium(130, 0)


def test_free_water_deficit_hypernatraemia():
    # Na 160, 70 kg male → 0.6 × 70 × (160/140 − 1) = 6.0 L
    assert free_water_deficit(160, 70, "male") == 6.0


def test_free_water_deficit_bad_sex():
    with pytest.raises(ValueError):
        free_water_deficit(160, 70, "x")


def test_corrected_calcium_low_albumin():
    # Ca 7.6, albumin 2.0 → 7.6 + 0.8 × 2 = 9.2
    assert corrected_calcium(7.6, 2.0) == 9.2


def test_corrected_calcium_bad_input():
    with pytest.raises(ValueError):
        corrected_calcium(8.0, 0)


def test_aa_gradient_room_air():
    # FiO2 0.21, PaCO2 40, PaO2 90 → 0.21 × 713 − 50 − 90 = 9.7
    assert aa_gradient(90, 40, 0.21) == 9.7


def test_aa_gradient_bad_fio2():
    with pytest.raises(ValueError):
        aa_gradient(90, 40, 0)


def test_serum_osmolality_normal():
    # Na 140, glucose 90, BUN 14 → 280 + 5 + 5 = 290
    assert serum_osmolality(140, 90, 14) == 290.0


def test_serum_osmolality_bad_input():
    with pytest.raises(ValueError):
        serum_osmolality(140, 90, 0)
