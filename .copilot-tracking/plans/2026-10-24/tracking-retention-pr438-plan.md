<!-- markdownlint-disable-file -->
# Tracking Retention and PR 438 Plan

## Task Metadata
Task ID: tracking-retention-pr438
Date: 2026-10-24
Branch: docs/capstone-cowork-story (owner selected)
Status: Complete locally after one independent implementation review; outcome Conformant. No publication requested.

## Executive Summary
Fix PR 438's remaining actionable feedback, preserve reusable build sources and unique evidence, and reduce generated tracking clutter without losing the current deck, recovered cost workings or historical review provenance. Create and verify a reversible external archive before any deletion. Keep original unknown/active RPI records until retention is demonstrably safe.

### What You May Not Know
Today's untracked slide-build directory is not recoverable from Git. The native builder currently depends on its original baseline. Some docs link directly to original reports, and old append-only log entries must not be rewritten during relocation. This work does not authorize publication or change review/approval gates.

## Sources
.copilot-tracking/research/2026-10-24/tracking-retention-pr438-research.md
PR 438 unresolved review threads retrieved 2026-10-24.
.github/copilot-instructions.md
src/README.md, Local RPI gate.

## User Decisions and Requirements
* Execute all three accepted retention recommendations.
* Continue on the current branch; preserve the untracked slide-build work while migrating it.
* Review and fix unresolved PR 438 comments; verify apparent existing fixes before resolving threads.
* Preserve the AI/works/conditional-grant calculations or recalculate from explicit inputs with their caveats.
* No commit, push, merge, remote issue changes, deployment or private-data access.

## Goals
* Make durable sources/evidence discoverable outside scratch tracking.
* Remove only archived, verified redundant/generated artifacts.
* Prevent recurring generated-output accumulation through a documented retention policy.

## Scope and Non-Goals
In scope: tracking presentation outputs, reusable builder inputs, directly referenced unique reports, affected links, retention guidance, scoped PR fixes and tests. Out of scope: mass deletion of original unknown-active RPI history, source application refactoring, legal/Finance approval, primary-price research, Git history rewriting and publication.

## Functional Requirements
* Maintain source/main-v2 authority distinction and require external native inputs for v2 editing.
* Produce an external archive with checksummed inventory and successful readback before deletion.
* Keep reusable builder and baseline access functional after promotion.
* Preserve original reports, source dates, adverse findings, current deck/notes/actions and all cost guards.
* Preserve historical references by relocation mapping and compatibility pointers where immutable logs require them.

## Non-Functional Requirements
* Small focused edits; no silent overwrites or unrelated user changes.
* No live cloud work, private data, credentials or approval claims.
* Evidence-backed retention and reversible cleanup; no broad wildcard deletion.

## Acceptance Criteria
* Every unresolved review thread has validated correction or a documented evidence-based disposition.
* Current 54-slide PPTX/PDF bytes and the cost check remain valid unless a separate reviewed correction requires changing them.
* Every removed/moved path has a verified archive or preserved canonical replacement; archive receipt records SHA-256 and path inventory.
* Reusable native-slide tooling operates from durable sources; linked unique evidence remains accessible.
* Selected generated files are removed, with before/after count/size reported.
* Retention guidance distinguishes active work, durable sources, generated output and original review evidence.
* Relevant focused tests, link checks, archive verification and independent review are recorded. Publication remains blocked until separately requested complete gates.

