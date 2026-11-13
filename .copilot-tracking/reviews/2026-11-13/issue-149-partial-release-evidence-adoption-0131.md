---
title: Issue 149 partial UX release evidence adoption and input-proof record (0131)
description: Final evidence assembly for the bounded partial independent UX release at source head 288b6a376, covering Review adoption, provenance complements, metadata input proof, issue 153 input and supersession notes
ms.date: 2026-11-13
---

## Status and boundary

This is a metadata record, not a new Review, not a Pass, not a finished RPI, not an independent exact-head assessment, not publication readiness and not a hosted result. It continues the existing issue 149 Implement/Review evidence handoff (task `issue-149-independent-ux-0042`, parent `issue-149-parent-plan-2333`). No source, test, tool, workflow, infrastructure, manifest or README file changed. No new plan, implementation, correction, allowance, issue or tick is created.

* Source head under evidence: `288b6a37665602718122ed0ab35b9bbdcca963ed`, `src` tree `6915b96c8ededf363b76c8fb4700153eb18ff588`. Checkpoint candidate before this record: `37e2715b5175cce0c5470904817fd69ea5eea5eb` (same `src` tree).
* Main: `origin/main` fetched read-only equals `c401e5d56446b5752e8d91af6a45f3f06269c4bd` (expected). No merge, rebase or other movement.
* Entire 233 feature: excluded and held, neither admitted nor deferred. Five correction cycles spent, the typing-only extension is unavailable and that is no approval. C3 (96) has three of five cycles spent, two left, not renewed. No approved 233 deferral, requirement relaxation or pivot exists.

## Adopted original Review

The original final Review `rpi-149-original-review-0104` is adopted as an immutable, Partial-execution original result, not upgraded and not replaced.

* Execution: Partial (full source, test and check reading; relevant RPI bodies sampled; long table cells truncated). Executed once, 2026-11-13.
* Outcome: conformant within the bounded partial source, test and check scope. No Critical, High or Medium finding. Five Low observations RV-L1 to RV-L5 stay open and routed to later work.
* Tracked public copy: `.copilot-tracking/reviews/2026-11-13/issue-149-original-review-0104-public-technical-copy.md` with the result `issue-149-original-review-0104-result-public-technical-copy.json`. These are labelled derivatives, not verbatim copies and not newly executed Reviews. SHA256 of the privately retained original report: `ad5a288ac821f434833926eed5d09df131106e4ea19ba5d52bcb20e501e72128`; of the original result JSON: `c20ed63138a1e1c99ebdcb7935d64e6ba3aefdbd87d48d6a8a805e1ed784814d`. The original bytes are preserved outside the repository.
* Privacy-only omissions: three passages of private operational handling text (one Execution bullet, two sentences in one validation table cell, one Routing bullet) and the matching result-JSON field. Each is replaced by an explicit marker. No source, test, check, finding, outcome, read-manifest or qualification text is removed.
* Source conformance and documentation coverage are separate. The original Review's source reading is not widened by the complements below.

## Provenance complements (0122)

Two distinct missing-evidence complements read the relevant child RPI bodies and public documentation that the original Review had sampled. Both are Partial by their own status and both exclude scope assigned to the other. Neither makes the original Review complete. Records are copied unchanged:

* Core complement: `issue-149-provenance-core-0122-result.json`. Read in full the relevant research, plan, details, changes, Review, critique and state bodies for 74, 82 (three tasks), 176 and 216 and the parent lineage. No Critical, High or Medium finding. Lows and informational items PV-1 to PV-10, including: commit history cannot prove prospective critique order for 74, 176, 216 and original 82 (self-reported); 176 and 216 have no standalone critique file; 74 and 176 negative controls are not reproducible tracked output; a 176 as-of control wording discrepancy; plan checkbox drift; mixed review independence. Residuals: raw runner logs summarised by grep only, the 74 evidence directory not opened by that complement, the 0048 and 0042 state files not read in full, about 150 other tracking files out of its portion.
* UX complement: `issue-149-provenance-ux-0122-result.json` and `issue-149-provenance-ux-0122-review.md`. Read in full the RPI chains for 96 backend, 96 UI, 96 C3, 215, 134 and 156, the seven changed documentation hunks with complete table cells, the 0048 plan with amendment 0055 and critique and state, and the 0042 changes and state. No Critical, High or Medium finding. Lows PV-L1 to PV-L6 and D-L1, D-L2, including: 96 backend 2236 plan, critique and Review are author-only (disclosed); unticked plan phase markers; fixes applied after the single Review without re-review; `role-screens.js` `TextDecoder` without `ignoreBOM` so a README phrase does not hold for a byte-order-mark file; a stale 0048 state marker; two log formatting and qualifier observations. Residuals: parent 2333 bodies and policy amendment A1 to A4 not read there, 74, 82, 176, 216 and 153 families out of its portion, hosted CI and GitHub issue states not read.
* These lows (including the BOM stripping, the unverified 176 as-of mutation, stale markers, author-only 96 original and the 134 ordering and amend-after-Review observations) stay OPEN and disclosed. No optional source repair is made and none consumes a correction cycle.
* Independent critic and reviewer launches are shown by actual native phase-log markers: 74 (lines 351 and 952), 176 (186 and 343), 216 (182 and 292) and original 82 (254 and 787). The 74 critique Verdict was Revise before implementation (log lines 349 to 384). Single-commit chronology still cannot prove ordering for those tasks (PV-1 remains) and this is not tamper-proof attestation. Model labels are launcher-asserted.
* 74 mutation and adverse outputs were read directly by the coordinator: M1 to M8 and A1 to A4 failed the intended document, quality and system assertions; A2 rejected a missing restriction key and is not a pure amount-only control; the final 74 browser check passed 24; the first M8 run used invalid JavaScript and timed out at login, which is not a valid discriminatory result, and the later M8 run failed the intended ZF-3 system assertion. All earlier adverse and cumulative qualifications are preserved.

