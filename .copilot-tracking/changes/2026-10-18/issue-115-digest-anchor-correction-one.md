---
title: Issue 115 digest anchor correction ONE
description: Coordinator adverse finding and bounded implementation receipt, not a new Review
ms.date: 2026-10-18
---

## Authority and Adverse Finding

Same task/session afd14196-e65e-4c89-b2cb-12c95fe860b4, same branch and PR404.
Correction ONE authorized on2026-10-18, maximum two total source corrections.
Starting head bbb13521dcdd8d7a760324619fc0f8f612f08ad6; exact base and remote
main c803614e8ca7c604e509f1c088f8b8f90f3063ef. Clean intake verified.

Coordinator independent complete16-path/13-artifact assessment: NOT ACCEPTED,
one Medium tightly coupled defect. Prefix-only recognition counts
digest-not-a-count.json with {} as a head, giving intact true, one digest,
LEDGER_DIGEST_OK/exit0. Original unrelated-only correction is insufficient.
Coordinator finding is supplied owner evidence, not a newly executed original
Review or an independently accepted correction. No new/amended Review allowed.

Frozen original critique:
d1add2a5642689cb9a615f3aaa989871a3b405f7f5cab076689fdcc0110314e0.
Frozen original Review:
dc72719806ba648af00d34c9ef6b0c0d049ed87372d60ee49e959b328694186e.
Both checked unchanged at intake; original positive source judgment is historical
and does not override coordinator NOT ACCEPTED.

## Existing Contract and Correction Boundary

Read actual ledger.make_digest/make_year_digest, read/write digest functions,
orchestrator publish/verify and existing fixtures. Publisher names head objects
with f"digest-{count:010d}.json" (minimum ten digits, not maximum); year objects
year-YYYY.json. Required verification invariants: mapping, integer count
(not bool; head nonnegative, year positive), SHA-256 lowercase hex head,
algorithm sha256, main chain for this publisher; year matches filename and
has SHA-256 first_prev. Empty head count0 must carry GENESIS. Head filename
must equal canonical formatting of payload count. Year is four ASCII digits
0001..9999; no new current-clock sealing restriction. Existing timestamp `at`
is provenance, not used by ledger verification, so not a new required timestamp
schema. Additional fields remain allowed for historical/forward compatibility.

Reject malformed prefixed name/payload explicitly with fixed diagnostics,
unsuccessful report and CLI ALERT/exit1. Do not silently ignore malformed
candidate evidence even beside a good anchor. Unrelated nonprefixed objects
remain ignored. No object delete/overwrite or policy changes; actual good
head/year history remains qualified. Invalid JSON gets a fixed, content-free
problem; transport failures retain existing availability error boundary.

## Execution Scope and Planned Evidence

Only correction P03 in existing plan/details, existing digest source/tests/README
and dated task receipts/state/PR body. New tests belong to existing fake suite;
original test methods/fake unchanged. Failing-first malformed-name and
valid-name bad-payload direct/CLI cases, valid controls and large-count naming
control, then local focused/coupled and full orchestrator/configured gates.
Use existing installed task venv, env -i and worktree .digest-anchor-tmp.
No private inputs/support/.env, Azure/IAM/Graph/spend/retention/deploy/services.
No issue/board writes, integration/rebase/force-push or new Review.

## Status

P03-T01 complete: chosen failing-first matrix ran3 methods,112 failures and30
errors at unchanged production SHA256
568e46a8963a274c1ee5a40bb27c6ab1fbe4c076057ea95b7b6068cde3159f1b.
Failures include actual true reports; errors are malformed data reaching
unguarded core .get/index/year/numeric operations or JSON reader, not setup.
Full output correction-one-before.log. No correction acceptance asserted.
Operational/retention/first-publication/human gates unchanged and unmet.

## Actual Implementation and Validation

Added four methods and one assertion helper in the existing fake suite; the
prior17 digest test methods and fake remain unchanged. The
four new methods bring digest coverage to21; coupled YearLedgerTests add4.
No existing method removed. Malformed candidates tested alone and beside a
genuinely valid prefix-head anchor, checking report, alert/status, absence of
OK/private sentinel/name output, no PUT/DELETE and byte-preserved remote objects.
Cases include canonical-name missing fields, bool/negative/fraction/string
counts, null/list/string bodies, invalid JSON/UTF-8, mismatched count/year
filenames, hash/chain/algorithm/year/first_prev and invalid zero-head GENESIS.
Extra metadata and absent informational at remain compatible. Eleven-digit
publisher count names qualify and reach normal truncation checking.

Implementation validates before core verification; invalid payloads never reach
unguarded core readers. InvalidDigestError is only the fixed JSON decode error,
caught specifically into `check=digests, problem=invalid remote digest anchor`.
Semantic failure follows the same fixed report path; invalid evidence is not
silently ignored even when another good anchor exists. Counts include qualified
anchors only. Transport DocumentStoreError still follows existing CLI
availability failure. No broad catch, fallback, schema migration or blob write.

Actual test runner prefix E (root cwd):

```bash
env -i PATH=/usr/bin:/bin TMPDIR=/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp PYTHONPATH=src/core/tests:src/orchestrator/tests /home/azureuser/.copilot/session-state/afd14196-e65e-4c89-b2cb-12c95fe860b4/files/digest-venv/bin/python
```

