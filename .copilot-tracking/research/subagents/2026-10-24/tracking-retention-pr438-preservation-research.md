<!-- markdownlint-disable-file -->
# Tracking Retention PR 438 Preservation Research

Status: Complete for bounded local preservation research; implementation and
archive/native reproduction validation not performed.
Task: tracking-retention-pr438.
Scope: Research only; current branch docs/capstone-cowork-story. No source,
PR, archive or deletion operations. Preserve untracked latest-slide work.

## Questions

* Identify the sole current native builder, manifest and baseline dependencies,
  durable placement and minimum Build/Verify/Render path adaptations.
* Enumerate conservative generated presentation removal candidates, retaining
  editable sources, images, templates, scripts and linked reports.
* Identify the smallest coherent promotion set for unique linked assurance and
  PRD evidence, including neighboring dependencies and immutable log links.
* Record exact candidate counts and logical bytes, counterevidence and checks.

## Working Hypothesis and Check

Generated render/build derivatives can be separated from reproduction inputs
by reading script path defaults and direct document backlinks. Disconfirm by
finding a candidate read as a baseline, manifest, image/template source or
linked original evidence. Unknown active RPI records remain out of scope.

## Confirmed Findings

* The current native route is a six-slide patch to an existing 54-slide PPTX,
  not a reconstruction from the older YAML decks or the portable 18-slide
  slides.json route. Its sole scoped script is
  .copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/Invoke-Recovery.ps1.
* The script reads content/recovery.json and slide-deck/original.pptx.
  Original PDF is historical visual evidence, not a runtime read dependency.
  Build currently creates missing originals from canonical deliveries: that
  fallback is unsafe after delivery because the canonical PPTX is already
  patched and slide 32 receives an added shape. Promotion must pin the original
  baseline and fail closed rather than bootstrap from the latest delivery.
* Presentation inventory is 812 files / 63,433,006 logical bytes. There are
  134 preview/contact images / 33,259,012 bytes. Of these, 113 / 25,505,539
  bytes predate the current build; the current 21 / 7,753,473 bytes stay protected.
* Six presentation files match docs byte-for-byte, but two are editable image
  inputs and must remain. Four are output copies totalling 8,326,217 bytes.
  Duplication alone is insufficient deletion authority: their Verify/Render
  consumers must be adapted or their documented restore path tested first.
* The older 22-slide candidate is a fixed input to the architecture refresh:
  .copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/slide-deck/zava-forward-executive-draft.pptx.
  It is not the published 24-slide draft and must not be removed as an output.
* Local Markdown links resolve to 24 file targets and one directory target.
  The smallest coherent assurance/PRD promotion bundle is 12 files / 160,967
  bytes: one RAI report, three v0.7.0 files, three v0.11.0 files and five
  v0.12.0 files. Original findings, failed outcomes, paired payloads, targeted
  closure and local-validation provenance must travel together.

## Evidence Read

* .copilot-tracking/research/2026-10-24/tracking-retention-pr438-research.md
* .copilot-tracking/plans/2026-10-24/tracking-retention-pr438-plan.md
* .copilot-tracking/details/2026-10-24/tracking-retention-pr438-phase-details.md
* .copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/changes/build-deck.md
* .copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/Invoke-Recovery.ps1
* .copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/content/recovery.json
* .copilot-tracking/ppt/2026-10-14/zava-forward-architecture-refresh/reports/parent-publication.md
* .copilot-tracking/ppt/2026-10-14/zava-forward-architecture-refresh/build-handover.md
* .copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/build-handover.md
* Direct docs backlinks and the four assurance/PRD report neighborhoods.

## Native Promotion Map

Use tools for the executable and manifest, and the existing capstone authoring
area for native baselines. These are proposed destinations, not files created
by this research. First copy and verify; keep all 89 current untracked files
until the parent has separately verified the migration and archive.

Source prefix N: .copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/

