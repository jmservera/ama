# Critique: issue 2303 plan (2026-11-23), executed once

Verdict: accept with direct dispositions.

* Risk: copying only the Dockerfile line fails the build because both dockerignore files exclude the file. Disposition: plan edits `Dockerfile`, `Dockerfile.dockerignore` and `src/.dockerignore`.
* Risk: the existing `test_cutover_audit` pin asserts exactly one golden. Disposition: update it to the two goldens rather than weaken it.
* Alternative (handler degrades to a named unavailable state) rejected: changes API behaviour and the Dockerfile fix is the issue's primary option and smaller.
* Test design: assert each golden is allowed in both ignore files, copied in the Dockerfile and its `ZF_*_GOLDEN` env var points at the copied path; derive the pairs from the Dockerfile so a future golden is covered by the same rule. Mutation check will prove the test fails when a line is removed.
* Criterion 3 cannot be claimed; record as unproven.
