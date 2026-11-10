<!-- markdownlint-disable-file -->
# Implementation Review: sensor review drafts (#111), 2026-11-10

**Related changes**: [2026-11-10-sensor-draft-111-1110-changes.md](../changes/2026-11-10-sensor-draft-111-1110-changes.md)
**Review execution**: executed once, after implementation (this is the single Review for the task)
**Outcome**: Conformant for the initial increment, no open material findings. Whole #111 remains unmet.

## Method

* Independent read-only `code-review` pass over the uncommitted diff and untracked files, with targeted reruns of the new core and API tests.
* Parent re-verification of the allocation, tests and served browser scope on the final source.

## Findings

* Independent reviewer: no high-confidence defects. Checked contractor and staff projection (allowlist plus pop), role then flag then current-staff then scope ordering, route error mapping, SqlStore `_case` change tracking, conflict rollback and `CommittedReloadError` handling.
* Reviewer limits: did not run the browser check; MSSQL path read only. The parent ran both (MSSQL: 61 core tests, 0 skips; browser: 42 checks with axe).

## Acceptance against the owner brief

| Criterion | Evidence | Result |
| --- | --- | --- |
| New case-local interface, no TaskQueue or assistant reuse | `sensor_review_draft.py`; no `store.py`, `sqlstore.py`, import, register, feed or `tools/` edits (`git diff --name-only`) | Met |
| Default-off, unapproved, no model or work | flag tests, `NO_APPROVED_RULE` served refusal, side-effect equality tests | Met |
| Exact lineage, idempotent reopen, immutable provenance | key, reopen, changed-key and bound tests on JSON, SQLite, MSSQL | Met |
| Need-to-know access | role gate before flag, staff revalidation, projection pop, contractor and liaison denials over HTTP and browser | Met |
| Consent, stale, missing, weather regressions | consent-withheld read, stale, declined and weather-only refusals | Met |
| Actual MSSQL rollback and conflict | disposable SQL Server container tests | Met |
| Served UI scope check | extended existing browser check, 42 checks, axe clean | Met for engineering evidence |
| Constructed approval only synthetic | `SYNTHETIC TEST ONLY` labels, private seam, no served path | Met |

## Routed work, not performed

* No actual rule, method or human approval source exists; a served write stays refused until one is separately approved.
* No UI creation control; native assistive technology and copy acceptance not performed.
* Hosted CI, independent exact-head review and human approvals remain.
* Parent #109 and main integration, and #135 and #132 textual ordering at integration, are later work.
* #1300 pinned MSSQL discovery does not include the new opt-in class; it is not edited here.
* Issue-wide correction balance UNKNOWN; no allowance inferred.
