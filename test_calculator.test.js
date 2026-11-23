/**
 * Evolvable regression tests — agents may add, modify, or remove these.
 * The oracle (test_oracle.test.js) is the locked reference.
 */

const { meanArterialPressure, pfRatio, anionGap, correctedAnionGap, deltaRatio, wintersExpectedPco2, serumOsmolality, osmolalGap, correctedSodium, aaGradient, shockIndex, correctedCalcium, creatinineClearance, DISCLAIMER } =
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
