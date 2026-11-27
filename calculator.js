/**
 * ICU Calculator — JavaScript lineage.
 * Single module; all formula functions exported from here.
 */

const DISCLAIMER = "NOT FOR CLINICAL USE — research experiment only";

function meanArterialPressure(sbp, dbp) {
    return Math.round((dbp + (sbp - dbp) / 3) * 10) / 10;
}

function pfRatio(pao2, fio2) {
    if (fio2 <= 0) throw new Error("FiO2 must be > 0");
    return Math.round((pao2 / fio2) * 10) / 10;
}

function anionGap(na, cl, hco3) {
    return Math.round((na - cl - hco3) * 10) / 10;
}

function correctedAnionGap(na, cl, hco3, albumin) {
    // Figge correction: AG + 2.5 × (4.0 − albumin[g/dL])
    return Math.round((na - cl - hco3 + 2.5 * (4.0 - albumin)) * 10) / 10;
}

function deltaRatio(na, cl, hco3) {
    // Delta-delta: (AG − 12) / (24 − HCO3)
    if (hco3 >= 24) throw new Error("HCO3 must be < 24 for delta ratio");
    return Math.round(((na - cl - hco3 - 12) / (24 - hco3)) * 100) / 100;
}

function wintersExpectedPco2(hco3) {
    // Winter's formula: expected PaCO2 = 1.5 × HCO3 + 8 (± 2) for metabolic acidosis
    const mid = 1.5 * hco3 + 8;
    return { expected: Math.round(mid * 10) / 10, low: Math.round((mid - 2) * 10) / 10, high: Math.round((mid + 2) * 10) / 10 };
}

function serumOsmolality(na, glucose, bun) {
    // Calculated osmolality (mOsm/kg): 2 × Na + glucose[mg/dL]/18 + BUN[mg/dL]/2.8
    return Math.round((2 * na + glucose / 18 + bun / 2.8) * 10) / 10;
}

function osmolalGap(measuredOsm, na, glucose, bun) {
    // Osmolal gap: measured − calculated osmolality (normal < 10 mOsm/kg)
    return Math.round((measuredOsm - (2 * na + glucose / 18 + bun / 2.8)) * 10) / 10;
}

function correctedSodium(na, glucose) {
    // Katz correction for hyperglycemia: Na + 1.6 × (glucose[mg/dL] − 100) / 100
    return Math.round((na + 1.6 * (glucose - 100) / 100) * 10) / 10;
}

function sfRatio(spo2, fio2) {
    // SpO2/FiO2 ratio — non-invasive P/F surrogate (S/F 315 ≈ P/F 300; valid only when SpO2 ≤ 97%)
    if (fio2 <= 0 || fio2 > 1) throw new Error("FiO2 must be in (0, 1]");
    return Math.round((spo2 / fio2) * 10) / 10;
}

function aaGradient(pao2, paco2, fio2, patm = 760) {
    // A–a gradient: PAO2 − PaO2, where PAO2 = FiO2 × (Patm − 47) − PaCO2 / 0.8
    if (fio2 <= 0 || fio2 > 1) throw new Error("FiO2 must be in (0, 1]");
    return Math.round((fio2 * (patm - 47) - paco2 / 0.8 - pao2) * 10) / 10;
}

function shockIndex(hr, sbp) {
    // Shock index: HR / SBP (normal 0.5–0.7; > 1.0 suggests shock)
    if (sbp <= 0) throw new Error("SBP must be > 0");
    return Math.round((hr / sbp) * 100) / 100;
}

function correctedCalcium(calcium, albumin) {
    // Payne correction: Ca[mg/dL] + 0.8 × (4.0 − albumin[g/dL])
    return Math.round((calcium + 0.8 * (4.0 - albumin)) * 10) / 10;
}

function freeWaterDeficit(na, weight, sex) {
    // Free water deficit (L): TBW × (Na / 140 − 1), TBW = weight × 0.6 (male) or 0.5 (female)
    if (na <= 0) throw new Error("Na must be > 0");
    const tbw = weight * (sex === "female" ? 0.5 : 0.6);
    return Math.round(tbw * (na / 140 - 1) * 10) / 10;
}

function roxIndex(spo2, fio2, rr) {
    // ROX index: (SpO2 / FiO2) / RR — HFNC success predictor (≥ 4.88 favourable)
    if (fio2 <= 0 || fio2 > 1) throw new Error("FiO2 must be in (0, 1]");
    if (rr <= 0) throw new Error("RR must be > 0");
    return Math.round((spo2 / fio2 / rr) * 100) / 100;
}

function oxygenationIndex(fio2, mpaw, pao2) {
    // Oxygenation index: (FiO2 × 100 × mean airway pressure[cmH2O]) / PaO2 — > 16 severe ARDS
    if (fio2 <= 0 || fio2 > 1) throw new Error("FiO2 must be in (0, 1]");
    if (pao2 <= 0) throw new Error("PaO2 must be > 0");
    return Math.round((fio2 * 100 * mpaw / pao2) * 10) / 10;
}

function idealBodyWeight(heightCm, sex) {
    // Devine IBW (kg): 50 (male) or 45.5 (female) + 2.3 × (height[in] − 60) — used for lung-protective tidal volume
    if (heightCm <= 0) throw new Error("Height must be > 0");
    const base = sex === "female" ? 45.5 : 50;
    return Math.round((base + 2.3 * (heightCm / 2.54 - 60)) * 10) / 10;
}

function protectiveTidalVolume(heightCm, sex, mlPerKg = 6) {
    // Lung-protective tidal volume (mL): mlPerKg (default 6, ARDSNet range 4–8) × Devine IBW
    if (mlPerKg < 4 || mlPerKg > 8) throw new Error("mL/kg must be in [4, 8]");
    return Math.round(mlPerKg * idealBodyWeight(heightCm, sex));
}

