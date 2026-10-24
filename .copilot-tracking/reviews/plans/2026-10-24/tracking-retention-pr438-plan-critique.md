<!-- markdownlint-disable-file -->
# Tracking Retention PR 438 Plan Critique

## Metadata

* Task ID: tracking-retention-pr438
* Critique date: 2026-10-24
* Plan: .copilot-tracking/plans/2026-10-24/tracking-retention-pr438-plan.md
* Phase details: .copilot-tracking/details/2026-10-24/tracking-retention-pr438-phase-details.md
* Critique execution status: Complete
* Verdict: Revise
* Severity counts: Critical 0; High 4; Medium 3; Low 0

## Inputs and Criterion Boundary

The bounded assessment uses the supplied plan, phase details, primary research
and preservation report, together with the caller's latest decisions. The
latest decisions outrank provisional choices in those documents. Findings
identify corrections to the written execution contract, not missing owner
approval for already settled choices.

Evidence inputs:

* .copilot-tracking/plans/2026-10-24/tracking-retention-pr438-plan.md
* .copilot-tracking/details/2026-10-24/tracking-retention-pr438-phase-details.md
* .copilot-tracking/research/2026-10-24/tracking-retention-pr438-research.md
* .copilot-tracking/research/subagents/2026-10-24/tracking-retention-pr438-preservation-research.md
* Caller requirements in this dispatch, including locked deletion scope,
  promotion limits, archive destination, native reproduction and validation.

The criterion boundary covers requirements, research conclusions, P01-P04,
task dependencies, preservation, rollback, acceptance evidence and authority.
No implementation, report contents, PR state or test result was independently
revalidated beyond the supplied evidence. Read-only branch/status inspection
confirmed docs/capstone-cowork-story with existing local edits to the two
handoff documents and test_build_assets.py, plus untracked tracking inputs.
The caller reports P01 passing 24 tests and three registry cases; that is
reported local evidence, not a fresh test run or published correction.

Current controlling decisions:

* Exactly D2's 113 older images plus D1a/D1b may be pruned: 115 files and
  26,219,104 logical bytes. Preserve every other existing tracking entry,
  including all 89 current build files, D1c/D1d, original baselines, current
  21 previews, mentor YAML, editable images and adverse RPI evidence.
* Copy the native script/manifest, pinned original PPTX baseline, durable
  cost/build narrative and at most the specified 12 assurance reports.
  Original PDF receives no new durable repository copy; its external archive
  preservation does not authorize deleting its existing tracking source.
* The archive defaults to ~/.local/share/ama/tracking-archives/2026-10-24-pr438-<unique>/,
  outside Git and owner-only. Full receipt stays external; a compact repository
  manifest/receipt maps the 115 removed paths to recoverable archive members.
* No source-original replacement, mass historical cleanup, secret/private-data
  reads, new branches, commits, pushes, merges or remote issue changes.
  Verified existing published PR fixes may have threads resolved. The local
  handoff fix remains pending publication unless separately justified.
* Complete publication gates cannot be claimed on dirty uncommitted input.
  Native Render is conditional on the actual Windows prerequisite; native
  Build/Verify and canonical hash guards are required local checks.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P01-T01; research C5/C6 | Partial | Existing/local distinction is recognized, but exact thread disposition and test evidence need to be recorded; PC-007. |
| P02-T01; preservation D1/D2 | Partial | Finite inventory exists in research, but the plan still opens selection; PC-001. |
| P02-T01; archive and rollback | Partial | External readback is required, but drift, restore safety and failure behavior lack acceptance checks; PC-002. |
| P03-T01; native promotion map | Partial | Durable ownership is chosen; pinned baseline and output isolation are not executable requirements; PC-003. |
| P03-T01; 12-report dependency closure | Partial | Coherent bundle is enumerated in research; source-byte retention and link dispositions remain optional in the plan; PC-004. |
| P03-T02; retention guidance | Partial | Gates are protected in principle; installation, destinations and prohibition on automatic historical pruning need definition; PC-006. |
| P04-T01; costs, native package, tests and links | Partial | Broad checks exist but do not bind the requested matrix and failure handling; PC-005. |
| P04-T01; review and publication boundary | Covered | No publication authorization or clean final receipt is inferred; retain this boundary. |
| Research C1/C2; preservation count scenarios | Partial | Historical counts are qualified, but final accounting must use the locked 115-only scenario; PC-001. |

## Verdict

Revise. The preservation research provides enough evidence to finalize a
credible bounded plan. The current plan/details are earlier, permissive drafts:
they leave destructive selection open and omit several safeguards already
specified by the caller or established by the supplied report. These are
direct planner corrections. No significant or divergent user decision is
currently necessary, and no additional critique cycle is requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Bind pruning and additions to the settled finite scope

