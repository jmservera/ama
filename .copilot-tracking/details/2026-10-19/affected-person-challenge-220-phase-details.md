<!-- markdownlint-disable-file -->
# RPI Phase Details: affected-person challenge

## Metadata

* Task ID: 220
* Task slug: affected-person-challenge-220
* Date: 2026-10-19
* Plan: .copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md
* Evidence: .copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Failing-first proof | Complete; actual missing-feature failures | P01-T01 |
| P02 | Core/HTTP/workbench | Complete; retained-priority slice | P02-T01, P02-T02 |
| P03 | Validation/documentation | Complete; scoped proof and explicit limitations | P03-T01 |
| P04 | Review/frozen gate | Original Review Partial / Not accepted; frozen external gate pending | P04-T01 |

<!-- rpi:phase id=P01 -->
## P01: Establish executable behavior proof

<!-- rpi:task id=P01-T01 -->
### P01-T01: Failing-first core and HTTP tests

Existing public dataset.DATA is the continuing tiny constructed regression
fixture, not replacement stock. Create priority records using actual
`ai_priority(..., mode="workflow-only")`, never real AI. Compare independently
specified IDs for same proposal, same case-source hash and same policy version
versus distinct proposal/source/case/version. Human reviews come through actual
resolve_priority where possible; fixture-only version variation is labelled
constructed, never represented as an approved policy. Copy negative-boundary
state before action and assert exact equality afterward. JSON/SQLite reopen and
real loopback HTTP prove persistence. Record actual preimplementation failures.
No production writes before this phase's proof is captured.

<!-- rpi:phase id=P02 -->
## P02: Implement retained-priority challenge slice

<!-- rpi:task id=P02-T01 -->
### P02-T01: Server-owned targets and actions

Target kinds are proposal, source and policy. Proposal fingerprint covers
immutable original priority content/creation references, not mutable review.
Separate decision token covers retained human disposition; challenge opening
must match both observed values so concurrent review cannot silently rebind.
Source reference is the actual captured per-case hash; policy is actual
recorded version. Old missing source is Unknown, never inferred from current
case. No arbitrary client dependency lists. Owner is `_person`; actor current
registered named staff plus resident/reason rights. Source/channel/request,
supplied explanation, non-digital route and next update are required. Resolve
with current owner/manager plus expected version and explicit supplied evidence.
No source edit, redress finding, resident choice or human approval is generated.
Store challenge and immutable target/human decision capture in the case so the
existing resident writer transaction replay covers actor/owner/rowversion.
SQL target reads must use current transaction rows rather than stale in-memory
recommendation when replay validates. Reject unknown/client actor/time fields.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Stale readers and safe manual workbench

Derive dependency matches against retained exact target references after a
human records correction. Proposal match is exact immutable fingerprint;
source match exact case ID/hash; policy match exact retained policy version,
restricted to the retained priority contract. Multiple causes compose. Old
human disposition stays historical and is separately labelled stale.
Block accept/edit at server, preserve reject/manual/hazard paths. Ensure latest
priority projection and exported evidence agree. No broad status rewriting.

Read challenge collection/catalog only under existing resident and reason
rights; contractor projection never includes either. Workbench uses existing
native semantics/tokens, labelled select/input/date controls, focused live error
feedback and textual states. Explicit correction confirmation is cancellable.
Protect unsaved drafts from unrelated refresh/navigation and never silently
bind a refreshed target into an old draft. Prefer an isolated challenge form
helper rather than changing unrelated resident forms if shared helper lacks
required protection. Source guideline successfully retrieved in Research W2;
refresh before original Review. No public-page redesign skill applies to the
internal app screen.

<!-- rpi:phase id=P03 -->
## P03: Validate and document

<!-- rpi:task id=P03-T01 -->
### P03-T01: Focused actual checks and knowledge compounding

Existing test modules own core and HTTP contracts. Browser script uses a
temporary public synthetic SqlStore and actual ThreadingHTTPServer, loopback-only
network and actual Chromium. Keyboard submit both routes, inspect persisted
records and stale review, error focus, cancellation, permitted/denied projection,
three viewport reflows and reduced motion. Record unperformed screen-reader and
human comprehension checks as such. Existing 17-group gate performs pinned axe,
SQL, four images/scans/SPDX and logo; extra issue selectors may supplement but
must not change the runner/workflow matrix.

Use pip-only isolated environment after missing dependencies; scrub credential
variables from test children, preserve existing Node PATH. Do not run heavy work
concurrently; gate owns /tmp/ama-rpi-heavy.lock. Update existing component docs,
KB index and append-only log for material durable findings. Keep memory intact.
Ruff/mypy use existing policy; no broad new exemption.

<!-- rpi:phase id=P04 -->
## P04: Original Review and frozen gate handoff

