---
title: "Issue 200 workflow rename changes (2026-11-01)"
ms.date: 2026-11-01
---
* .github/workflows/mvp-ci.yml: name `Source CI`.
* .github/workflows/mvp-validation.yml: name `Source validation`.
* tools/rpi-checks.py: WORKFLOW_HASHES updated for both files.
* infra/README.md: rename note replaces retention note.

Validation (pip venv): infra/tests 498 + test_pipeline 29 OK; tools/test_rpi_checks 55 OK; rename-zava-tests OK. ruff check/format on tools/rpi-checks.py report findings that pre-exist (hash-only edit); no mypy-relevant source touched.