## Metadata input proof (0125)

`issue-149-metadata-inputs-0125-result.json` is copied unchanged. It binds candidate `37e2715b5` (not any later head).

* Result PARTIAL-SUPPORTED: for every observed lane, no test, lint or type input actually read differs between `288b6a376` and `37e2715b5`. Exactly three metadata files differ (the pack, the 0042 changes and the 0042 state). The lanes' archives included those files, so the proof rests on showing no lane selector, import, helper or configuration reads them, not on whole-archive equality.
* Documentation inputs actually read by lanes and pinned unchanged: design system, atlas screen trace, runbook, the PRD, the synthetic pack and generator, `.gitignore`.
* Core 72 is REUSED from d790 with exactly three historic inputs unchanged (`src/core` tree, `src/README.md`, `README.md`); it is not a fresh observation.
* Dynamic and transitive-read caveats and the unselected readers of the changed pack remain (for example `test_live_doc_links`, not in any lane). No blanket new documentation or full-gate campaign is adopted: documentation needs no executable gate, and this record applies a focused Markdown, link, table, JSON and diff review only. No failed applicable check is waived.
* The final independent assessor must recheck the actual new metadata paths against the input manifest, a clean final head and current main. The tracked files added here sit under `.copilot-tracking/reviews/2026-11-13/`; only fixtures in `tools/test_rpi_phase_witness.py` and `.github/rubric/scripts/test_safe_output_runtime.py` mention that directory, and neither was in a lane.

## 216 law-link coexistence

The 216 law-link test-only content and its six tracking artifacts are already on actual main via merge `e05606413` and squash `e44de171e` (PR 1495). They are not a child introduced by this branch. The original child commit `e4aac8b72` is not an ancestor of the head or of main because of the squash. The fresh integrated 216 run (`issue-149-216-integrated-validation-0117-result.json`, `test_regulatory_chat_api` 12 of 12, exit 0, no skips, single pass) proves coexistence on the integrated head only, not child introduction, and not 216 criteria.

## Issue 153 employee-denial-copy race: read as input

Both complements excluded this family. The complete main-relative set was read here: the nine tracked paths with prefix `employee-denial-copy-153-1112` (the earlier NOT_READY research and state, and the race research, plan, critique, details, changes, Review and state).

* Content: the earlier research traced one action and found reason, owner and next action present for the safety-stop denial (NOT_READY research-only). The race continuation reproduced a stale-stage `400` with no owner or next action, and changed the single `Store.advance` message and added `test_stale_advance_refusal_names_case_owner_and_next_action`. One independent critique (one blocking and two non-blocking, applied) and one Review (approve, zero blocking, text-only) are recorded. Criteria 2, universal 3 and 5 of issue 153 stay unproven and unticked. The records disclose non-repository browser evidence under `/tmp`, an overwritten first missing-Playwright output, truncated check transcripts, and plan checkboxes left unticked.
* Lineage at this head: the 153 candidate `c358dd675` is not an ancestor of the head or of main. Its content arrived through the UX-parent squash `8f8be74e1` (PR 1487), which is an ancestor of the head and not of main. All nine tracked 153 paths have identical blobs at `c358dd675`, `8f8be74e1` and the head. The two source files equal the candidate blobs at `8f8be74e1`; at the head they differ only by later UX-parent changes (the test file has 24 further insertions, `store.py` carries the later strict funding reader). The `store.py` stale-stage message and the new test are present at the head.
* Per-input independent Pass, retained from root records and not repeated here: the original independent assessment `issue-149-153-independent-final-1112.json` returned functional approve with exact-head readiness Deferred; the bounded closure `issue-149-153-independent-closure-1112.json` returned Pass for candidate `c358dd675` (tree `47f5a94ed`) against target `43b2187b9`, with pinned execution (72 tests, configured ruff and mypy) and `issue-149-153157-provenance-2228.json` binding head, tree, clean status and a clean merge-tree. That Pass is per input and bound to that head and target. It does not automatically assess this head or this branch, and the 157 entry in the provenance file is not part of this release.
* No source review, test or check was repeated for 153.

## Historical blockers and stale markers: supersession

The 0048 state file lists blockers `roles-failures`, `validators-incomplete`, `publication-gates` and `c3-candidate`, and the 0042 state lists `validation-pending` and a pending Review. These are historical records of earlier points and are not edited. Current facts: the C3 candidate was integrated (M0 `d4f0c92fc`, M1 `b705b61f1`); the role lane failures at `9085e85c6` are history and the role lane passed 21 at `288b6a376`; all executed validation lanes passed on actual results; the original Review has an actual outcome and is adopted here as above. The current 0042 state is authoritative. The original critique files and child state history are not rewritten.

## Remaining gates and unproven items

* Final independent exact-head assessment of the final local candidate (not performed here).
* Current-main applicability at assessment time, and publication authority with `Refs`-only closing hygiene (no close, fix or resolve keyword even negated, empty closing references before and after any body edit, #83 verified open). The historical commit `8307d2580` hazard remains.
* Actual hosted checks for the exact head. An absent, skipped or path-filtered workflow is not success.
* Unproven and unticked: human and assistive-technology acceptance, Finance and numeric-fidelity decision, legal review, live operation, actual SQL Server, whole issue 149, A2 cut line, epic. Classification stays focused-tier and must be reassessed by the independent assessor; doubt takes the full tier.
* Not claimed: RPI fully accepted, fresh validation of the final head, publication readiness. No push, pull request, merge, issue action or approval is made.
