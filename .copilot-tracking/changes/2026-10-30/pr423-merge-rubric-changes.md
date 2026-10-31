<!-- markdownlint-disable-file -->
# RPI Changes: PR423 merge and rubric diagnosis

## Metadata

* Task ID: pr423-merge-rubric-2026-10-30
* Date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/pr423-merge-rubric-plan.md
* Details: .copilot-tracking/details/2026-10-30/pr423-merge-rubric-phase-details.md
* Original head: 4696866850f230238617c95b0dbd4297f7e8b245
* Reviewed main: 5634f9a077d175a931c15e3400114665d8c071ee

## Execution Status

Full-plan local execution complete: P01/P02 and all task markers complete,
including the attempted full gate. Original independent Review Complete /
Residual work is preserved. Full-gate acceptance/publication remains Blocked.
No source edits before Research and Plan/critique completed.

## Execution Summary

Local-only merge, exact D1 regression and honest evidence navigation.
No Azure, deploy, private data, live sign-in, warming or push.

## Conflict Resolution and Two-Parent Preservation Ledger

| Conflict | Resolution and reason |
| --- | --- |
| docs/architecture/cutover-evidence-pack.md | Keep main's 2026-10-30 ms.date and both auto-merged bodies, including transport failures/Blob decision and later cut-over/identity records |
| docs/reference/README.md | Keep latest date plus useful overview topic and both bodies; add current transport/rubric pointer |
| docs/reference/log.md | Remove only markers, retaining both appended entry ranges in order; append the new entry after both |
| tools/rpi-checks.py | Retain main's runner and other workflow fingerprints plus Blob lint/type entries; recompute actual combined src-ci.yml SHA256 0594da63fac922b15020a45f1263a8bc7a0aa43cb505592c6f66177b5b3cb63c |

Two-parent content inspection, not ancestry alone:

* All five workflow hashes match actual files. Combined src-ci contains main's
  added checks and Blob lint/format/mypy targets. No check names changed.
* Main's role matrix and tests retain dedicated IoT sender/receiver scopes,
  while branch's private container-only Blob writer, lifecycle, controller,
  worker, .dockerignore and Dockerfile remain. No restored tags permission.
* Main's complete 4,123 pre-existing tracking blobs remain byte-identical.
  Of original head's 3,002 tracking blobs, 2,998 are byte-identical, including
  every PR423 RPI artifact and original adverse outcome. The other four are
  pre-existing main corrections to two architecture-refresh notes-association
  CSVs and cowork-cost-recovery native-navigation/native-text-bounds JSON.
  They equal main byte for byte; their earlier versions remain in the original
  parent history. This merge creates no new historical-evidence rewrite.
* Both complete parent log bodies survive as ordered line subsequences.
  Frontmatter uses the current date; both conflicting append sequences remain.
* No path is deleted relative to main. The sole deletion relative to original
  branch head is main's already-authorized mvp/README.md retirement, retained
  rather than recreating retired code. Transport helpers belong in infra;
  SQL import is already the installed zava_forward.core namespace.
* Four old main tag-specific test names are replaced by branch's Blob
  corruption/preflight/paging/worker tests; same-VNet and cleanup behavior
  remain covered. This is the intended DN1-DN2 channel replacement, not deleted
  validation. Four original-head IoT static test names are replaced by main's
  compiled/mutation suite. All these differences predate this integration;
  no new test is removed here.
* DN1 maps to private Blob discovery/write-only role and no-tag regression;
  DN2 to BlobCodecTests size/page/count/expiry validation; DN3 to retained
  unknown historical failures and no resource-deletion authority; DN4 to
  unchanged app-role/manual production authority; DN5 to retained controlled
  worker checks and explicitly deferred signed attestation. All five remain
  in the infra README decision table.

P01-T02 adds two exact D1 evidence2 parameter cases in the existing adapter
and actual jq-preflight tests, with existing valid controls retained. No
scorer, rubric, registry, prompt, generated lock or score changed. The infra
evidence/rationale/change_reason map and dated-expiry qualification improve
engineering traceability, not the submitted tool payload. Evidence pack,
rubric README and KB index/log record the same honest boundary.

