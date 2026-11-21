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
    albumin_corrected_anion_gap,
    osmolar_gap,
    corrected_calcium,
    winters_formula,
    delta_ratio,
    aa_gradient,
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


def test_albumin_corrected_ag_normal_albumin():
    # albumin = 4.0 (normal) → correction = 0, same as standard AG
    assert albumin_corrected_anion_gap(140, 104, 24, 4.0) == 12.0


def test_albumin_corrected_ag_low_albumin():
    # albumin = 2.0 → correction = 2.5 × (4-2) = 5.0, corrected AG = 17.0
    assert albumin_corrected_anion_gap(140, 104, 24, 2.0) == 17.0


def test_albumin_corrected_ag_bad_albumin():
    with pytest.raises(ValueError):
        albumin_corrected_anion_gap(140, 104, 24, -1)


def test_osmolar_gap_normal():
    # Na=140, glucose=90, BUN=14 → calc=280+5+5=290; measured=295 → OG=5.0
    assert osmolar_gap(295, 140, 90, 14) == 5.0


def test_osmolar_gap_elevated():
    # Same electrolytes, measured=330 → OG=40.0 (toxic alcohol pattern)
    assert osmolar_gap(330, 140, 90, 14) == 40.0


def test_osmolar_gap_negative_glucose():
    with pytest.raises(ValueError):
        osmolar_gap(295, 140, -1, 14)


def test_osmolar_gap_negative_bun():
    with pytest.raises(ValueError):
        osmolar_gap(295, 140, 90, -1)


def test_corrected_calcium_normal_albumin():
    # albumin = 4.0 (normal) → no correction, Ca stays same
    assert corrected_calcium(8.5, 4.0) == 8.5


def test_corrected_calcium_low_albumin():
    # albumin = 2.0 → correction = 0.8 × (4-2) = 1.6, corrected Ca = 10.1
    assert corrected_calcium(8.5, 2.0) == 10.1


def test_corrected_calcium_bad_albumin():
    with pytest.raises(ValueError):
        corrected_calcium(8.5, -1)


def test_corrected_calcium_bad_calcium():
    with pytest.raises(ValueError):
        corrected_calcium(-1, 4.0)


def test_winters_formula_typical():
    # HCO3 12 → 1.5×12+8 = 26 → range 24–28
    assert winters_formula(12) == (24.0, 28.0)


def test_winters_formula_bad_bicarbonate():
    with pytest.raises(ValueError):
        winters_formula(0)


def test_delta_ratio_pure_hagma():
    # Na 138, Cl 98, HCO3 10 → AG 30; (30-12)/(24-10) = 18/14 = 1.29
    assert delta_ratio(138, 98, 10) == 1.29


def test_delta_ratio_mixed():
    # Na 140, Cl 110, HCO3 12 → AG 18; (18-12)/(24-12) = 0.5
    assert delta_ratio(140, 110, 12) == 0.5


def test_delta_ratio_bad_bicarbonate():
    with pytest.raises(ValueError):
        delta_ratio(140, 104, 24)


def test_aa_gradient_room_air():
    # FiO2 0.21, PaCO2 40, PaO2 90 → PAO2 = 0.21×713 − 50 = 99.73 → 9.7
    assert aa_gradient(90, 40, 0.21) == 9.7


def test_aa_gradient_elevated():
    # FiO2 0.5, PaCO2 40, PaO2 80 → PAO2 = 356.5 − 50 = 306.5 → 226.5
    assert aa_gradient(80, 40, 0.5) == 226.5


def test_aa_gradient_bad_fio2():
    with pytest.raises(ValueError):
        aa_gradient(90, 40, 1.5)


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
