---
title: Issue 122 authorized correction TWO final source cycle
description: Audience-safe limited export implementation and actual validation, not Review
ms.date: 2026-10-18
---

## Intake and Decision

Same session 33f480bb-395e-4492-8a02-d3a84c5a7a89, clean branch
fix/continuity-epoch-export-122 at 649d242c3b6fb6236d2f039fd0eeee50daf77af3.
Pinned base remains 99056cae7bc679d2ace3e42c75f28577cfce8887; no PR,
rebase or coordinator checkout access. This is correction TWO, the final source
cycle. Original critique and Review remain frozen, not repeated or self-Passed.

Coordinator explicitly authorizes audience projection within existing continuity
export/helpers: reuse recorded-need policy, preserve manager access, retain the
canonical ledger server-side and emit explicit limited/incomplete evidence for
audiences not entitled to raw free text. A redacted chain is not original proof.
No appointment/projection-policy/shared SQL/web/crypto protocol change.
Source completeness and permitted audience completeness are distinct: full
external-head verification remains available only to reason-authorized managers.

Original critique SHA-256:
4eeda2d60235f571916a83de65fa9cda8d73e2159291a50286e8055328fc77be.
Original Review SHA-256:
9d9d0bff0fdda5a8d163967c4ba8a997ee1bc315ae5a896611fc331aff200abc.

## Execution

Retained focused HTTP disclosure reproduced before source edits: 1 run, 1 fail.
Prior art: projection.py can_see_reason uses the existing DEFAULT_REASON_ROLES/
ZF_REASON_ROLES recorded-need policy; NOTE_HELD and closed contractor response
allowlists explicitly avoid pattern-based text redaction. Existing /api/audit-check
returns verify_ledger summary, not raw rows. hold_notes is case-shaped and cannot
safely classify arbitrary ledger/proposal/release/envelope text. It is not
misrepresented as a universal evidence sanitizer.

P05-T01 implements the same closed-allowlist/held-marker policy in continuity.py,
without changing projection.py. Full reason-authorized managers retain the exact
canonical ledger, head/digests and release reference resolver. Ineligible manager
exports retain structured numeric/boolean lifetime/revision and known disposition
summaries, collection counts, epoch and recorded canonical head; arbitrary text,
identifiers, reference snapshots/events, version/governance narratives and raw
ledger entries are withheld rather than selectively string-filtered. This
conservative projection deliberately cannot reconstruct full references/chain.
It says audience.scope=limited, full_ledger_proof=false, ledger.full_proof=false,
report.intact=false and complete=false with a fixed nonsensitive reason. Verifier
rejects limited full-proof verification even after complete/reasons/digest rewrite.
No projected entry claims to carry its original hash; canonical storage is
unchanged. Full bundle digest is generated only after audience projection.

The one additional semantic method exercises actual HTTP with nested legacy/
proposal provenance, release snapshot/lifecycle, governance/continuity and ledger
canaries; original manager external-head proof remains valid and unchanged after
limited export. Both managers under existing reason-role override receive limited
evidence, not a newly granted privilege. Existing role-denial inventory is retained.

Fixture development failed explicitly on ISO expiry, append-only event update,
and missing recommendation user; fixed only the new fixture: ISO expiry supplied,
real change_release lifecycle writer used instead of forbidden UPDATE, and owner
recorded. No trigger/schema relaxation or source bypass. The final nested method
then passed. These were fixture errors, not successful source validation.

Fresh host/owned SQL/hardened-image/static checks completed without known source
failures at the assessed boundary. Correction count is exhausted; no third source
cycle, new Review or independent acceptance is implied.

## Fresh Validation

All commands used installed src distributions and synthetic fixtures only.
Existing editable pip dependencies were already available; no install/uv or
application PYTHONPATH workaround was needed. Test-helper path only:
`src/api/tests:src/core/tests:src/agents/tests`.

| Boundary | Actual result |
| --- | --- |
| Pre-fix retained PSO disclosure HTTP regression | 1 run, 1 failure, before source edits |
| Initial focused HTTP/offline/role inventory | 33 run, 1 new-fixture expiry error; corrected explicitly, not counted as Pass |
| New nested fixture development | Append-only UPDATE refused, then missing legacy user refused; source guards unchanged, fixture corrected as above |
| Final host targeted selectors below | 245 run, 196 pass, 49 opt-in MSSQL skips, no failures |
| Existing store/recovery/governance/roles/procurement selectors below | 163 run, 163 pass, no skips |
| Actual owned MSSQL default selectors below | 72 run, 72 pass, no skips, SQL Server 2022 RTM-CU27-GDR 16.0.4305.5 |
| Rebuilt installed hardened image targeted classes plus existing role endpoint inventory | 44 run, 44 pass, no skips; actual HTTP canary/full-proof/manual paths, no mounted application source |
| API/core/agents Ruff check, format --check and mypy | All pass; mypy 57 / 122 / 23 source files |
| Source-context API build and existing check-container.py | sha256:95de8929099b3a4568afd15e540d5361815e118e1adbddd653490e6a1ba7f3f1; Docker controls, negative probes and compatible startup pass |
| Installed image parity against final worktree | All five affected original/current core modules match SHA-256 exactly |
| Store AST arguments against pinned base | All 72 signatures preserved |
| Projection byte comparison against pinned base | Only prior authorized continuity/continuity_export append; no further edit, appointment semantics untouched |
| Frozen critique/Review, whitespace and cleanup | Exact original hashes; git diff --check clean; no issue-owned containers remain |

