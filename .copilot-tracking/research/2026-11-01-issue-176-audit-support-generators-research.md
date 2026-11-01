<!-- markdownlint-disable-file -->
# Research: issue 176 remaining slice (2026-11-01)

Task: `issue-176-audit-support-generators`. Disposition: executed. Planning Readiness: Ready.

## Prior delivery (merged PRs referencing #176)

* #237, #257: pack, MVP builder, fabric and EPC generators gain seed, version, `generator_revision`, `--as-of`; tests in `src/core/tests/test_generated_dataset.py`.
* #309, #368: scale fixture and sensor snapshots, protected refresh policy (criterion 3 ticked).
* #633: one-command replay audit `zava_forward.core.synthetic.determinism_audit` covering scale fixture, sensor backfill, sensor scenarios and stock fabric.
* Open #651 is unrelated to this slice (is_synthetic labels).

## Gap

* The one-command audit does not replay the public pack generator (`generate_pack.py`) or the EPC generator (`zf_stock_epc.py`) under `support/`; their determinism is only proven in a separate unit test.
* Their revisions are 16 hex characters (`sha256:` plus 16), while the audit accepts only 64.
* The original private stock register generator and pinned OSM inputs remain absent (`docs/reference/research/retrofit-synthetic-data/README.md`, offline acceptance audit). This cannot be fixed in code, so criteria 1 and 2 stay unmet overall.

## Decision

Deliver the narrow slice: add the pack and EPC generators to the audit, accept 16 or 64 hex revisions, test, update README and log. Use "Refs #176" naming unmet criteria 1 and 2.
