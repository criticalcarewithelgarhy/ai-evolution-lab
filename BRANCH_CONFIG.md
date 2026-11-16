# Branch Config: lineage/js

cap: 1500 lines
pressure: neutral — language comparison lineage (JavaScript)

## Instructions for the agent (override RULES.md)

**Language:** This lineage uses JavaScript (Node.js). All formula logic lives in
`calculator.js`. Tests use Jest (`test_calculator.test.js`).

**Step 0 — Setup:**
```
git checkout lineage/js && git pull origin lineage/js
npm install
```

**Step 3 — Carrying capacity:** Cap is 1,500 lines.
Run `python metrics.py`. If lines >= 1,400, delete before adding. Never exceed 1,500.

**Step 5 — Run tests:**
```
npx jest test_calculator.test.js --no-coverage
```
If any test fails: `git checkout -- .` then log REJECTED, commit log, push, stop.

**Step 7 — Commit:**
```
git add -A
git commit -m "gen-js-NNNN: <slug>"
git tag gen-js-NNNN
git push origin lineage/js --tags
```

**Step 2 — Choose one change:** Neutral pressure. Pick whatever single change
feels most natural. You may add formulas, improve accuracy, or refactor.
No directional bias.
