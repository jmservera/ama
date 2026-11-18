<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #216 Child Hardening Pass 4 (`RV-001`..`RV-002`)

## Metadata

* Task ID: 216-citation-eval-2142-c4
* Critique date: 2026-11-14
* Verdict: Revise (compatible finding applied directly)

## Findings

### PC-001 (Low) - Project `cases` in `verified_comparison_inputs` to the 6 canonical case keys

* Detail: Caller `cases` dicts may include extra test-fixture keys (e.g., `bundle`), whereas `case_set_digest` and `evaluated_outputs_digest` hash only `{id, set_name, scenario, question, expected, actual}`. Projecting `verified_comparison_inputs["cases"]` to those 6 canonical keys via `_to_plain_json` preserves identical `case_set_sha256` and `evaluated_outputs_sha256` across replay while guaranteeing `json.dumps` safety even if callers attach non-JSON helper objects outside those 6 keys.
* Disposition: Applied directly to `216-citation-eval-2142-c4-plan.md` and `216-citation-eval-2142-c4-phase-details.md`.
