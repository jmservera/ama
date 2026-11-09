---
title: Archive filesystem checkpoint 440 correction 1 research
description: Evidence for two scoped structure corrections and one timing qualification of the twelfth checkpoint
ms.date: 2026-11-06
---

## Scope and identity

Correction 1 of the twelfth checkpoint (task `archive-filesystem-checkpoint-440-correction1`, parent task `archive-filesystem-checkpoint-440`). Documentation only, local only. The R1 artifacts and the R1 Review stay unchanged. Frozen R1 head `f702e34b9605e93793993f104e010f4bbf585937`, tree `10216a593e8fd956036f0f3f5d4f505a9397f771`, ignored-clean at intake (empty `git status --short --ignored`). Parent `feat/discovery-assurance-integration-123` `dce6498cf850de9bdc79ecb1706f8491d75b2ea8`; main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`.

## Coordinator findings under research

* C1: the Classification row for the 702-line log and 11-file diff consumption uses "coordinator-supplied" as a classification. It is an attribution, not one of the allowed classes (local observed, Azure observed, implemented-unverified, deferred, blocked, unknown).
* C2: the Traceability bullets lack a document-qualified BRD requirement joined to code, tests, observed journey and owner or gate.
* C3: R1 Research says "Written before any plan". The create calls for research, plan and details were dispatched together (05:03:07.973 to .974Z), completed at 05:03:08.006, .017 and .028Z, and were committed at 05:03:14Z before any target edit. Reported by the coordinator from native events; not re-read here beyond the commit time already in git history.

## Evidence read in this cycle

All observed locally on 2026-11-06 from the frozen worktree and the read-only #1231 child worktree (`57b3b6a09f6ac5b77b37881e21447751a56be5ff`).

| Item | Observation |
| --- | --- |
| BRD NFR-006 (BRD 0.21.0, line 1624) | "The solution shall preserve exportable, versioned evidence independently of an AI supplier." Maps to BR-048. AC-060: export tests retain source, approval and supersession history; contracts specify data access, retention, support and exit responsibilities. Must. |
| BRD NFR-002 (line 1596) | Controlled assessments, designs, consents, instructions, evidence packs, handovers and decisions shall have immutable version identifiers and retained prior versions. AC-049: approved records are superseded rather than overwritten. Must. |
| BRD AC-015 (line 1532) | Belongs to BRD FR-011 (consent is not inferred from consultation, silence or access). It is NOT the ranking acceptance criterion. |
| PRD PR-006 (line 488) | Deterministic ranking: same data and same published policy version give the same order; a policy change creates a new version and keeps the old one. Cites PRD FR-012 and PRD AC-015 (line 2111, prioritisation inputs missing or conflicting give unknown or held, never silent exclusion; status Not run). |
| PRD DH-002 (line 466) | Constructed non-identifying data only until DPIA, retention schedule and processor terms are approved. |
| PRD DH-003 (line 467) | Later: scheduled retention job with owner approval and legal hold. |
| PRD PR-003 (line 485) | Addendum retention defaults are the design baseline pending DPO and Legal approval. |
| ADR 0006 | Source layout and cut-over policy; mentions the runtime data directory via `ZF_DATA` but no hard-link or archive mount contract was found. |

Document-qualification hazard: the same identifier AC-015 exists in both documents with different meanings (BRD: consent; PRD: prioritisation inputs). The new table must qualify every ID by document.

## Code and test identities (child #1231, read only)

* Helper: `src/core/src/zava_forward/core/ranking_publication.py`, `publish` (stage, `os.link`, `FileExistsError` readback, `os.unlink` of the owned stage), plus `verify`, `overdue`.
* Tests: `src/core/tests/test_ranking_publication.py`, class `ConcurrentWriterTests` (names include `test_same_snapshot_different_dates_keep_one_truthful_record`, `test_delayed_contender_leaves_a_finished_record_unchanged`, `test_cleanup_removes_only_the_staging_file_it_owns`, `test_failed_publication_removes_its_stage_and_keeps_foreign_files`, `test_sequential_bytes_and_name_are_unchanged`, `test_separate_processes_publish_one_truthful_record`); `src/core/tests/test_ranking_publication_runner.py` `test_same_snapshot_on_two_dates_publishes_once_and_reports_the_retained_date`.
* Observed retained local results are the R1 values (RED 48 tests, 4 failures, 2 errors; GREEN 48 tests; API wiring 12 tests); they were read, not rerun, and are unchanged.

## Relevance judgement

NFR-006 is relevant to the archive only as a partial, indirect fit: the archive keeps versioned, exportable publication records, and AC-060 asks for retained source and supersession history. Nothing observed shows an export test, an approval history or an exit contract for the archive. NFR-002 and AC-049 are closer on "never overwritten" semantics: the child keeps a finished record unchanged. Neither requirement mentions a filesystem, hard links or retention period, so neither is a hard-link requirement. The mapping is a joined reading by this author, not an owner-confirmed trace.

## Owner question

The coordinator asked the owner once whether the archive may require atomic hard links and refuse unsupported filesystems; the result was OWNER UNAVAILABLE. No answer, default or approval is inferred. The compatibility disposition stays blocked; the deployment mount and legal retention period stay unowned.

## Planning readiness

Ready for a bounded documentation-only plan: one table row reclassification, one small traceability table, one process qualification, index and log note. No runtime, requirement or ADR change.
