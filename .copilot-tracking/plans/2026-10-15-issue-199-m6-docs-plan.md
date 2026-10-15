---
title: Issue 199 M6 plan
ms.date: 2026-10-15
---

## Phases

* [x] 1. Split `mvp/README.md` into five per-package READMEs byte-preserving the evidence sections; recreate `mvp/README.md` as a pointer.
* [x] 2. Repoint docs, infra README, comments, tests' dead `sys.path`, copilot instructions, rubric registry.
* [x] 3. Remove importer exemptions; list the others as follow-ups.
* [x] 4. Matrix, index and log updates.
* [x] 5. Validate, record, commit, open PR (Refs #199).

## Critique (executed once)

Verdict: accepted. Risk: removing orchestrator exemptions is not small (reverted). Risk: dropping the `mvp/README.md` rubric glob is safe because `src/**/*` scores the moved text. No conflict with confirmed decisions.
