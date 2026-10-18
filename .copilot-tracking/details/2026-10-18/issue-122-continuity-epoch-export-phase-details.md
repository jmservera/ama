---
title: Issue 122 continuity epoch and export phase details
description: Evidence-based task details for bounded source correction
ms.date: 2026-10-18
---

Task 122, issue-122-continuity-epoch-export. Plan and research use the same dated
slug. Current phase: authorized Implement correction TWO FINAL after the frozen
original Complete / Not accepted Review. Original critique is Complete / Revise.

Current continuation supersedes the correction ONE blocker: coordinator authorizes
P05 correction TWO FINAL. Existing recorded-need projection governs all exported
evidence, including nested ledger, legacy/proposal/release and governance text.
Ineligible audiences retain permitted access with explicit limited/incomplete
proof. Never rewrite canonical ledger rows or claim projected rows retain their
original hashes. Full authorized manager unchanged-head verification must remain.
P05-T01 starts with retained failing-first HTTP reproduction and existing audit
projection prior art; P05-T02 requires fresh actual local SQL and installed image.

<!-- P01 -->
## P01 - Lifetime enforcement

<!-- P01-T01 -->
### P01-T01 - Epoch currentness

C1/C2 show identity excludes epoch and `_view` omits claim epoch. Introduce a
creation epoch in task body/identity, compare it to persisted epoch in claim,
dispatch, completion and derived views/export. Pre-change records can use their
retained claim_epoch only for historical currentness when present; unbound
pending records must not be admitted. Missing epochs must never default to current.
Use a shared pure predicate where useful, not per-route divergent logic.

C5/C6 show legacy lifetime and stale-process gaps. Read persisted epoch on
SQL-backed stores through existing connection/lock boundaries. Bind legacy
priority and cache records as well as ai_tasks records; template/manual paths are
not AI reliance. Keep accepted history and original dispositions. Rejection remains
possible without making stale material current.

Completion expectation: tests fail on baseline and pass after implementation,
including accepted-before-suspend history and missing-epoch records. Deterministic
barriers must start the competing action while the first transaction is open,
not join suspension before beginning review. SQL serialization can validly let
review commit first, but after suspension/restart no current reliance remains.

PC-001 direct correction: legacy epoch/suspension admission and record publication
must be atomic at the existing SQL writer boundary, not a fresh read followed by
an unchecked append. A checked continuity-document publication fence may reuse
the existing optimistic `_proc_write` validation without changing sqlstore.py.
If a committed competing epoch wins, publication must retry only the local
record decision as quarantined or fail explicitly; never call the provider again.
No intermediate actionable persisted legacy record. Test provider-result barriers
before final text/document/priority publication with gate-aware stale processes
and independent SQLite/MSSQL connections. Publication committed before suspension
can succeed; already delivered bytes are not remotely revoked.

<!-- P02 -->
## P02 - Offline release evidence

<!-- P02-T01 -->
### P02-T01 - Release resolver

C3/C4: task release references retain ID/version/digest; SQL release body is
immutable but status is updated separately. Export reference-time active snapshot
with ID/status as used in digest, current lifecycle status/revision and all
permitted release-ID events. Preserve proposal provenance and top-level legacy
release field. Resolve absent references explicitly; bound reads and report
truncation, unavailable stores and missing lifecycle evidence as incomplete.
Do not add raw prompts, inputs, credentials or new role privileges.

Completion expectation: serialize bundle, close/disable provider/store, verify
using only bundle and externally supplied head; demonstrate active->revoked
history, missing record/event and truncation. Retain current no-reliance policy
if epoch changes between proposal collection and outer export.

PC-002 direct correction: offline verification must resolve every durable/legacy
release reference, recompute reference-time snapshot digest and reject missing/
contradictory/incomplete lifecycle evidence even with recomputed outer digest and
forced complete=true. Export events as ID, release association, timestamp, body;
include total/exported/truncated counts and coherent current status/revision.
Negative fixtures remove/replace references and snapshots, drop events and
truncate history. Self-contained hashes cannot authenticate wholesale rewriting
of unanchored task-release events; record that limitation explicitly.

<!-- P03 -->
## P03 - Validation and one Review

<!-- P03-T01 -->
### P03-T01 - Actual local evidence

Use pip .venv source installations (already completed after missing packages).
Use unique local Docker SQL Server and UUID-named owned databases, no shared
container/database. Existing mssql-python available. Run focused tests under
SQLite and actual MSSQL independent connections, actual loopback App HTTP, manual
case/resident challenge/hazard writers and negative safety/authority checks.
Read existing manual API fixture patterns before selecting request bodies.
Run relevant existing assistant/continuity/legacy/release and appointment suites.
Run current component Ruff/format/mypy. Build with
docker build -f src/api/Dockerfile -t zf-issue122-api:local src;
execute src/check-container.py for nonroot/read-only/capability/startup contract.
Always stop/remove exact owned SQL/API containers promptly, including failure.
Record SQL Server local versus Azure, template versus inference, and unknown
billing explicitly.