## Phase Checklist
<!-- rpi:phase id=P01 -->
### [x] P01: PR review corrections
<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Correct handoff inputs and authority; existing reset/navigation/registry corrections inspected. Twenty-four source tests and three size cases pass; final matrix also includes three exact-registry cases and native labels.
<!-- rpi:phase id=P02 -->
### [x] P02: Preserve and inventory
<!-- rpi:task id=P02-T01 -->
* [x] P02-T01: Created verified owner-only external archive, exact115-path manifest and successful external restore proof; 37 safety tests pass.
<!-- rpi:phase id=P03 -->
### [x] P03: Promote and prune
<!-- rpi:task id=P03-T01 -->
* [x] P03-T01: Promoted builder/manifest/pinnedbaseline/buildnarrative and exactly12 report copies; active links repaired and original log prefix preserved.
<!-- rpi:task id=P03-T02 -->
* [x] P03-T02: Exactly115 paths /26,219,104bytes pruned with verified archive/restore and removal journal. Policy and discoverability installed; all89currentbuildfiles retained.
<!-- rpi:phase id=P04 -->
### [x] P04: Validate and review
<!-- rpi:task id=P04-T01 -->
* [x] P04-T01: Independent review Complete/Conformant;67tests,archive/restore/journal/exactprotectedbytes,promotedcopies/nativepackages and859linkschecked. No new material findings. Latestreceiptthread staysopenpendingpublication.

## Validation Ownership and Change Limits
Reuse docs/capstone/pitch/cowork-main-presentation/test_build_assets.py, existing rubric tests and suitable tools tests. Add at most one cleanup-specific test module if required for the archive/manifest mechanism; no new application dependencies or frameworks. No canonical deck bytes removed. Lock exact removals in a generated inventory before cleanup implementation, and preserve all unmapped original sources. Native build promotion requires a baseline-aware regression/check. Execute the complete publication gate only as a separate authorized publication workflow; no claim of clean final receipt here.

## Locked Execution Contract
* Exact removals: preservation research D2's 113 older image paths plus D1a/D1b's two duplicate PPTX paths, exactly 115 regular files / 26,219,104 logical bytes. Expand those finite lists into a hash-bound manifest; reject missing, additional, changed or symlink paths. No new removal discovery. D1c/D1d and all 89 current build entries remain intact after migration. Every other pre-existing tracking entry remains byte-identical.
* Additions: at most tools/tracking_retention.py and tools/test_tracking_retention.py; tools/cowork-native-recovery/Invoke-Recovery.ps1 and content/recovery.json; one preserved PPTX baseline under docs/capstone/pitch/cowork-main-presentation/native-recovery/baseline/original.pptx; one unchanged build narrative; exactly the research's 12 unchanged assurance-report copies; compact receipt/removal manifest and retention/README/index/log guidance. Do not add another durable original PDF.
* Archive: unique owner-only external directory under ~/.local/share/ama/tracking-archives/2026-10-24-pr438-<unique>/. Inventory complete tracking file/link types without following symlinks; refuse unreadable/special/changing entries. Preserve link identity without opening targets. Full inventory/receipt stays external, SHA-256 bound to archive bytes and each member. Verify complete readback, then restore all 115 selected paths into empty isolated external scratch and compare hashes. Refuse traversal, symlink escape and overwrite. Recheck the entire set before deleting any file, then each file immediately before removal; record each actual removal for interruption/recovery. Tampering, missing member, drift or failed tests blocks pruning.
* Native promotion: resolve manifest from PSScriptRoot; require one external OutputDir for Build/Verify/Render. Preserve original baseline SHA-256 d41acc969efb1687cfdd0103b753a62ea697005652760b1579a8e6de955cf447 and reject missing/wrong baseline before output; remove canonical-delivery fallback. Each Build starts from original. Compare two independently built candidates by ZIP member sets/bytes, not ZIP order. Only six slides/six notes differ from original; 54 slides/54 nonempty notes/27 caller actions; no duplicate 70001. Keep canonical PPTX hash 39659a3ad9974f802a8418177a9ca0ca8daf7478e71cd82d04cd7677d9ad2cc0 and PDF hash b816f3f2282ffad4e0afd41cc39ba76a6871bc62c2292c5a62129a4864bd9a9c. Native Render is conditional on real Windows COM; report Not run if unavailable, no false visual acceptance.
* Reports/links: copy exactly the 12-file research map with siblings and unchanged bytes; retain originals and embedded original paths. Copy build narrative unchanged. Update four active capstone backlinks and active index/PRD/addendum references. Never rewrite historical log prefix. The 24 external file targets and one directory remain accessible; references to removed images become explicitly archive-backed with exact member restore map, not blanket link exclusions.
* Final matrix: all24 source tests; six rubric cases using -k 'deck_size_override or cowork_registry'; --check-only --check-pptx on canonical and promoted candidate; archive tamper/missing/drift/out-of-set/unsafe-link/overwrite/partial failure tests; real snapshot/restore proof; source-copy hash/link/fragment checks; two native Builds/Verify; canonical hash and all-unremoved-tracking-byte comparison after prune. Record Pass/Fail/Blocked/Not run separately. Required archive and Build/Verify failures stop deletion. Complete publication gate is Not run on dirty uncommitted nonpublication input, not a passing receipt.
* PR threads: verified existing published reset/navigation/registry/native-label fixes may be resolved only with evidence; the new local handoff correction remains unresolved until publication. No commit/push authorization is inferred. Preserve original imported handoffs and review findings.
* Policy: discoverable docs/reference/method/tracking-retention-policy.md plus root tracking README and existing repo guidance pointer. Preserve current original-review and publication-gate requirements. No age-based, unreferenced-file or automatic historical deletion authority. Durable sources and input baselines stay separate from regenerable outputs.

