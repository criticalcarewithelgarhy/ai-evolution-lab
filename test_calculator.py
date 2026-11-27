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
    corrected_sodium,
    free_water_deficit,
    ideal_body_weight,
    shock_index,
    rox_index,
    sf_ratio,
    driving_pressure,
    static_compliance,
    oxygenation_index,
    mechanical_power,
    fractional_excretion_sodium,
    fractional_excretion_urea,
    qtc_bazett,
    rapid_shallow_breathing_index,
    qtc_fridericia,
    ventilatory_ratio,
    dead_space_fraction,
    arterial_oxygen_content,
    oxygen_delivery,
    oxygen_extraction_ratio,
    oxygen_consumption,
    cardiac_index,
    systemic_vascular_resistance,
    pulmonary_vascular_resistance,
    cardiac_power_output,
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


def test_corrected_sodium_normal_glucose():
    # glucose 100 → no correction
    assert corrected_sodium(140, 100) == 140.0


def test_corrected_sodium_hyperglycaemia():
    # Na 130, glucose 600 → 130 + 1.6×5 = 138.0
    assert corrected_sodium(130, 600) == 138.0


def test_corrected_sodium_bad_glucose():
    with pytest.raises(ValueError):
        corrected_sodium(140, -1)


def test_free_water_deficit_male():
    # 70kg male, Na 160 → 42 × (160/140 − 1) = 6.0 L
    assert free_water_deficit(160, 70, "male") == 6.0


def test_free_water_deficit_female():
    # 70kg female, Na 154 → 35 × 0.1 = 3.5 L
    assert free_water_deficit(154, 70, "female") == 3.5


def test_free_water_deficit_bad_weight():
    with pytest.raises(ValueError):
        free_water_deficit(160, 0, "male")


def test_ibw_male():
    # 152.4 cm = 60 in → 50.0 kg; 177.8 cm = 70 in → 50 + 23 = 73.0
    assert ideal_body_weight(177.8, "male") == 73.0


def test_ibw_female():
    # 165.1 cm = 65 in → 45.5 + 11.5 = 57.0
    assert ideal_body_weight(165.1, "female") == 57.0


def test_ibw_bad_height():
    with pytest.raises(ValueError):
        ideal_body_weight(0, "male")


def test_shock_index_normal():
    # HR 72, SBP 120 → 0.6
    assert shock_index(72, 120) == 0.6


def test_shock_index_shock():
    # HR 130, SBP 90 → 1.44
    assert shock_index(130, 90) == 1.44


def test_shock_index_bad_sbp():
    with pytest.raises(ValueError):
        shock_index(80, 0)


def test_rox_index_success():
    # SpO2 95, FiO2 0.4, RR 20 → 237.5 / 20 = 11.88
    assert rox_index(95, 0.4, 20) == 11.88


def test_rox_index_high_risk():
    # SpO2 88, FiO2 0.8, RR 32 → 110 / 32 = 3.44
    assert rox_index(88, 0.8, 32) == 3.44


def test_rox_index_bad_fio2():
    with pytest.raises(ValueError):
        rox_index(95, 0, 20)


def test_rox_index_bad_rr():
    with pytest.raises(ValueError):
        rox_index(95, 0.4, 0)


def test_driving_pressure_protective():
    # Pplat 25, PEEP 12 → 13
    assert driving_pressure(25, 12) == 13.0


def test_driving_pressure_high():
    # Pplat 30, PEEP 8 → 22
    assert driving_pressure(30, 8) == 22.0


def test_driving_pressure_bad_plateau():
    with pytest.raises(ValueError):
        driving_pressure(5, 10)


def test_static_compliance_normal():
    # Vt 500, Pplat 20, PEEP 10 → 50.0
    assert static_compliance(500, 20, 10) == 50.0


def test_static_compliance_ards():
    # Vt 420, Pplat 30, PEEP 12 → 23.3
    assert static_compliance(420, 30, 12) == 23.3


def test_static_compliance_bad_plateau():
    with pytest.raises(ValueError):
        static_compliance(500, 10, 10)


def test_oxygenation_index_mild():
    # FiO2 0.4, MAWP 10, PaO2 100 → 4.0
    assert oxygenation_index(0.4, 10, 100) == 4.0


def test_oxygenation_index_severe():
    # FiO2 1.0, MAWP 20, PaO2 60 → 33.3
    assert oxygenation_index(1.0, 20, 60) == 33.3


