---
title: Employee expanded-map filters phase details
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 551
* Task slug: employee-map-filters-551
* Plan: .copilot-tracking/plans/2026-10-30/employee-map-filters-551-plan.md
* Research: .copilot-tracking/research/2026-10-30/employee-map-filters-551-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Harden and validate acceptance evidence | Complete | P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Harden and validate acceptance evidence

Existing C1-C6 prove feature already shipped in starting ancestry. Do not
reimplement it. Keep current runtime controls and inspect real behavior.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Extend existing regression and guide

Inside check_expanded_filters' all-flag loop, compare map list hrefs with
the actual API's item IDs, activate each native marker with Enter and read
its selected summary case/link identity, close the summary, then compare the
sorted IDs. Include empty selection. Collapse, verify same original controls,
current flag, text, area and marker set; change to a different flag in the
header and verify state before re-expanding and restoring the loop flag.
Keep focus checks before marker interaction and ensure final loop state remains
support/zero for the existing assertions. Preserve existing race tests.
Retain observed and expected IDs per selection in filters.json.

Dependencies: critique disposition. Targets: existing browser check and guide.
No tests in package; no new runtime attributes needed for test selection.
Completion: diff contains bounded assertions and honest documentation only.
Unresolved: none. Completed: exact-home and all-flag header round-trip blocks
added within the existing loop; guide updated. No runtime source changes.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate locally and reconcile evidence

From src/api, PATH may prepend /tmp/mv/bin to use installed tools:

```bash
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests \
  python3 -m unittest discover -s tests -q
ruff check .
ruff format --check .
mypy
```

Run the existing map browser harness against a newly constructed loopback app,
with pinned axe, under the shared lock. Keep outputs in a fresh external
session directory. Inspect browser geometry/axe reports and screenshots.
Browser admission failure is a blocker, not a pass. Existing broad full-gate
requirements are not replaced by targeted checks. After one independent Review,
commit original evidence and implementation; admit full --all runner only if
it can respect no-Azure/no-credential boundaries. Read-only inspection found
mandatory `az bicep` invocations, so record the full-gate publication blocker
rather than run those commands or change the runner.
Any post-commit gate receipt must stay external; coordinator owns publication.
Completion: commands, exits, evidence pointers, AC mapping, honest gaps and
consistent plan/details/changes/state. No approval checkboxes self-completed.

Completed P01-T02: requested API discovery passed (1379 tests, 320 existing
skips); Ruff lint/format and mypy passed. Actual local Chromium 156.0.8078.4
and pinned axe passed all map checks, including six exact-ID/filter round trips,
320/390/1280px, 390x568 and enlarged-text layouts. Screenshots inspected at
320x900, 390x568 and 1280x900. Fourteen axe states had zero violations and
14 incomplete color-contrast results; no full conformance claim.
External logs and report names are in the changes record.
