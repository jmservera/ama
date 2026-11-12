<!-- markdownlint-disable-file -->
# Research: accuracy follow-up for the post-153 checkpoint (2026-11-12)

* Task ID: `post153-integration-440-1112-accuracy`; parent `post153-integration-440-1112`; native session `d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b`; branch `docs/post153-integration-checkpoint-440-1112`, base commit `8bfd52729048bc7c94b4d266188307f1d9bc213c` (tree `5ea0ce16fa7f5b53d35a69a9064db9edb26a93d5`).
* Purpose: verify four factual claims named by the coordinator's independent read of the frozen diff (file `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/independent-post153-initial-1112.json`, DOC-1 to DOC-4) and decide the smallest documentation-only correction.
* Scope: documentation accuracy only. Non-goals: no product, test, tool, workflow, instruction, approval or requirement edit; no assistants.js fix; no new issue; no test rerun, browser, SQL, cloud, model or live call; no change to the 145 executed, 92 skipped counts or the `4074b44f3` source pin; the original seven artifacts, original review, original adverse critique and raw evidence stay byte-for-byte.
* Posture: `focused` (named claims, local git and GitHub merge metadata). Research disposition: `executed`. Waves ran inline (wider: all four claims and neighbouring claims in the same section; deeper: git objects and merge metadata; contrarian: whether each original statement could still be read as true). No worker was dispatched; one independent critique follows in the plan phase.
* Raw evidence (outside the repository): `/home/azureuser/.copilot/session-state/d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b/files/checkpoint-440-post153-1112-accuracy/` (`five-id-tracked-search.out`, `merge-times-and-counts.out`, `original-blobs-before.txt`).

## Findings

| ID | Claim in original | Evidence | Disposition |
| --- | --- | --- | --- |
| C1 / DOC-1 | Pack, five-home section: "No other public tracked file mentions the five ids." | `git grep -l -E <five ids> HEAD` returns three files: `docs/architecture/cutover-evidence-pack.md`, `docs/capstone/demo/runbook.md` and tracked `.copilot-tracking/research/2026-11-12/five-home-script-134-1112-research.md` (it holds a table with `ZF-2025-0355`, `ZF-2025-0382`, `ZF-2026-0829` and cites a generator under `support/`). The static script read only `runbook.md` and the source tree, so tracking files were outside its boundary. | Original statement is inaccurate. Correct to the real boundary: the string-level check read `runbook.md` and web source only; a tracked-file search finds one historical tracking record; that record and its generator replay were not reproduced or read here. No claim on deployed membership or nonexistence. |
| C2 / DOC-2 | Original research line 31: "plus 16 tracking files" for #1470; critique PC-007 says 19 and the plan records the correction as applied. | `git show --format= --name-only 088e8c3c0` lists 20 paths under `.copilot-tracking`; `38d3ed187` lists 7 (matches the research figure for #1475). | Both original counts are wrong (16 and 19); 20 is the observed count. PC-007 was not fully applied: the research count was left at 16. Originals are preserved; the accurate figure is recorded in the additive accuracy note only. The count is context and does not affect the evidence boundary (tracking files are not product source). |
| C3 / DOC-3 | Original research line 9: two inputs "merged after the previous #440 checkpoint (PR #1478 ...)". | `gh pr view`: #1470 merged 2026-11-12T17:38:13Z, #1475 17:46:55Z, #1478 18:00:25Z. So both merged before #1478. They followed the historical tested pin `bbb1d20cc` and were not in its 281-test wave. | Original wording is wrong about ordering. Correct reading: merged after the historical tested pin, before the #1478 publication, and excluded from the #1478 evidence. The pack section's opening ("after the previous checkpoint (PR 1478 ...) ... later-merged") needs the same qualification. The post-checkpoint base `4074b44f3` is unchanged. |
| C4 / DOC-4 | Pack F1: "ARIA 1.2 prohibits naming a role-less element ... possibly ignored by assistive technology." Original research line 59 repeats it. | No standard was fetched in the original run, and none is fetched here (no web review is authorised). Native elements carry implicit roles, and the generic role question for `pre` is not settled by repository evidence. The blanket claim is overbroad as stated. | Narrow F1 to what is observed: two `pre` elements carry `aria-label` and `tabindex="0"` with no explicit `role` (`assistants.js:103,133`), whereas the repository's focusable scroll areas for tables use `role="region"`. Whether an accessible name is exposed for a `pre` with an implicit generic role is unverified. No fetched-standard, fresh web review, assistive-technology observation, conformance or confirmed defect claim. Not fixed. |

## Contrarian wave

* C1: the original sentence might be read as "no other file in the public documentation tree"; the tracking file is a tracked public file, so the sentence still overstates. Kept as inaccurate.
* C2: 16 might count only changed non-log tracking files; no breakdown reproduces 16 or 19. Not credible; 20 is the plain count.
* C3: "after" might mean after the tested pin; the original text names #1478 explicitly, so it is wrong as written.
* C4: the original concern may still be valid for generic roles in some assistive-technology combinations; evidence is absent either way, so the concern is retained only as unverified.

## Unchanged by this follow-up

* 145 executed tests (19, 31, 95), 92 skipped, `node --check` exit 0, 7 of 7 origin hashes, and the `4074b44f3` pin.
* Requirement-qualified positive coverage remains partial (FR-036 not exercised). No invented mapping and no approval.
* Any proposed acceptance gate stays a proposal; it neither prohibits independent source work nor records an owner decision.

## Decisions and readiness

* Parent decision (from the user's direction): documentation-only corrections of exactly C1 to C4, additive artifacts, no edit of originals.
* Planning Readiness: `Ready`. Broader-scope gaps: none found. Further research: none.
