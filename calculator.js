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

function creatinineClearance(age, weight, creatinine, sex) {
    if (creatinine <= 0) throw new Error("Creatinine must be > 0");
    const crcl = ((140 - age) * weight) / (72 * creatinine);
    const adjusted = sex === "female" ? crcl * 0.85 : crcl;
    return Math.round(adjusted * 10) / 10;
}

module.exports = { DISCLAIMER, meanArterialPressure, pfRatio, anionGap, creatinineClearance };
