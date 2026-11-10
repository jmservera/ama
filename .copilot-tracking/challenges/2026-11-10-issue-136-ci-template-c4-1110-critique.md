---
title: Critique for issue-136-ci-template-c4-1110
description: One author-inline critique of the plan
ms.date: 2026-11-10
---

Executed once, author-inline, no nested agent. Verdict: proceed.

* Weakening risk: dropping the literal alone would lose the cap-4 guarantee. The compiled conditional equality assertion keeps it and adds the enabled branch, so it fails on inversion or a lost 4.
* Template regression ruled out by compiled semantics and the existing policy tests, so no template edit.
* The mutation check must not touch repository files; use a temporary copy of the compiled JSON or a patched in-memory template.
* Keep the `compiled()` signature backwards compatible (default argument) so other callers are unaffected.
* No compatible finding changes the plan.