## Critique Disposition
One independent critique executed at .copilot-tracking/reviews/plans/2026-10-24/tracking-retention-pr438-plan-critique.md; original Revise verdict retained. PC-001 through PC-007 accepted as planner-owned corrections, all resolved by the Locked Execution Contract above and corresponding detail tasks. No new owner decision, second critique or scope expansion. P01's local formatting-sensitive prose test was repaired and the same focused tests rerun successfully.

## Current Implementation Evidence
* Archive: ~/.local/share/ama/tracking-archives/2026-10-24-pr438-hex6oe57/tracking.tar.gz; SHA25606e9c007eaad0d3c9d30eb885176ceae87902cda51ec14130550c7be5a9a5f05. Full2420files/600dirs snapshot verified. Restore115selected members passed before pruning; journalrecords115actualremovals.
* tools/tracking_retention.py and tools/test_tracking_retention.py:37tests. Source/handoff suite24tests; sixregistrycases. Full archive+protected snapshot comparison passed independently after pruning. These three currenttaskplan/details/changes records are now intentionally updated AFTER that proof; no older source/evidence changes are permitted or concealed.
* docs/reference/resources/tracking-retention-promotion.json records exactcopies, two nativeBuild/Verify runs, missing/wrongbaseline refusal,54nonemptynotes/54slides/27actions/single70001, nativePowerPointCOM54pagePDF+18nonblankpreviews,unchangedcanonicalhashes.
* NetGitvisiblecheckout decrease23,341,236bytes/95files atP03; tracking57,757,533bytes/2306files before currentphase-record updates. Externalarchive growslocalstorage; noGit-historyshrinkingclaim.
* RefreshedPRstate already had reset/navigation/handoff threads resolved externally. Three remaining publishedfix threads (registry,size/nativeLIVElabels/testselection) resolved after verifying sixregistrycases/nativepackage. New missingreceipt thread PRRT_kwDOUU8JX86v3Wki remains open pending publication; localdurablenarrative/validationreceipt plus allfour evidencecustody links addressit. No commit/push.
* Nine inheritedbrokenlinkoccurrences recorded bypromotionreceipt; no new unexplainedlinks. CurrentmainPowerPoint/PDFbytes unchanged; costs retained. No fullpublicationgate or independentacceptance yet.

## Follow-Up Items
* Separate owner-authorized publication: commit through existing identity/conventions, run complete exact-head local gate, independent/hosted checks, then push and reassess remaining receipt thread. No authority inferred here.
* Transfer/verify the owner-local archive to an approved durable store if cross-machine or longer retention is needed. The compact manifest alone does not restore bytes.
* Existing presentation/Finance/funder/current-price/human acceptance gates remain separate; no new delivery authority or wholehistoricalRPIcleanupscope.

## Handoff
All local phases complete; review .copilot-tracking/reviews/logs/2026-10-24/tracking-retention-pr438-review.md records Complete/Conformant with no new material findings. Discover completed with the three separate follow-ups above. Leave localreceiptfixthread unresolved until publication; no commit/push/fullgate claimed.
