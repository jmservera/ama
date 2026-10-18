---
title: Issue 122 continuity epoch and export changes
description: Actual implementation and validation evidence, not issue acceptance
ms.date: 2026-10-18
---

Task 122, issue-122-continuity-epoch-export. Full approved plan in scope.
Implementation started after Research and Plan with one independent critique.
Original critique Complete / Revise is frozen; PC-001/002 directly incorporated
in plan/details before source editing. Original Review subsequently ran once:
Complete / Not accepted, RV-001/RV-002 High. Original evidence below is retained.
Current authorized correction ONE evidence is in
.copilot-tracking/changes/2026-10-18/issue-122-continuity-epoch-export-correction-one.md.
It is not a new Review or independent acceptance.
Correction ONE is blocked for publication by a newly exposed Programme Support
Officer restricted-ledger-reason disclosure. Fresh original-finding checks pass,
but existing role inventory and focused host/actual-SQL/image HTTP fail. Commit
local evidence only; coordinator owns remaining correction TWO. Do not relabel
this implementation validation result as a new Review.

## P01 - Epoch lifetime

Creation epoch now participates in durable identity; claim, dispatch, complete,
list/detail/review and export enforce epoch lifetime. Missing epochs fail closed.
Legacy text/document publication uses an optimistic continuity-document fence
through the existing writer; a known rolled-back continuity conflict retries only
local publication, never inference. Priority and briefing cache are epoch-bound.
Original ready/accepted dispositions are retained as non-current history.

Five initial epoch tests failed before source correction (stale process, queued
claim, scan reuse, ready revival and pre-dispatch restart), then all passed.
New focused tests cover accepted history, independent overlap, late unknown-token
liability, legacy publication, offline evidence and actual HTTP/manual actions.

## P02 - Offline release evidence

Full reference-time active release snapshots, current status/revision and
release-ID event envelopes now accompany export. Offline verifier checks
ID/version/digest/task, event associations/counts/truncation and lifecycle status.
Missing/unavailable/truncated referenced evidence explicitly makes a bundle
incomplete. Legacy top-level release is retained. External head/digest checks
remain. A self-contained unanchored release history is not externally authenticated.

## P03 - Validation and reconciliation

Execution complete, with a material HTTP export failure retained. Installed missing core/agents/API editable distributions with pip into
local .venv. Docker daemon 29.9.0 and mssql-python are available.

First actual owned SQL run: 65 tests, 64 pass, one new HTTP fixture health parser
error (plain-text health response parsed as JSON). All SQL epoch/publication/
offline cases and existing selected SQL assistant suites passed. Exact container
zf-issue122-sql-33f480bb was removed promptly. Initial runner import failed once;
it also cleaned its exact owned container. Running via installed Python -c/runpy
resolved runner context without application PYTHONPATH workarounds.

Source-context API image built as zf-issue122-api:local,
sha256:92a99d516f2dd8047fdfa800f48a8968a1cd50dd658f49545d10b6c576fc5ab7.
Existing src/check-container.py reported Docker controls, negative probes and
compatible startup PASS (UID/GID 10001, read-only root, zero capabilities and
no-new-privileges). No image claim of authenticated affected-path coverage.

Actual manual HTTP exercised case contact, resident complaint/challenge intake,
hazard raise/refer/receive/accept/repair, self-release refusal and blocked retrofit
advance. Rule evaluation remained explicitly Unknown because this synthetic App
fixture has no law store; independent hazard/authority gates still executed.

### Shared-file overlap requiring coordinator authorization

Actual GET /api/continuity/export returns 403 for the authenticated programme
manager before reaching continuity_export: projection.STAFF_GET lacks both
continuity and continuity_export, although server._endpoint maps those kinds.
Exact proposed shared change: append only those two route kinds to STAFF_GET in
src/core/src/zava_forward/core/projection.py. This is a coordinator #87 overlap
file, so it has NOT been edited or bypassed in the HTTP test. There is no
coordinator agent available in this isolated session to authorize overlap.
Coordinator authorization/correction is requested; the failing HTTP regression
will remain adverse evidence for the original Review. No knowingly defective PR
will be published.

### Final validation evidence

All commands ran from the requested worktree against constructed data only.
Test selectors use installed src distributions; test-helper PYTHONPATH is
src/api/tests:src/core/tests:src/agents/tests, never mvp.

