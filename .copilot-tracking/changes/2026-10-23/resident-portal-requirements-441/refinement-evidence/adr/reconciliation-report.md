# Completed-PRD reconciliation — delta and contradiction disposition

## Recommendation and custody

Recommend **one integration architecture candidate**:
[resident-service-unregistered-proposal-reconciled.md](../../resident-service-unregistered-proposal.md).
This is a proposed, unregistered, id-null **unsigned review-publication
candidate only**, not publication performed or approved. The original ADR
candidate, state, maps, validation and manifests remain untouched historical
outputs. The PRD package’s subsidiary ADR is retained solely as a source input;
do not publish it alongside this candidate as another canonical decision.
This choice is artifact consolidation, not formal ADR supersession/lineage.

| Exact input | SHA-256 |
| --- | --- |
| Original ADR candidate | e63a39d1556e55056b7130356cdf63772345d53f4c6a24a6b46223be36f2aba6 |
| Original ADR output manifest | 70990fb8e5df9bfe97cb1bbe681335daa9a086cde858825d94e362363701a499 |
| Completed PRD v0.19.1 | 7fb40549ba4975c2feb8d8a2a3de882e06677875c02e4a43c4b3a94ddf218343 |
| Completed PRD output-manifest.json | cbbcc45fde3653343115a2071793cb21dcede1c335cbf1e3800e7e41a59c46b1 |
| Subsidiary PRD-directory ADR | 5aa5184d7fab1b81df643cd8442f386fd5004b9b582c7f1928ce10988959b46f |
| Current independent reviewer summary | 20853b85a852d7df3b8c87ce66fb3c925c40f24b9668d96880d0987d3989e99b |

The two supplied completed-PRD hashes and original ADR candidate hash were
recomputed and matched. All 18 PRD-manifest outputs and three separately
labelled co-located ADR inputs also matched their declared bytes/hashes.
This is local file custody, not an independent Git/head or review attestation.
[Reconciliation input manifest](reconciliation-input-manifest.json) inventories
all 17 original ADR files and all 23 completed PRD files before new authoring;
inventory is not read coverage. Exact convention/tool input hashes are in the
unchanged original authoring-conventions manifest. Output hashes are in the
[new output manifest](reconciliation-output-manifest.json), excluding its own
self-reference. No original manifest is extended or silently reinterpreted.

## Exact completed PRD delta from pinned canonical PRD

Direct text comparison finds only three single-line metadata/banner replacements
(exercise status, version 0.19.1, display banner), two substantive insertion
blocks (resident refinement and qualified full FR trace) and one appended
version-history row. Removed baseline lines are only those three metadata/
banner lines. No FR/AC/NFR/CON/GOAL/DD/OQ definition is deleted or edited.
All 30 actual resident AC-111–140 definition rows are compared byte-for-byte:
criterion text, parent and Not-run status unchanged; line numbers move because
of inserted material. New map records both old and completed source hashes and
lines rather than replacing original provenance.

| Surface | Disposition | Effect on recommended ADR |
| --- | --- | --- |
| Source basis | CHANGED completed input now available | Add exact v0.19.1 hash/source links and new custody; remove stale future-PRD/not-read statements from the new candidate only. Original candidate remains accurate prior history. |
| Option B / rationale | UNCHANGED | Exact owner rationale, shared API/case authority, portal first, task separately gated; no repeat Frame/Decide question. |
| Current quality status | NEW CURRENT ADVERSE EVIDENCE | Add actual independent FAIL/BLOCKED result and all seven findings; do not substitute historic review or author self-check. |
| Twenty stories and R0–R5 stages | COMPATIBLE ELABORATION | Map PR442-S01–S20 and PRD stages to C1–C9 and prior ADR slice keys; no new issue, estimate, date or execution. |
| Freeze timing | COMPATIBLE DEPENDENCY CLARIFICATION | PR442-S19 is in R5 but requires protocol freeze before testing; R0 and R3 freeze/baseline precede R4; R5 reviews results. No retrospective denominator selection. |
| Identity/grants/recovery | COMPATIBLE / no new authority | Explicit person/case/field/document/task/representative scopes, next-request revocation and managed external identity already covered. No login/address/relationship-derived rights. |
| Documents/events/appointment/help | COMPATIBLE | Quarantine/scan/review/acceptance/publication; durable receipts/idempotent replay/manual capture; no booking or consent inference; deterministic human/urgent continuity retained. |
| Numeric resident fixtures | CLARIFIED, not absent | Acknowledge existing 10 MiB/PDF-JPEG-PNG/one-file, 60s scan-follow-up, one-call/15s model and 1/2-working-day queue ages as proposed synthetic configuration only. Actual approval and finite token/budget/live limits absent. |
| Generic/resident NFR precedence | OPEN CONTRADICTION / applicability debt | Preserve 1s list/detail core versus 2s ordinary resident p95, 5 MB core evidence versus 10 MiB resident upload, without selecting/overriding a rule; scope/units/owner clarification needed before shared-operation acceptance. |
| Performance sample method | COMPATIBLE DETAIL | Freeze request mix/window/warm-up; report p50/p95 plus all attempts/errors/timeouts; receipt is durable intake, scan/model/sign-in separate; no achieved SLO. |
| Grounding/review/policy | UNCHANGED | Distinct task registry/evaluation; sources/version/as-of, abstain/handoff; human default and full excluded-category list; routine OFF, simulated outbox only under separate approved exercise policy. |
| Qualified requirement trace | COMPATIBLE supplements | Keep exact BRD/PRD namespaces and explicit scheduling/hazard/representative/policy cross-cutting parents; 30-row trace is design coverage, not approved whole-PRD fidelity. |
| Whole-PRD inherited debt | OPEN, not repaired | Bundled FR/ACs, malformed staff table and FR-059 goal overlink remain; no unrelated PRD rewrite or waiver in ADR. |
| Workload/value | UNCHANGED | Six scripts; five fictional sessions/30 min; 60,000 homes not accounts; WIP 324/720/1200 and hours −1.594/14.74/94.333 judgement only; review cost and disjoint denominators retained. |
| Diagrams | UNCHANGED byte reuse | Same 47 elements, matched SVG/Chrome PNG; mermaid primary, Excalidraw supplementary; inactive baseline and future-task-registration label caveat retained. |
| Registration/lineage | UNCHANGED owner-deferred | id:null, proposed, no supersession, full registration UNMET; no allocator retry/config/new registry. |

