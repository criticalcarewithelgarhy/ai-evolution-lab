/**
 * Evolvable regression tests — agents may add, modify, or remove these.
 * The oracle (test_oracle.test.js) is the locked reference.
 */

const { meanArterialPressure, pfRatio, anionGap, correctedAnionGap, deltaRatio, wintersExpectedPco2, serumOsmolality, osmolalGap, correctedSodium, sfRatio, aaGradient, shockIndex, correctedCalcium, freeWaterDeficit, roxIndex, oxygenationIndex, idealBodyWeight, protectiveTidalVolume, drivingPressure, staticCompliance, mechanicalPower, creatinineClearance, DISCLAIMER } =
    require("./calculator");

test("MAP typical", () => {
    expect(meanArterialPressure(120, 80)).toBe(93.3);
});

test("MAP hypotension", () => {
    expect(meanArterialPressure(90, 60)).toBe(70.0);
});

test("P/F normal", () => {
    expect(pfRatio(100, 1.0)).toBe(100.0);
});

test("P/F ARDS", () => {
    expect(pfRatio(60, 0.8)).toBe(75.0);
});

test("P/F bad FiO2", () => {
    expect(() => pfRatio(100, 0)).toThrow();
});

test("anion gap normal", () => {
    expect(anionGap(140, 104, 24)).toBe(12.0);
});

test("anion gap elevated", () => {
    expect(anionGap(138, 98, 10)).toBe(30.0);
});

test("corrected anion gap low albumin", () => {
    // AG 12 + 2.5 × (4.0 − 2.0) = 17.0
    expect(correctedAnionGap(140, 104, 24, 2.0)).toBe(17.0);
});

test("corrected anion gap normal albumin", () => {
    expect(correctedAnionGap(140, 104, 24, 4.0)).toBe(12.0);
});

test("delta ratio pure HAGMA", () => {
    // AG 30, HCO3 10 → (30−12)/(24−10) = 1.29
    expect(deltaRatio(138, 98, 10)).toBe(1.29);
});

test("delta ratio bad HCO3", () => {
    expect(() => deltaRatio(140, 104, 24)).toThrow();
});

test("Winter's formula HCO3 10", () => {
    // 1.5 × 10 + 8 = 23 (21–25)
    expect(wintersExpectedPco2(10)).toEqual({ expected: 23.0, low: 21.0, high: 25.0 });
});

test("Winter's formula HCO3 15", () => {
    // 1.5 × 15 + 8 = 30.5 (28.5–32.5)
    expect(wintersExpectedPco2(15)).toEqual({ expected: 30.5, low: 28.5, high: 32.5 });
});

test("serum osmolality normal", () => {
    // 2×140 + 90/18 + 14/2.8 = 280 + 5 + 5 = 290
    expect(serumOsmolality(140, 90, 14)).toBe(290.0);
});

test("serum osmolality hyperglycemia", () => {
    // 2×130 + 540/18 + 28/2.8 = 260 + 30 + 10 = 300
    expect(serumOsmolality(130, 540, 28)).toBe(300.0);
});

test("osmolal gap normal", () => {
    // 296 − 290 = 6
    expect(osmolalGap(296, 140, 90, 14)).toBe(6.0);
});

test("osmolal gap toxic alcohol", () => {
    // 325 − 290 = 35
    expect(osmolalGap(325, 140, 90, 14)).toBe(35.0);
});

test("corrected sodium hyperglycemia", () => {
    // 130 + 1.6 × (600 − 100)/100 = 138
    expect(correctedSodium(130, 600)).toBe(138.0);
});

test("corrected sodium normoglycemia", () => {
    expect(correctedSodium(140, 100)).toBe(140.0);
});

test("S/F ratio moderate hypoxaemia", () => {
    // 94 / 0.4 = 235
    expect(sfRatio(94, 0.4)).toBe(235.0);
});

test("S/F ratio bad FiO2", () => {
    expect(() => sfRatio(94, 1.5)).toThrow();
});

test("A-a gradient room air", () => {
    // 0.21 × 713 − 40/0.8 − 90 = 9.73 → 9.7
    expect(aaGradient(90, 40, 0.21)).toBe(9.7);
});