* Related IDs: P02-T01, P03-T01, P03-T02; preservation D1/D2 and Explicit Exclusions.
* Evidence: The plan status says final selection is pending; its handoff calls
  for finalizing a manifest, while the research still offers 115- and 117-file
  scenarios and an optional durable original PDF. The caller has settled those choices.
* Concern: An implementor can legitimately follow an obsolete option, promote
  an extra PDF, replace retained sources with pointers, or treat successful
  native migration as authority to delete D1c/D1d or other current build files.
* Impact: Destruction or additional durable artifacts can exceed the approved
  boundary even while satisfying the plan's generic acceptance criteria.
* Smallest useful change: Make exact set equality to D2 plus D1a/D1b a P02/P03
  prerequisite. Expand the report's finite names once into an allowlist with
  sizes/hashes; require 115 unique regular-file paths and 26,219,104 bytes.
  Reject extra, missing or changed entries, never discover additional pruning
  candidates dynamically. Record the approved addition map: the two optional
  tracking-retention tool/test files, native script and manifest, one PPTX
  baseline, narrative copy, no more than the enumerated 12 reports, compact
  manifest/receipt and retention/README/index/log guidance. Preserve all other
  existing content, including all 89 current build files after migration.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02/P03 and acceptance criteria cite the
  locked set, exclusions and destination map; implementation acceptance compares
  actual deletion paths/count/bytes to that allowlist and verifies every other
  pre-existing tracking path/content remains. Use fresh counts and distinguish
  gross pruning from copies/additions and external archive storage; do not claim
  Git history shrinkage or reuse the report's five-file-promotion net estimate.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Make verified snapshot and safe rollback prerequisites to pruning

* Related IDs: P02-T01, P03-T02, P04-T01; preservation Proposed Validation steps 1 and 7.
* Evidence: P02 requires all existing tracking entries archived, owner-only
  storage, inventory readback and no symlink following. It does not define
  archive identity, pre-delete drift checks, restoration safety or interruption.
* Concern: A valid archive checksum alone does not prove complete recovery of
  the selected paths, protection of untracked evidence or safe extraction.
  Concurrent edits after snapshot can make even a correct archive stale.
* Impact: Pruning can lose newer bytes, omit unique adverse images, overwrite
  unrelated restoration targets or leave an unaccounted partially pruned state.
* Smallest useful change: Specify a unique external root resolved outside the
  repository, owner-only directories/files and no silent archive overwrite.
  Inventory types without following symlinks; preserve links without opening
  their targets and never prune them. Stop on unreadable, special, changing or
  unsafe entries rather than silently skipping them or reading private paths.
  Bind the full external receipt and compact restore map to the archive SHA-256,
  per-file SHA-256 and member identities. Verify full readback before deletion,
  rehearse exact relative-path restoration into isolated external scratch, and
  recheck the whole selected set before pruning plus each entry at removal.
  Define fail-closed behavior and an actual-removed-path record for interruption;
  restoration must refuse path traversal, symlink escape and unrelated overwrites.
* Action owner: Planning parent; implementation owner executes the checks.
* Exact resolving evidence: P02/P03 name positive snapshot/readback/restore tests
  and negative tests for tampering, missing members, source drift, out-of-set
  deletion, unsafe paths/symlinks, overwrite and partial-failure recovery. A real
  external full inventory/readback receipt covers the pre-prune snapshot; restore
  proof covers selected bytes, including older contact/full-size images and both
  duplicate decks. Any failed prerequisite leaves affected files unpruned.
* Decision route: Direct planner correction; the default archive location and
  approved set need no renewed owner selection.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Turn native reproduction recommendations into fail-closed tasks

* Related IDs: P03-T01, P04-T01; preservation Native Promotion Map.
* Evidence: The report identifies canonical-copy fallback as unsafe because
  the delivered deck is already patched and slide 32 adds shape 70001. Details
  currently ask only for promotion and a baseline-aware regression/check. The
  report permits tracking outputs; the caller now requires outputs outside Git.
* Concern: Moving the script without explicit path and baseline changes can
  rebuild from the patched delivery, add duplicate objects or keep Verify
  reading the old candidate, falsely validating the migration.
* Impact: The durable tool may not reproduce the intended native package and
  can contaminate canonical delivery or newly promoted input directories.
* Smallest useful change: Name the durable script/manifest and baseline paths.
  Pin original.pptx to d41acc969efb1687cfdd0103b753a62ea697005652760b1579a8e6de955cf447;
  remove delivery fallback and fail before output on missing/wrong input.
  Resolve manifest relative to the script, keep RepoRoot explicit, and require
  one shared external OutputDir for Build/Verify/Render. Each Build starts from
  the pinned original. Retain the old script and all current build evidence.