<!-- P03-T02 -->
### P03-T02 - Handoff

Update component guide with lifetime/export contract and compatibility boundary.
Reconcile plan markers/details/changes, then invoke rpi-review once using a fresh
independent reviewer with exact scope and artifact path. Freeze original verdict
and findings. If Not accepted, commit local evidence, no push/PR, return coordinator
defects. Otherwise configure privacy-safe identity, Conventional Commit with
required Copilot trailer, normal push and PR base main using Refs #122.

Human approval checkboxes remain unchecked. No worker acceptance of issue AC,
real authority, Azure head, drill or general serving reversibility.

## Implementation Reconciliation for Original Review

P01 and P02 implemented with 16 new semantic test methods (below the 30-method
ceiling), no removed tests. New SQL classes inherit the same contracts; HTTP
class also retains three existing API regressions. PC-001 deterministic legacy
publication races ran on SQLite and actual SQL Server; PC-002 independent
snapshot/envelope/lifecycle negatives ran serialized offline and on SQL Server.
All 72 Store method argument signatures match the pinned base. No protected #87
file changed. API/core/agents existing static checks pass.

P03 execution completed but acceptance is not achieved: HTTP export returns 403
for the permitted manager because projection.STAFF_GET omits continuity route
kinds. Proposed minimal shared-file correction is documented in changes; no
coordinator is available to authorize overlap. The adverse regression remains
failing on host SQLite, actual local SQL Server and hardened installed image.
Source work is frozen for the one original Review; no worker self-Pass or PR
publication while this material defect remains.

## P04 - Authorized correction ONE current boundary

Coordinator authorization permits only appending continuity and continuity_export
to STAFF_GET in projection.py; all other #87 runtime files and projection
semantics remain untouched. Actual loopback HTTP iterates all seven staff roles,
Contractor and Unknown: register access only for two managers plus Quality
Inspector/Building Safety Liaison; export only for the two managers. Existing
manual/challenge/hazard transactions and safety/authority denials remain exercised.

P04-T01 completed. Three failing-first methods yielded 28 failing subtests and
two malformed-metadata errors before production edits. Both original RV-002
negatives use serialized evidence, forced complete/reasons and recomputed digest
against separately retained unchanged heads. Proposal list/source metadata now
receive independent shape/count/boolean/truncation checks. Exact source_status
available/unsupported/unavailable distinguishes legitimate empty JSON support
from missing evidence; old metadata-less bundles fail closed. No consistent
wholesale rewrite authentication claim. Legacy-only happy fixture explicitly
adds the constructed lifecycle event omitted by direct fixture installation.

P04-T02 fresh validation is recorded in the separate correction-one receipt.
Original failures remain historical evidence, not passing correction evidence.
No second critique/Review, amended Review or independent acceptance is requested.
Execution is complete but publication is blocked. Existing endpoint inventory
exposes a restricted reason through the restored Programme Support Officer export;
the minimal focused actual HTTP regression fails on host, actual MSSQL and hardened
image. No test relaxation, role denial change or hash-breaking redaction was
applied. Coordinator must route correction TWO for audience-safe evidence integrity;
the same-session correction ONE source/evidence is committed locally only.

## P05 - Authorized correction TWO FINAL

P05-T01 implemented using existing can_see_reason policy, NOTE_HELD and closed
allowlist response prior art. No projection.py changes in this cycle. Full
reason-authorized manager exports retain canonical ledger rows/hash/head and
reference snapshots/lifecycle; ineligible managers retain HTTP 200 with explicitly
limited/incomplete summaries and no arbitrary text subtrees. The held canonical
head is a reference, not proof of withheld rows. No rewritten chain is certified.
Verifier rejects full proof from declared limited evidence even after producer
flags/reasons/digest are reset. This is the coordinator's precise authorized
audience decision, not a new entitlement or cryptographic protocol.

One added semantic test exercises nested release/proposal/legacy/governance/
continuity/ledger canaries, original full-manager external head proof, preserved
canonical storage, both managers under configured recorded-need override and
no stale proposal reliance. Existing inventory assertions and original High
negatives are retained. P05-T02 fresh outcomes and exact commands are recorded in
the correction-two receipt; no new Review or self-acceptance follows from tests.
P05-T02 execution complete: final host 245 with 49 opt-in MSSQL skips, existing 163,
actual local MSSQL 72, hardened installed image 44 and configured static checks
pass. Original frozen hashes and all 72 Store signatures preserved. Exact owned
containers removed. Bounded task transitions to Follow-up with automatic session
running, publication authorized and independent coordinator acceptance pending.
Genuine human/Azure/deployment gates remain unmet; correction limit is exhausted.