## Rubric Cause, Changes and Remaining Work

The last run failed **before any score was recorded**. Actual fallback
`safeoutputs.jsonl` from run 40556907743 contains D1 keys `change_reason`,
`evidence`, `rationale`, **plus `evidence2`**. The error is not proof of a
missing field in project documentation. The adapter requires exactly three
keys for all 20 criteria, including closed ones.

Original submission replay: valid false, passed false, same exact D1 error,
baseline 77, no total. Diagnostic in-memory removal of only `evidence2`:
valid true, passed true, total 77 versus 77, floors met. Not a new assessment,
not a recorded/published score, no score files changed by this task.

Only infrastructure criteria A1/A3/A5 were open, already 5/5. Current main's
77 baseline has B3/B4/B5/C2 = 2 and D1/D2/D3 = 4/3/2. Evidence improvements
cannot honestly raise already-ceiling open scores or change closed dimensions.
Section D is substantive thought leadership, editing/publish readiness and
actual dissemination, not this transport proposal. Actual timed demo/recovery,
Q&A/listening evidence, author-resolved manuscript readiness and real
submission/publication evidence are separate future work, not fabricated here.

Existing workflow requires template-derived 22 flat string arguments, 20
scores "1"-"5", JSON-encoded details with all exact criterion/field keys,
evidence array, nonblank short rationale and change_reason string (empty when
unchanged), validated with jq before the one accepted output. The current
preflight already rejects extra keys. No adapter relaxation or workflow rewrite
is warranted. Hosted agent compliance still requires a fresh run after the
coordinator publishes; this work neither reruns nor claims a hosted pass.

## Implementation-Time Plan and Detail Updates

Critique executed once, original Revise retained. PC-001 preservation ledger
and PC-003 blocker classification applied. PC-002 rejected: its asserted
parent runtime /tmp prohibition is absent, so it cannot establish a blocker.
Normal local gate remains required; no broad tooling change or bypass.

## Validation Record

| Check | Result | Evidence |
| --- | --- | --- |
| Initial infrastructure discovery | Failed prerequisites | Namespace not installed, 10 import/startup errors; no source workaround |
| Restored infrastructure discovery | Passed | Installed all five src dev distributions in task-owned external venv; REQUIRE_AZ_BICEP=1; 498 tests, zero skips |
| Rubric adapter/gate/prepare/record-workflow | 350 passed, 8 failed | Exact D1 regressions passed; main archive independently reproduces same eight failures with 348 passed |
| Main rubric baseline comparison | Inherited debt | Six old 66-point fixture assumptions, one retired-deck selection expectation and one deleted-BRD 64-point expectation; no new failures |
| Local gate orchestration | Passed | 31 tests, including matrix drift and failure/receipt contracts; printed injected failures are expected test stimuli |
| Migration regressions | Passed after dependency restore | Initial missing pptx/PIL; restored tools/rename-zava-requirements.txt in external venv; 25 tests |
| Namespace | Passed | Installed five-distribution namespace has five paths, no init file; core SQL/API auth import |
| Transport/gate Ruff and format | Passed | Seven files |
| Transport mypy / strict gate mypy | Passed | Four and two files respectively |
| Native actionlint | Passed after corrected invocation | Existing infra/tests/actionlint.yaml supplies custom runner labels; all five native workflows pass |
| Exact adapter/preflight suite | Passed | 51 tests, including two new D1 cases and unchanged valid-card controls |
| Focused Git diff whitespace | Passed | Current task/integration surfaces against main pass; no conflict markers |
| Whole staged merge whitespace | Failed, inherited | Original main tracking whitespace retained byte-identical; not a clean whole-index check (RV-003) |
| New documentation links | Passed | New single-line relative links and heading anchors verified in four changed guides |
| First full local gate | Blocked before checks | Candidate f74b270d: ignored task-generated caches/metadata; no receipt |
| Clean full local gate retry | Blocked before checks | Candidate f74b270d: Global heavy-resource lock timeout after 600 seconds; no receipt, no pass |
| Local commit identity/ancestry | Passed | f74b270d7cd370173272b801ff3a93b434b37262 has both pinned parents; author/committer 8036360+jmservera@users.noreply.github.com, required Copilot trailer and Refs #360 |

