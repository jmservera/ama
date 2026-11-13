# Plan critique (independent rubber-duck, one pass, tests not yet run)

Verdict: Proceed with changes. All findings compatible; applied directly, no user decision needed.

1. Blocking: tests/ has no __init__.py; run from src/api/tests with bare module names, record module __file__ and test counts. Applied in details.
2. Blocking: record static audit as partial evidence only; not criterion 4 or WCAG conformance. Applied.
3. Non-blocking: two modules invoke Node; check node availability; record install, import, test, cleanup failures separately. Applied.
4. Non-blocking: name the two prior paths, no overwrite (cp -n semantics), label as historical. Applied.
5. Non-blocking: each rule gets evidence or "not assessed"; static inspection cannot establish keyboard operation or rendered accessibility. Applied.
