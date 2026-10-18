---
title: Scoped consultation hold integration and publication receipt
description: Same-task authorized rebase, exact source parity, fresh checks and publication boundary
ms.date: 2026-10-18
ms.topic: reference
---

## Scope and exact boundary

Same task 92 / issue-92-scoped-consultation-hold, integration/publication only.
Full new RPI already completed; original Review outcome Residual work, with no
bounded implementation defects. No new source correction, policy change,
critique or original Review is authorized or performed.

| Boundary | Exact value |
| --- | --- |
| Owned topic | feat/consultation-record-controls-92 |
| PR | 389, target main; Refs #92 only |
| Old local candidate | 7e4aa6eca3a65dd9fe5a403a57f63b3edf62cb5c |
| Prior base | 9c648b2006e8b2e563823ea7d5aabdf7f1ac7096 |
| Authorized fetched main | a86282c4badebc58eabbf9e441410d930a201ac2 |
| Initial remote lease | 9fb84836e3e3ad24a17e142bd6a3e9d1a68d70e7 |
| Integrated source candidate | adc9ad984cd9cd6bcfbd30db6d52485d9506ab47 |

Rebased only this topic onto the authorized main, incorporating PR407. No
conflicts occurred, including no production or persistence conflict. Both
upstream and own README sections auto-merged and were inspected. All later
integration changes are receipt/current-metadata updates and an append-only log
entry, not runtime/test changes. A later main move requires coordinator wait.

## Exact parity and full inventory

Generated `issue-92-scoped-consultation-hold-integration-parity.json` records
both changed-file inventories, exact normalized patches, blob preservation,
original SHA256 values, README addition preservation and log prefix checks.
The adjacent `issue-92-scoped-consultation-hold-integration-inventory.json.gz`
contains complete git tree inventories for old local candidate, authorized
main and integrated source candidate, including path, mode, object type and
blob object ID for every tracked file. Its uncompressed SHA256 and counts are
in the parity summary. This is the source-candidate snapshot before receipt-only
commits; final-head source parity is rechecked before publication.

Normalization: `git diff --no-ext-diff --no-renames --no-color --unified=0`,
removing only `index ` and `@@ ` lines. All remaining bytes, including paths,
added/removed source and order, compare exactly. Separate reverse-direction
comparison proves the upstream patch from old candidate to integrated candidate
equals prior-base to authorized-main on all protected source/test paths.

| Comparison | Before and after SHA256, identical |
| --- | --- |
| Own four runtime/test files | a886b897815c534424cad0c7132bd01586cf5192fd9f79755acfc2601b4343cb |
| Protected five upstream runtime/test files | 5deef027e5ee3f5dbc9d2b0b6e2072066c984e274cd895fabeb3a2468f7ba386 |

Own files: API server, procurement API tests, core procurement and consultation
tests. Protected upstream files: task queue API tests, sqlstore, taskqueues,
SQL queue tests and task queue tests. Every other upstream changed file is
byte-identical except the two deliberately additive READMEs. Full-tree comparison
finds no unrelated delta outside the previously owned files and integration
receipt files. SQL recorder, current-actor, source/version, pending/committed
audit, recovery and optimistic writer controls are not redesigned.

Both README deltas retained: core own 65 added lines and upstream 15; API own
39 and upstream one. Exact upstream log prefix: 418574 bytes, SHA256
4a91d2afd6337ca0f8e333470e9ceb3a4f409973f3a10fb5b39a39e81f56edc2.
All old local appended entries remain intact before the new integration entry.

## Original assessments, unchanged

| Artifact | SHA256 before and after |
| --- | --- |
| 2026-10-17 original critique | dc6c9bca23f55e9f80cfc9ed231547ae668b0e72cee5b538ab5b6f25ec24ce17 |
| 2026-10-17 original Review | e4a7543ac73f1e0fdaee61ca8c093acdb1cc4f6b9b2c433b69fcb7384391a59f |
| 2026-10-18 scoped original critique | a404f6d5381e2e5520c0a60d328a56d45bc46a5d660e5876936e51fd130818ec |
| 2026-10-18 scoped original Review | ab5cb437f994e556b08febb57903385c337090d5f12f42b92d099de582af5573 |