<!-- rpi:task id=P04-T01 -->
### P04-T01: Independent original Review and exact-head evidence

Reconcile plan markers/details/changes before original Review. Reviewer activates
rpi-review once, reads actual diff/requirements/validation, writes only original
review. Preserve verdict and every finding unmodified; route defects to later
work rather than repair and re-review. Update current state before freeze,
including explicit pending external-gate/coordinator handoff. Resolve `gh api
user`, configure only local privacy-safe noreply, commit both author/committer
and Copilot trailer. Commit all source and issue-owned original RPI evidence,
not unrelated tracking. Fetch main; use caller base
eeb6c3aba5d07244ae3cc0e53d839617fd928e3b. Full gate:

```bash
PATH="/tmp/rpi-413-tools:$PATH" PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --base eeb6c3aba5d07244ae3cc0e53d839617fd928e3b --out <fresh-external-dir>
```

Verify receipt externally; record clean HEAD/base/receipt hashes in final
handoff only. No subsequent commit or source change. No push/PR/merge/issue
mutation. Coordinator independent exact-head assessment and owner
human/tenant/qualified approvals remain outstanding regardless of local pass.

## Original Critique Direct Amendments

PC-001: priority accept/edit needs a dedicated context validated inside existing
SQL writer, reading current case-held corrections including other-case policy
causes. Restore refused pending disposition/audit; reject/manual paths remain.
Test actual two-store correction between read and save for both accept and edit.

PC-002: source hash captures the audience-filtered citation labels beside the
initial facts/template before generation, never a later current-case read.
An intervening source change during workflow-only generation must leave the old
proposal hash unchanged and give later generation a different hash.

PC-003: resolution is Open -> Resolved exactly once; opening and terminal
evidence immutable. A second current-version resolution is denied.

PC-004: explicitly remove new collection/catalog unless both existing
resident-view and reason entitlements hold, after resident-data restoration.
Do not add these fields blindly to RESIDENT_FIELDS. General audit contains only
record/action IDs; evidence export includes derived stale flags without raw
challenge text. Test all three denied actor classes with canaries.

PC-005: actual accepted and edited human reviews are mandatory fixture facts.
Expected sets distinguish identical-content proposal IDs, same case/hash,
same hash/different case, same policy across cases, changed policy and unrelated
contract. Explanation-only and multiple independent corrections are required.

PC-006: issue-specific store coverage is JSON/SQLite, not native SQL Server.
The unchanged 17-group native-SQL selectors are general regression only. Extra
selectors do not retain the owned SQL endpoint; do not claim otherwise.

PC-007: parent shell verified /tmp/rpi-413-tools exists. Critique's restricted
worker context does not establish a parent restriction. Run caller's unchanged
command with actual preflight/shared lock; if unavailable report blocked, never
bypass or borrow a receipt. No additional gate/matrix/framework is introduced.

## Implemented Boundary and Evidence

P01-P03 executed in sequence. Ten new core methods (seven JSON methods inherited
by SQLite plus three SQLite-specific writer cases), two HTTP methods and one
browser script remain within the ownership budget; no tests removed. Focused
run: 19 passed, no skips. Broader surrounding suites: 238 discovered, OK with 38
existing opt-in skips; this is not native SQL challenge coverage.
Core/API full Ruff, format and strict mypy pass (128/62 checked Python sources),
as do changed JavaScript syntax checks. Browser runs actual public synthetic
SQLite/HTTP and Chromium 156.0.8078.4; four scoped pinned axe scans include
expanded new forms, keyboard error/cancellation/draft controls and three
viewport reflows. Zero violations/incomplete checks in those scans; not a
whole-page, screen-reader or human acceptance result.

The new challenge collection/catalog is explicitly removed without BOTH
entitlements. Audit omits narrative; export retains original status plus derived
staleness, with reliance disabled. Accept/edit writer fence reads current
cross-case corrections; resident replay validates current actor, owner and human
decision token. Unknown legacy source never gets a guessed hash.
Independent hazard intake still succeeds after correction, with the supplied
awareness instant normalized by the existing hazard contract, not reset.

Component guides, resident journey synthesis, KB index and append-only log
updated. No memory/original case study/regulatory snapshot modification, new
framework, workflow matrix or real inference. Changes artifact contains
intermediate failures and exact evidence pointers. Fresh complete current web
guidelines retrieved again immediately before original Review preparation.

Original Review subsequently executed once, preserving four Medium RV findings:
historical UI action cutoff (later implementation), independent raw-log access
gap (eligible evidence follow-up), other-assistant integration and qualified/
resident/live/native-specific acceptance. Its original file and verdict are
immutable. Parent freeze/gate is not a correction or second Review. P04 stays
unchecked in committed snapshot because the authoritative gate can only run
after this commit; final external receipt/handoff records actual results.
