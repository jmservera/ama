---
title: RAI reliance review fixes phase details
description: Implementation and validation boundary
ms.date: 2026-10-15
---

## P01 / P01-T01

Current evidence is sufficient: reproduce RV-001 with AI off in SQL/JSON,
including summary/document records, cached briefing and priority; preserve
template/manual reviews and rejection. Register fast/strong routing for six
retained tasks and select current route on reliance, never historical alias.
Require a nonempty valid exact reference and current selection. Exercise fast
and strong route changes on cached/view/review paths; renewal cannot revive old
outputs. Denied configured fallback must not hide a later approval at unchanged
store version. Own all regressions in existing API release test file; at most
eight test methods, no new modules, removals or schema changes.

## P02 / P02-T01

Run targeted API release tests first and capture failure evidence before fixes.
Full API validation identified coupled offline harness setup that supplied no
release reference. Existing core test support and agents scripted output harness
now explicitly provide labelled offline references; no production JSON bypass,
golden evaluation changes, new helper or extra test methods. Include agents
suite/static checks because this existing harness is affected.
Then from src/core run /tmp/zf164/bin/python -m unittest discover -s tests -q;
from src/api run the same with PYTHONPATH=../core/tests:../agents/tests.
Run /tmp/zf164/bin/ruff check ., ruff format --check . and mypy in both
projects. Restore missing packages with pip only after a missing-module error.
Record each actual outcome and skips in changes; no live-service claims.
Update owning README with inference-off, route and cache behavior.

## P02 / P02-T02

Perform one bounded independent post-implementation review against plan and
recorded results. Route newly open work instead of another fix/review loop.
Commit scoped artifacts and source changes with privacy-safe identity and
required trailer, push same topic, update Refs #219 PR 315 with open RV-004
criteria unchecked and mark ready after engineering acceptance. Do not merge.

## Starting State and Boundaries

Clean correct branch at intake; origin/main conflicted only in the log, resolved
with owner-specified script and merged as 80143a9. Existing review remains
historical, unchanged. No product decisions or active engineering blockers.
RV-004 is an explicit excluded acceptance follow-up, not fabricated approval.

## Completion Evidence

P01/P02 complete. Single critique Complete/Pass; single post-implementation
Review Complete/Conformant for RV-001 through RV-003. Fixes committed as 0d44f03.
Main advanced during validation; merged a6e26fe normally in 266f292, resolving
only append-only log with /tmp/reslog.py and preserving both added API README
sections. Reviewed core guards/tests/harnesses unchanged by that merge.
Revalidated merged API: 492 run/98 skipped, ruff/format pass and mypy 36 files;
merged app.js module syntax passes. Prior final core 312 and agents 70 pass.
PR 315 pushed/updated/ready with Refs #219; no new PR, main push or force push.
Merge state CLEAN at publication, no CI result yet. RV-004 remains open; no
actual provider, platform or human acceptance supplied.
