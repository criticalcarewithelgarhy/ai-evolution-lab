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
    corrected_sodium,
    creatinine_clearance,
    winters_formula,
    delta_ratio,
    aa_gradient,
    serum_osmolality,
    corrected_calcium,
    predicted_body_weight,
    shock_index,
    free_water_deficit,
    rox_index,
    qsofa_score,
    driving_pressure,
    oxygenation_index,
    sf_ratio,
    static_compliance,
    rsbi,
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


def test_corrected_ag_normal_albumin():
    # Albumin 4.0 → no correction: 140 - (104 + 24) = 12
    assert corrected_anion_gap(140, 104, 24, 4.0) == 12.0


def test_corrected_ag_hypoalbuminaemia():
    # Albumin 2.0: 12 + 2.5 * (4.0 - 2.0) = 17
    assert corrected_anion_gap(140, 104, 24, 2.0) == 17.0


def test_corrected_ag_bad_albumin():
    with pytest.raises(ValueError):
        corrected_anion_gap(140, 104, 24, -1)


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


def test_winters_dka():
    # HCO3 10: 1.5 * 10 + 8 = 23
    assert winters_formula(10) == 23.0


def test_winters_fractional():
    # HCO3 15.5: 1.5 * 15.5 + 8 = 31.25 → 31.2
    assert winters_formula(15.5) == 31.2


def test_winters_bad_bicarbonate():
    with pytest.raises(ValueError):
        winters_formula(-1)


def test_delta_ratio_pure_hagma():
    # Na 138, Cl 98, HCO3 10 → AG 30; (30-12)/(24-10) = 1.29
    assert delta_ratio(138, 98, 10) == 1.29


def test_delta_ratio_mixed_nagma():
    # Na 140, Cl 110, HCO3 12 → AG 18; (18-12)/(24-12) = 0.5
    assert delta_ratio(140, 110, 12) == 0.5


def test_delta_ratio_bad_bicarbonate():
    with pytest.raises(ValueError):
        delta_ratio(140, 104, 24)


def test_aa_gradient_room_air():
    # FiO2 0.21, PaCO2 40, PaO2 90: 0.21*713 - 50 = 99.73 → 9.7
    assert aa_gradient(90, 40, 0.21) == 9.7


def test_aa_gradient_high_fio2():
    # FiO2 1.0, PaCO2 40, PaO2 100: 713 - 50 - 100 = 563
    assert aa_gradient(100, 40, 1.0) == 563.0


def test_aa_gradient_bad_fio2():
    with pytest.raises(ValueError):
        aa_gradient(90, 40, 1.5)


def test_osmolality_normal():
    # 2*140 + 90/18 + 14/2.8 = 280 + 5 + 5 = 290
    assert serum_osmolality(140, 90, 14) == 290.0


def test_osmolality_hyperglycaemia():
    # 2*130 + 600/18 + 28/2.8 = 260 + 33.33 + 10 = 303.3
    assert serum_osmolality(130, 600, 28) == 303.3


def test_osmolality_bad_bun():
    with pytest.raises(ValueError):
        serum_osmolality(140, 90, -1)


def test_corrected_calcium_normal_albumin():
    # Albumin 4.0 → no correction
    assert corrected_calcium(9.0, 4.0) == 9.0


def test_corrected_calcium_hypoalbuminaemia():
    # Ca 7.6, albumin 2.0: 7.6 + 0.8 * 2.0 = 9.2
    assert corrected_calcium(7.6, 2.0) == 9.2


def test_corrected_calcium_bad_albumin():
    with pytest.raises(ValueError):
        corrected_calcium(9.0, -1)


def test_pbw_male():
    # 175 cm male: 50 + 0.91 * 22.6 = 70.566 → 70.6
    assert predicted_body_weight(175, "male") == 70.6


def test_pbw_female():
    # 160 cm female: 45.5 + 0.91 * 7.6 = 52.416 → 52.4
    assert predicted_body_weight(160, "female") == 52.4


def test_pbw_bad_height():
    with pytest.raises(ValueError):
        predicted_body_weight(0, "male")


def test_shock_index_normal():
    # HR 70, SBP 120 → 0.58
    assert shock_index(70, 120) == 0.58


