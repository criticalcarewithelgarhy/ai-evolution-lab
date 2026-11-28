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


def test_map_sbp_upper_bound():
    # Extra-digit typo (1200 for 120) must not return a plausible-looking hypertensive MAP
    with pytest.raises(ValueError):
        mean_arterial_pressure(1200, 80)
    assert mean_arterial_pressure(400, 100) == 200.0


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


def test_pf_ratio_pao2_upper_bound():
    # Extra-digit typo (850 for 85) would mislabel severe hypoxaemia as normal oxygenation
    with pytest.raises(ValueError):
        pf_ratio(850, 1.0)
    assert pf_ratio(800, 1.0) == 800.0


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


def test_anion_gap_sodium_upper_bound():
    # Extra-digit typo (1400 for 140) would report a false AG of 1272 (or a normal-looking
    # AG when Cl/HCO3 are similarly mistyped) instead of flagging the entry error
    with pytest.raises(ValueError):
        anion_gap(1400, 104, 24)
    assert anion_gap(250, 104, 24) == 122.0


@pytest.mark.parametrize("cl,hco3", [(1040, 24), (104, 240)])
def test_anion_gap_chloride_bicarbonate_upper_bound(cl, hco3):
    # Extra-digit typo would return a large negative AG instead of flagging the entry error
    with pytest.raises(ValueError):
        anion_gap(140, cl, hco3)


def test_anion_gap_chloride_bicarbonate_at_bounds():
    assert anion_gap(250, 200, 0) == 50.0
    assert anion_gap(140, 30, 100) == 10.0


def test_anion_gap_zero_bicarbonate():
    # HCO3 of 0 is extreme but measurable; must still compute
    assert anion_gap(140, 100, 0) == 40.0


def test_corrected_anion_gap():
    # Normal measured AG 12 with albumin 2.0 g/dL → corrected 17 (masked high-AG acidosis)
    from calculator import corrected_anion_gap
    assert corrected_anion_gap(140, 104, 24, 2.0) == 17.0
    assert corrected_anion_gap(140, 104, 24, 4.0) == 12.0
    for bad in (0, -1, 11, float("nan")):
        with pytest.raises(ValueError):
            corrected_anion_gap(140, 104, 24, bad)
    with pytest.raises(ValueError):
        corrected_anion_gap(140, 104, -24, 2.0)


def test_corrected_anion_gap_in_app():
    from app import app
    c = app.test_client()
    html = c.post("/", data={"calc": "ag", "na": "140", "cl": "104", "hco3": "24",
                             "albumin": "2.0"}).get_data(as_text=True)
    assert "Albumin-corrected AG 17.0" in html and "12.0" in html
    html = c.post("/", data={"calc": "ag", "na": "140", "cl": "104", "hco3": "24",
                             "albumin": ""}).get_data(as_text=True)
    assert "Albumin-corrected" not in html


def test_crcl_male():
    # 50yo, 70kg, Cr 1.0 → 87.5  (Cockcroft-Gault: (90×70)/72)
    assert creatinine_clearance(50, 70, 1.0, "male") == 87.5


def test_crcl_female():
    # Same but female → 74.4  (87.5 × 0.85)
    assert creatinine_clearance(50, 70, 1.0, "female") == 74.4


def test_crcl_bad_creatinine():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 0, "male")


def test_crcl_creatinine_upper_bound():
    # µmol/L entered as mg/dL (88 for 1.0) would report near-anuric CrCl and drive underdosing
    with pytest.raises(ValueError):
        creatinine_clearance(50, 70, 88, "male")
    assert creatinine_clearance(50, 72, 40, "male") == 2.2


def test_crcl_bad_age_zero():
    with pytest.raises(ValueError):
        creatinine_clearance(0, 70, 1.0, "male")


def test_crcl_bad_age_over_120():
    with pytest.raises(ValueError):
        creatinine_clearance(150, 70, 1.0, "male")


def test_crcl_bad_weight_zero():
    with pytest.raises(ValueError):
        creatinine_clearance(50, 0, 1.0, "male")


def test_crcl_weight_upper_bound():
    # Extra-digit typo (700 for 70 kg) would silently inflate CrCl tenfold
    with pytest.raises(ValueError):
        creatinine_clearance(50, 700, 1.0, "male")
    assert creatinine_clearance(50, 650, 1.0, "male") == 812.5


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


