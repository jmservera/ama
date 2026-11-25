---
description: Correct the reserved arXiv ancillary directory in generated packages
ms.date: 2026-11-25
---

# RPI Plan: arXiv reserved anc directory

## Task Metadata

Task arxiv-reserved-anc, child of arxiv-release-package. Automatic,
agent-owned decisions; original document-review branch retained.

## Executive Summary

Move compilation dependencies out of the reserved root anc directory inside
archives, not in the repository. Local PDFLaTeX compilation did not test
arXiv's file classification, so the original validation missed this defect.

## Phase Checklist

The changed parts are package_arxiv.py and its tests and usage instructions.

<!-- rpi:phase id=P03 -->
### [x] P03: Correct submission layout

Goals: arXiv sees every compilation dependency as source, not ancillary material.

Dependencies: original dependency graph and official ancillary-file rule.

Changes in the map: archive transformation and existing instructions.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Remap reserved directory and validate

Goals: corrected ZIP/tar.gz compile with no root anc members.

Requirements: FR-005, NFR-004.

Details:
* Rewrite only active literal file arguments in archived TeX; preserve comments,
  verbatim/listing examples, evidence-path text, binary images and prompt bytes.
* Keep original bytes for existing pre/post-build Git checks.
* Reject destination collisions. Share file-command parsing with collection.
* Add two focused regressions to the existing test module; no test removals.
* Run combined package/PaperCheckerTests, Ruff check/format, strict mypy and
  git diff --check. Build the actual current paper, verify both archive
  member sets, assert no anc paths, check nested inputs and literal prompts,
  and verify that repository manuscript files are unchanged.
* Document deleting old upload files before uploading one corrected archive.

References: https://info.arxiv.org/help/ancillary_files.html, retrieved
2026-11-25; user's three missing anc paths and ancillary classification.

Dependencies: no external service execution or new package dependency.

## User Decisions and Requirements

The user supplied the failed arXiv upload. The attached main.tex snapshot is
read-only. Existing publication, author-approval and no-push boundaries stand.

## Functional Requirements

* FR-005: No compilation input is packaged under root anc; all rewritten
  input, include, graphics and literal-listing references resolve in the bundle.

## Non-Functional Requirements

* NFR-004: Repository source and non-file-reference content remain unchanged;
  original-source Git binding and deterministic archives remain intact.

## Planning Readiness and Next Step

Ready. The official rule and observed error establish the correction.
No new research or user decision is needed.

## Critique Disposition

Skipped by inherited child-task defaults. Review is also skipped by the
child-task default; validation will not be described as a new independent review.

## Follow-Up Items

* Actual arXiv re-upload and publication remain owner actions.

## Handoff

Implement P03-T01 and record concrete tests and corrected archive hashes.