| Actual command (E expanded above) | Result and receipt |
| --- | --- |
| E -m unittest test_digest_blob.BlobDigestTests.test_malformed_prefixed_anchor_names_fail_closed test_digest_blob.BlobDigestTests.test_malformed_anchor_payloads_fail_closed test_digest_blob.BlobDigestTests.test_invalid_zero_head_is_not_an_anchor -q | Before edit exit1;3 methods,112 behavioral assertion failures and30 malformed-data errors; correction-one-before.log |
| E -m unittest test_digest_blob test_recovery.YearLedgerTests -v | After edit exit0;25 passed, zero errors/failures/skips; correction-one-focused.log |
| From src/orchestrator, same E with PYTHONPATH=../core/tests: -m unittest discover -s tests -q | Exit0;44 passed, zero errors/failures/skips; correction-one-orchestrator.log |
| From src/orchestrator: task-venv/bin/ruff check . && task-venv/bin/ruff format --check . && task-venv/bin/mypy | Exit0; All checks passed;9 files already formatted; no mypy issues in12 files; correction-one-quality.log |
| E stdin: compile git-show exact base then exact bbb13521 digest source into isolated in-memory modules; existing fake/fixture only | Both reproduce reported intactTrue/digests1/CLI0/OK; correction-one-probes.log |
| Same stdin: current malformed prefix, valid head name with {}, year name with {}, invalid JSON | All explicit invalid-anchor reports, qualified counts0, intactFalse/CLI1/ALERT/noOK; correction-one-probes.log |
| git diff --check | Exit0 |

No installation was needed: previously installed task-venv packages/tools were
available. Configured Ruff/mypy migration exemptions still apply to digest
source/test; passing configured gates is not strict typing/format coverage.
SQL Server/Docker/Azure/browser/services not run, N/A for this bounded offline
delta; existing SQLite unit coverage is not operational acceptance.

### Corrected Source and Receipt SHA-256

| File (source paths or adjacent receipt suffix) | SHA-256 |
| --- | --- |
| src/orchestrator/src/zava_forward/orchestrator/digest_blob.py | 9b684dd8828945903753ddcd8d6830dae46b91876a3fa2953a6a92adf44b8d0e |
| src/orchestrator/tests/test_digest_blob.py | ad79c4d64a637cacb1bb26aa498a04898f282e827295381712c23b4ca3e5a421 |
| src/orchestrator/README.md | e27e844e4f2a29ce89bd545d616b6dbb65a438681c1d4d2eb0b50e261488ec1f |
| correction-one-before.log | 5ea99c793ec979cff00a3201e070b03a3814a036bb961f60543a4839d8ccbe8e |
| correction-one-focused.log | 126580921ed24a1e27f79a59ffb0e033457cedb5760c6f591659619688a3a684 |
| correction-one-orchestrator.log | f65fa8f5519b7945b8afdce5077bf5e67290d5036558191997290c455913dcc1 |
| correction-one-probes.log | 20397106d912dc5726b8c3519a5c9cbb394c692052d549d233d833b3628cae7c |
| correction-one-quality.log | 0f343a3c5f6774fb1ec8317f69d48a8e255054cb7b2feada73bf2666f251b007 |

Frozen originals match intake hashes after validation. Coordinator adverse
NOT ACCEPTED is retained; this receipt is implementation evidence only, not
a new/amended Review or artificial Pass. Same coordinator must adjudicate
corrected exact final head. Main still pinned; gh api user freshly resolved
8036360/jmservera for local noreply author/committer. Normal same-branch push
and PR404 update authorized, no integration or issue/board writes.

## Actual Publication and Same-Coordinator Handoff

Correction ONE source/receipt commit:
`d0088301ba64cba8c632b6d0b4dcd80474580e41`.
Normal `git push origin fix/digest-anchor-evidence-115` succeeded, moving remote
bbb13521 to d0088301. Remote main checked immediately before push remains exact
base c803614e8ca7c604e509f1c088f8b8f90f3063ef. No integration authorized or done.
PR404 remains the same delivery surface. Final evidence-only commit containing
this publication receipt has its exact head recorded in live PR metadata/body
and final handoff rather than recursively embedded in its own bytes.

Full correction changed boundary relative to bbb13521 (15 paths):

* src/orchestrator/src/zava_forward/orchestrator/digest_blob.py
* src/orchestrator/tests/test_digest_blob.py
* src/orchestrator/README.md
* .copilot-tracking/plans/2026-10-18/issue-115-digest-anchor-plan.md
* .copilot-tracking/details/2026-10-18/issue-115-digest-anchor-phase-details.md
* .copilot-tracking/rpi-sessions/2026-10-18/issue-115-digest-anchor-state.json
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-changes.md
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-delivery.md
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-pr-body.md
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-correction-one.md
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-correction-one-before.log
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-correction-one-focused.log
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-correction-one-orchestrator.log
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-correction-one-quality.log
* .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-correction-one-probes.log

Original research, critique, Review and initial validation logs untouched.
Task fixture root confirmed empty and removed with rmdir. No new dependencies
or services. All tests/logs are constructed public fixtures; no private input or
environment/secret reads. Fresh gh identity8036360/jmservera and local noreply
used for both author and committer, required Copilot trailer included.

Correction ONE implementation/publication complete, not coordinator accepted.
Coordinator's NOT ACCEPTED remains recorded, awaiting SAME reviewer's exact
corrected-head follow-up. Original Revise critique and Residual work Review stay
byte-exact at frozen hashes above; no new/amended Review or self-issued Pass.
Operational/legal/resident/retention/lock/scheduled-monitoring/recovery and
initial-history approval gates remain unmet; no whole115/114 closure.