def test_form_inputs_accept_any_decimal():
    # Browser step validation silently blocked values like creatinine 0.85 or PaO2 85.5,
    # forcing users to round inputs and skewing results (e.g. CrCl by up to ~6%)
    import re
    from app import app
    html = app.test_client().get("/").get_data(as_text=True)
    inputs = re.findall(r'<input type="number"[^>]*>', html)
    assert inputs and all('step="any"' in i for i in inputs)
    resp = app.test_client().post("/", data={
        "calc": "crcl", "age": "50", "weight": "70", "creatinine": "0.85", "sex": "male"})
    assert "102.9" in resp.get_data(as_text=True)


def test_crcl_dosing_weight():
    # Actual-weight Cockcroft-Gault overestimates CrCl in obesity
    from calculator import crcl_dosing_weight
    # 177.8 cm (70 in) male: IBW 73 kg
    assert crcl_dosing_weight(60, 177.8, "male") == (60, "actual")
    assert crcl_dosing_weight(80, 177.8, "male") == (73.0, "ideal")
    assert crcl_dosing_weight(150, 177.8, "male") == (103.8, "adjusted")
    # below 5 ft: no subtraction (female IBW floor 45.5)
    assert crcl_dosing_weight(50, 140, "female") == (45.5, "ideal")
    for h in (50, 300, float("nan")):
        with pytest.raises(ValueError):
            crcl_dosing_weight(70, h, "male")
    with pytest.raises(ValueError):
        crcl_dosing_weight(70, 170, "x")


def test_crcl_adjusted_in_app():
    from app import app
    c = app.test_client()
    data = {"calc": "crcl", "age": "50", "weight": "150", "creatinine": "1.0",
            "sex": "male", "height": "177.8"}
    html = c.post("/", data=data).get_data(as_text=True)
    assert "187.5" in html and "adjusted body weight 103.8 kg: CrCl 129.8" in html
    data["height"] = ""
    assert "body weight" not in c.post("/", data=data).get_data(as_text=True)


@pytest.mark.parametrize("w", [0, -60, 7, 19.9, 700, float("inf")])
def test_crcl_dosing_weight_rejects_impossible_weight(w):
    # Previously returned (w, "actual") or a huge "adjusted" weight silently
    from calculator import crcl_dosing_weight
    with pytest.raises(ValueError):
        crcl_dosing_weight(w, 177.8, "male")
    assert crcl_dosing_weight(650, 177.8, "male") == (303.8, "adjusted")
    assert crcl_dosing_weight(20, 177.8, "male") == (20, "actual")


def test_crcl_creatinine_lower_bound():
    # mmol/L entered as mg/dL (0.088 for 1.0) would silently report a ~tenfold CrCl
    # and drive overdosing of renally cleared drugs
    for cr in (0.088, 0.05, 0.099):
        with pytest.raises(ValueError):
            creatinine_clearance(50, 70, cr, "male")
    assert creatinine_clearance(50, 72, 0.1, "male") == 900.0


@pytest.mark.parametrize("age", [1, 10, 17.9])
def test_crcl_rejects_paediatric_age(age):
    # Cockcroft-Gault is adult-only; a 10-year-old previously got a confident adult CrCl
    with pytest.raises(ValueError):
        creatinine_clearance(age, 30, 0.5, "male")
    assert creatinine_clearance(18, 72, 1.0, "male") == 122.0


@pytest.mark.parametrize("v,label,cls", [
    (14.9, "Kidney failure", "crit"), (15.0, "Severely", "crit"), (29.9, "Severely", "crit"),
    (30.0, "Moderately", "warn"), (59.9, "Moderately", "warn"), (60.0, "Mildly", "warn"),
    (89.9, "Mildly", "warn"), (90.0, "Normal", "normal"),
])
def test_crcl_interp_bands_not_ckd_stages(v, label, cls):
    # A single Cockcroft-Gault value cannot stage CKD (needs > 3 months; ICU AKI is non-steady-state)
    from app import _crcl_interp
    text, c = _crcl_interp(v)
    assert text.startswith(label) and c == cls and "CKD" not in text


