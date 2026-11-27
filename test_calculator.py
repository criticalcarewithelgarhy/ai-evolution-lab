"""
Regression tests — clinical correctness is the selection pressure.
Known inputs must always produce known outputs.
A generation that breaks any test is rejected entirely.
"""

import pytest
from calculator import (
    has_bled,
    meld_na,
    child_pugh,
    fena,
    feurea,
    urine_anion_gap,
    mean_arterial_pressure,
    pf_ratio,
    anion_gap,
    creatinine_clearance,
    glasgow_coma_scale,
    curb65,
    ideal_body_weight,
    oxygenation_index,
    corrected_sodium,
    corrected_calcium,
    serum_osmolality,
    qsofa,
    shock_index,
    aa_gradient,
    winters_formula,
    delta_ratio,
    free_water_deficit,
    rsbi,
    driving_pressure,
    rox_index,
    qtc_bazett,
    osmolal_gap,
    body_surface_area,
    parkland_formula,
    albumin_corrected_anion_gap,
    egfr_ckd_epi_2021,
    wells_pe,
    cha2ds2_vasc,
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


def test_winters_typical():
    # HCO3 12 → 1.5×12 + 8 = 26.0
    assert winters_formula(12) == 26.0


def test_winters_severe():
    # HCO3 5 → 7.5 + 8 = 15.5
    assert winters_formula(5) == 15.5


def test_winters_negative():
    with pytest.raises(ValueError):
        winters_formula(-1)


def test_delta_ratio_pure_hagma():
    # Na 140, Cl 100, HCO3 12 → AG 28; (28−12)/(24−12) = 1.33
    assert delta_ratio(140, 100, 12) == 1.33


def test_delta_ratio_mixed_nagma():
    # Na 140, Cl 110, HCO3 12 → AG 18; 6/12 = 0.5
    assert delta_ratio(140, 110, 12) == 0.5


def test_delta_ratio_metabolic_alkalosis():
    # Na 140, Cl 90, HCO3 18 → AG 32; 20/6 = 3.33
    assert delta_ratio(140, 90, 18) == 3.33


def test_delta_ratio_bad_hco3():
    with pytest.raises(ValueError):
        delta_ratio(140, 100, 24)


def test_fwd_male():
    # 70 kg male, Na 160: 42 × (160/140 − 1) = 6.0
    assert free_water_deficit(160, 70, "male") == 6.0


def test_fwd_elderly_female():
    # 60 kg female ≥65, Na 154: 27 × 0.1 = 2.7
    assert free_water_deficit(154, 60, "female", age=80) == 2.7


def test_fwd_normal_sodium():
    assert free_water_deficit(140, 70, "male") == 0.0


def test_fwd_bad_weight():
    with pytest.raises(ValueError):
        free_water_deficit(150, 0, "male")


def test_ibw_male():
    # 175 cm male: 50 + 0.91 × 22.6 = 70.566 → 70.6
    assert ideal_body_weight(175, "male") == 70.6


def test_ibw_female():
    # 160 cm female: 45.5 + 0.91 × 7.6 = 52.416 → 52.4
    assert ideal_body_weight(160, "female") == 52.4


def test_ibw_bad_height():
    with pytest.raises(ValueError):
        ideal_body_weight(0, "male")


def test_rsbi_typical():
    # RR 25, VT 500 mL: 25 / 0.5 = 50.0
    assert rsbi(25, 500) == 50.0


def test_rsbi_failure_range():
    # RR 35, VT 250 mL: 35 / 0.25 = 140.0
    assert rsbi(35, 250) == 140.0


def test_rsbi_bad_volume():
    with pytest.raises(ValueError):
        rsbi(20, 0)


def test_oi_typical():
    # FiO2 0.6, MAP 15, PaO2 90: 0.6 × 15 × 100 / 90 = 10.0
    assert oxygenation_index(0.6, 15, 90) == 10.0


def test_oi_severe():
    # FiO2 1.0, MAP 25, PaO2 60: 2500 / 60 = 41.67 → 41.7
    assert oxygenation_index(1.0, 25, 60) == 41.7


def test_oi_bad_pao2():
    with pytest.raises(ValueError):
        oxygenation_index(0.5, 15, 0)


def test_dp_typical():
    # Pplat 25, PEEP 10 → 15.0
    assert driving_pressure(25, 10) == 15.0


def test_dp_protective():
    # Pplat 22.5, PEEP 8 → 14.5
    assert driving_pressure(22.5, 8) == 14.5


def test_dp_bad_inputs():
    with pytest.raises(ValueError):
        driving_pressure(5, 10)


def test_rox_typical():
    # SpO2 95, FiO2 0.5, RR 20: 190 / 20 = 9.5
    assert rox_index(95, 0.5, 20) == 9.5


def test_rox_high_risk():
    # SpO2 88, FiO2 0.8, RR 32: 110 / 32 = 3.4375 → 3.44
    assert rox_index(88, 0.8, 32) == 3.44


def test_rox_bad_rr():
    with pytest.raises(ValueError):
        rox_index(95, 0.5, 0)


def test_qtc_hr60():
    # HR 60 → RR 1 s: QTc = QT = 400.0
    assert qtc_bazett(400, 60) == 400.0


def test_qtc_tachycardia():
    # QT 360, HR 100 → RR 0.6 s: 360 / sqrt(0.6) = 464.76 → 464.8
    assert qtc_bazett(360, 100) == 464.8


def test_qtc_bad_hr():
    with pytest.raises(ValueError):
        qtc_bazett(400, 0)



def test_osm_gap_normal():
    # measured 295, calc 290 (Na 140, glu 90, BUN 14) → 5.0
    assert osmolal_gap(295, 140, 90, 14) == 5.0


def test_osm_gap_toxic_alcohol():
    # measured 330, calc 290 → 40.0
    assert osmolal_gap(330, 140, 90, 14) == 40.0


def test_osm_gap_bad_measured():
    with pytest.raises(ValueError):
        osmolal_gap(0, 140, 90, 14)


def test_corrected_ag_normal_albumin():
    assert albumin_corrected_anion_gap(140, 104, 24, 4.0) == 12.0


def test_corrected_ag_hypoalbuminaemia():
    assert albumin_corrected_anion_gap(140, 104, 24, 2.0) == 17.0


def test_corrected_ag_negative_albumin():
    with pytest.raises(ValueError):
        albumin_corrected_anion_gap(140, 104, 24, -1)


def test_parkland_typical():
    # 70 kg, 30 % TBSA: 4 × 70 × 30 = 8400 mL
    assert parkland_formula(70, 30) == 8400.0


def test_parkland_zero_tbsa():
    assert parkland_formula(70, 0) == 0.0


def test_parkland_bad_tbsa():
    with pytest.raises(ValueError):
        parkland_formula(70, 120)


def test_bsa_typical():
    # 180 cm, 80 kg: sqrt(14400 / 3600) = 2.0
    assert body_surface_area(180, 80) == 2.0


def test_bsa_small_adult():
    # 160 cm, 60 kg: sqrt(9600 / 3600) = 1.633 → 1.63
    assert body_surface_area(160, 60) == 1.63


def test_bsa_bad_weight():
    with pytest.raises(ValueError):
        body_surface_area(170, 0)


def test_egfr_male_typical():
    # 50 y male, Scr 1.0: 142 × (1.0/0.9)^-1.2 × 0.9938^50 = 91.7
    assert egfr_ckd_epi_2021(1.0, 50, "M") == 91.7


def test_egfr_female_low_creatinine():
    # 40 y female, Scr 0.6: 142 × (0.6/0.7)^-0.241 × 0.9938^40 × 1.012 = 116.3
    assert egfr_ckd_epi_2021(0.6, 40, "F") == 116.3


def test_egfr_bad_creatinine():
    with pytest.raises(ValueError):
        egfr_ckd_epi_2021(0, 50, "M")


def test_wells_pe_zero():
    assert wells_pe(0, 0, 80, 0, 0, 0, 0) == 0.0


def test_wells_pe_likely():
    # DVT signs 3 + PE most likely 3 + HR 110 1.5 = 7.5
    assert wells_pe(1, 1, 110, 0, 0, 0, 0) == 7.5


def test_wells_pe_max():
    assert wells_pe(1, 1, 120, 1, 1, 1, 1) == 12.5


def test_wells_pe_bad_hr():
    with pytest.raises(ValueError):
        wells_pe(0, 0, -1, 0, 0, 0, 0)


def test_cha2ds2_vasc_zero():
    assert cha2ds2_vasc(0, 0, 50, 0, 0, 0, "M") == 0


def test_cha2ds2_vasc_age_bands():
    # age 65–74 scores 1, age ≥ 75 scores 2
    assert cha2ds2_vasc(0, 0, 70, 0, 0, 0, "M") == 1
    assert cha2ds2_vasc(0, 0, 75, 0, 0, 0, "M") == 2


def test_cha2ds2_vasc_max():
    # CHF 1 + HTN 1 + age ≥75 2 + DM 1 + stroke 2 + vascular 1 + female 1 = 9
    assert cha2ds2_vasc(1, 1, 80, 1, 1, 1, "F") == 9


def test_cha2ds2_vasc_bad_age():
    with pytest.raises(ValueError):
        cha2ds2_vasc(0, 0, -1, 0, 0, 0, "M")


def test_has_bled_zero():
    assert has_bled(0, 0, 0, 0, 0, 0, 50, 0, 0) == 0


def test_has_bled_age_threshold():
    # elderly point requires age > 65 (65 itself scores 0)
    assert has_bled(0, 0, 0, 0, 0, 0, 65, 0, 0) == 0
    assert has_bled(0, 0, 0, 0, 0, 0, 66, 0, 0) == 1


def test_has_bled_max():
    assert has_bled(1, 1, 1, 1, 1, 1, 80, 1, 1) == 9


def test_has_bled_bad_age():
    with pytest.raises(ValueError):
        has_bled(0, 0, 0, 0, 0, 0, -1, 0, 0)


def test_meld_na_floor():
    # all values at lower bounds: 6.43 -> 6; MELD <= 11 so no sodium adjustment
    assert meld_na(0.5, 0.5, 0.9, 140) == 6


def test_meld_na_sodium_adjusted():
    # MELD = 25; Na 130 -> 25 + 1.32*7 - 0.033*25*7 = 28.465 -> 28
    assert meld_na(2, 3, 2, 130) == 28


def test_meld_na_dialysis_and_cap():
    # dialysis forces Cr to 4.0; very high bilirubin/INR capped at 40
    assert meld_na(1.0, 1, 1, 137, dialysis=1) == meld_na(4.0, 1, 1, 137)
    assert meld_na(10, 40, 8, 120) == 40


def test_meld_na_bad_input():
    with pytest.raises(ValueError):
        meld_na(0, 1, 1, 137)


def test_child_pugh_class_a_minimum():
    assert child_pugh(1.0, 4.0, 1.1, 1, 1) == 5


def test_child_pugh_boundaries():
    # bilirubin 2 and 3 -> 2 points; albumin 3.5 and 2.8 -> 2; INR 1.7 and 2.3 -> 2
    assert child_pugh(2.0, 3.5, 1.7, 1, 1) == 8
    assert child_pugh(3.0, 2.8, 2.3, 1, 1) == 8


def test_child_pugh_class_c_maximum():
    assert child_pugh(5.0, 2.0, 3.0, 3, 3) == 15


def test_child_pugh_bad_grade():
    with pytest.raises(ValueError):
        child_pugh(1.0, 4.0, 1.1, 0, 1)


def test_fena_prerenal():
    # (10 × 2) / (140 × 100) × 100 = 0.14 %
    assert fena(10, 140, 100, 2) == 0.14


def test_fena_intrinsic():
    # (60 × 3) / (135 × 40) × 100 = 3.33 %
    assert fena(60, 135, 40, 3) == 3.33


def test_fena_bad_input():
    with pytest.raises(ValueError):
        fena(20, 140, 0, 1)


def test_feurea_prerenal():
    # (200 × 2) / (40 × 100) × 100 = 10.0
    assert feurea(200, 40, 100, 2) == 10.0


def test_feurea_intrinsic():
    # (300 × 3) / (30 × 50) × 100 = 60.0
    assert feurea(300, 30, 50, 3) == 60.0


def test_feurea_bad_input():
    with pytest.raises(ValueError):
        feurea(200, 0, 100, 2)


def test_urine_anion_gap_negative():
    # 40 + 20 − 100 = −40 (GI bicarbonate loss)
    assert urine_anion_gap(40, 20, 100) == -40.0


def test_urine_anion_gap_positive():
    # 60 + 30 − 70 = 20 (renal tubular acidosis)
    assert urine_anion_gap(60, 30, 70) == 20.0


def test_urine_anion_gap_bad_input():
    with pytest.raises(ValueError):
        urine_anion_gap(40, -1, 100)