| Command / boundary | Actual result |
| --- | --- |
| Initial `python -m unittest test_continuity_epoch_export.EpochTests -q` before correction | 5 run, 5 fail, reproducing baseline defects |
| Final targeted selectors EpochTests, LegacyTests, OfflineTests, HttpTests, test_continuity, test_ai_tasks, test_assistants, test_assistant_release, test_assistants_dispatch, test_workflows | 220 run, 170 pass, 49 opt-in MSSQL skips, 1 fail: authenticated HTTP export 403 |
| test_mvp, test_sqlstore, test_governance, test_recovery, test_role_matrix | 87 run, 87 pass, no skips |
| Final focused EpochTests, LegacyTests, OfflineTests and test_continuity after envelope verifier additions | 30 run, 30 pass, no skips |
| Actual local SQL Server 2022 RTM-CU27-GDR 16.0.4305.5; new four MSSQL classes plus existing MssqlContractTests/MssqlReviewTests/MssqlDurabilityTests/MssqlApiTests | 66 run, 65 pass, 1 fail: same real HTTP export 403; no skips |
| Actual local MSSQL OfflineTests after final verifier additions | 4 run, 4 pass, no skips |
| Existing Ruff check, Ruff format --check and mypy in src/api, src/core and src/agents | All pass; mypy checks 57 / 122 / 23 source files respectively |
| Final API/core Ruff/format/mypy after verifier additions | All pass |
| Final source-context Docker build and src/check-container.py | Image sha256:7ad70d5c969ec33fd1b88ae38d53c3a5aaaa34f76af5c3ca339a0944b85040ce; hardened/plain startup and negative security probes pass |
| Affected new classes inside final installed image under read-only root, zero capabilities, no-new-privileges, UID/GID 10001, writable tmpfs only | 19 run, 18 pass, same HTTP export 403 failure; includes actual local HTTP/manual paths |
| Image installed core source SHA-256 parity against worktree | All four changed core modules exactly match |
| AST comparison of all Store method argument signatures against pinned base | All 72 preserved |
| git diff --check; prohibited #87 file diff; owned container check | Clean whitespace; zero prohibited files changed; no issue-owned containers remain |

SQL command used the session-only owned-container runner via installed
`.venv/bin/python -c "import runpy; runpy.run_path(..., run_name='__main__')"`.
It generated a private temporary local-only SQL password, selected Docker's
ephemeral loopback port, required explicit task ownership, ran unittest selectors,
and stopped/removed only zf-issue122-sql-33f480bb in finally. No credential enters
artifacts. Each new SQL testcase creates/drops its UUID-named database. Existing
SQL fixture databases lived only inside that same owned disposable container.

Image commands:

```bash
docker build -q -f src/api/Dockerfile -t zf-issue122-api:local src
.venv/bin/python src/check-container.py api zf-issue122-api:local
```

The hardened image test mounted only synthetic test modules read-only, not
application source; installed source hashes were independently compared. Local
SQL Server is not Azure SQL. No optional browser/UI work ran because no UI was
changed. No live inference, human authorization, external head storage, Azure
drill or real notices ran. Unknown rule evaluation in the synthetic HTTP fixture
was retained explicitly, not represented as a regulatory evaluation Pass.

### Original Review assessed source boundary

Pinned base and pre-review HEAD: 99056cae7bc679d2ace3e42c75f28577cfce8887.
No source changes are permitted after the one original Review starts.

| Source | SHA-256 |
| --- | --- |
| assistants.py | 878bdff0b7cd981f3ae7337ba18796de60d12477dccc85dcad42c11438b63600 |
| continuity.py | dc15e394a8d7eacf7f25d7a5bf2d06f10ab544e48ec7ca64ae5a26a555f1f92e |
| ai_tasks.py | c66d591851b40cffb3eba2f2eb2acae4386ffba31d1ed08d85e6a27eac9eb02c |
| store.py | 3dac9b7269bf3b24f65bb439523d865bccdc198a92946d4539e535bcd6989055 |
| test_continuity_epoch_export.py | 50f20761cc88c3c3fb4b531136b5946f8965e7b124374ac7c89a6e122d2545b9 |
| src/api/pyproject.toml | 828a5ab401afeb1cedb60bd507c6e1ef6c423c3597619cf87153b432d5edbebf |
| src/api/README.md | e35df30af38b092ddfcefeab032f78f2d1d768cb49ae3a592d6b5e899bae17fa |

P01/P02 implemented. P03 validation executed, not universally passed. Evidence,
plan/details and known blocker reconciled for the one original independent
Review. Submit this adverse result without suppressing the failing test.

## Amendments and Divergences

Original implementation had no scope divergence. Tightly coupled store.py legacy
priority/cache changes were planned. Later correction ONE authorizes only the
two-name projection.STAFF_GET append, documented in plan/details and receipt.

## Unmet Gates and Remaining Work

Genuine OQ-017 authority, witnessed authorized drill, immutable external Azure
head and Azure SQL drill remain unmet. Local synthetic results cannot satisfy
them. No live inference, remote cancellation, exactly-once billing, real notices
or general serving configuration reversibility claim.
