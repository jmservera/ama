<!-- markdownlint-disable-file -->
# RPI Changes: PR 507 evidence corrections

## Metadata

Task ID/slug: pr507-evidence-corrections. Date: 2026-10-30.
Plan: .copilot-tracking/plans/2026-10-30/pr507-evidence-corrections-plan.md.
Details: .copilot-tracking/details/2026-10-30/pr507-evidence-corrections-phase-details.md.

## Execution Status

Complete; full plan P01/P02 and P01-T01/P02-T01/P02-T02 complete.
Write boundary: evidence pack, KB index/append-only log, new dated task evidence
and requested /tmp/pr507-body.md. No source, tests, guide, registry or scores.
No blockers to implementation. Original critique retained; PC-001 rejected
under confirmed caller paths, no repeated critique.

## Completed Work

### Evidence correction and replacement body

P01-T01 complete. Corrected stale test/fixture/guide prose and both acceptance
rows in the pack, with a dated original-versus-integrated boundary explanation.
Historical three-document frozen hash reproduced before edits, then explicitly
qualified as pre-correction. Original candidate's hash and different domain
retained separately. Named proposed later B6 PR with actual scored src README;
no fictitious number or score gain. Updated KB index and appended log.
Created /tmp/pr507-body.md including suggested documentation-only title;
owner applies it, no remote write. P02 validation complete below.

## Implementation-Time Plan and Detail Updates

No material divergence. Parent retains requested /tmp paths and isolates missing
test dependency outside shared venv, as recorded in critique disposition.
P02 current-state update: record actual focused adverse results, full inherited
reproduction, semantic checks and frozen body/source hashes. No tests added,
removed or repaired. Plan, details, markers and handoff now agree.

## Validation Record

All commands from repository root. Runner /tmp/mv/bin/python is Python 3.12.3.
External session root:
/home/azureuser/.copilot/session-state/cbeb6513-8cdf-4d52-a064-5adc86e8e3e9/files.
No shared venv mutation or application dependency change.

| Check / actual invocation | Result |
| --- | --- |
| `/tmp/mv/bin/python -m pytest --version` | Missing pytest, exit 1; establishes installation need |
| `/tmp/mv/bin/python -m pip install --quiet --target <session-root>/pr507-pytest pytest==8.3.5` | Passed; isolated missing test-tool dependency only |
| `PYTHONPATH=<session-root>/pr507-pytest /tmp/mv/bin/python -m pytest --version` | pytest 8.3.5 |
| `/tmp/mv/bin/python tools/rename-zava-tests.py` | Passed: 25 tests, 0.653s; expected broken-PPTX fixture diagnostic |
| `env -u GITHUB_OUTPUT /tmp/mv/bin/python .github/rubric/scripts/prepare.py decide --root . --base-ref ffd8f35e63b24905b9aeb937dbf2a7fe9968747f --event pull_request` | Passed: should_score=false, baseline_total=77, no scored artifact changed, empty changed_artifacts/removed_files/open_criteria |
| `PYTHONPATH=<session-root>/pr507-pytest /tmp/mv/bin/python -m pytest .github/rubric/scripts/test_prepare.py .github/rubric/scripts/test_gate.py -q -k 'registered_implementation_change or src_project_file or src_vendor_data_or_build_file or change_without_changed_evidence or closed_criterion or increase_citing_removed_file or unchanged_deck_slide_citation'` | Exit 1: 14 passed, 2 inherited failures, 84 deselected, 0.98s |
| `PYTHONPATH=<session-root>/pr507-pytest /tmp/mv/bin/python -m pytest .github/rubric/scripts -q -ra` | Exit 1: 355 passed, 18 failed, 7 skipped, 35.59s |
| `/tmp/mv/bin/python <session-root>/pr507-verify.py` | Passed; actual matcher/prepare, synthetic B6 gate contracts, original frozen hash, protected inputs/original artifacts, log prefix, PR-body requirements and 2 changed local links/anchors |
| `git diff --check`; `git diff --numstat`; `git rev-parse HEAD` | Passed; three docs only, starting HEAD unchanged pending local commit |

Focused failures: test_given_closed_criterion_when_agent_changes_it_then_carried_forward
and test_given_increase_citing_removed_file_when_evaluated_then_baseline_kept,
both mutable recorded-score assumptions. The focused command initially chained
the full suite with &&; its failure prevented that full invocation, so the
complete suite was subsequently run independently and logged.
Full suite adverse output: <session-root>/pr507-rubric-pytest.log.
Six mutable-score failures in test_gate, one mutable-score failure in
test_prepare, one deck-selection mismatch and ten workflow event/path failures.
Seven safe-output runtime cases skip because GH_AW_RUNTIME_DIR is absent.
This exactly reproduces the integrated 355/18/7 boundary; no green claim.