| Exact source suffix under N | Proposed durable destination | Bytes | Role |
| --- | --- | ---: | --- |
| Invoke-Recovery.ps1 | tools/cowork-native-recovery/Invoke-Recovery.ps1 | 10,855 | Sole scoped native Build/Verify/Render implementation |
| content/recovery.json | tools/cowork-native-recovery/content/recovery.json | 15,498 | Six-page manifest; patch targets 6, 11, 21, 32, 36, 52 |
| slide-deck/original.pptx | docs/capstone/pitch/cowork-main-presentation/native-recovery/baseline/original.pptx | 2,645,729 | Mandatory pre-patch source, native layouts/media/themes/shapes/notes |
| slide-deck/original.pdf | docs/capstone/pitch/cowork-main-presentation/native-recovery/baseline/original.pdf | 4,962,731 | Original visual baseline; not read by Verify or Render |
| changes/build-deck.md | docs/capstone/deck/cowork-generated/native-recovery-build-2026-10-24.md | 7,696 | Durable build narrative; preserve original unchanged as historical evidence |

Three execution inputs total 2,672,082 bytes. Including original PDF gives
four native-source files / 7,634,813 bytes. Including the build narrative gives
five promoted files / 7,642,509 bytes. The original PDF can instead stay only
in the verified archive if the owner prefers a smaller durable bundle; it is
not a reason to substitute the delivered PDF as the original baseline.

Observed SHA-256 on 2026-10-24:

```text
Invoke-Recovery.ps1 1a7e56d264ecb6a44daba36c1b2a3082d1919b714b8dbbf2e9e2b43a8520e278
content/recovery.json 387f700b9f73a4a8db808e862b9ae01e351061b7d40c56c7137d488b9ab53574
slide-deck/original.pptx d41acc969efb1687cfdd0103b753a62ea697005652760b1579a8e6de955cf447
slide-deck/original.pdf 308c6053634a25e0a78e581a44d3abfd1ee3be7d98e0df6d9af18c7f2d12db93
```

Minimum path/behavior adaptations, recommended only:

1. Keep RepoRoot explicit. Resolve manifest from PSScriptRoot rather than the
   dated tracking Work constant. Resolve Original from the durable baseline
   path above and verify its pinned hash before Build and Verify.
2. Add one OutputDir parameter for disposable build/validation files. Default
   to a new run's tracking output directory or require it explicitly; do not
   mix writable output with the durable tools or baseline directory. Candidate
   stays OutputDir/zava-forward-cowork-v2-draft.pptx; receipt and Render output
   stay below OutputDir. Verify and Render must receive the same OutputDir.
3. Remove the missing-original fallback that copies canonical PPTX/PDF.
   Fail with the expected baseline path/hash instead. Do not use the patched
   current PPTX as input or silently regenerate the original. Every Build
   starts from the preserved original, never the previous candidate.
4. Render continues to require Windows PowerPoint COM and a Windows-visible
   RepoRoot and OutputDir, not an unconverted Linux path. Build/Verify use
   PowerShell plus .NET compression/XML and the two execution data inputs;
   there is no Python/YAML/external-image read in this native script.
5. Preserve the six original timing lines, native package objects and all
   historical cost/source caveats. The manifest's evidence/ai-cost-evidence.md
   text is a narrative reference, not a file loaded at runtime. Its existing
   durable context is docs/capstone/pitch/cowork-main-presentation/evidence/ai-cost-evidence.md.
   Keep the current notes/refinement records and assets in that authoring
   folder; do not claim the manifest reconstructs all 54 pages from scratch.
6. Update the four active capstone README/brief/correction backlinks to the
   promoted build narrative. Leave docs/reference/log.md line 6936 unchanged
   and retain N/changes/build-deck.md. The original narrative and all current
   validation records remain accessible at their historical paths.

Proposed invocation after implementation, NOT executed in this lane:

```powershell
pwsh -NoProfile -File tools/cowork-native-recovery/Invoke-Recovery.ps1 -Action Build -RepoRoot <repo> -OutputDir <scratch>
pwsh -NoProfile -File tools/cowork-native-recovery/Invoke-Recovery.ps1 -Action Verify -RepoRoot <repo> -OutputDir <same-scratch>
powershell.exe -NoProfile -File <Windows-repo>/tools/cowork-native-recovery/Invoke-Recovery.ps1 -Action Render -RepoRoot <Windows-repo> -OutputDir <Windows-scratch>
```

