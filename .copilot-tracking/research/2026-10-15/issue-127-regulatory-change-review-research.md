---
title: Issue 127 regulatory change review research
ms.date: 2026-10-15
---

## Task

Issue #127 (parent #123): route every detected regulatory change to a human-owned assessment before activation (RULE-021, AC-068; RULE-002, CON-001, CON-002, CON-005).

## Evidence

* `mvp/zavaforward_mvp/rulecards.py` already holds append-only versioned cards with owner-only approve/activate and `source_changed`, which logged a bare open review item with no affected requirements, rules or tests and no assessment record.
* `mvp/zavaforward_mvp/lawstore.py` retains source versions and snapshots (prior versions retained).
* BRD RULE-021/AC-068: review identifies affected requirements, rules, decisions, communications, templates, reports and journeys; approval records interpretation, owner, tests, effective date, notification, rollback and any hold.
* ADR 0005: labelled synthetic exercise fixtures only; Azure deployment; non-Azure services local tests only.
* Comment on #127: #213 supplies automated detection; this issue is the human-owned review requirement.

## Gaps against acceptance criteria

* AC1 review items with affected requirements, rules, tests: missing.
* AC2 prior versions and effective dates: card versions retained; source prior version and source effective date not recorded on the item.
* AC3 no activation without named human: enforced for cards; no assessment step existed.

## Planning Readiness

Ready. Research disposition: executed. Open items: real owners, interpretation authority and source effective dates need owner/Legal evidence; communications, templates, reports and journeys mapping is not modelled.
