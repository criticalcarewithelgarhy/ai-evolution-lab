/**
 * LOCKED ORACLE — do not modify under any circumstance.
 * Independently verified reference values. Run by CI on every push.
 * Any agent session that modifies this file invalidates the generation's
 * correctness record.
 */

const { meanArterialPressure, pfRatio, anionGap, creatinineClearance, DISCLAIMER } =
    require("./calculator");

// MAP
test("oracle MAP(120,80) = 93.3", () => { expect(meanArterialPressure(120, 80)).toBe(93.3); });
test("oracle MAP(90,60) = 70.0",  () => { expect(meanArterialPressure(90, 60)).toBe(70.0); });
test("oracle MAP(100,70) = 80.0", () => { expect(meanArterialPressure(100, 70)).toBe(80.0); });
test("oracle MAP(80,50) = 60.0",  () => { expect(meanArterialPressure(80, 50)).toBe(60.0); });

// P/F
test("oracle P/F(100,1.0) = 100.0",  () => { expect(pfRatio(100, 1.0)).toBe(100.0); });
test("oracle P/F(60,0.8) = 75.0",    () => { expect(pfRatio(60, 0.8)).toBe(75.0); });
test("oracle P/F(300,0.5) = 600.0",  () => { expect(pfRatio(300, 0.5)).toBe(600.0); });
test("oracle P/F bad FiO2 throws",   () => { expect(() => pfRatio(100, 0)).toThrow(); });

// Anion gap
test("oracle AG(140,104,24) = 12.0", () => { expect(anionGap(140, 104, 24)).toBe(12.0); });
test("oracle AG(138,98,10) = 30.0",  () => { expect(anionGap(138, 98, 10)).toBe(30.0); });
test("oracle AG(136,100,22) = 14.0", () => { expect(anionGap(136, 100, 22)).toBe(14.0); });

// CrCl
test("oracle CrCl male(50,70,1.0) = 87.5",   () => { expect(creatinineClearance(50, 70, 1.0, "male")).toBe(87.5); });
test("oracle CrCl female(50,70,1.0) = 74.4",  () => { expect(creatinineClearance(50, 70, 1.0, "female")).toBe(74.4); });
test("oracle CrCl male(65,80,2.0) = 41.7",   () => { expect(creatinineClearance(65, 80, 2.0, "male")).toBe(41.7); });
test("oracle CrCl bad creatinine throws",      () => { expect(() => creatinineClearance(50, 70, 0, "male")).toThrow(); });

// Invariant
test("oracle DISCLAIMER contains NOT FOR CLINICAL USE", () => {
    expect(DISCLAIMER).toContain("NOT FOR CLINICAL USE");
});