Preserve all 62 current nonbinary/nonimage records / 62,124 bytes at N,
including changes/build-deck.md, slide-deck/package-validation.json,
slide-deck/validation/slide-001-deck-validation.json through
slide-054-deck-validation.json, and these six validation files:

```text
deck-validation-report.md
deck-validation-results.json
delivery-validation.json
native-navigation-validation.json
native-text-bounds.json
pdf-arithmetic-validation.json
```

The six names above are relative to N/slide-deck/validation/. These records
were inventoried/read as source evidence, not rerun or independently accepted.

## Exact Generated-Output Selection

The sets below are finite inventories, not shell globs or recursive deletion
instructions. A numerical range expands only to the explicitly bounded,
zero-padded or unpadded filenames stated. Before implementation, the parent
must expand them into exact archive-member paths/hashes and confirm equality
to the observed inventory. Preserve every unlisted file and every symlink.

### D1: Four Exact Duplicate Binary Outputs

| ID | Exact tracking path | Existing byte-identical durable file | Bytes |
| --- | --- | --- | ---: |
| D1a | .copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/slide-deck/ama-mentor-progress-review.pptx | docs/presentations/ama-mentor-progress-review.pptx | 105,811 |
| D1b | .copilot-tracking/ppt/2026-10-14/zava-forward-architecture-refresh/slide-deck/zava-forward-executive-draft.pptx | docs/capstone/deck/draft/zava-forward-executive-draft.pptx | 607,754 |
| D1c | .copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/slide-deck/zava-forward-cowork-v2-draft.pptx | docs/capstone/deck/zava-forward-cowork-v2-draft.pptx | 2,643,853 |
| D1d | .copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/slide-deck/zava-forward-cowork-v2-draft.pdf | docs/capstone/deck/zava-forward-cowork-v2-draft.pdf | 4,968,799 |

Hashes for the pairs:

```text
D1a c40c4295c2bcf45bcdba98c8c65ab39579a6694e80cc4337ef9495aac2307f3e
D1b f14ee526ef93e9412b7b3409245307a8fd5cd3b7b3e52a21b6082d99527eb603
D1c 39659a3ad9974f802a8418177a9ca0ca8daf7478e71cd82d04cd7677d9ad2cc0
D1d b816f3f2282ffad4e0afd41cc39ba76a6871bc62c2292c5a62129a4864bd9a9c
```

D1a/D1b are the smallest older-copy removal recommendation: two files /
713,565 bytes, only after archive verification and a documented restore or
regeneration step for tooling that still expects those working-output paths.
Do not rewrite historical validation records to claim they used the docs copy.
D1c/D1d are deferred until native promotion, Build/Verify/Render and delivery
comparison pass. They are NOT immediately disposable while Verify/Render
still read the candidate at the existing location. This preserves the user's
latest untracked build during the first cleanup phase.

### D2: 113 Older Preview Images

All directory paths below begin with .copilot-tracking/ppt/. The filenames
and finite expansions are the complete candidate set. This is archive-only
until the archive can restore the visual evidence used by the linked reports.
Keep JSON/CSV/Markdown reports, extracted source images and content images.

| Exact directory suffix | Exact finite filename set | Files | Bytes |
| --- | --- | ---: | ---: |
| 2026-09-11/proper-warm-cxo-introduction/final/preview/ | Slide1.PNG through Slide14.PNG; overview.png | 15 | 1,218,338 |
| 2026-09-11/proper-warm-cxo-introduction/slide-deck/preview/ | Slide1.PNG through Slide12.PNG; overview.png | 13 | 1,050,534 |
| 2026-09-18/proper-warm-cxo/slide-deck/validation/ | Slide1.JPG through Slide11.JPG; contact-sheet.jpg; corrected-slides.jpg | 13 | 2,156,265 |
| 2026-09-26/ama-mentor-progress-review/slide-deck/validation/ | slide-001.jpg through slide-015.jpg | 15 | 2,906,169 |
| 2026-10-13/zava-forward-agent-process/slide-deck/validation/ | parent-slide-12.jpg; parent-slide-13.jpg; parent-slide-14.jpg | 3 | 511,880 |
| 2026-10-14/zava-forward-architecture-refresh/slide-deck/validation/ | slide-001.jpg through slide-024.jpg; contact-01-06.jpg; contact-07-12.jpg; contact-13-18.jpg; contact-19-24.jpg | 28 | 9,988,825 |
| 2026-10-14/zava-forward-capstone-rebuild/slide-deck/validation/ | slide-001.jpg through slide-022.jpg; contact-01-06.jpg; contact-07-12.jpg; contact-13-18.jpg; contact-19-22.jpg | 26 | 7,673,528 |