def test_shock_index_shock():
    # HR 120, SBP 90 → 1.33
    assert shock_index(120, 90) == 1.33


def test_shock_index_bad_sbp():
    with pytest.raises(ValueError):
        shock_index(80, 0)


def test_fwd_male():
    # 70 kg male, Na 160: 42 * (160/140 - 1) = 6.0
    assert free_water_deficit(160, 70, "male") == 6.0


def test_fwd_female():
    # 60 kg female, Na 154: 30 * 0.1 = 3.0
    assert free_water_deficit(154, 60, "female") == 3.0


def test_fwd_bad_weight():
    with pytest.raises(ValueError):
        free_water_deficit(150, 0, "male")


def test_disclaimer_present():
    assert "NOT FOR CLINICAL USE" in DISCLAIMER


def test_rox_typical():
    # SpO2 95, FiO2 0.5, RR 20 → 190 / 20 = 9.5
    assert rox_index(95, 0.5, 20) == 9.5


def test_rox_failure_range():
    # SpO2 88, FiO2 0.8, RR 30 → 110 / 30 = 3.67
    assert rox_index(88, 0.8, 30) == 3.67


def test_rox_bad_inputs():
    with pytest.raises(ValueError):
        rox_index(95, 0, 20)
    with pytest.raises(ValueError):
        rox_index(95, 0.5, 0)



def test_qsofa_zero():
    assert qsofa_score(16, 120, False) == 0


def test_qsofa_full():
    # RR 22, SBP 100, altered → 3 (thresholds inclusive)
    assert qsofa_score(22, 100, True) == 3


def test_qsofa_bad_inputs():
    with pytest.raises(ValueError):
        qsofa_score(-1, 120, False)


def test_dp_typical():
    # Pplat 25, PEEP 10 → 15
    assert driving_pressure(25, 10) == 15.0


def test_dp_high():
    assert driving_pressure(32.5, 8) == 24.5


def test_dp_bad_inputs():
    with pytest.raises(ValueError):
        driving_pressure(8, 10)
    with pytest.raises(ValueError):
        driving_pressure(20, -1)



def test_oi_typical():
    # FiO2 0.6, mPaw 15, PaO2 75 → 900 / 75 = 12
    assert oxygenation_index(0.6, 15, 75) == 12.0


def test_oi_severe():
    # FiO2 1.0, mPaw 25, PaO2 55 → 2500 / 55 = 45.45 → 45.5
    assert oxygenation_index(1.0, 25, 55) == 45.5


def test_oi_bad_inputs():
    with pytest.raises(ValueError):
        oxygenation_index(0, 15, 75)
    with pytest.raises(ValueError):
        oxygenation_index(0.6, 15, 0)


def test_sf_typical():
    # SpO2 92 %, FiO2 0.4 → 230
    assert sf_ratio(92, 0.4) == 230.0


def test_sf_room_air():
    assert sf_ratio(97, 0.21) == 461.9


def test_sf_bad_inputs():
    with pytest.raises(ValueError):
        sf_ratio(92, 0)
    with pytest.raises(ValueError):
        sf_ratio(120, 0.5)


def test_cstat_typical():
    # VT 450 mL, Pplat 25, PEEP 10 → 30
    assert static_compliance(450, 25, 10) == 30.0


def test_cstat_normal():
    # VT 500, Pplat 15, PEEP 5 → 50
    assert static_compliance(500, 15, 5) == 50.0


def test_cstat_bad_inputs():
    with pytest.raises(ValueError):
        static_compliance(450, 10, 10)
    with pytest.raises(ValueError):
        static_compliance(0, 25, 10)


def test_rsbi_typical():
    # RR 20, VT 400 mL → 20 / 0.4 = 50
    assert rsbi(20, 400) == 50.0


def test_rsbi_failure_range():
    # RR 35, VT 250 mL → 35 / 0.25 = 140
    assert rsbi(35, 250) == 140.0


def test_rsbi_bad_inputs():
    with pytest.raises(ValueError):
        rsbi(20, 0)
    with pytest.raises(ValueError):
        rsbi(-1, 400)
