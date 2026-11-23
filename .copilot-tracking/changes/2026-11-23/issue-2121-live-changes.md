---
title: Issue 2121 live changes
ms.date: 2026-11-23
---

Refs #2121. Tier: focused. No source change.

## Files

* docs/reference/research/issue-2121-live-2026-11-23.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/evidence/2026-11-23/issue-2121-live/ (anonymous curl, Azure state, sign-in JSON, screenshots, proof script)

## Per-criterion result

| Criterion | Proven | Unproven or owner-gated |
| --- | --- | --- |
| c. Owner approves migration plan | none | Owner-gated: no approval on #2121 |
| d. Live verification | Direct HTTPS welcome and health 200; anonymous API denied (401, browser-mode 302); real browser Entra sign-in; role claim and 403 on a forbidden route; SQL cross-session persistence | Live AI call (`ai-suspended`, workflow-only, model_calls 0); second role; restart persistence (no drills) |
| e. Retire Front Door after d | No Front Door resource exists in `ama`; group `ama` Succeeded | Owner authorisation and full d absent; nothing to delete |

No box is ticked. Validation: Markdown and link review plus git diff; no executable test applies. Evidence scan found no credential values. The only write was one throwaway chat thread, deleted; no Azure resource created.
