<!-- markdownlint-disable-file -->
# Discovery CLI checkpoint 440 plan critique (2026-11-10)

Executed once on the final candidate plan by the author, before any run. Verdict: proceed with amendments applied directly.

* A1 Scope only the delivered CLI and its affected helpers; do not rerun the broad merged-wave matrix or any package-wide suite.
* A2 The expected-constants check is constructed, not observed analyst work; the section must say so and must not present NOT_READY, DENY or model_used=false as readiness or approval.
* A3 The poisoned-environment values are constructed markers, never real credentials; the report says that the product reads no environment, and absence of a difference is evidence for these markers only.
* A4 Hosted CI for PR 1355 is read metadata from the PR, not for the exact main head `0d262beee`; do not claim exact-head hosted CI.
* A5 Do not claim no write access to an operational system: only policy decisions exist; no tool is registered.
* A6 No new issue unless a failure is reproduced; the known open question (subprocess test needs an installed package, review R2) is a recorded prerequisite, deduplicated against the existing Core CI install step rather than filed.
* A7 Preserve the #440 ledger statement (C3 of five, two left) and name the 135 C4, 1300 C2, 185 and 132 exclusions.