* Action owner: Planning parent; native-tool implementation owner.
* Exact resolving evidence: Two Builds into separate external directories,
  followed by Verify using the new paths, compare ZIP member-name sets and
  per-member bytes rather than archive ordering. Only six selected slide parts
  and their six notes may differ from baseline; unchanged parts, relationships,
  order, media and timing remain intact. Both candidates have 54 slides,
  54 nonempty notes, 27 Last Slide Viewed actions and no duplicate 70001.
  Missing/wrong-baseline tests fail before candidate creation; canonical PPTX/PDF
  hashes remain D1c/D1d's supplied hashes. Render uses the adapted candidate only
  when real Windows COM is available, otherwise records Not run and its reason.
* Decision route: Direct planner correction; unavailable Render is a reported
  limitation, not authority to remove additional outputs or claim visual acceptance.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Preserve source bytes and distinguish active links from archived evidence

* Related IDs: P03-T01, P03-T02, P04-T01; research C3; preservation Minimal Assurance and PRD Promotion and Immutable Log Compatibility.
* Evidence: The plan permits compatibility pointers and calls paths moved;
  the report instead specifies 12 exact byte-preserved copies with sibling
  dependencies and retention of originals. D2 includes images cited by retained
  historical handovers and publication evidence.
* Concern: Replacing originals or editing copied reports to repair paths loses
  byte identity, embedded original-path provenance, anchors or original adverse
  outcomes. Conversely, claiming every historical local link still resolves
  after removing D2 conceals its new archive dependency.
* Impact: Historical reviews become misleading or inaccessible despite a
  nominally successful document migration and superficial Markdown check.
* Smallest useful change: Adopt the report's exact 12-file copy map, retain all
  original report/payload bytes and fragments, and record both source/destination
  hashes. Do not insert pointers over originals. Copy the dated build/cost
  narrative while retaining its original; update the four active capstone
  backlinks and active reference-index/PRD/ADR links to durable destinations.
  Keep append-only historical log entries byte-identical, adding only a new
  entry. Classify links to the 115 pruned files as archive-backed evidence with
  a discoverable exact-member restore map, not as ordinary live local links.
* Action owner: Planning parent; documentation implementation owner.
* Exact resolving evidence: Source/copy digest equality for the 12 reports and
  narrative, preserved paired payloads/anchors/original embedded paths, active
  link and fragment checks, and historical-log prefix equality before append.
  The 24 file targets plus one directory from the supplied report have explicit
  dispositions. Any permitted missing historical image target is one of the
  exact 115 restore-map entries and has proven recovery; no blanket link-check
  exclusion or new unexplained dangling target is accepted.
* Decision route: Direct planner correction; the caller already resolved
  copy-versus-move and original-retention choices.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Bind validation to the requested matrix and honest stop conditions

* Related IDs: P01-T01, P04-T01; preservation Proposed Validation; caller validation list.
* Evidence: P04 says original focused tests, costs, native counts and links.
  The caller requires metadata, cost guard, 24 source checks, six registry cases,
  archive positive/negative tests, native Build/Verify and canonical hashes.
  P01's reported three registry cases are not the requested final six-case check.
* Concern: Generic test wording permits a partial green run to stand in for the
  final matrix or treats the already reported P01 checks as migration validation.
* Impact: Missing source guards, registry behavior or failed archive/native
  prerequisites can be missed while cleanup is described as complete.
* Smallest useful change: Add an explicit check-to-command/owner/result matrix
  using the existing suites, not a new test framework. Include metadata, cost
  guards and caveats, all 24 source checks, six registry cases, archive failure
  cases, report/source-byte checks, link/fragment checks and PC-003's package
  comparison. Validate code changes before prune; rerun affected guards and
  canonical hashes after prune. Require independent final implementation review
  without overwriting original adverse outcomes or creating another plan-critique loop.
* Action owner: Planning parent; implementation reviewer records outcomes.
* Exact resolving evidence: P04 names each check's actual command or precise
  acceptance assertion, prerequisites and expected scope. Results distinguish
  Pass, Fail, Blocked and Not run. Missing required archive/Build/Verify evidence
  stops destructive work; unavailable Render remains explicitly qualified.
  Final accounting includes actual removals and protected-content checks.
  No clean publication receipt is claimed, and no complete gate, commit or push
  is attempted under this dirty, uncommitted, non-publication authorization.
* Decision route: Direct planner correction; no additional publication approval
  should be solicited merely to complete this local retention task.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Install retention guidance without creating automatic deletion authority

* Related IDs: P03-T02; plan retention goal and non-goals.
* Evidence: The plan requires documented retention but does not name its durable
  owner/discovery path. The caller requires a policy page, baseline README and
  installation through existing repository guidance if needed, while retaining
  original RPI evidence and complete-local-gate obligations.
