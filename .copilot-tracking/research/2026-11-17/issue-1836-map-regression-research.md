---
title: Issue 1836 map count and tile fallback regression research
description: Research for committed regression coverage of the map result count and tile-fallback relationship
ms.date: 2026-11-17
ms.topic: reference
---

## Status

* Research disposition: executed.
* Planning Readiness: Ready.
* Base: `origin/main` 9da3fcd0dbc0f148ccc2abc350de3bfd96757392, tree
  40271fe4a14851b4df2b692082610286752309af, branch
  `test/map-tile-status-regression-1836`.
* Validation tier: FOCUSED, provided the change stays test-only (no security,
  permission, deployment, dependency pin, gate semantics or runtime change).
  Basis: only `src/api/checks` and `src/api/tests` files and the component
  README would change; no production file, workflow, Dockerfile, manifest or
  gate tool is touched. Escalate to the full tier if that stops being true.
* HVE behaviour testing: not applicable. The change is ordinary test code, not
  a prompt, agent, instruction or skill artifact.

## Witness disclosure

The first `research-open` attempt (event seq 2) was refused by the phase
witness (`missing persisted artifact evidence: research`) because this
artifact did not yet exist. The refusal is retained as recorded. This file was
created afterwards and `research-open` was retried prospectively (seq 3, ok).
The refusal was not edited, deleted or back-filled.

## Scope from the task brief

Issue #1836 asks for committed regression coverage of the relationship between
the map result-count notice and the tile-fallback notice. Current main already
avoids the old strict-mode failure by using `.first` on `.map-info
[role=status]`, so no production or harness-behaviour fix is needed. The
remaining increment is a committed regression and a full directly affected
harness run. #440 and #1641 are unpublished, independent and not touched.

## Findings

### Markup (src/api/src/zava_forward/api/web/app.js, `mapPanel`)

* `info` and `tileNote` are both `<p role="status" aria-live="polite">`,
  created at the top of `mapPanel` and placed adjacent in the `.map-info`
  sidebar (`sidebar = h("aside", { class: "map-info" ... }, ..., info, tileNote,
  listBox, open)`).
* `renderView` writes the count into `info`: points mode gives
  `"{n} home(s) shown"`, clusters mode gives `"{n} homes in this view, grouped
  into {m} areas..."`, and the coordinator view gives a longer sentence.
* `tileNote` is empty until the Leaflet tile layer emits `tileerror`; it then
  holds the fixed fallback message `"The map background could not load. The
  homes and the list of map areas still work. ..."`. A `load` event with no
  errors since the last `loading` event empties it again.
* The tile layer exists only when `/api/me` supplies `me.map.tiles`. In
  development without `ZF_TILE_URL` that is the OSM URL, and the CSP allows its
  host, so a synthetic fulfilment is a faithful substitute for the network.

### Why the old locator fails

`page.locator(".map-info [role=status]")` always resolves to two elements,
`info` and `tileNote`, in both tile states. When tiles succeed `tileNote` is
present but empty and not visible; when they fail it carries the fallback text.
Playwright's strict mode therefore rejects `expect(...).to_have_text(...)` and
`inner_text()` on the bare locator with "strict mode violation ... resolved to
2 elements". The brief frames the failure as occurring "while the fallback
notice is present"; the spike shows it occurs whenever the second element
exists, which is every time. The fallback state is one of two states in which it
is observable, not a precondition.

### Harness state at the pinned head

* Current `checks/map_fullscreen_browser_check.py` uses
  `page.locator(".map-info [role=status]").first` at three zero-result
  assertions (lines 288, 338 and 342 at the pinned head). `.first` is
  positional: it hides the ambiguity rather than naming the count notice.
* The harness aborts all non-loopback requests (`context.route("**/*", ...)`),
  so tile requests fail and the fallback is present for its whole run. It never
  exercises the tile-available state and never asserts the fallback itself.
* `src/api/tests/test_map_viewport_premise.py` is the existing pattern for a
  focused unit test of this module (FakePage, `unittest`, mypy strict).
* The scenario manifest binds the recipe `checks/workbench_browser_check.py`
  (sha256 9a9755434d07...). The map checks are not in the manifest, so no
  recipe SHA update is needed unless that file changes. It will not.

### Baseline runs on the unmodified pinned head (preserved, not claimed as the new regression)