An initial inline validator failed while importing prepare's sibling
scorecard_adapter. The persisted validator adds the rubric script directory
to its import path, matching the existing test convention; rerun passed.
This is a validation harness correction, not an application/source change.
Actual B6 membership: src/README.md belongs only to solution-code and informs
B6; rubric guide and evidence pack belong to no artifact. Synthetic gate
checks reject guide citations, accept a hypothetical changed src README
citation for open B6, and preserve a closed B6. Synthetic 2-to-3 values are
contract checks, not a model score or edit to recorded scores.

No full API, browser/SQL/image suite, full publication gate, external legal
currentness, fresh hosted CI, scorer, cloud operation or private dataset read.

## Pre-Review Reconciliation

Plan/details/changes agree: all implementation markers complete; actual
adverse results and separate acceptance limitations remain explicit. Ready
for one independent Review. Parent owns later local commit and metadata.

Assessed immutable base: ffd8f35e63b24905b9aeb937dbf2a7fe9968747f.
Pre-commit HEAD: 254d2274693c8190f827067c3732e03d102a563d.
Frozen three-document diff (same paths as prior integrated boundary), computed
with `git diff BASE -- docs/architecture/cutover-evidence-pack.md docs/reference/README.md docs/reference/log.md`:
SHA-256 2f71a66c06ac5b7647a997f5f9a2a51301283f1a07a7306a225186cccc014fda.
External /tmp/pr507-body.md SHA-256:
bcd8e350ba2ded0eb912d35aaba4ebe145194ac1fdc72ac93c2293309eca221e.
Tracking-only lifecycle bookkeeping is outside the frozen documentation delta.
The external body carries the new corrected three-document hash; production
pack records the two immutable historical boundaries without self-reference.

## Blockers and Remaining Work

No active implementation remains. Inherited suite/runtime and historical acceptance are distinct
unmet evidence, not repaired or waived here. Publication gate not performed:
local-only commit, no push, no publication approval claim.

## Follow-Up Items

Proposed later B6 README PR; inherited rubric/runtime repairs; owner historical
#198 gaps; owner metadata application and coordinator publication gates.
Prior audit-path RV-001 is outside this task, unchanged.

## Return-to-Caller State

Full-loop execution Complete; sole independent Review Complete / Conformant.
Local correction committed and verified below; no push. The historical and
current Review outcomes remain separate from publication or whole-issue approval.

## Independent Review and Local Persistence Handoff

The sole independent Review executed Complete / Conformant, zero new RV
findings, in
.copilot-tracking/reviews/logs/2026-10-30/pr507-evidence-corrections-review.md.
Independent Git/content/hash/link/matcher/prepare checks passed. Reviewer could
not inspect the external body or raw test logs and assessed supplied evidence
for those; parent directly checked the body bytes/content and exact suite
output. This limitation is not a claim of independent external-byte inspection.
Original critique, original Reviews and prior routed audit finding remain
unchanged. No same-task implementation correction or repeat Review follows.

Parent lifecycle action: commit the three docs and seven task-owned artifacts,
using freshly authenticated repository-local noreply email for both author and
committer, Refs #198 and the required Copilot trailer. Then verify metadata,
clean status and frozen hashes. Final bookkeeping is tracking-only and does
not change the assessed docs/body. No push or remote metadata operation.

## Local Commit Results and Final State

| Action | Result |
| --- | --- |
| Fresh `gh api user` identity and repository-local `user.email` | Authenticated privacy-safe noreply address used for both author and committer |
| Explicit staging of three docs and seven task artifacts; `git diff --cached --check` | Passed; ten files only |
| `git commit` with subject `docs(rubric): correct PR 507 integrated evidence claims`, Refs #198 and required Copilot trailer | Created 7a6aabbbd2366904ae110cdf4fe49043e03df332 |
| `git log -1 --format=...`; `git status --short` | Correct subject, matching authenticated author/committer emails, required trailer; clean worktree |
| Post-commit `/tmp/mv/bin/python <session-root>/pr507-verify.py` | Passed; protected inputs/original artifacts and all semantic/link checks retained; exact frozen docs/body hashes unchanged |

This final tracking-only bookkeeping is persisted in a separate local
Conventional Commit with the same Refs #198 and trailer, without amending
history or changing the reviewed three-doc delta or external body. Its exact
SHA is canonical in Git, avoiding a self-referential commit claim.
The single bounded full-loop request is completed; manual mode, session stopped,
Follow-up, no child work selected. Owner applies /tmp/pr507-body.md and its
suggested title. Full publication gates and hosted acceptance remain separate;
no push, score edit, remote metadata update or issue acceptance performed.
