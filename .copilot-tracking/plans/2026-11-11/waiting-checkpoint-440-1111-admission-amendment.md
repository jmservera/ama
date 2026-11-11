---
title: Root admission of the handoff waiting integrated-main checkpoint
ms.date: 2026-11-11
---

## Admission and provenance

The coordinator admits only the planned focused observation and in-place documentation, not product changes, fixes, acceptance, publication or issue closure.

* PR #1444 actually squash-merged on 2026-11-11 at 09:02:15 UTC as `ef3e00ad05a78c3a0fd3b342b860fb3d43796223`.
* Fresh `origin/main` is that merge. Its root tree `513c3f9d8f7ae7c0c78672aa9f1650e23f7451cd` exactly equals the independently assessed and tested candidate `441fd7edf8597972f79c8100caafc39d9afcd844` and the coordinator's pre-merge prediction. Its `src` tree is `f82975dfc345f1a3705d62e08819383f6dd7bfd5`. No intervening main movement occurred.
* All 19 reported PR contexts passed when freshly checked before merge, including actual API (18m33s), MSSQL and rubric 78 versus baseline 78. Source CI run `42989184094`; scorer run `42989184013`. Earlier failed run `42984858029` remains historical adverse evidence, not an unchanged rerun.
* Independent exact-head assessment of `441fd7edf` read all 21 actual changed paths and approved with zero functional findings. Git/test attestation was coordinator provenance, not reviewer execution. The squash has a new commit identity but identical complete tree; do not claim the reviewer independently assessed the new squash SHA.
* Main's scorer run `42991793134` was actually observed in progress. No Source CI run on that main SHA was observed. Neither is called passing. Root explicitly permits this local-only observation while main scoring is pending, because the exact integrated tree passed the PR gates. This does not permit publication, downstream source admission or acceptance on red/missing required evidence.
* Original planning's UNPUBLISHED/UNMERGED descriptions of `441fd7edf` remain dated planning history. The feature is now integrated through `ef3e00ad`; do not present its old exclusion as the current state.
* Issue #83 remains open, no closing references, criterion 3 unticked pending OD-09 approved times and operational acceptance. Source-reference drift and PRD FR-066/AC-120 gaps remain recorded, not corrected.
* Issue #153's planning head `99f01d7` remains unimplemented/unmerged. Issue #521's independent fixture-only candidate `1587f4baa` is also excluded from this pin.

## Admitted commands and bounded amendments

The coordinator's actual candidate command, from `src/api`, was:

```bash
ZF_BROWSER_TESTS=1 PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests:tests \
python3 -m unittest -q test_accessibility_baseline test_handoff_waiting_view \
test_unaccepted_handoff_download_ui test_handoff_read_guidance test_handoff_api \
test_role_endpoint_inventory test_workbench test_role_screens
```

It ran 81 tests in 33.360 seconds with zero skips. Node syntax, configured Ruff check and mypy passed. Baseline-test formatting drift was separately disclosed as pre-existing, not passed.

For this checkpoint use the planned individual W4-W8 and W2/W3/W1 selectors, once each, on the pinned integrated main. Counts differ from the coordinator command because the plan includes CSV API tests and selects only WorkbenchNavigation rather than all role screens; report actual module/count mapping, not a manufactured reconciliation. W9 is NOT admitted. S1 is admitted only using existing Node/Ruff; no tool installation solely for S1.

* Commit this admission before any test, then ordinarily merge the pinned main into the planning branch. Preserve history and verify product/document trees equal the pin before canonical edits.
* W1 and W3 take their own nonqueued heavy lock: no outer lock for those modules.
* W2 takes no internal lock. Root amends the plan's preflight-only arrangement: acquire and hold the shared nonqueued lock **around W2 only**, with actual-holder verification and memory headroom. A prior free-lock probe alone is not protection against another user's concurrent admission. Never wrap W1/W3 or the complete combined selection in that outer lock.
* Prefer existing installed tools with explicit worktree source imports. Restore a private environment only after an actual missing-import/tool result; no global installs, uv, image pull, service/scanner installation or shared-cache mutation.
* Use an owned isolated HOME and existing browser cache explicitly, without reading the actual default/private dataset. No package install is authorized merely to normalize the environment.
* A missing prerequisite, busy lock, unexpected skip or failure preserves raw evidence and stops only the affected surface; no source correction, new issue, automatic retry or full-gate fallback.

## Output and resume boundary

Append the single dated checkpoint section to the existing cut-over pack, the append-only log entry and only a necessary existing index pointer, followed by genuine changes and original Review artifacts. Keep proposed/draft documents and ADR 0007 status unchanged. Raw results remain local; persist concise lasting findings and exact commands in the canonical record.

Return a clean frozen local candidate for independent exact-head review. Do not push, open a PR, alter issue criteria/board or admit #153 source. Root will consume the actual recommendation and main scoring before deciding that next admission. No historical Quality campaign, new correction allowance, production approval or acceptance is granted.