function drivingPressure(pplat, peep) {
    // Driving pressure (cmH2O): Pplat − PEEP — target < 15 in ARDS
    if (pplat < peep) throw new Error("Pplat must be >= PEEP");
    return Math.round((pplat - peep) * 10) / 10;
}

function staticCompliance(vt, pplat, peep) {
    // Static respiratory compliance (mL/cmH2O): Vt[mL] / (Pplat − PEEP) — normal ~50–100
    if (pplat <= peep) throw new Error("Pplat must be > PEEP");
    return Math.round((vt / (pplat - peep)) * 10) / 10;
}

function mechanicalPower(rr, vt, ppeak, pplat, peep) {
    // Mechanical power (J/min), Gattinoni simplified: 0.098 × RR × Vt[L] × (Ppeak − ½ × (Pplat − PEEP)) — > 17 harmful
    if (pplat < peep) throw new Error("Pplat must be >= PEEP");
    if (ppeak < pplat) throw new Error("Ppeak must be >= Pplat");
    return Math.round(0.098 * rr * (vt / 1000) * (ppeak - 0.5 * (pplat - peep)) * 10) / 10;
}

function ventilatoryRatio(ve, paco2, pbw) {
    // Ventilatory ratio (Sinha): (VE[mL/min] × PaCO2) / (PBW[kg] × 100 × 37.5) — dead-space surrogate, normal ≈ 1
    if (pbw <= 0) throw new Error("PBW must be > 0");
    return Math.round((ve * paco2) / (pbw * 100 * 37.5) * 100) / 100;
}

function deadSpaceFraction(paco2, peco2) {
    // Enghoff-modified Bohr dead space: Vd/Vt = (PaCO2 − mixed-expired PECO2) / PaCO2 — normal 0.2–0.35, > 0.6 poor ARDS prognosis
    if (paco2 <= 0) throw new Error("PaCO2 must be > 0");
    if (peco2 < 0 || peco2 > paco2) throw new Error("PECO2 must be in [0, PaCO2]");
    return Math.round(((paco2 - peco2) / paco2) * 100) / 100;
}

function arterialOxygenContent(hb, sao2, pao2) {
    // Arterial O2 content (mL O2/dL): 1.34 × Hb[g/dL] × SaO2[%]/100 + 0.003 × PaO2[mmHg] — normal ~16–22
    if (sao2 < 0 || sao2 > 100) throw new Error("SaO2 must be in [0, 100]");
    return Math.round((1.34 * hb * sao2 / 100 + 0.003 * pao2) * 10) / 10;
}

function oxygenDelivery(hb, sao2, pao2, co) {
    // Systemic O2 delivery DO2 (mL O2/min): CaO2[mL/dL] × CO[L/min] × 10 — normal ~900–1100
    if (co <= 0) throw new Error("CO must be > 0");
    if (sao2 < 0 || sao2 > 100) throw new Error("SaO2 must be in [0, 100]");
    return Math.round((1.34 * hb * sao2 / 100 + 0.003 * pao2) * co * 10);
}

function oxygenExtractionRatio(sao2, svo2) {
    // O2 extraction ratio (simplified, ignoring dissolved O2): (SaO2 − SvO2) / SaO2 — normal ~0.25–0.30, > 0.5 inadequate DO2
    if (sao2 <= 0 || sao2 > 100) throw new Error("SaO2 must be in (0, 100]");
    if (svo2 < 0 || svo2 > sao2) throw new Error("SvO2 must be in [0, SaO2]");
    return Math.round(((sao2 - svo2) / sao2) * 100) / 100;
}

function oxygenConsumption(hb, sao2, svo2, co) {
    // Fick VO2 (mL O2/min), dissolved O2 ignored: CO[L/min] × 1.34 × Hb[g/dL] × (SaO2 − SvO2)[%]/100 × 10 — normal ~200–250
    if (co <= 0) throw new Error("CO must be > 0");
    if (sao2 < 0 || sao2 > 100) throw new Error("SaO2 must be in [0, 100]");
    if (svo2 < 0 || svo2 > sao2) throw new Error("SvO2 must be in [0, SaO2]");
    return Math.round(co * 1.34 * hb * (sao2 - svo2) / 100 * 10);
}

function bodySurfaceArea(heightCm, weightKg) {
    // Mosteller BSA (m²): √(height[cm] × weight[kg] / 3600) — used for cardiac index and drug dosing
    if (heightCm <= 0 || weightKg <= 0) throw new Error("Height and weight must be > 0");
    return Math.round(Math.sqrt(heightCm * weightKg / 3600) * 100) / 100;
}

function creatinineClearance(age, weight, creatinine, sex) {
    if (creatinine <= 0) throw new Error("Creatinine must be > 0");
    const crcl = ((140 - age) * weight) / (72 * creatinine);
    const adjusted = sex === "female" ? crcl * 0.85 : crcl;
    return Math.round(adjusted * 10) / 10;
}

module.exports = { DISCLAIMER, meanArterialPressure, pfRatio, anionGap, correctedAnionGap, deltaRatio, wintersExpectedPco2, serumOsmolality, osmolalGap, correctedSodium, sfRatio, aaGradient, shockIndex, correctedCalcium, freeWaterDeficit, roxIndex, oxygenationIndex, idealBodyWeight, protectiveTidalVolume, drivingPressure, staticCompliance, mechanicalPower, ventilatoryRatio, deadSpaceFraction, arterialOxygenContent, oxygenDelivery, oxygenExtractionRatio, oxygenConsumption, bodySurfaceArea, creatinineClearance };
