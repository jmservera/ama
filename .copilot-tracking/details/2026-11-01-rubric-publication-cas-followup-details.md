---
title: Rubric publication CAS details
date: 2026-11-01
---

Files: `.github/workflows/rubric-score.md` and `.lock.yml`, `.github/rubric/scripts/prepare.py`, `test_prepare.py`, `test_record_workflow.py`, `.github/rubric/README.md`.
Serialization alternative (workflow concurrency) rejected: gh-aw safe-output jobs do not expose a shared cross-event group; CAS is enforced in the step itself.
