# Issue 116 round 3 changes

Tier: FOCUSED. Basis: documentation and evidence only; no `src/`, workflow, infra, SQL or deployment change. `rpi-checks.py --all` not run.

## Files

* docs/reference/research/issue-116-live-r3-evidence-2026-11-18.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/evidence/2026-11-18/issue-116-live-r3/ (probe scripts, JSON, offline test outputs)
* .copilot-tracking/{research,critiques,plans,details,changes,reviews}/2026-11-18/issue-116-live-r3-*.md and the session state file

## Validation

* Live (ca-cutover-test-demo-api, GET only): 88 paths swept as Retrofit Programme Manager, 0 reason-value hits (first run's 379 hits were the word "None", kept as adverse). Unknown AI task: 400.
* core: `PYTHONPATH=src:tests:../agents/src:../agents/tests python3 -m unittest test_ai_provider_payload_spy test_data_protection test_ai_input_bounds -q`: 52 OK.
* api: `... python3 -m unittest test_role_matrix test_role_endpoint_inventory test_document_controls -q`: 57 OK.
* mypy, ruff and web tests not applicable (no source change). No Azure resource created, nothing to delete. Credential literal scan of retained evidence: see review.

## Per-criterion table

| Criterion | Verdict | Reason |
| --- | --- | --- |
| Roles allowed to see a vulnerability reason confirmed (OD-14, OD-19) | Unproven | Enforcement shown for one reason role; other roles not signable; confirmation is a human approval excluded for the demo |
| Allowlists and size limits at every provider boundary | Unproven live | Payloads not exposed; offline spy and bound tests pass (52) |
| Permissions rechecked on outputs, citations, explanations, errors, review records, exports | Partly proven | 88 outputs for one role leak no reason value; other roles and citations not shown |
| Document AI requires derivative or necessity exception | Unproven live | No uploaded document; upload would change state; offline document tests pass |
| Already ticked criteria (role x endpoint, contractor canaries, redaction decision, provider-spy, unknown-field refusal, proposal-only, reuse of wrappers) | Not re-claimed | Offline suites re-run green |
