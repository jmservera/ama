# Issue 218 live r2 research (2026-11-19)

Refs #218. Synthetic desktop demo; owner decisions of 2026-11-18 apply. Research disposition: executed (read-only `gh` and `az` reads).

## Findings

* The first unticked #218 criterion is the #440 stabilization checkpoint; the second is "all child features closed or deferred by the owner".
* #440 is OPEN. Its two unticked criteria are issue triage with owner-approved deferrals, and PR-delivered artifacts with independent review. Both need the owner or a PR, so no code can deliver them.
* Children: #219 closed; #220, #221, #222, #223, #224 open (gh, 2026-11-19). No owner deferral comment is recorded for them. #224 is deferred to production by the 2026-11-18 decision, but that decision is not an issue-level deferral.
* Deployed API: revision `ca-cutover-test-demo-api--0000033`, digest `sha256:5368f4e4...`, unchanged since the r1 note, so the r1 staff-write live observation still needs a redeploy.
* Prior r1 work (`docs/reference/research/issue-218-first-unmet-demo-criterion-2026-11-19.md`) already added the offline #220 test; nothing further in source is supported by evidence.

## Planning Readiness

Ready for a no-source outcome: the first unmet criterion is not implementable as code. A redeploy would change deployment and need the FULL tier, so it is not attempted.