def test_oxygenation_index_bad_pao2():
    with pytest.raises(ValueError):
        oxygenation_index(0.5, 15, 0)


def test_mechanical_power_typical():
    # 0.098 × 20 × 0.45 × (28 − 6) = 19.404 → 19.4
    assert mechanical_power(20, 450, 28, 22, 10) == 19.4


def test_mechanical_power_low():
    # 0.098 × 14 × 0.4 × (20 − 4) = 8.7808 → 8.8
    assert mechanical_power(14, 400, 20, 16, 8) == 8.8


def test_mechanical_power_bad_peak():
    with pytest.raises(ValueError):
        mechanical_power(20, 450, 20, 25, 10)


def test_sf_ratio_typical():
    # SpO2 92 / FiO2 0.4 → 230.0
    assert sf_ratio(92, 0.4) == 230.0


def test_sf_ratio_room_air():
    # SpO2 96 / FiO2 0.21 → 457.142… → 457.1
    assert sf_ratio(96, 0.21) == 457.1


def test_sf_ratio_bad_fio2():
    with pytest.raises(ValueError):
        sf_ratio(95, 0)


def test_fena_prerenal():
    # UNa 10, PNa 140, UCr 100, PCr 2.0 → 20 / 14000 × 100 = 0.14
    assert fractional_excretion_sodium(10, 140, 100, 2.0) == 0.14


def test_fena_atn():
    # UNa 60, PNa 135, UCr 40, PCr 3.0 → 180 / 5400 × 100 = 3.33
    assert fractional_excretion_sodium(60, 135, 40, 3.0) == 3.33


def test_fena_bad_creatinine():
    with pytest.raises(ValueError):
        fractional_excretion_sodium(20, 140, 0, 1.0)


def test_feurea_prerenal():
    # UUrea 300, PUrea 40, UCr 100, PCr 2.0 → 600 / 4000 × 100 = 15.0
    assert fractional_excretion_urea(300, 40, 100, 2.0) == 15.0


def test_feurea_atn():
    # UUrea 200, PUrea 60, UCr 30, PCr 3.0 → 600 / 1800 × 100 = 33.3
    assert fractional_excretion_urea(200, 60, 30, 3.0) == 33.3


def test_feurea_bad_plasma_urea():
    with pytest.raises(ValueError):
        fractional_excretion_urea(300, 0, 100, 2.0)


def test_qtc_bazett_hr60():
    # HR 60 → RR 1 s → QTc = QT
    assert qtc_bazett(400, 60) == 400.0


def test_qtc_bazett_tachycardia():
    # QT 360, HR 100 → RR 0.6 s → 360 / 0.7746 = 464.8
    assert qtc_bazett(360, 100) == 464.8


def test_qtc_bazett_bad_hr():
    with pytest.raises(ValueError):
        qtc_bazett(400, 0)


def test_qtc_fridericia_hr60():
    # HR 60 → RR 1 s → QTcF = QT
    assert qtc_fridericia(400, 60) == 400.0


def test_qtc_fridericia_tachycardia():
    # QT 360, HR 100 → RR 0.6 s → 360 / 0.8434 = 426.8
    assert qtc_fridericia(360, 100) == 426.8


def test_qtc_fridericia_bad_qt():
    with pytest.raises(ValueError):
        qtc_fridericia(0, 80)


def test_rsbi_weanable():
    # RR 20, Vt 400 mL → 20 / 0.4 = 50
    assert rapid_shallow_breathing_index(20, 400) == 50.0


def test_rsbi_rapid_shallow():
    # RR 35, Vt 250 mL → 35 / 0.25 = 140
    assert rapid_shallow_breathing_index(35, 250) == 140.0


def test_rsbi_bad_vt():
    with pytest.raises(ValueError):
        rapid_shallow_breathing_index(20, 0)


def test_ventilatory_ratio_normal():
    # VE 7500 mL/min, PaCO2 37.5, PBW 75 → 281250 / 281250 = 1.0
    assert ventilatory_ratio(7500, 37.5, 75) == 1.0


def test_ventilatory_ratio_high_dead_space():
    # VE 12000 mL/min, PaCO2 55, PBW 70 → 660000 / 262500 = 2.51
    assert ventilatory_ratio(12000, 55, 70) == 2.51


def test_ventilatory_ratio_bad_pbw():
    with pytest.raises(ValueError):
        ventilatory_ratio(7500, 40, 0)


def test_dead_space_normal():
    # PaCO2 40, PECO2 30 → 10 / 40 = 0.25
    assert dead_space_fraction(40, 30) == 0.25


