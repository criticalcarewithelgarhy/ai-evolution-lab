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

function creatinineClearance(age, weight, creatinine, sex) {
    if (creatinine <= 0) throw new Error("Creatinine must be > 0");
    const crcl = ((140 - age) * weight) / (72 * creatinine);
    const adjusted = sex === "female" ? crcl * 0.85 : crcl;
    return Math.round(adjusted * 10) / 10;
}

module.exports = { DISCLAIMER, meanArterialPressure, pfRatio, anionGap, correctedAnionGap, deltaRatio, wintersExpectedPco2, serumOsmolality, creatinineClearance };
