---
title: Issue 86 integration of local parent 720d9e4 plan
description: Plan for one normal merge and no-service checks (Refs #86)
ms.date: 2026-11-07
---

Tier: FULL eventually for the integrated head; none admitted here, no services or lock. A child merge needs a new parent integration FULL and independent assessment; old receipts invalid.

1. Commit records (critique author-only, not independent).
2. Re-verify identities; stop on drift.
3. One `git merge --no-ff 720d9e4`; append-only log conflicts would keep both entries.
4. Verify two parents, whole incoming delta (raw modes/blobs) against the parent, and child-owned blobs unchanged.
5. Run from a git-archive snapshot: `tests.test_resident_decisions` (expect 308/110 skips), core strict mypy, ruff check/format; `src/api` `tests.test_assistant_release` if its installed namespace resolves, with import origins.
6. Write changes and one author Review; commit; freeze.
