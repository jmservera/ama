---
title: 435 capstone deck tooling verification research
description: Research for verify-only run of Capstone deck tooling tests and validation.json hash integrity at 74a93a137a
ms.date: 2026-11-13
---

## Scope

Verify-only (Refs #435). No edits to `docs/` or `tools/`; no deck or diagram rebuild.
Read at start: case study original, addendum, reference README, memory (context only).

## Evidence

* Python suites: `tools/capstone/test_render_preview.py`, `docs/capstone/history/cowork-main-presentation/test_build_assets.py`, `docs/capstone/thought-leadership/everything-but-the-software/anc/test_*.py` (5 files).
* Node suites: `docs/capstone/source/diagrams/architecture/test-architecture.mjs`, `test-geometry.mjs`.
* Receipt `docs/capstone/source/validation.json` hashes:
  * `package.candidate_sha256` and `linux_preview.source_sha256` -> `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx` (raw bytes, per Test-SourceHashes.ps1).
  * `linux_preview.pdf_sha256` -> deck `.pdf`.
  * `baseline_sha256` -> `docs/capstone/source/baseline.pptx`.
  * `manifest_sha256` -> `docs/capstone/source/slides.json`; `builder_sha256` -> `tools/capstone/Invoke-Capstone.ps1` (canonical LF-normalised hash).
  * `pitch.speaker_script_sha256`, `questions_and_answers_sha256` -> `docs/capstone/pitch/*.md`.
* Brief names `deck/slides.json`, which does not exist; the manifest is `source/slides.json`. `deck/` has only the PPTX and PDF.

## Risks and unknowns

* Tests may need third-party packages (pptx, PDF libs, node modules); a missing prerequisite is reported as blocked, not installed from cloud beyond pip need.
* Whether raw or LF-normalised hashing applies per file is resolved by computing both and reporting which matches.

## Planning readiness

Ready.