## Subsidiary ADR input: useful content, stale wording not adopted

The subsidiary ADR supports the same API authority, scoped grants, file
lifecycle, no-memory bounded task, human default and optional assisted service.
Its `status: proposed-unregistered` is a descriptive custom value, not the
installed closed status enum. The recommended candidate instead retains
`status: proposed` plus `registration_status: unregistered` and `id: null`;
no source file is edited to conceal that distinction.

Its policy section/review-handoff still lists FR-044/AC-084 reconciliation as
something to perform and asks to confirm/revise the already selected Option B.
Its later notes correctly acknowledge prospective reconciliation. Disposition:
use the canonical completed PRD and owner-confirmed decision, **not** stale
requests to reopen Frame/Decide or unresolved wording. Actual OD-53 policy/
release approval remains open and OFF. Subsidiary v0.19.0/snapshot-only basis
and claim that all numerical limits are unselected are dated history; the new
candidate binds v0.19.1 and explicitly distinguishes proposed fixtures from
unapproved live/execution limits. No contradictory authority is imported.

The PRD manifest itself labels these co-located ADR files as not authored/used
by the PRD author. Treating them now as subsidiary inputs does not change that
historical statement or imply the completed PRD independently endorsed them.
No source instructions to invoke reviewers/agents or write registries were
executed. No additional author or ADR agent was spawned.

## Current independent PRD quality is blocking, not accepted handoff

[Actual reviewer summary](../prd/review/reviewer-result-summary.md) identifies
assessment `requirements-quality-PRD-2026-AMA48-001-20261023T225531005Z` and
report `PRD-2026-AMA48-001-quality-20261023T225531005Z`.
Findings payload CAUTION; quality report **FAIL**; Validate **BLOCKED**;
Finalize **NOT_EVALUATED**. Counts: 0 RISK / 7 CAUTION / 34 COVERED;
cautions: 2 HIGH / 3 MEDIUM / 2 LOW. Applied core minimum 2;
**singular = 1** breaches it; feasible and conforming also score 1.
SMART GOAL-005 lacks achievability/time-bound evidence. Structural 71/71
FR-to-AC and FR-to-goal links do not override this outcome.

| Finding | Severity | Explicit retained disposition |
| --- | --- | --- |
| pr442-qual-005 | HIGH | PRD FR-044/FR-060 and AC-104–106 bundles remain nonsingular; no atomization or parent-pass substitution in this ADR. |
| pr442-qual-040 | HIGH | BRD unsigned, governed handoff absent; no fabricated signature/waiver. |
| pr442-qual-006 | MEDIUM | Identity/provider/staffing/recovery/budget/delivery feasibility unknown. |
| pr442-qual-024 | MEDIUM | GOAL-005 Achievable/Time-bound failure remains; review-window wording is not a deadline/commitment. |
| pr442-qual-041 | MEDIUM | Generic/resident NFR target/file-size applicability and precedence unresolved; no silent choice. |
| pr442-qual-009 | LOW | AC-104–106 malformed two-cell rows remain in five-column PRD table; no whole-document conformance claim. |
| pr442-qual-039 | LOW | PRD FR-059 GOAL-004 definition versus GOAL-002 matrix overlink remains. |

This reconciles documentary consistency sufficiently for unsigned human review,
not for Validate exit or approved requirements/architecture. Original source
BRD/PRD FAIL/BLOCKED records and current independent PRD review are distinct
and both preserved. Older change-gap text saying no fresh review is superseded
only as a current-status statement by the later reviewer summary, not deleted.
No independent review of this reconciled ADR was commissioned or claimed.

## Operational, integration and drift limits

OD-52–55, applicable OD-41/42/47 and other retained legal/privacy/service/
release decisions remain open. No actual provider, account, enrolment/recovery,
retention, DPO/legal approval, named staffing/SLA, live consent or activation
is decided here. Architecture registration and FR-036 AI task registration
are distinct; neither is completed by source reconciliation.

The earlier 22:40 coordinator remote drift to d8b416a3… was score-only relative
to the 4017b214 snapshot; source metadata stays unchanged. The supplied drift
note and current user report are not live remote verification. The current
user says native #441 validator/link/bot correction and #126 maintenance are
active. This lane does not inspect worktrees, status, processes, current gate
or remote heads; it makes no assertion about their current completion.
The reported tracked validate-integration.py:273 scope/empty-BASE/numbered-ADR
rejection defect is neither reproduced nor repaired here; current focused
report reproducibility is not claimed. Native integration owns its fix and
fresh exact-byte review/gate/publication process, outside this bounded task.
No native gate receipt or hosted result is transplanted to these new bytes.

Only new files in this ADR directory are written. No original ADR, completed
PRD or immutable snapshot bytes are overwritten. Bounded package checks
are document/hash/arithmetic/trace checks, not application implementation,
security/legal/privacy/accessibility approval, user research, paid inference,
Azure operations or production acceptance. Stop after this package and return
one recommended candidate plus exact hashes and the integration handoff.