Do not remove D2 merely because it is generated. The handovers and publication
record expressly cite contact sheets and full-size visual inspection. Preserve
the reports in place and provide an archive manifest/member restoration map
alongside the durable retention/build documentation. If that evidence cannot
be restored by exact path and checksum, retain the affected images locally.
Original adverse render images may be unique and cannot be recreated by
rendering only the corrected deck; archive their actual bytes.

### Explicit Exclusions

* All YAML, style/voice guides, content-extra.py hooks, scripts, templates,
  source/extracted trees, diagrams, manifests, content images and research,
  changes, handover and validation reports stay. All files outside D1/D2 stay.
* Keep the unique current mentor content/global/style.yaml and content.yaml
  files under .copilot-tracking/ppt/2026-09-26/ama-mentor-progress-review/content/.
  Published PPTX is not an editable-source replacement.
* Keep N/slide-deck/original.pptx and original.pdf until durable-copy and archive
  verification; neither matches the delivered pair. Do not rename the delivery
  to original or use age as a selection rule.
* Keep these 21 current previews in N/slide-deck/validation/: slide-005.png,
  slide-006.png, slide-007.png, slide-010.png, slide-011.png, slide-012.png,
  slide-020.png, slide-021.png, slide-022.png, slide-031.png, slide-032.png,
  slide-033.png, slide-035.png, slide-036.png, slide-037.png, slide-051.png,
  slide-052.png, slide-053.png, contact-adjacent-18.png, contact-all-54.png,
  contact-changed-six.png. Total 7,753,473 bytes; not part of D2.
* Keep the two duplicated authoring images: .copilot-tracking/ppt/2026-10-13/zava-forward-agent-process/content/slide-013/images/agents-in-retrofit-process.png
  and .copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/source/extracted/slide-013/images/image-01.png.
  Each is 293,135 bytes; their match to docs/capstone/deck/draft/agents-in-retrofit-process.png
  does not make them generated-output candidates.
* Keep .copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/slide-deck/zava-forward-executive-draft.pptx
  (419,383 bytes): architecture-refresh/generate_content.py pins it to
  7b25fd7e77d1ed7d9aa908cf3da429bcfeae104beadea5ac90c1e97dbc71fbb4.
  Also keep its source/canonical-22-slides.pptx (393,862 bytes), the refresh's
  source/structural-24-slides.pptx (420,785 bytes), and all other source inputs.
* Keep both older validation/slides.pdf files, reports/baseline-comparison.pdf,
  reports/initial-candidate-receipts/candidate.pptx and slides.pdf in the refresh
  project. These support baseline comparison and initial failure provenance;
  even matching PDF bytes are not sufficient reason to prune a reader's input.
* Keep all other historical PPTX/PDF outputs. Their exact replacement and
  regeneration contracts have not been established in this bounded lane.

## Minimal Assurance and PRD Promotion

Recommend one small durable reports area:
docs/reference/research/reports/. These are assurance/requirements-history
records, not company facts, sector synthesis or UX findings, so placing them
in company/, sector/ or ux/ would misclassify them. Do not move hundreds of
plans/reviews or create a new top-level evidence system.

Copy the exact 12 files below with sibling filenames and original dated
groups intact. This is 160,967 bytes and preserves the six directly linked
targets plus six needed neighboring records. Retain originals in tracking
unchanged in this cleanup; none is a pruning candidate. Copying rather than
rewriting avoids corrupting their original resolved-path fields, original
outcomes and append-only log links. Record original path/hash and promoted
path/hash in the parent's migration receipt. Update active index/PRD/ADR
references to the durable copies, without claiming a fresh review.

