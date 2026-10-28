---
title: Map fullscreen issue 532 phase details
description: Evidence-based task details and completion expectations
ms.date: 2026-10-28
---

## P01: Map interaction and lifecycle

P01-T01 owns the existing `mapPanel` in `app.js`, not briefing code. Use the
existing `h` DOM helper and permitted map point properties. A placeholder lets
the native dialog temporarily host the existing box, preserving Leaflet state.
The sidebar hosts the same card in expanded mode; embedded card lives above the
map surface, not in Leaflet's transforming marker panes. Keep the dialog named,
close button first-class, title focusable, and `Open home` a native link.
Relevant evidence: research C1, C3, C6-C8, W3-W4.

P01-T02 owns keydown/cancel, marker sources keyed by case ID, and route abort
cleanup. Redraw replaces markers: never restore an obsolete element. Clear
selected cards when their point leaves the returned set, becomes clustered, or
the map request fails. Do not steal focus on ordinary background redraws.
Embedded map clicks must not swallow card actions or marker clicks. Native
dialog focus containment avoids a custom trap. Dispose the map and remove the
dialog before another route renders; session login must also dispose it.
Disable Leaflet animations, including explicit pan and invalidateSize paths.
Map/list controls remain operable without pointer gestures. On every user marker
activation, focus the summary heading so Tab reaches close/navigation controls.
Expanded entry focuses its exit toggle. If selection removal or failure removes
the current focus, focus the named map region inside the current surface.
Same-ID background redraws preserve summary focus or restore a recreated marker.

Implementation-time clarification: summary entry uses ordinary focus scrolling
to reveal the heading in a scrolled sidebar. Native map Arrow/+/- handlers
disable animated pan/zoom, along with drag inertia and marker focus autopan.
The redundant Leaflet tooltip was removed after axe exposed dangling
aria-describedby references on close; native marker title/name and summary
retain the same information. These are current-state refinements within approved
intent, not a significant scope/architecture divergence or new critique cycle.

## P02: Regression coverage and documentation

P02-T01 owns one new `test_map_fullscreen.py` and one
`checks/map_fullscreen_browser_check.py`. Reuse the constructed real-server
harness; no private data. Use pinned axe 4.10.3 with the existing SHA-256
integrity contract; abort non-loopback network traffic during application checks.
Do not silently skip axe. Test embedded/expanded pointer and Enter/Space,
Escape ordering, close and map-click focus return, native navigation, list
alternative, stale/failed/filter redraw, coordinator summary omission, route
disposal, 320/390/1280px geometry and reduced motion. Update the existing
design-system browser marker tests to activate summary then link.

P02-T02 updates `src/api/README.md` with controls, fields, unavailable data and
the reproducible check command. No unrelated knowledge-base synthesis changes.

P02-T03 uses isolated `/tmp/ama-532-venv`, created only after the actual missing
Playwright dependency error. Installed src distributions follow repository
instructions. Test fixtures can use the documented test-only PYTHONPATH.
Take nonblocking `/tmp/ama-rpi-heavy.lock` before unit/browser/type checks,
retrying for at most 40 minutes without interrupting another owner. Retain
external output and original adverse evidence. Run targeted API map, design,
accessibility, content and routing tests, new unit checks and existing/new
synthetic browser checks; JS syntax, new-file Ruff line length 100 and mypy.

## P03: Review and local delivery

P03-T01 refreshes Web Interface Guidelines and delegates one bounded independent
Review against issue acceptance and plan. Findings use file:line; preserve the
original outcome, do not repeat Review or claim human AT acceptance.

P03-T02 resolves `gh api user` identity before commits; derive the local
`{id}+{login}@users.noreply.github.com` email from that response for both
author/committer, with Conventional Commit messages and the requested Copilot
trailer. Stage only owned changes.

P03-T03 fetches origin/main read-only and records full-gate prerequisite evidence
without running any az command. If the required runner invokes az, preserve a
local commit and block publication. Prepare exact stacked PR text using
`Refs #532` and dependency PR #529; do not push merely to create a PR while
publication is blocked. Coordinator owns publication in that case. Preserve the
original one-time RPI Review, commit the final source and dated evidence, then
run the complete gate only when every prerequisite is available and permitted.
Retain a new external receipt. Fetch main and verify the receipt against current
origin/main immediately before independent exact-head assessment and push.
Any later candidate/base/input/tool/image change invalidates that gate.
The original RPI Review is not the later exact-head publication assessment.
The current remote parent has diverged from the supplied local ancestry.
Coordinator owns authorized stack reconciliation before that gate; this task
does not merge, rebase or rewrite history to follow a moving parent.