Host commands:

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity test_ai_tasks test_assistants test_assistant_release \
  test_assistants_dispatch test_workflows test_role_endpoint_inventory -q
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_mvp test_sqlstore test_governance test_recovery test_role_matrix \
  test_procurement_api test_quality_procurement -q
```

Configured checks, from each of src/api, src/core and src/agents:

```bash
../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy
```

Actual SQL command:

```bash
.venv/bin/python -c "import runpy; runpy.run_path('/home/azureuser/.copilot/session-state/33f480bb-395e-4492-8a02-d3a84c5a7a89/files/run_owned_sql.py', run_name='__main__')"
```

Existing default selectors: MssqlEpochTests, MssqlLegacyTests, MssqlOfflineTests,
MssqlHttpTests and test_assistants.MssqlContractTests/MssqlReviewTests/
MssqlDurabilityTests/MssqlApiTests. They include deterministic independent-connection
publication/suspend/review/restart/completion overlap, queued/leased/ready and old
gate-aware-process checks, truthful unknown billing, offline original High
negatives and nested audience/full-head HTTP proofs. Runner uses only exact owned
zf-issue122-sql-33f480bb, private random temporary credentials, loopback ephemeral
port, UUID test databases and finally stop/remove. No shared server was touched;
local SQL Server is not Azure SQL.

Image commands:

```bash
docker build -q -f src/api/Dockerfile -t zf-issue122-api:local src
.venv/bin/python src/check-container.py api zf-issue122-api:local
docker run --rm --name zf-issue122-image-33f480bb --read-only --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,uid=10001,gid=10001 \
  --tmpfs /state:rw,nosuid,nodev,uid=10001,gid=10001 \
  -e PYTHONPATH=/tests/api:/tests/core:/tests/agents \
  --mount type=bind,source="$PWD/src/api/tests",target=/tests/api,readonly \
  --mount type=bind,source="$PWD/src/core/tests",target=/tests/core,readonly \
  --mount type=bind,source="$PWD/src/agents/tests",target=/tests/agents,readonly \
  --entrypoint python zf-issue122-api:local -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_role_endpoint_inventory -q
```

Image runs UID/GID10001, read-only root, zero capabilities, no-new-privileges and
only writable tmpfs. Tests start the real local HTTP server inside the installed
image. Both outside-need manager audiences retain permitted export access with
limited proof; unrelated staff/contractor/unknown remain denied. Existing role
inventory assertions were not removed. Canonical full authorized export verifies
against the independently retained unchanged head; limited export cannot acquire
valid/complete proof merely by rewriting producer flags/reasons/digest.

Actual manual path executes contact, resident challenge intake and independent
hazard raise/refer/receive/accept/repair, refuses self-release and blocks unsafe
advance. No law store is loaded in this synthetic App, so rule checks explicitly
log Unknown; this is not regulatory acceptance. Original ready/accepted epoch,
fresh enqueue/scan/claim, late quarantine and unknown-liability regressions pass.
No notices, live inference, external-head custody or real-authority drill ran.
No browser/UI check was required because no UI changed.

Raw constructed-fixture logs remain in the same session files directory:
correction-two-failing-first.log, correction-two-focused.log,
correction-two-nested.log, correction-two-host.log, correction-two-existing.log,
correction-two-sql.log and correction-two-image.log. Earlier correction ONE failures
and the original adverse verdict are preserved; they are not reused as new passes.

## Source Boundary and Publication Readiness

Only continuity.py source and focused tests changed in this final cycle.
No appointment, projection-policy, SQL adapter, server or web change; original
epoch publication controls and unknown billing semantics are unchanged.

| Module | Final SHA-256 |
| --- | --- |
| continuity.py | 0616465f7da75c04acceb6cd0da4e6fa2f69e6e9ce40781c0b8ba1c13983a9c8 |
| assistants.py | 43b2ec7bac11d86fa48baeb2e0ac93d0cf1d5418525081b5541075e9bf9f9adf |
| projection.py | 65618ca0c9f955a564ad76c1fd9c0531f31d0b1fff6a3bf56726ef2983abcc40 |
| ai_tasks.py | c66d591851b40cffb3eba2f2eb2acae4386ffba31d1ed08d85e6a27eac9eb02c |
| store.py | 3dac9b7269bf3b24f65bb439523d865bccdc198a92946d4539e535bcd6989055 |

Read-only remote check still reports main at pinned base
99056cae7bc679d2ace3e42c75f28577cfce8887. No rebase or history rewrite.
Issue blockedBy remains empty; parent #113 is hierarchy, not a dependency.
PR #269 is merged baseline. Owner comment explicitly leaves immutable Azure head
and Azure SQL drill unmet.

P05 implementation and fresh validation execution complete. No known source
failure remains in the bounded checks; publication is permitted by the coordinator,
but independent acceptance remains pending and original Review stays Not accepted.

## Residuals

Genuine OQ-017 authority, witnessed authorized drill, immutable externally held
Azure head, Azure SQL drill and unsupported-old-image exclusion remain unmet.
No whole-issue completion or independent acceptance is claimed.