| Exact original | Proposed path below docs/reference/research/reports/ | Bytes |
| --- | --- | ---: |
| .copilot-tracking/rai-reviews/2026-10-14/rai-report-ama-20261014.md | 2026-10-14/rai-report-ama-20261014.md | 75,110 |
| .copilot-tracking/reviews/2026-10-06/proper-warm-prd-v0-7-0/challenge-disposition.md | 2026-10-06/proper-warm-prd-v0-7-0/challenge-disposition.md | 4,614 |
| .copilot-tracking/reviews/2026-10-06/proper-warm-prd-v0-7-0/quality-report.yaml | 2026-10-06/proper-warm-prd-v0-7-0/quality-report.yaml | 1,952 |
| .copilot-tracking/reviews/2026-10-06/proper-warm-prd-v0-7-0/standard-findings.yaml | 2026-10-06/proper-warm-prd-v0-7-0/standard-findings.yaml | 2,911 |
| .copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-11-0/challenge-disposition.md | 2026-10-10/proper-warm-prd-v0-11-0/challenge-disposition.md | 4,278 |
| .copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-11-0/quality-report.json | 2026-10-10/proper-warm-prd-v0-11-0/quality-report.json | 11,497 |
| .copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-11-0/standard-findings.json | 2026-10-10/proper-warm-prd-v0-11-0/standard-findings.json | 17,041 |
| .copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-12-0/challenge-disposition.md | 2026-10-10/proper-warm-prd-v0-12-0/challenge-disposition.md | 2,759 |
| .copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-12-0/quality-report.json | 2026-10-10/proper-warm-prd-v0-12-0/quality-report.json | 11,920 |
| .copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-12-0/standard-findings.json | 2026-10-10/proper-warm-prd-v0-12-0/standard-findings.json | 23,170 |
| .copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-12-0/targeted-closure.md | 2026-10-10/proper-warm-prd-v0-12-0/targeted-closure.md | 3,061 |
| .copilot-tracking/reviews/2026-10-10/proper-warm-prd-v0-12-0/local-validation.md | 2026-10-10/proper-warm-prd-v0-12-0/local-validation.md | 2,654 |

Dependency closure and counterevidence:

* v0.7.0 challenge-disposition.md links the two YAML siblings. Its final PASS
  is only a narrow paragraph review; preserve the earlier RISK/FAIL narrative.
* v0.11.0 challenge-disposition.md links both JSON siblings. Original overall
  FAIL, Validate BLOCKED and Finalize NOT_EVALUATED remain unchanged.
* v0.12.0 challenge-disposition.md links both JSON siblings. The quality JSON
  contains workspace-path references to the original paired payloads; retain
  those originals. targeted-closure.md explicitly depends on the original
  paired findings; local-validation.md documents subsequent editorial checks,
  not independent regrading or runtime acceptance. All five are coherent.
* The RAI report has self-contained tables and commit-pinned external source
  citations. No additional local Markdown sibling was found in its directory.
  Keep owner-acceptance-2026-10-15 anchor, baseline commit, original resolved
  report path, 29-check rollup, all eleven residuals and unassessed gates.
  Its acceptance is baseline/remediation planning, not operational approval.
* Do not promote inferred issue-state closure. The directly linked remediation
  plan and backlog records remain in place, as do unknown-active original RPI
  research/plans/reviews. This lane did not enumerate their state stores.

## Complete Direct-Link Disposition

The 24 linked file targets partition into six report targets promoted above,
five presentation targets retained below, and thirteen other retained targets.
The architecture directory link is a twenty-fifth unique local target but not
a file, resolving the apparent 24-versus-25 inventory discrepancy. Commit-pinned
remote MVE URLs are historical external references, not relocation targets.

Five presentation targets to retain in place, including their report/source
neighbors; only the current narrative receives a durable copy in this proposal:

```text
.copilot-tracking/ppt/2026-10-14/zava-forward-architecture-refresh/build-handover.md
.copilot-tracking/ppt/2026-10-14/zava-forward-architecture-refresh/reports/parent-publication.md
.copilot-tracking/ppt/2026-10-14/zava-forward-architecture-refresh/research/ux-design-review.md
.copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/build-handover.md
.copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/changes/build-deck.md
```

