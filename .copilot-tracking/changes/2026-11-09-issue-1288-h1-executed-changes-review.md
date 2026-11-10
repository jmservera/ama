<!-- markdownlint-disable-file -->
# Changes and review: issue 1288 H1 restart-context (executed)

Readback `date -u` 2026-11-09T23:54Z. Refs #1288 only. Verification, not a correction; E11 success, E12 and E13 unused. No source, test or schema change. Original H0 (33 selected, 31 ok, 1 skip, 1 FAIL) remains failed-inconclusive; the six H0 and six original H1 records are unchanged.

## Execution

One holder inspection (lock free, no `run-mssql`), one `flock -n /tmp/ama-rpi-heavy.lock` admission at 23:53:30Z, exit 0. Owned venv (hash-locked requirements, editable from this worktree, since deleted). SQL Server 2022 image `sha256:cf8f0ab2ebe6...`, container `cff8f2ef074d...` on 127.0.0.1, removed (0 left). Harness sha256 `fbec7186270b...`, start head `002a720f8` (tree `ca1e5e46`). One test: exit 1, Ran 1, FAILED 1, 0 skips, 3.7 s. Raw (external): `logs-h1-executed-1109/sql-run/` (`h1.json` sha `cf1947ecae57...`, `api.stderr.txt` sha `6689c75f2b41...`).

## Observed

* First service: `review-suggested`, actionable, no denial; cited IDs `sensor:SENS-SYN-1:LIVE-SENS-SYN-1-20261109T1750Z` and `sensor:SENS-SYN-1:R-ZF-1-000`; stored release equals current `fx-quality-evidence` fixture-v1.
* Variant A (H0 construction, default `Ai`): `not-current`, `release-denied` ("no approved release matches ... provider, endpoint, deployment, model_version, actual authorisation"), `current_release` null, `actionable` false. Cited IDs, ID pairs and role projection (Quality Inspector and Retrofit Programme Manager allowed, others refused) were identical to the first service. Task state `ready` and the task body hash unchanged.
* Durable change: after A, `assistant_releases` row `fx-quality-evidence` went from `active` revision 1 to `revoked` revision 2 (other releases unchanged). The harness assertion `raw0 == rawA` failed on this.
* Variant B (independent provider, same binding digest `b4791e0c22b1f1be` as the first service, no writes by B): `not-current` and `release-denied` with `current_release` null, because it ran after the durable revocation. B therefore did not discriminate; it is a harness ordering confound (A before B on shared durable rows), not evidence about B's context.

## Conclusions

* Partially supported: the H0 mismatch is a release-guard outcome (`release_denial`), not loss or change of persisted source/flag IDs, citations or role projection.
* New observation: a service built over a default `Ai` coincides with a durable revoke of the active synthetic release row. Which call performed the revoke (construction, `detail`, `release_reference` or `sensors`) is NOT established. Whether this is intended safety behaviour or a defect is not classified; no defect claim.
* Unproven: that a restarted service with matching provider context reads `review-suggested`. A fresh variant B on unmodified rows (without A first) was not run; one probe was authorised and is spent. Owner/requirement: a fresh-service-equality check needs B first or a separate database, under a new authorisation. No E12 use, no source fix.

## Review

Outcome: probe failed on a harness-ordering confound; H0 stays failed-inconclusive; the revoke side effect is a routed finding for a later user-selected task. Whole #1288, #440 and live-model criteria remain open.
