---
title: Setup API selection changes
description: Source, regression and publication evidence for issue 360
ms.date: 2026-10-17
---

## Scope and Status

Full approved plan setup-api-selection-360, P01-T01 active. Research complete,
Plan Ready after one independent critique PC001-003 accepted/resolved directly.
No implementation review yet. Worktree source startd11c273, mainbbbc924 ancestor.

## Boundaries

Only safe compatibility selection/read-only guard and related tests/runbook/KB.
No live setup/private SQL/Graph/secret/cloud mutation. Historical ACR receipt,
prior review, sourcebab4bf3 and current integration heads remain distinct.

## P01-T01: Red-first regressions

Baseline setup101 passed under system Python. New actual deployed-pair test
failed twice with exact owner's ambiguity message; mixed modern/legacy direct
pool test failed because no refusal. Staff test initially could not import
zava_forward; created .venv and pip installed editable core/agents/api/orchestrator
only after missing-import failure. Real central guard test then failed six
check/list-staff payload/execute subcases as expected (dry-run already guarded).
Five new test methods total, no removals. No source edit before red captures.

## P01-T02: Implementation

Explicit ingress tag filter now supports absent-modern-role/workloadapi and
rejects conflicting modern role. Direct-pool cardinality before generic chooser
prevents mixed tag generation tie-break; exact override bypasses preference.
Central azure_staff refuses check/dry-run/list-staff before request payload or
execute; mutation-mode check operation unaffected. Green validation pending.

## P01-T03: Validation and documentation

Green combined command from infra/tests:
`../../.venv/bin/python -m unittest test_setup_entra test_staff_azure test_initialize_api_auth -q`
passed164 (104 setup,43 staff,17 legacy). Compileall passed. Ruff0.17.1 F-only
setup/script test; full existing E/F/I/B/UP staff-test lint/format passed.
Mypy2.4.0 `--follow-imports=silent --ignore-missing-imports infra/scripts/setup-entra.py`
passed. Tools installed via pip into task-local .venv after missing-tool errors.
Initial new callback closure lint warning corrected; an overbroad patch briefly
changed the pre-existing callback and caused NameError, immediately restored
with exact method context; final combined164 green. No test removed.

Runbook explains actual tag mismatch, safe compatibility, direct ambiguity and
exact override. Active check/list-staff advice corrected to private-host path;
KB route/log updated, documentation skill session recorded. Git diff whitespace
and five changed relative links passed; eight prior ACR artifacts/JSON exact
bytes retained and prior owned log is byte prefix.

## P02: Integration and Review preparation