parent-publication.md links sibling parent-publication.json; preserve that
receipt, not just the Markdown. The two older handovers cite their reports,
changes, scripts, baseline/source and YAML trees. Retaining these trees in
place avoids a transitive mass move. D2 concerns only archived render images.

Thirteen other retained file targets, none selected for relocation/removal:

```text
.copilot-tracking/architecture-diagrams/2026-10-14/zava-forward/validation.md
.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md
.copilot-tracking/changes/2026-10-15/resident-decisions-86-changes.md
.copilot-tracking/changes/2026-10-17/finance-match-controls-94-changes.md
.copilot-tracking/github-issues/prds/rai-remediation/artifact-analysis.md
.copilot-tracking/github-issues/prds/rai-remediation/handoff-logs.md
.copilot-tracking/github-issues/prds/rai-remediation/handoff.md
.copilot-tracking/github-issues/prds/rai-remediation/issues-plan.md
.copilot-tracking/plans/2026-10-15/rai-remediation-plan.md
.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html
.copilot-tracking/research/2026-10-06/proper-warm-profile-journey-critique-research.md
.copilot-tracking/reviews/logs/2026-10-17/coordinator-lifecycle-funnel-101-review.md
.copilot-tracking/reviews/plans/2026-10-15/rai-remediation-plan-critique.md
```

Also retain the linked directory
.copilot-tracking/architecture-diagrams/2026-10-14/zava-forward/ intact.
No finding here supersedes an unknown active task or its original review.

### Immutable Log Compatibility

Do not edit old log entries. docs/reference/log.md links original RAI and PRD
records at lines 1501, 1565-1566 and 2409, current native build at 6936, and
other retained records elsewhere. Original paths and anchors continue working
because the originals remain byte-identical. Append a new migration/retention
entry and update the reference index only during parent implementation.

If a future cleanup genuinely requires replacing an original Markdown with a
compatibility pointer, it must retain every inbound fragment ID and point to a
byte-preserved durable report. A one-line redirect loses anchors such as
owner-acceptance-2026-10-15 and is insufficient. Do not replace JSON/YAML
payloads with prose stubs. No such replacement is needed for this minimal map.

## Potential Counts and Logical Sizes

The supplied whole-tracking baseline is 2,414 files, 2,325 tracked,
89 untracked, approximately 80.02 MiB. Parent task files and this report were
added after that audit, and the parent may be editing concurrently. Do not
present that baseline as a fresh whole-tree measurement or infer current
tracked/untracked counts from it. Fresh scoped PPT baseline: 812 files /
63,433,006 bytes (60.494 MiB), including all 89 current untracked build files.

| Conditional scenario, not executed | Removed files | Removed bytes | PPT files after | PPT bytes after |
| --- | ---: | ---: | ---: | ---: |
| Smallest older duplicate-only set D1a/D1b | 2 | 713,565 | 810 | 62,719,441 |
| All four duplicates D1, only after native migration | 4 | 8,326,217 | 808 | 55,106,789 |
| D2 older previews only, after archive restore proof | 113 | 25,505,539 | 699 | 37,927,467 |
| D2 plus D1a/D1b; keep latest build intact | 115 | 26,219,104 | 697 | 37,213,902 |
| D2 plus all D1, after native migration | 117 | 33,831,756 | 695 | 29,601,250 |

These totals exclude archive storage and newly written task/manifest/pointer
documents. They count removals only, not source promotions. Copying the
recommended 12 reports and five native/narrative files adds 17 files /
7,803,476 bytes before path-adaptation or documentation edits. With originals
retained, the 115-file scenario gives net repository reduction of 98 files /
18,415,628 bytes, excluding new implementation receipts. The 117-file scenario
gives net reduction of 100 files / 26,028,280 bytes on the same basis.
The minimal two-duplicate phase alone increases repository bytes if all
promotions are copied first; do not describe that phase as net disk saving.

