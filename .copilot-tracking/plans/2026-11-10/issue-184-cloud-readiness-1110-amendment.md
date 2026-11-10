<!-- markdownlint-disable-file -->
# Issue 184 cloud-readiness: pre-implementation amendment (2026-11-10, Refs #184 #440)

Appended after the original research, plan, details and critique (witness seq 1 to 3, commit `dff226f8`), which are unchanged. This amendment is disclosed before `implement-start`.

## Plan and target amendments

* Shared-file dependency re-evaluated by Root. The 108 author is finished and frozen at `f241a3681eadd7ffb78e35cfd8184d1086976e59`; only independent review remains and there is no concurrent KB writer. Original plan Phase 1 ("wait for 108 merge or no-KB-change disposition") is superseded by Root's written local declared-stack admission in the 2026-11-10 resume instruction.
* Local declared stack: an ordinary merge (no rebase, no rewrite) of the exact local `docs/demo-model-metadata-108-1110` at `f241a3681` into the 184 topic. Both parent 108 commits (`272899349`, `f241a3681`) and the original stage commit `dff226f8` are ancestors of the result. Planned PR target is initially that parent topic; the parent targets `main`. No push, PR, remote or board write has occurred.
* If the parent merges first, Root explicitly re-evaluates target `main` after an ordinary merge of `origin/main` and a fresh exact-head review. This task does not retarget silently and does not claim the parent merged. If parent review requires changes, this candidate waits for Root's updated parent reconciliation and discards neither branch.
* Ownership: the 108 AI Tokenomics index row and its log entries are immutable here. 184 owns only the IoT synthesis subsection, its per-file index row clause, the "For #110/#184" paragraph sentences and its own appended log entry.
* Detail correction: the original details targeted the existing README "For #110/#184" paragraph and the existing per-file row; unchanged. The parent 108 README change touches only the AI Tokenomics row (verified by diff), so there is no overlap.

## Stale-history corrections (before any KB record)

* The original research called the linked #440 sensor checkpoint "local-only and qualified" with "publication HOLD". Per Root's 2026-11-10 coordinator statement, PR 1412 is MERGED (`0da7b8573`) and the current `179c23` canonical chain verified clean (7 records, verify 0, independent readiness 0); only the older `806` and `c218` chains are qualified. There is no current `179` HOLD. This task did not re-run those verifications; the figures are Root-reported, with the chain evidence held externally by Root.
* Quality PRs 1331 and 1336 were already merged on 2026-11-09; no new Quality campaign is implied here. PR 1414 merged as `b23c08e33` on current `origin/main` (2026-11-10T17:58:44Z) and carries no IoT runtime change; it is not merged into this topic.
* Original wording in the research file is retained as history and superseded by this section.

## Unchanged boundaries

* Only the five dated ARM configuration reads from 17:54Z (budget 5 of 8, no retry) are used. No further Azure query is made, even though three of eight are unspent; no model, transport, device, job or cloud write; no runtime gate, source, infra or test change; no source-cycle grant.
* `job-live-simulator` and `job-live-receiver` returned `ResourceNotFound` for those exact names only. This is not proof that no other job, deployed reader or scheduler exists. Actual job identity, runtime flow and image-to-build mapping stay UNKNOWN; absence is not inferred.
* No new billable operation is requested. Existing Azure costs are NOT measured; this does not say all costs are zero.
* No live, model, transport, serving, role, budget or whole #184, #110, #140 or #440 acceptance. All four criteria sets stay OPEN.