## Pre-Review Reconciliation

Original independent Review executed once: Complete, outcome Residual work;
full-task execution Partial at the intentionally pre-commit boundary.
No new scoped implementation defect identified. Independent content/hash/
schema/preflight checks support AC2-AC4; final commit and gate remain P02-T02.
The original Review is preserved, not repeated or promoted to acceptance.

| Finding | Disposition | Remaining requirement |
| --- | --- | --- |
| RV-001 High | Commit/ancestry/identity completed; gate still blocked | Actual clean full-gate attempt timed out on shared lock; no publication pass inferred |
| RV-002 Medium | Deferred inherited rubric maintenance | Same eight failures reproduced on unchanged main; separate follow-up, not repaired by this task |
| RV-003 Low | Qualified, original finding preserved | Focused whitespace passes; whole staged merge contains byte-identical historical main whitespace and is not clean |

## Blockers

RV-001: full-gate evidence unavailable because the shared heavy-resource lock
timed out after 600 seconds. Do not remove/bypass that lock or interfere with
other tasks. Coordinator must run a new full gate on the final clean commit,
verify a successful receipt against current reviewed main, and obtain the
separate exact-head/hosted/human assessments. No publication is performed here.

## Remaining Work

No remaining implementation markers. Full-gate acceptance is blocked, not
silently treated as passing; separate coordinator publication work remains.

## Local Commits and External Evidence

2026-10-31 integrated-candidate qualification (PR #423, Refs #360):
the historical run9 receipt and `f30d9583`/`b4d467ca` provenance are not
VERIFIED evidence for the candidate integrating main
`ec2d784255c3377ab39e5d2d1b5140e76c8e7f36`. No successful full-gate receipt
exists for this integrated candidate. The earlier failed gate attempts below
remain historical; they are not a new gate run or current exact-head success.
The owner retains the PR description edit; it was not changed by this task.

The two-parent merge is f74b270d7cd370173272b801ff3a93b434b37262.
This subsequent evidence-only commit records actual gate outcomes and current
state; it does not change source or the original critique/Review. It invalidates
any earlier candidate receipt in principle; no successful receipt exists here.
A final exact-head retry uses a new external directory and a finite lock wait;
its console is retained beside the earlier adverse attempts.

External root:
`/home/azureuser/.copilot/session-state/d04ece3f-6926-4a9f-96ce-ecc3975fc9db/files/`.

* `pr423-gate-initial-console.log`: ignored-input refusal.
* `pr423-gate-clean-console.log`: actual 600-second lock timeout.
* `validation-generated-inputs/manifest.json`, `archive/` and
  `restore-selected/`: exact finite selection of 163 task-generated cache/
  metadata files in 16 directories; full restore/readback hashes verified before
  externalization. No historical tracking output or private dataset selected.
* `rubric-tests.log` and `rubric-main-tests.log`: 350/8 versus 348/8.
* Saved run context and fallback output remain external with hashes in Research.
* `index-whitespace.log`: preserved whole-index inherited whitespace failure.

No Azure activity, warming, live sign-in, push or other worktree access occurred.

## Follow-Up Items

Ranked current follow-ups:

1. Coordinator full exact-head gate after shared-lock availability: highest
   priority because RV-001 blocks publication, despite completed local repair.
2. Separate rubric fixture/registry maintenance: eight inherited failures
   reproduced on main; bounded quality improvement without grade manipulation.
3. Authorized real transport validation and actual pitch/dissemination evidence:
   larger operational/human work, never inferred from offline infrastructure.

Fresh hosted rubric and exact-head assessment belong to coordinator after
push. No child follow-up is selected or started in this non-interactive task.