All logs and outputs live in `/mnt/tmp/ama-run-74bd1fe9-20261117/evidence-1836/`.

| Run | Result | Evidence |
| --- | --- | --- |
| `checks.map_fullscreen_browser_check` with the container's default fontconfig | FAIL: `filter label and focus fit at 390x568` | `runs/baseline-main-map-harness.log` |
| Same harness with a dedicated-runtime fontconfig mapping `system-ui` to Liberation Sans | exit 0, 332 PASS lines, 0 FAIL, 0 skip lines | `runs/baseline-main-liberation-font.log`, `tools/fonts.conf` |
| `ruff check .`, `ruff format --check .` in `src/api` | exit 0 | `runs/baseline-ruff.log` |
| `mypy` in `src/api` (strict) | exit 0, 307 files | `runs/baseline-mypy.log` |

The default-font failure is environmental, not a regression. A diagnostic copy
of the harness (scratch, outside the repository, `diag/map_diag.py`) showed the
failing button's bottom edge at 315.17px against a panel bottom of 315px
(`diag/out3`), a 0.17px difference caused by the container's `system-ui`
fallback (WenQuanYi Zen Hei) having different line metrics from the Liberation
Sans and Arial the CSS stack otherwise falls back to. The container has no
DejaVu or Segoe UI. The font repair is confined to the run's dedicated
fontconfig file; no check, threshold, network policy or axe step changes. This
must be reported as a runtime qualification on every browser run.

### Tooling facts

* Pinned axe 4.10.3 fetched from the CI URL; sha256
  `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` equals
  `AXE_SHA256` (`tools/axe-4.10.3.min.js`).
* Dedicated venv `venv/` with `--system-site-packages`; `src/core`,
  `src/agents` and `src/api` installed editable from this worktree
  (`pip-install.log`); ruff 0.17.1 and mypy 2.4.0 match the dev pins.
* Playwright 1.64.0, Chromium 156.0.8078.4 from `/opt/browsers`.
* Heavy lock `/tmp/ama-rpi-heavy.lock` acquired non-blocking with `flock -n`
  for every browser run.

### Spike (scratch, outside the repository)

`diag/spike_tiles.py` signs in with the synthetic account, selects Point
examples and the zero-result "Residents needing extra support" tile, and runs
two browser contexts. Output: `diag/spike-output.log`.

* Tile-available (tile host fulfilled with a 1x1 PNG, 48 intercepted tile
  requests): count notice reads "0 homes shown"; the second status element is
  empty and not visible.
* Tile-unavailable (tile host aborted): count notice unchanged; the second
  status element is visible with the fallback message.
* In both states the old locator resolves to 2 elements and both
  `expect(...).to_have_text("0 homes shown")` (AssertionError) and
  `inner_text()` (`playwright.sync_api.Error`) report a strict-mode violation.
* `.map-info [role=status]` filtered by `has_text=^\d+ homes? shown$` resolves
  to exactly 1 element; `.map-info [role=status] + [role=status]` resolves to
  exactly 1 element, the fallback note, in both states.
* An earlier spike attempt wrongly showed the fallback on the available path
  because the route handler's default argument was overwritten by Playwright's
  second callback argument. The fix was in the spike, not the app.

## Options considered

| Option | Verdict |
| --- | --- |
| Change only `.first` to a filtered locator in the harness | Rejected alone: nothing would fail if the old locator returned, and tile-available is never exercised |
| Add a focused browser check plus a shared locator helper used by the full harness and a small static guard | Selected |
| Change `app.js` to give the two notices distinct ids or test ids | Rejected: production change, out of the test-only scope |
| Fill the 0.17px gap by relaxing the harness tolerance | Rejected: relaxes a check |

## Planning Readiness

Ready. Open questions: none blocking. Remaining criteria for the coordinator:
independent exact-head review and hosted CI, which this run cannot supply.

## Sources

* `src/api/src/zava_forward/api/web/app.js` (`mapPanel`, `renderView`, tile layer handlers).
* `src/api/src/zava_forward/api/server.py` (`tile_config`, CSP).
* `src/api/checks/map_fullscreen_browser_check.py`, `src/api/checks/design_system_browser_check.py`.
* `src/api/tests/test_map_viewport_premise.py`, `src/api/pyproject.toml`, `.github/workflows/src-ci.yml`.
* `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`.
