---
title: Issue 86 Main 4bc1e3f3 CI dependency integration research
description: Why reviewed Main PR1275 is merged into the child and what it changes
ms.date: 2026-11-08
---

Scope: issue #86 only. Head `fb7231c7`, tree `5320185b`; Main `4bc1e3f3` (tree `85ef5852`); parent ref `c5edb320`; PR 1243 head `fb7231c7`. Merge-base with Main is `0f05e9aa`. PR1243 namespace retry 2 failed on an official actionlint archive HTTP 503; Main's PR1275 changes the installer.

Incoming delta from the merge-base outside tracking: `.github/workflows/src-ci.yml`, `docs/reference/log.md`, `infra/README.md`, `tools/ci-affected.py`, `tools/install-actionlint.py`, `tools/rpi-checks.py`, `tools/test_ci_affected.py`, `tools/test_install_actionlint.py`. No `src/` change from `0f05e9aa`. A trial `git merge-tree --write-tree` reported no conflicts (it may write loose objects).

Not authorised: any application, auth, consent, metering, SQL, UX or policy change. The fourth issue criterion stays unmet.
