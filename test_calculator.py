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
    corrected_sodium,
    corrected_calcium,
    serum_osmolality,
    qsofa,
    shock_index,
    aa_gradient,
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


def test_corrected_na_normal_glucose():
    # At glucose 100, no correction needed
    assert corrected_sodium(135, 100) == 135.0


def test_corrected_na_hyperglycemia():
    # glucose 300 → (300-100)/100 = 2.0 → 1.6 * 2.0 = 3.2 → 140 + 3.2 = 143.2
    assert corrected_sodium(140, 300) == 143.2


def test_corrected_na_severe():
    # glucose 600 → (600-100)/100 = 5.0 → 1.6 * 5.0 = 8.0 → 130 + 8.0 = 138.0
    assert corrected_sodium(130, 600) == 138.0


def test_corrected_na_negative_glucose():
    with pytest.raises(ValueError):
        corrected_sodium(135, -1)


def test_corrected_ca_normal_albumin():
    # Albumin 4.0 → no correction
    assert corrected_calcium(9.5, 4.0) == 9.5


def test_corrected_ca_hypoalbuminaemia():
    # Ca 7.6, albumin 2.0 → 7.6 + 0.8 × 2.0 = 9.2
    assert corrected_calcium(7.6, 2.0) == 9.2


def test_corrected_ca_high_albumin():
    # Ca 10.0, albumin 5.0 → 10.0 − 0.8 = 9.2
    assert corrected_calcium(10.0, 5.0) == 9.2


def test_corrected_ca_negative_albumin():
    with pytest.raises(ValueError):
        corrected_calcium(9.0, -1)


def test_osm_normal():
    # Na 140, glucose 90, BUN 14 → 280 + 5 + 5 = 290
    assert serum_osmolality(140, 90, 14) == 290.0


def test_osm_hyperglycaemia():
    # Na 130, glucose 900, BUN 28 → 260 + 50 + 10 = 320
    assert serum_osmolality(130, 900, 28) == 320.0


def test_osm_negative_input():
    with pytest.raises(ValueError):
        serum_osmolality(140, -5, 14)


def test_qsofa_zero():
    assert qsofa(16, 120, 0) == 0


def test_qsofa_max():
    assert qsofa(24, 90, 1) == 3


def test_qsofa_thresholds():
    # RR exactly 22 and SBP exactly 100 each score a point
    assert qsofa(22, 100, 0) == 2


def test_qsofa_negative_input():
    with pytest.raises(ValueError):
        qsofa(-1, 120, 0)


def test_shock_index_normal():
    # HR 70, SBP 120 → 0.583 → 0.58
    assert shock_index(70, 120) == 0.58


def test_shock_index_shock():
    # HR 120, SBP 80 → 1.5
    assert shock_index(120, 80) == 1.5


def test_shock_index_zero_sbp():
    with pytest.raises(ValueError):
        shock_index(80, 0)


def test_shock_index_negative_hr():
    with pytest.raises(ValueError):
        shock_index(-1, 120)


def test_aa_gradient_room_air():
    # FiO2 0.21: PAO2 = 0.21×713 − 40/0.8 = 149.73 − 50 = 99.73; minus PaO2 90 → 9.7
    assert aa_gradient(90, 40, 0.21) == 9.7


def test_aa_gradient_high_fio2():
    # FiO2 1.0: PAO2 = 713 − 50 = 663; minus PaO2 100 → 563.0
    assert aa_gradient(100, 40, 1.0) == 563.0


def test_aa_gradient_altitude():
    # Patm 630: PAO2 = 0.21×583 − 40/0.8 = 122.43 − 50 = 72.43; minus 60 → 12.4
    assert aa_gradient(60, 40, 0.21, patm=630) == 12.4


def test_aa_gradient_bad_fio2():
    with pytest.raises(ValueError):
        aa_gradient(90, 40, 0)