test("A-a gradient FiO2 1.0", () => {
    // 713 − 50 − 100 = 563
    expect(aaGradient(100, 40, 1.0)).toBe(563.0);
});

test("shock index normal", () => {
    // 70 / 120 = 0.583 → 0.58
    expect(shockIndex(70, 120)).toBe(0.58);
});

test("shock index shock", () => {
    // 120 / 80 = 1.5
    expect(shockIndex(120, 80)).toBe(1.5);
});

test("corrected calcium low albumin", () => {
    // 7.6 + 0.8 × (4.0 − 2.0) = 9.2
    expect(correctedCalcium(7.6, 2.0)).toBe(9.2);
});

test("corrected calcium normal albumin", () => {
    expect(correctedCalcium(9.5, 4.0)).toBe(9.5);
});

test("free water deficit male hypernatremia", () => {
    // 70 × 0.6 × (160/140 − 1) = 42 × 0.142857 = 6.0
    expect(freeWaterDeficit(160, 70, "male")).toBe(6.0);
});

test("free water deficit female hypernatremia", () => {
    // 60 × 0.5 × (154/140 − 1) = 30 × 0.1 = 3.0
    expect(freeWaterDeficit(154, 60, "female")).toBe(3.0);
});

test("ROX index favourable", () => {
    // (92 / 0.5) / 20 = 9.2
    expect(roxIndex(92, 0.5, 20)).toBe(9.2);
});

test("ROX index HFNC failure risk", () => {
    // (88 / 0.8) / 30 = 3.667 → 3.67
    expect(roxIndex(88, 0.8, 30)).toBe(3.67);
});

test("oxygenation index moderate", () => {
    // (0.6 × 100 × 15) / 60 = 15.0
    expect(oxygenationIndex(0.6, 15, 60)).toBe(15.0);
});

test("oxygenation index bad PaO2", () => {
    expect(() => oxygenationIndex(0.6, 15, 0)).toThrow();
});

test("ideal body weight male", () => {
    // 175 cm = 68.9 in → 50 + 2.3 × 8.9 = 70.46 → 70.5
    expect(idealBodyWeight(175, "male")).toBe(70.5);
});

test("ideal body weight female", () => {
    // 160 cm = 62.99 in → 45.5 + 2.3 × 2.99 = 52.38 → 52.4
    expect(idealBodyWeight(160, "female")).toBe(52.4);
});

test("protective tidal volume default 6 mL/kg", () => {
    // IBW 70.5 kg (175 cm male) × 6 = 423
    expect(protectiveTidalVolume(175, "male")).toBe(423);
});

test("protective tidal volume out-of-range mL/kg", () => {
    expect(() => protectiveTidalVolume(175, "male", 10)).toThrow();
});

test("driving pressure lung-protective", () => {
    // 24 − 10 = 14
    expect(drivingPressure(24, 10)).toBe(14.0);
});

test("driving pressure Pplat below PEEP", () => {
    expect(() => drivingPressure(5, 10)).toThrow();
});

test("static compliance ARDS", () => {
    // 420 / (24 − 10) = 30
    expect(staticCompliance(420, 24, 10)).toBe(30.0);
});

test("static compliance zero driving pressure", () => {
    expect(() => staticCompliance(420, 10, 10)).toThrow();
});

test("mechanical power typical ARDS", () => {
    // 0.098 × 20 × 0.5 × (25 − 0.5 × (20 − 10)) = 0.98 × 20 = 19.6
    expect(mechanicalPower(20, 500, 25, 20, 10)).toBe(19.6);
});

test("mechanical power Ppeak below Pplat", () => {
    expect(() => mechanicalPower(20, 500, 18, 20, 10)).toThrow();
});

test("CrCl male", () => {
    // 50yo, 70kg, Cr 1.0 → (90×70)/72 = 87.5
    expect(creatinineClearance(50, 70, 1.0, "male")).toBe(87.5);
});

test("CrCl female", () => {
    // 87.5 × 0.85 = 74.375 → 74.4
    expect(creatinineClearance(50, 70, 1.0, "female")).toBe(74.4);
});

test("CrCl bad creatinine", () => {
    expect(() => creatinineClearance(50, 70, 0, "male")).toThrow();
});

test("disclaimer present", () => {
    expect(DISCLAIMER).toContain("NOT FOR CLINICAL USE");
});
