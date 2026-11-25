# Issue 2302 critique (one pass, 2026-11-25)

Verdict: proceed. Risk: importing a private harness from a sibling test couples files; accepted, same tests dir already shares helpers. Risk: a test that passes first time is not failing-first; mitigated by a recorded mutation (rename the server key) that must fail it. Criterion 3 (tick on #100) needs a GitHub write and is left to the owner/coordinator.
