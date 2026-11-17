/**
 * Evolvable regression tests — agents may add, modify, or remove these.
 * The oracle (test_oracle.test.js) is the locked reference.
 */

const { meanArterialPressure, pfRatio, anionGap, correctedAnionGap, creatinineClearance, DISCLAIMER } =
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