Initial main bbbc924 was ancestor. Later prefix validation detected shared
origin/main advance; fresh fetch confirmed d400eb8d1d0d6567445b0fc11803260eab897a65
(#383 finance), no changes to selected infra source/tests. Do not claim fresh
main log prefix yet: authorized owned-topic rebase required. Commit current
owned work first, integrate while clean, preserve upstream full log prefix plus
all own appends and routes; exact old remote lease d11c273eb744c440965375c3638583565b28db6c.
Review/publication pending; prior ACR single Review remains residual, not rerun.

Authorized integration completed: source/evidence committed423f9193, clean rebase
onto verified d400eb8. Only conflict docs/reference/log.md in oldest ACR evidence
commit; resolved by retaining full upstream finance append then all own entries.
Four owned commits replayed, integration source head
f48cc9b4661f3375110a96b66829eb5678d32057. No source conflict/mutation in integration.
Eight prior ACR artifact bytes unchanged; fresh main log is exact prefix and
entire owned423f9193 suffix after bbbc924 is exact suffix. Upstream #84/#94 index
rows retained. All JSON parses. Full combined164 and scoped lint/format/mypy/
compile repeated after integration and passed. Original ACR recipe/sourcebab4bf3,
retained base/payload hashes and adverse/residual Review unchanged.

Reviewed-source candidate fingerprints SHA256:

| Path | SHA256 |
| --- | --- |
| infra/scripts/setup-entra.py | 8cf36e2d01d19c8b94cca0dcda9f6105bcaf14471eead977dc3ed4e961f060bb |
| infra/tests/test_setup_entra.py | 9bf651ef1eab149b0e90a58a8e5823c6cd0a27570abf7a8bd98ea8558b16f9fb |
| infra/tests/test_staff_azure.py | 626a78dc1144cc3bed8cf23ac317daa937ee2f79ba6a85f4d74d4a8f78504c1f |

P01 complete; P02-T01 ready for the one independent NEW task Review. This
review does not revisit or upgrade prior ACR delivery/acceptance conclusions.

## P02-T01: Single independent Review

Complete / Residual work. Reviewer found bounded selection/no-write implementation
conformant, no defects or unresolved decision; zero correction cycles used.
Independently checked current fingerprints, test inventory (five additions/no
removals), syntax, nine central guard mode/operation combinations, upstream
ancestry/log prefix and eight original ACR artifact byte parity. Reviewer
assessed parent164 test/lint/type receipts, did not claim a separate full rerun.
RV001 real operator/live acceptance, RV002 exact-image publication/smoke/pin,
RV003 later old-stack retirement remain outside active work. d/e UNMET.
One new Review is committed with all new phase artifacts before first push.

## P02-T02: Publication readiness

Fresh gh api user8036360/jmservera, repository-local privacy-safe author/committer
8036360+jmservera@users.noreply.github.com, required Copilot trailer. Existing
PR385 OPEN/main, remote stilld11c273eb744c440965375c3638583565b28db6c. Authorized
rebase requires that exact topic-only lease; no force to main, no merge/close.
Push/PR body update and confirmed clean-head handoff pending.

## Verified Publication and Final Handoff

Review/metadata commit03d90083447fbbb71d48ecc0413235561c9b0ff5 pushed successfully
with exact expected remote d11c273eb744c440965375c3638583565b28db6c on owned topic
only. gh pr edit updated385 title to
"fix(infra): select configured demo API and retain ACR publication evidence";
PR readback confirms OPEN/main and exact matching head03d90083. Body contains
new full RPI/checks/artifact links and preserved explicitly historical ACR evidence.
No closing reference. Original ACR artifacts unchanged; original historical source
bab4bf3 remains distinct from new reviewed setup sourcef48cc9b and main d400eb8.
Final completion-only metadata commit follows with ordinary push and unchanged
reviewed executable bytes; final exact head will be reported from PR readback.

P01 and P02 active tasks complete, no review correction needed. Task-owned
.venv cleanup after all validation; no private data or unrelated cleanup.
No Azure writes in this diagnosis/setup continuation: no build, initializer
update/start, SQL/Graph/private-data/secret payload, API restart, IAM/network/
public/bypass/new pool/infrastructure/resource-group/teardown operation.
Old API/edge and ama retained. Exact-image smoke/pin and genuine runtime
browser/role/SQL/AI acceptance remain unperformed, issue360 d/e UNMET.
No merge/close. External coordinator final-head gate and owner merge decision
remain separate. Resume69875c40-cceb-4bdf-aece-bee3304c45b5.

## Coordinator Integration Recheck (2026-10-17)

New explicit coordinator instruction after completed publication: integrate only
this run-owned #360 topic onto latest fetched main, preserve upstream finance/
stock/procurement transaction protections and historical evidence. Clean
`git status --short`, branch fix/initializer-acr-cli-360 and local/remote head
1fdcdd3de5a55fdda0a3b55831118741bfdf47a6 verified before integration.
`git fetch origin` returned main d400eb8d1d0d6567445b0fc11803260eab897a65,
already an ancestor from the preceding authorized integration.
`GIT_EDITOR=true git rebase origin/main` reported "Current branch
fix/initializer-acr-cli-360 is up to date." Head unchanged; no replay/conflict.

Bounded byte checks passed: all326 upstream src/infra files identical to main
except the existing infra guide and three already independently reviewed setup
files; those three match reviewed source f48cc9b exactly. This includes unchanged
finance/stock SQL save hooks, staged-state/current-actor protections and
procurement dependency/quota/source guards. Full upstream KB log remains exact
prefix, upstream #84/#94 and own #360 routes retained. Eight original ACR phase
artifacts, including command receipt and original Review, are byte-identical to
d11c273; actual ACR sourcebab4bf3 is unchanged, not relabeled to main or new head.
Task JSON parses and whitespace checks passed. No source change, so no broad
suite or actual MSSQL repeat; prior164 offline tests remain historical reviewed
source validation, not a new runtime/transaction or independent Pass.

This integration recheck changes tracking/PR evidence only. Fresh gh api user
8036360/jmservera and privacy-safe local author/committer/trailer required.
Expected remote head1fdcdd3de5a55fdda0a3b55831118741bfdf47a6 recorded; no rewritten
history occurred, so ordinary descendant push is sufficient (no force required).
PR385 remains open/main; external coordinator final-head gate pending.
No new RPI/Review/correction, merge/closure/cloud write. Image smoke/pin and
real operator/runtime criteria d/e remain unmet.

## Coordinator Integration After PR384 (2026-10-17)

Explicit authorization scoped to run-owned fix/initializer-acr-cli-360/PR385,
input reviewed/expected remote head25f3d0ff3abbfe2ba76864d397441291694ec732.
Clean status and matching local/remote/PR head verified; `git fetch origin`
confirmed latest main b5d4c8402692758bd929a7ff9bf1832770738346 (merged PR384).
`GIT_EDITOR=true git rebase b5d4c8402692758bd929a7ff9bf1832770738346`
replayed seven owned commits. Only conflict was docs/reference/log.md in oldest
ACR evidence commit; retained entire upstream prefix then every owned append,
no blind ours/theirs. `git add docs/reference/log.md` and
`GIT_EDITOR=true git rebase --continue` completed. Integrated pre-receipt head
27383faa4108b9b8c1bce0e76326e8f8544c5153, no production/test conflict or mutation.

Exact binary/full-index source/test patch comparison:
`git diff --binary --full-index d400eb8 25f3d0ff -- src infra :(exclude)infra/README.md`
equals corresponding b5d4c840-to-integrated-head diff byte for byte: 12867bytes,
SHA256 f46873f5e3263d7a3bec32aba8447c8d892d8c021318b5c8db084de7372dc155.
All328 upstream src/infra files outside the existing guide and three reviewed
setup files match new main exactly; three setup files match reviewed25f3d0ff.
Thus upstream procurement dependency/quota/source and finance/stock SQL-save/
current-actor/staged-state protections retained, no unrelated edits.

All16 existing both-task RPI artifacts byte-identical at integration, including
both original single Reviews and original ACR receipt/sourcebab4bf3. Only this
new setup Changes/state append is subsequently updated for publication receipt;
neither original Review nor ACR artifact changes. Main KB log exact prefix and
entire own suffix exact; #84/#90/#94 and own #360 index routes preserved. JSON
parse and whitespace checks passed. Minimal changed-document links checked
at publication. No source change, so no full suite/MSSQL repeat; previous164
offline passes are historical validation of identical reviewed source, not a
new independent Pass or live acceptance. Coordinator review of25f3d0ff is
running separately; byte parity supplied for its applicability, verdict not inferred.

Fresh gh user8036360/jmservera, local privacy-safe author/committer and Copilot
trailer. Exact expected-remote lease25f3d0ff3abbfe2ba76864d397441291694ec732
authorized ONLY topic for this rebase. Integration receipt commit and PR body
update follow; final exact pushed head obtained by remote/PR readback. No main
rewrite, merge/close, Azure action/build/pin/start/SQL/Graph/secret/restart/
IAM/network/public/bypass/infrastructure/teardown. d/e still unmet.
