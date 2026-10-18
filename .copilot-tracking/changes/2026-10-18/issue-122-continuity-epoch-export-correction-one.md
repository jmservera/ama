---
title: Issue 122 authorized correction ONE receipt
description: RV-001 and RV-002 implementation evidence, not a new Review
ms.date: 2026-10-18
---

## Authorization and Boundary

Same task/session 122 / 33f480bb-395e-4492-8a02-d3a84c5a7a89, correction ONE
of maximum two. Clean branch fix/continuity-epoch-export-122 verified at
441da95000318b9b13c928717aba069c5f748487, base
99056cae7bc679d2ace3e42c75f28577cfce8887. No PR at intake.
Coordinator explicitly authorizes only appending continuity and continuity_export
to projection.STAFF_GET. No appointment semantics, other projection edits,
SQL refactor, web change, rebase, live inference or Azure activity.

Original critique remains Complete / Revise, SHA-256
4eeda2d60235f571916a83de65fa9cda8d73e2159291a50286e8055328fc77be.
Original Review remains Complete / Not accepted, SHA-256
9d9d0bff0fdda5a8d163967c4ba8a997ee1bc315ae5a896611fc331aff200abc.
Neither will be edited or repeated. This receipt records correction execution,
not independent acceptance or a second Review.

## Work and Validation

Both original findings have bounded code changes and fresh regression evidence.
Publication is now blocked by a newly exposed audience-projection regression:
the existing endpoint inventory detects a restricted reason in the Programme
Support Officer continuity export. Correction ONE is not ready for publication.
Earlier 66 SQL / 19 image runs contained real HTTP failures and are not reused
as passing evidence. No new Review has run.

### Additional audience blocker found during required regression validation

Existing test_role_endpoint_inventory.RoleEndpointInventory.
test_every_role_against_every_endpoint fails for Programme Support Officer at
/api/continuity/export: synthetic SEEDED-REASON-dementia-and-hearing-loss occurs
in raw ledger entries, although this role is outside DEFAULT_REASON_ROLES.
The previously blocked route concealed this existing inner-export disclosure.
The authorized outer route append exposes it, so it is tightly coupled, not an
unrelated baseline failure. Do not remove/relax the inventory or the new focused
HTTP canary regression, and do not publish a knowingly defective PR.

No speculative redaction was implemented: changing hashed ledger detail breaks
the existing ledger-chain proof, denying the role changes explicitly preserved
inner manager access, and inventing a new projected-proof protocol exceeds this
precise correction authorization. Coordinator must route the remaining correction
(maximum TWO) with an evidence/audience contract. This is an implementation
validation blocker, not a second Review or amended original verdict.

### Actual command/result receipt

All commands ran from the pinned issue worktree with installed pip editable src
packages. Test helper path was
`PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests`.
No uv, private data, paid provider or live infrastructure was used.

| Boundary / command | Actual result |
| --- | --- |
| Failing-first three selectors: OfflineTests.test_original_review_missing_and_truncated_proposals_with_unchanged_head, OfflineTests.test_proposal_metadata_shapes_counts_and_source_status_fail_closed, HttpTests.test_continuity_http_audiences_and_offline_export | 3 methods run; 28 failing subtests, 2 malformed-metadata errors before source changes |
| First corrected focused EpochTests/LegacyTests/OfflineTests/HttpTests/test_continuity | 38 run; 1 fixture failure: legacy direct installation lacked lifecycle event, not a verifier false-valid result; fixture now explicitly retains constructed event |
| Host final targeted existing suites command below | 224 run, 175 pass, 49 opt-in MSSQL skips; no failures at that boundary |
| Existing test_mvp/test_sqlstore/test_governance/test_recovery/test_role_matrix | 87 run, 87 pass, no skips |
| Actual local SQL default runner selectors below | 70 run, 70 pass, no skips; SQL Server 2022 RTM-CU27-GDR 16.0.4305.5, independent connections and deterministic barriers |
| Ruff check, Ruff format --check, mypy in src/api/core/agents | All pass; mypy 57 / 122 / 23 source files |
| Source-context API image build and src/check-container.py | sha256:1d1f3126ea7daf2714b82fb5f631018ce9229939ada3bbc898aac7df3923b7bb; hardened/plain startup and negative security probes pass |
| Installed hardened image EpochTests/LegacyTests/OfflineTests/HttpTests, before added disclosure canary | 23 run, 23 pass, no skips; actual HTTP/manual/export, UID/GID 10001, read-only root, no capabilities, no-new-privileges |
| Additional existing test_role_endpoint_inventory/test_procurement_api/test_quality_procurement | 95 run, 94 pass, 1 fail: existing role inventory detects Programme Support Officer reason disclosure |
| New focused HttpTests.test_export_preserves_programme_support_reason_redaction on host | 1 run, 1 fail; retained adverse regression |
| Same focused MssqlHttpTests selector on fresh owned SQL container | 1 run, 1 fail; exact owned container stopped/removed in finally |
| Same focused HttpTests selector in rebuilt hardened installed image | 1 run, 1 fail; --rm container removed |
| Installed source hash parity | assistants/continuity/projection/ai_tasks/store all exactly match worktree |
| Store AST argument signatures against pinned base | All 72 preserved; no shared SQL/appointment/server/web edits |
| Frozen original critique/Review hashes | Exact originals retained, no second critique/Review |

