# Changes 2026-11-23 issue 198 r5

Tier: focused (test file only under .github/rubric/scripts; no src, workflow, registry, rubric or gate-semantics change).
Changed: .github/rubric/scripts/test_prepare.py: test_given_registry_when_scanned_then_no_pattern_targets_retired_roots; test_given_current_checkout_when_matching_then_code_artifacts_have_files (solution-code, infrastructure).
Validation: pytest -k "retired or code_artifacts" 3 passed; full test_prepare.py 79 passed before the capstone-deck case was removed (it is skipped over 2000000 bytes without its per-artifact override); ruff check clean. Hosted CI not observed. Live Azure, browser and sign-in not applicable (registry is repository-only; earlier note records live revisions unrelated).
Process note: an exploratory edit preceded the implement-start witness; it was reverted (git checkout) and reapplied after the witness.

## Per-criterion table

| # | Criterion | Status | Why |
| --- | --- | --- | --- |
| 1 | Baseline recorded | Proven (ticked) | earlier notes, latest.json |
| 2 | src coverage registry PR | Proven (ticked) | #292 |
| 3 | Per-PR dual-window totals | Unproven, owner-gated | totals not recorded in PRs; cannot be recreated |
| 4 | Cut-over registry PR and ordering | End state proven and now regression-tested (no mvp/prototype pattern; code artifacts match tracked files); ordering unproven | PR history not reconstructible |
| 5 | README and failures reassessed | Proven (ticked) | #705 |
| 6 | Lock recompiled | Proven (ticked) | #748 |
| 7 | Before and after comparison | Proven (ticked) | #880 |
