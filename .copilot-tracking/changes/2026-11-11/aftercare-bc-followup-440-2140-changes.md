---
title: Aftercare post-1458 follow-up changes (Refs #440 #1402 #1401)
description: Changes record for the dated follow-up observation
ms.date: 2026-11-11
---

## Files changed

* `docs/architecture/cutover-evidence-pack.md`: appended a dated subsection at the end of the existing numeric-order checkpoint section. The `077ad5ad2` text is retained.
* `docs/reference/README.md`: three sentences added to the existing index paragraph. `docs/reference/log.md`: one entry appended. Memory untouched.
* Original artifacts under `.copilot-tracking/` for task `aftercare-bc-followup-440-2140`: research, plan, details, critique, this record, review, state.

## Commands (export of `src` from `origin/main` `97ec3f3c8`, outside the repository; `env -i`, owned `HOME`, export-only `PYTHONPATH`)

| Id | Selector | Exit | Result (from stderr) |
| --- | --- | --- | --- |
| Preflight | origins probe and six file hashes | 0 | three modules import from the export; hashes equal `origin/main` blobs |
| B1 | `test_aftercare_intake` | 0 | Ran 44, OK |
| B2 | `test_aftercare.SnapshotTests` | 0 | Ran 5, OK |
| B3 | `test_aftercare_store` | 0 | Ran 42, OK, skipped 15 (SQL Server opt-in) |

No install, no rerun, no dependency change, no SQL Server, browser, cloud or model. Raw files: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/aftercare-bc-followup-440-2140/`.

## Deviations

* The research, plan and details files were first written with a shell heredoc, contrary to the file-change rule; later files used the create and edit tools. Content unchanged, deviation retained. A `git add -N` I ran there was reversed with `git reset -q` on the tracking path only.
* Critique PC-001 to PC-003 applied.
