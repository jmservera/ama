---
title: Issue 1292 before-fix paired validation changes
description: Changes, commands, identities and outcomes of the evidence-only paired SQL validation
ms.date: 2026-11-11
---

## Identities

* Base and target main `cea1cee5b20f63d7bb134fb7cb87a1bbc7d8618f`; branch `test/demo-priority-before-fix-1292-1111`; prospective commit `0ba32c2c227f6b46119b37946d0810414bc9ea05` (research, plan, details, critique and state) made before any SQL execution (campaign started 2026-11-11 06:32:52Z).
* Original source `e2ecee2565e86889c6beb43cb32e7c5b54270e01`: `store.py` a99948569d64b3f0c2e0a34d409a5d810651dd06, `sqlstore.py` d790455892b6965cc7506713f14b9315ea2dd641, `mssqlstore.py` 842d790484eef7a129f9d04a514f71b4267016bf. Head: `store.py` 70d71de39a79670a75ee64ad18be3e5c472cd3da, `sqlstore.py` 01a3a44c926981fbf02ba26e91fc23b9fc710225, `mssqlstore.py` c712ad4a8a15f794f3a555de48bead66bb86eb39. Test file blob c140d4a8249ba38042d86755a94445925ac5f7be.
* Image `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`, SQL Server 2022 16.0.4305.5, Python 3.12.3, `mssql-python` 1.15.0, Docker 29.9.0, context `default` (`unix:///var/run/docker.sock`).

## Changes

* No source, test, fixture, config or old tracking file was changed. New dated RPI records, one pack subsection, one index sentence and one log entry were added.
* Session-external runner, verifier and snapshots (not committed): two non-editable venvs built by `pip` from `git archive` snapshots in an owned temporary directory (removed afterwards by its exact path), and the external raw receipts.

## Commands and outcomes

1. One non-queued `flock -n /tmp/ama-rpi-heavy.lock` admission under `timeout -k 10 1190`: exit 0, 75 s in total.
2. Original arm, once: `python -c <print sys.path and modules; unittest.main> -v` for 5 `MssqlPriorityOrder` ids, cwd `src/core/tests`, `env -i`, no `PYTHONPATH`: Ran 5, FAILED (failures=4), exit 1, 22 s, no skips, no errors. Wrong-newest assertions on lines 78, 88, 98 and 194; decision boundary passed.
3. Current arm, once: the same 5 ids plus 5 `SqlitePriorityOrder` and 4 `JsonPriorityOrder` ids: Ran 14, OK, exit 0, 0 skips, 5 on SQL Server.
4. Cleanup: container id equal to removal id, leftover-database query status 0 with an empty list, post-removal labelled `docker ps -a` empty with status 0.
5. External verifier: PASS (gates N arm, cleanup, id, image, import-path and skip checks); O observation REPRODUCED-ORDERING (4 wrong-newest, 0 errors).

Raw receipts (session-held): `SHA256SUMS.txt` digest prefix b247dbd1a5c9, `O.stderr.txt` 41c46d7f27e3, `N.stderr.txt` 63cd1512f29e, `verifier.txt` fdcbe9c7758b.

## Divergences and limits

* The critique (Revise) was applied before execution; no divergence from the revised plan occurred.
* Outer bound only; no timeout path was exercised. Image identity is by local id, not a registry attestation.
* The incremental-reload method failed at its cold-load assertion first.
