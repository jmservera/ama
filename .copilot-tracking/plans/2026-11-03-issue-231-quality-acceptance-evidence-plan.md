# Plan: issue #231 slice 5, quality acceptance evidence blocks handover

* [x] `qualityAcceptanceGap` and `qualityName` in `role-screens.js`; add blockers for missing or non-independent accepter and ownerless open defect
* [x] Add `test_unnamed_or_non_independent_acceptance_and_ownerless_defect_block`
* [x] Run focused unit tests, ruff, mypy

## Critique (one pass, inline)

Verdict: proceed. Keep read-only and text-based, no new controls. Independence is compared by name only (case-insensitive); a server-side check is later work. No finding conflicted with a confirmed decision. Tier: focused; no security, infrastructure, SQL or deployment change.

Details: [details](../details/2026-11-03-issue-231-quality-acceptance-evidence-details.md)
