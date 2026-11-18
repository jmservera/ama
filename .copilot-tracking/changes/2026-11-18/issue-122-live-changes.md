# Issue 122 live changes

Refs #122. Docs-only; no src change; FOCUSED tier (classification basis: no source, workflow, SQL, infra or deployment edit). No rpi-checks run.

## Files

* `docs/reference/research/issue-122-live-continuity-evidence-2026-11-18.md` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)
* `.copilot-tracking/` research, plan, details, critique, changes, review, state

## Live actions

Read-only GETs, then one synthetic configuration change (`CHG-1`) recorded and reversed (`CHG-2`) on the demo API; two exports verified offline. No Azure resource created, no drill, no suspension, no restore repeated (cites #145).
Witness note: the first two `plan-done` calls were refused (seq 3, 4) because the critique file was missing after a path error; created and accepted at seq 5.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Disable mechanism and tested manual fallback | Proven (read only; no live suspension) |
| Versioned, evaluated, reversible changes | Proven live (pass path; fail path not run) |
| Export independent of AI supplier | Proven live (offline verify, tamper detected) |
| Persist suspension, owner, containment, restart decision | Unproven live (drill-class; repository tests only) |
| Epoch recheck across invoke/scan/claim/dispatch/complete | Unproven live |
| Independent SQL, race, old-image restart tests | Unproven live |
| In-flight and late-result quarantine | Unproven live (assistants disabled) |
| Corrective evidence plus distinct approval gates restart | Unproven live (see #221) |
| Reconstructable history without reliance | Proven live |
| Manual work during suspension | Partly proven (stated by view, not exercised) |
| Witnessed authorised drill | Unproven; excluded by owner, production work |
