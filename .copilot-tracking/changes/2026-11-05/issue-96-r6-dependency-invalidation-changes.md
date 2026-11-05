<!-- markdownlint-disable-file -->
# Changes: issue-96-r6-dependency-invalidation

Refs #96 (criterion C6, bounded part only). Parent #93 (`feat/finance-integration-93`). Base `ead177ef9`; ancestry of unpublished r5 research `1819a9f7c` preserved by the earlier merge commit.

## Added or changed

* `src/core/src/zava_forward/core/forms.py`: `schema_impact`, `_lineage`, `FORM_WIDE` (exact definition diff, form-wide references, condition closure, undeclared calculation inputs, Unknown on lineage failure).
* `src/core/src/zava_forward/core/form_review.py`: per-field schema staleness from the impact (source freshness now always checked); `dependency_impact` (`schema`, `approvals`) in reports; manifest `schema_dependent_fields` and impact-based schema reason; read-only `proposal_freshness`; approval-reference evaluation.
* `src/core/src/zava_forward/core/form_export.py`: `schema_impact` outside the hashed body; `export_freshness` reports a changed or unknown-lineage schema even with no stale field.
* Tests: new `src/core/tests/test_form_dependencies.py` (8 behavioural tests, JSON and SQL stores); `rule_successor()` helper and three existing tests amended from an identical version 2 to a rule-reference change because an identical successor now correctly affects nothing.
* `src/core/README.md` and `docs/reference/log.md`: documentation and log entry.

## Divergences and amendments

* Plan critique accepted; the first design evaluated proposals inside `_report`. It changed the exact read budgets and cross-draft availability isolation (existing tests), so proposals became a separate read-only function `proposal_freshness`.
* A draft-schema-digest tamper check was dropped because an existing test deliberately mutates a frozen schema in place; registry-row digest verification is retained.

## Not changed

No edit to `quality.py`, `store.py`, `gates.py`, `projection.py`, ranking publication, API server or web files. No approval, schema approval, reviewed export, submission, AI dispatch or registry change.

## Validation (focused, local)

* ruff check/format, `mypy --cache-dir=/tmp/mypy-96-r6` (src+tests of core): clean.
* unittest `test_form_export test_form_review test_form_staging test_form_dependencies` (core), `test_form_staging_api` (api, 7 tests): OK.
* FULL tier: see the final return; the receipt is kept external.