All seven old-task artifacts plus new research/critique/Review are hash-identical
to the old local candidate. Only current new-task plan/details/state/changes
are reconciled. Historical verdicts and original review routing remain intact.

## Fresh validation

Existing installed editable distributions, UID/GID 1000; paths resolve into this
worktree. No dependency install, private dataset, uv or mvp workaround.

Common command prefix from repository root:

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest
```

Focused selectors: `test_consultation_controls test_procurement_api
test_quality_procurement test_mvp test_workflows -q`.

Combined selectors: focused selectors plus `test_taskqueues test_sqlqueues
test_task_queue_api test_buildings test_hazard_referral test_resident_decisions
test_role_matrix test_scenario_manifest test_stock_reconciliation
test_grant_lifecycle_controls test_finance_match_controls -q`.

| Fresh check | Actual result |
| --- | --- |
| Focused consultation/provider/workflow/API | 212 run, 199 passed, 13 explicit skips; 80.599s |
| Combined protected queue and coupled controls smoke | 553 run, 458 passed, 95 explicit skips; 151.838s |
| Core Ruff check / format --check / mypy | Pass; 72 files formatted, 125 typed source files |
| API Ruff check / format --check / mypy | Pass; 24 files formatted, 56 typed source files |
| Git diff whitespace check | Pass |

Focused and combined outputs are retained in adjacent integration-prefixed
text files. Expected unknown law-store diagnostics remain visible; no fallback
or fabricated pass. Optional backend/browser skips remain skips. Counts overlap
and are not unique-test totals.

Historical actual owned SQL: 136 run, 135 passes, one intentional skip. Upstream
hardened-image/SQL evidence is retained unchanged in the upstream receipts.
Neither is a fresh integration result. No rerun was justified: there was no
production conflict or integration-authored persistence change, own source is
byte-identical, and inherited queue/sqlstore changes are exactly upstream.
No browser/WCAG, human, live Legal, genuine let/renew or deployed acceptance
was performed or claimed.

## Publication gate and remaining boundary

Initial publication must use only the explicit lease for
`refs/heads/feat/consultation-record-controls-92` at
`9fb84836e3e3ad24a17e142bd6a3e9d1a68d70e7`. Normal pushes only afterward.
Verify main remains exact authorized a86282c4 immediately before publication.
Commit identity is authenticated GitHub 8036360/jmservera, repository-local
`8036360+jmservera@users.noreply.github.com` for author and committer, Conventional
Commit and required Copilot co-author trailer.

PR389 must describe the current scoped behavior and full RPI, exact current
head/base, original outcomes, historical versus fresh evidence and remaining
Legal/genuine let-renew/human/live acceptance. Closing issue references must
be empty. No issue/board/merge operation, Azure/spend, private input, Legal
approval, real let/renew or expanded scope. Stop after publication for complete
independent coordinator review; no follow-up implementation.

## Actual publication disposition: blocked before push

Evidence/receipt candidate:
`ae2bc36b14025f833d449bc12c18873ee65e4b0d`. Exact parity rechecked at this
commit after receipt-only changes. The immediate pre-push guard found remote
main `ab0613f3336109ff9b96560a16758ee842232715`, not authorized
`a86282c4badebc58eabbf9e441410d930a201ac2`, and exited before `git push`.
No force lease was consumed and no normal push followed.

Read-only confirmation: topic remains
`9fb84836e3e3ad24a17e142bd6a3e9d1a68d70e7`; PR389 is open with unchanged
head/body and empty closingIssuesReferences. Its reported baseRefOid remains
historical `1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c`, not evidence that remote
main is unchanged. No PR write or issue/board/merge action occurred.

Integration onto authorized a86282c4 and fresh validation are complete locally;
publication is blocked, not complete. Current state is automatic / running /
Follow-up / blocked, awaiting coordinator direction under the explicit
"if main moves again, report wait" instruction. Do not integrate the new main,
publish, run another original Review/critique or begin follow-up implementation.
The commit containing this final metadata-only stop is the local handoff tip;
resolve it with `git rev-parse HEAD`. The caller reports its exact hash.
