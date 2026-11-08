---
title: Issue 530 C4 chat privacy test helper typing plan
ms.date: 2026-11-08
---

* Research: `.copilot-tracking/research/2026-11-08-issue-530-c4-privacy-typing-research.md`. Details: `.copilot-tracking/details/2026-11-08-issue-530-c4-privacy-typing-details.md`.

## Phases

* [ ] Phase 1: commit research, plan, details and independent critique alone before any edit.
* [ ] Phase 2: annotate `src/core/tests/test_chat_privacy.py` only (typed mixin base, return and parameter annotations, no behaviour change).
* [ ] Phase 3: LIGHT checks: API strict mypy with candidate sources, Core ruff and mypy, the file's own unit tests, `git diff --check`, AST-equivalence proof, origins.
* [ ] Phase 4: authored Review, state record, final commit, ignored-clean freeze.

## Constraints

* No production, Bicep, schema, dependency, runner, workflow or config edit. No suppression, `Any` casts or dynamic imports. Every assertion, skip predicate, fixture backend and public interface preserved.
* No SQL, browser, Docker, lock, gate or full suite. Remaining 21 SQL methods and three Chromium/axe states remain a separately admitted continuation. The failed r1 receipt stays failed.