@pytest.mark.parametrize("na", [14, 50, 79.9])
def test_anion_gap_sodium_lower_bound(na):
    # Dropped-digit typo (14 for 140) previously returned a large negative AG silently
    with pytest.raises(ValueError):
        anion_gap(na, 104, 24)
    assert anion_gap(80, 60, 10) == 10.0


@pytest.mark.parametrize("alb", [0.04, 0.4, 0.49])
def test_corrected_anion_gap_albumin_lower_bound(alb):
    # Decimal-slip albumin (0.4 for 4.0) would add a false +9 mEq/L to a normal AG
    from calculator import corrected_anion_gap
    with pytest.raises(ValueError):
        corrected_anion_gap(140, 104, 24, alb)
    assert corrected_anion_gap(140, 104, 24, 0.5) == 20.8


@pytest.mark.parametrize("pao2", [1, 8, 14.9])
def test_pf_ratio_pao2_lower_bound(pao2):
    # Dropped-digit typo (8 for 80) previously returned P/F 38, a false severe ARDS
    with pytest.raises(ValueError):
        pf_ratio(pao2, 0.21)
    assert pf_ratio(15, 1.0) == 15.0


@pytest.mark.parametrize("w", [7, 1, 19.9])
def test_crcl_weight_lower_bound(w):
    # Dropped-digit typo (7 for 70 kg) previously returned CrCl 8.8, a false kidney failure
    with pytest.raises(ValueError):
        creatinine_clearance(50, w, 1.0, "male")
    assert creatinine_clearance(50, 20, 1.0, "male") == 25.0


@pytest.mark.parametrize("cl", [0, 10, 14, 19.9])
def test_anion_gap_chloride_lower_bound(cl):
    # Dropped-digit typo (10 for 104) previously returned AG 106, a false high-AG acidosis
    with pytest.raises(ValueError):
        anion_gap(140, cl, 24)
    assert anion_gap(140, 20, 24) == 96.0


@pytest.mark.parametrize("dbp", [0, 8, 9.9])
def test_map_dbp_lower_bound(dbp):
    # Dropped-digit typo (8 for 80) previously returned MAP 45.3, a false vasopressor threshold
    with pytest.raises(ValueError):
        mean_arterial_pressure(120, dbp)
    assert mean_arterial_pressure(40, 10) == 20.0


def test_crcl_adjusted_not_double_rounded():
    # Adjusted CrCl was computed from the dosing weight already rounded to 0.1 kg
    # (156 kg, 172 cm male: AdjBW 103.0488 -> 103.0), shifting CrCl 873.1 to 872.6
    from calculator import crcl_dosing_weight
    from app import app
    exact, basis = crcl_dosing_weight(156, 172, "male", ndigits=None)
    assert basis == "adjusted" and abs(exact - 103.0488) < 1e-3
    assert crcl_dosing_weight(156, 172, "male") == (103.0, "adjusted")
    html = app.test_client().post("/", data={"calc": "crcl", "age": "18", "weight": "156",
        "creatinine": "0.2", "sex": "male", "height": "172"}).get_data(as_text=True)
    assert "adjusted body weight 103.0 kg: CrCl 873.1" in html


@pytest.mark.parametrize("alb", [6.1, 7.0, 8.5])
def test_corrected_anion_gap_albumin_upper_bound(alb):
    # Total protein (~7 g/dL) entered as albumin previously subtracted a false 7.5 mEq/L,
    # turning a high AG of 20 into a "normal" 12.5 and masking a high-AG acidosis
    from calculator import corrected_anion_gap
    with pytest.raises(ValueError):
        corrected_anion_gap(140, 96, 24, alb)
    assert corrected_anion_gap(140, 104, 24, 6.0) == 7.0


@pytest.mark.parametrize("pf", [75.0, 150.0, 250.0, 400.0])
def test_pf_interp_not_ards_diagnosis(pf):
    # P/F alone cannot diagnose ARDS (Berlin also needs PEEP >= 5, bilateral opacities, onset <= 1 wk)
    from app import _pf_interp
    text = _pf_interp(pf)[0]
    assert "ARDS" not in text.split(" — ")[0]
    assert ("PEEP" in text) == (pf <= 300)