* Concern: An unlinked policy does not prevent accumulation; an overbroad
  generated-output rule could later authorize deletion of unique adverse renders
  or original closed-issue evidence merely by age or status.
* Impact: Cleanup recurs without preserving the same safeguards, or the new
  guidance conflicts with the repository's existing evidence and gate rules.
* Smallest useful change: Name a durable retention page and baseline README,
  link them through the existing index/repository guidance as appropriate, and
  define active work, immutable sources/reviews, reproducible outputs and external
  archive receipts. Default future tool output outside Git. State that this
  allowlist is one approved batch, not a recurring wildcard or issue-closure
  policy; originals and adverse findings remain protected. Explain the archive
  location dependency and restoration when a checkout lacks local archive bytes.
* Action owner: Planning parent; documentation implementation owner.
* Exact resolving evidence: P03 lists the page/README/link destinations; final
  link review can discover both guidance and restore map from maintained entry
  points. Guidance explicitly preserves original evidence, human approval and
  complete publication gates, and does not imply archive availability to every
  clone or full deletion of archived historical source records.
* Decision route: Direct planner correction using existing guidance, not a new
  instruction hierarchy or significant user decision.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Record PR dispositions against published evidence, not local passes

* Related IDs: P01-T01, P04-T01; primary research C5/C6.
* Evidence: Six unresolved threads are reported; five have apparent published
  fixes and the last has a local handoff correction. The plan asks for evidence
  before resolution, but does not bind each thread to its exact correction and
  publication state. Current status confirms local P01 files are modified.
* Concern: Passing local tests or finding a matching label can be mistaken for
  proof that the PR thread's published defect has been addressed. Treating P01
  as wholly unstarted can also duplicate or overwrite the existing local fix.
* Impact: Threads may be resolved prematurely or the review records can obscure
  which correction reviewers can actually inspect remotely.
* Smallest useful change: Carry forward P01 as locally implemented with reported
  evidence pending final validation/publication. Maintain six thread dispositions
  identifying published correction/head, relevant regression or native-label
  evidence, local-only work and permitted resolution action. Resolve only the
  existing published fixes after checking them. Keep the local handoff thread
  pending until publication unless a specific evidence-based exception is recorded.
* Action owner: Planning parent; authorized PR-review handler.
* Exact resolving evidence: Six-entry disposition record separates verified
  published, locally corrected and remaining/unverified states. Any resolution
  cites the published correction and check; no commit/push/branch/merge/issue
  operation is used to manufacture eligibility. The handoff thread remains
  pending under the current local-only evidence.
* Decision route: Direct planner correction; no remote mutation is performed
  by this critique worker and no new owner decision is required.

## Strengths and Residual Risk

* The report distinguishes output duplication from source dependencies and
  explicitly protects the 22-slide input, mentor YAML, editable images,
  baseline PDFs, original reviews and all current previews.
* The 12-file assurance bundle includes neighboring payloads and preserves
  failed, blocked and unassessed outcomes rather than implying fresh acceptance.
* The external archive makes old adverse image bytes recoverable in principle;
  implementation must still demonstrate that property. A local archive is not
  automatically available to another checkout or another operator.
* Required native Build/Verify does not establish Windows-rendered appearance,
  accessibility, business-cost validity or human acceptance. Conditional Render
  and separate publication gates remain explicit limitations.

## Questions or Blocking Evidence Gaps

No unresolved significant user decision prevents the planner corrections.
The locked set, archive default, PDF treatment, branch and publication boundary
are supplied decisions, not questions to reopen. Fresh per-path digests,
archive restore proof, implementation test commands and runtime results are
implementation prerequisites, not facts established by this critique.

## Limitations

Only the supplied assessment boundary was reviewed. No open-ended research,
source inspection, subagents, PR API calls, archive creation, native execution,
test reruns or source changes were performed. The original branch head and
published-fix assertions remain dated supplied evidence until the parent checks
them. Counts/hashes from preservation research were not independently recomputed.
The sole write from this worker is this critique artifact.

## Recommended Next Action

* Highest-impact finding: PC-001, preventing cleanup outside the approved set.
* Action owner: Planning parent.
* Smallest next action: Finalize P02/P03 against the locked 115-path manifest
  and settle PC-001 through PC-007 in one plan/details revision, then execute
  preservation and focused checks before any permitted pruning.
* User response required: No. All findings are direct corrections within the
  caller's existing decisions; do not invoke another independent critique pass.

## Next Steps

Return this Complete / Revise assessment to the active planning parent. The
parent should apply the seven bounded corrections and record their resolving
evidence before implementation; no peer stage is invoked by this worker.
Publication and remote issue changes remain unauthorized. No user action is
required, and no additional follow-up work is proposed outside this boundary.