Promotions do not reduce tracking counts while original evidence is retained.
Even the 117-file subtraction from the supplied 2,414 baseline is only 2,297
before new task files; it is not the actual final tracking count. External
archive size is unmeasured, and tracked pruning does not shrink Git history.

## Proposed Validation Before Parent Pruning

1. Capture fresh branch/status and canonical PPTX/PDF hashes. Preserve all
   untracked entries; do not stash/move unrelated work. Expand D1/D2 to an
   exact inventory with type, logical size and SHA-256; reject drift and
   symlinks. Verify every intended archive member by readback/restoration in
   an external owner-only location. Do not follow symlinks or inspect private
   datasets/secrets. No archive was created in this lane.
2. Confirm promoted input bytes and preserved original report bytes against
   hashes. Run migrated Build twice into separate disposable directories;
   compare ZIP member-name sets and per-member bytes, not ZIP entry order or
   whole-PPTX bytes alone. Verify both candidates against the pinned original.
   Missing/wrong baseline must fail before producing a candidate.
3. Require exactly 54 slides, 54 nonempty notes and 27 Last Slide Viewed
   actions. Only the six selected slide parts and their six notes may differ
   from the baseline; retain order, sections, relationships, themes, masters,
   media and timing. Verify the no-duplicate-added-shape behavior from fresh
   original input, including manifest slide 32 shape 70001.
4. Render under real Windows PowerPoint using the migrated candidate. Read
   back native caller navigation, inspect all six changed slides and adjacent
   slides, and validate restored arithmetic. PDF must have 54 pages. Keep
   native history navigation distinct from PDF static links. Re-exported PDF
   bytes may differ by environment/metadata; never overwrite canonical
   deliveries merely to satisfy a hash expectation.
5. Keep canonical hashes D1c/D1d unchanged. Reuse the existing focused
   docs/capstone/pitch/cowork-main-presentation/test_build_assets.py test slice
   and cost guards, with a baseline-aware migration check. This lane did not
   run those tests or scripts, as requested. Do not infer independent
   presentation, accessibility, financial or live acceptance.
6. Resolve all active docs links and fragments after promotion; verify the
   three PRD bundles' sibling references and preserved embedded original paths.
   Confirm old log bytes unchanged except a new appended entry, and retain
   original FAIL/Blocked/Not assessed outcomes. No whole-repository lint pass
   is claimed; historical link/format issues are not this cleanup's repairs.
7. Restore sampled older contact sheets, full-size slides and both old deck
   outputs to their exact former paths before allowing D2/D1a/D1b pruning.
   Verify validators' input paths and baseline PDFs remain reachable. Recount
   exact removals/retained files and bytes from the manifest; seek the required
   independent parent review. Publication gates remain separate and unrun.

## Recommendation and Unresolved Decisions

Recommend the 12-report coherent copy bundle plus the native source/manifest/
baseline promotion, retaining originals during verification. Limit the first
possible pruning phase to D1a/D1b and archive-backed D2 after their explicit
checks; preserve the entire current untracked build. D1c/D1d become eligible
only after native reproduction verification, not as a prerequisite to it.
Do not prune current previews, original baselines, authoring images or any
unmapped RPI history. If archive/native prerequisites are unavailable, stop
at preservation and keep affected files; generated status is not proof.

Parent/owner decisions still required: approve final expanded archive/removal
manifest and archive location; choose whether original PDF has a durable local
copy as recommended or archive-only preservation; decide when deferred current
output pruning is justified. This research does not make those decisions.

## Validation and Open Questions

Completed: branch/status inspection, scoped file-size inventory, SHA-256
duplicate/input comparison, direct docs backlink resolution, local report
dependency extraction and static builder reads. Only this research file was
written. No existing project script, PR tool, cloud/model operation, source
edit, archive, deletion, commit or push was performed. No subagents used.

Recommended next checks, not completed:

* [ ] Parent expands and approves finite D1/D2 inventory and archive receipt.
* [ ] Archive full readback and exact-path sampled restoration.
* [ ] Promoted Build/Verify and Windows COM Render reproduction.
* [ ] Cost/native package, source parity and active/historical link checks.
* [ ] Independent final selection review and actual post-cleanup measurement.
