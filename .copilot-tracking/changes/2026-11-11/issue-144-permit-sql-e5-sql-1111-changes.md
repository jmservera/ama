<!-- markdownlint-disable-file -->
# Changes: issue-144-permit-sql-e5-sql-1111

Refs #144 only. Runtime validation record for the frozen E5 module. No source, test, helper, workflow, gate, requirements or pyproject change.

## Outcome

* Disposable real SQL Server validation ran once, to completion, against frozen source `3bfa7e2a` (tree `5b238bfa`, module sha256 `2f45a6905337328793b5937c3079e407735cd54484b51b3949d6c7b8520de017`).
* Fixed source: 7 SQL tests ok, Ran 7, zero errors, zero skips, 3 causal WITNESS lines (E1-MARGIN, E1-AUTHORITY, E1-ISSUED-AT) with real lock-wait, KEY/applock, SPID, statement-offset and DB-clock evidence.
* N1 (stale pre-lock clock read, external core copy): Ran 7, failures=2 exactly case 1 `E1-MARGIN` (permit True instead of lease-expiring) and case 3 `E1-ISSUED-AT` (issued_at 1794405589.775 below t_pre-bound 1794405590.89). Cause text confirmed, not only labels.
* N2 (historical E2 reverse hunk, external core copy): Ran 7, failures=2 exactly case 5 `E2-STORED-ROOT` (0 != 1) and case 6 subTest `E2-CONFLICT-ROOT` (True is not false); ID-conflict passed first.
* Cleanup: safe readback (0 open transactions, 0 blocked), exact-owned check, `docker rm -f` of the captured id, container absent, owner label filter empty, credential scan 0 hits over 2415 files, lock released, no containers remain.

## Limitations

* This is disposable local SQL Server 2022 Developer (16.0.4305.5) evidence for the permit boundary only. It is not production, model, provider, deployment or whole-#144 acceptance, and not publication approval.
* Each run executed once; timing witnesses are single observations, host polls are bounds only.
* Private `owner.token` and `scratch-manifest.json` were retained (scratch manifest is separate from the SQLGuard manifest); `sa.pw`, `sql.env`, `sql-secret.json` and the SQLGuard manifest were unlinked after container removal.
* Independent assessment of the executed driver and evidence belongs to Root.

## Evidence

External X = `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/144-permit-sql-e5-sql-1111` (logs 01-89, receipts, scripts; driver sha256 `4b6d0eef27bf520b41fabe36bf54beb65198003f1240fb60e906a0b5a5d3ec8b`). Handoff: `handoff-144-permit-sql-e5-sql-1111.txt` under the coordinator files directory.