Final validation is adverse: earlier passing boundaries do not cancel the later
role-disclosure failures. No PR or remote push is authorized while this defect
is known. Correction ONE source and evidence are committed locally for coordinator
routing; independent acceptance remains pending.

Host commands:

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_continuity_epoch_export.EpochTests test_continuity_epoch_export.LegacyTests \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity test_ai_tasks test_assistants test_assistant_release \
  test_assistants_dispatch test_workflows -q
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_mvp test_sqlstore test_governance test_recovery test_role_matrix -q
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_role_endpoint_inventory test_procurement_api test_quality_procurement -q
```

Static checks, from each component directory:

```bash
../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy
```

Actual SQL used the existing session-owned
`/home/azureuser/.copilot/session-state/33f480bb-395e-4492-8a02-d3a84c5a7a89/files/run_owned_sql.py`
through `.venv/bin/python -c "import runpy; runpy.run_path(..., run_name='__main__')"`.
Default selectors: MssqlEpochTests, MssqlLegacyTests, MssqlOfflineTests,
MssqlHttpTests, test_assistants.MssqlContractTests/MssqlReviewTests/
MssqlDurabilityTests/MssqlApiTests. New cases use UUID databases; both runs
require explicit ownership and loopback, keep generated credentials private and
remove only zf-issue122-sql-33f480bb in finally. This is local SQL Server,
not Azure SQL. The second invocation selected only
test_continuity_epoch_export.MssqlHttpTests.test_export_preserves_programme_support_reason_redaction.

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
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests -q
```

The final adverse image invocation reused the same flags/image and selected only
HttpTests.test_export_preserves_programme_support_reason_redaction. Application
source was not mounted. Initial hash-parity probe failed because core is a
namespace package with no __file__; resolving via assistants.__file__ succeeded.
This failed tooling attempt is not passing validation. No raw private inputs
were read or printed. All logs contain constructed fixtures only and remain in
the same session files directory as correction-one-*.log.

The actual HTTP manual path performed case contact, resident service/challenge
intake and hazard raise/refer/receive/accept/repair, refused self-release and
blocked unsafe advance; stale proposal verify/accept/edit remained denied.
The synthetic App has no law store, so rule evaluation logged explicit Unknown,
not a regulatory Pass. Epoch/publication controls and unknown billing behavior
were not changed by this correction.

### Corrected source hashes

| Module | SHA-256 |
| --- | --- |
| assistants.py | 43b2ec7bac11d86fa48baeb2e0ac93d0cf1d5418525081b5541075e9bf9f9adf |
| continuity.py | 3c00de35db2a3b4b1a978f913f0aad39d48f6bb622684ca0342b3aa93ba9e44f |
| projection.py | 65618ca0c9f955a564ad76c1fd9c0531f31d0b1fff6a3bf56726ef2983abcc40 |

Unchanged original epoch-publication source hashes:
ai_tasks.py c66d591851b40cffb3eba2f2eb2acae4386ffba31d1ed08d85e6a27eac9eb02c;
store.py 3dac9b7269bf3b24f65bb439523d865bccdc198a92946d4539e535bcd6989055.

## Residuals

Genuine OQ-017 authority, witnessed authorized drill, immutable external Azure
head, Azure SQL drill and enforceable unsupported-old-image exclusion remain
unmet. Self-contained digests do not authenticate consistent adversarial rewriting.