def test_dead_space_ards():
    # PaCO2 50, PECO2 15 → 35 / 50 = 0.7
    assert dead_space_fraction(50, 15) == 0.7


def test_dead_space_bad_peco2():
    with pytest.raises(ValueError):
        dead_space_fraction(40, 45)


def test_cao2_normal():
    # Hb 15, SaO2 98, PaO2 100 → 1.34×15×0.98 + 0.3 = 19.698 + 0.3 = 20.0
    assert arterial_oxygen_content(15, 98, 100) == 20.0


def test_cao2_anaemia():
    # Hb 7, SaO2 90, PaO2 60 → 8.442 + 0.18 = 8.622 → 8.6
    assert arterial_oxygen_content(7, 90, 60) == 8.6


def test_cao2_bad_sao2():
    with pytest.raises(ValueError):
        arterial_oxygen_content(15, 101, 100)


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


def test_oxygen_delivery_normal():
    # CO 5 L/min, CaO2 20 mL/dL → 5 × 20 × 10 = 1000
    assert oxygen_delivery(5, 20) == 1000.0


def test_oxygen_delivery_low():
    # CO 3.2 L/min, CaO2 11.5 mL/dL → 368.0
    assert oxygen_delivery(3.2, 11.5) == 368.0


def test_oxygen_delivery_bad_co():
    with pytest.raises(ValueError):
        oxygen_delivery(-1, 20)


def test_o2er_normal():
    # SaO2 98, SvO2 73 → 25 / 98 × 100 = 25.5
    assert oxygen_extraction_ratio(98, 73) == 25.5


def test_o2er_high():
    # SaO2 95, SvO2 50 → 45 / 95 × 100 = 47.4
    assert oxygen_extraction_ratio(95, 50) == 47.4


def test_o2er_bad_svo2():
    with pytest.raises(ValueError):
        oxygen_extraction_ratio(90, 95)


def test_vo2_normal():
    # CO 5, CaO2 20, CvO2 15 → 5 × 5 × 10 = 250
    assert oxygen_consumption(5, 20, 15) == 250.0


def test_vo2_low_output():
    # CO 3.5, CaO2 18.2, CvO2 11.4 → 3.5 × 6.8 × 10 = 238.0
    assert oxygen_consumption(3.5, 18.2, 11.4) == 238.0


def test_vo2_bad_cvo2():
    with pytest.raises(ValueError):
        oxygen_consumption(5, 15, 20)


def test_cardiac_index_normal():
    # CO 5, 180 cm, 80 kg → BSA √(14400/3600) = 2.0 → 2.5
    assert cardiac_index(5, 180, 80) == 2.5


def test_cardiac_index_low():
    # CO 3, 160 cm, 60 kg → BSA 1.633 → 1.84
    assert cardiac_index(3, 160, 60) == 1.84


def test_cardiac_index_bad_height():
    with pytest.raises(ValueError):
        cardiac_index(5, 0, 80)


def test_svr_normal():
    # MAP 90, CVP 10, CO 5 → 80 × 80 / 5 = 1280
    assert systemic_vascular_resistance(90, 10, 5) == 1280


def test_svr_septic():
    # MAP 60, CVP 8, CO 8 → 80 × 52 / 8 = 520
    assert systemic_vascular_resistance(60, 8, 8) == 520


def test_svr_bad_co():
    with pytest.raises(ValueError):
        systemic_vascular_resistance(90, 10, 0)


def test_pvr_normal():
    # mPAP 18, PAWP 10, CO 5 → 8 / 5 = 1.6 WU
    assert pulmonary_vascular_resistance(18, 10, 5) == 1.6


def test_pvr_pulmonary_hypertension():
    # mPAP 40, PAWP 12, CO 4 → 28 / 4 = 7.0 WU
    assert pulmonary_vascular_resistance(40, 12, 4) == 7.0


def test_pvr_bad_pawp():
    with pytest.raises(ValueError):
        pulmonary_vascular_resistance(10, 15, 5)


def test_cpo_normal():
    # MAP 90, CO 5 → 450 / 451 = 0.998 → 1.0
    assert cardiac_power_output(90, 5) == 1.0


def test_cpo_cardiogenic_shock():
    # MAP 60, CO 3 → 180 / 451 = 0.399 → 0.4
    assert cardiac_power_output(60, 3) == 0.4


def test_cpo_bad_co():
    with pytest.raises(ValueError):
        cardiac_power_output(80, -1)
