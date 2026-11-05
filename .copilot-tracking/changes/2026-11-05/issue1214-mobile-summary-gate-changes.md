---
title: Issue 1214 changes record
description: Implementation evidence for the 320px case-summary gate recovery
ms.date: 2026-11-05
ms.topic: reference
---

## Scope Declared

Full plan (P01, P02) for task issue1214-mobile-summary-gate. Branch fix/mobile-summary-gate-1214, base main c6d5a8f3c3a35892322300be27b9747f7b11362d (origin/main refreshed at session start and again before implementation: unchanged).

## Source Change (P01-T01)

* `src/api/src/zava_forward/api/web/style.css`, existing `@media(max-width:600px)` block (line 317): added `.top nav{row-gap:.125rem}`. One rule, row-gap only. No JS, HTML, check or bound change. `static_assets.py` content-hashes assets, so no manual cache bump.

## Root Cause (durable finding)

At 320x800 the check measures the document-absolute bottom of `.case-summary`. The shell header was 526.8px: nine 42px nav links wrapped to seven rows with `nav{gap:1rem}` also acting as a 16px row gap (96px of vertical gap). The summary itself was 754.7px with six safety-relevant items and was left unchanged. Full analysis in the research artifact.

## Geometry Before and After (instrumented Chromium runs, external logs)

| Width | Header height before | after | Nav height before | after | Summary bottom before | after | Summary height |
|---|---|---|---|---|---|---|---|
| 320 | 526.8 | 442.8 | 390 | 306 | 1676.4 | 1592.4 | 754.7 both |
| 390 | 295.2 | 253.2 | 216 | 174 | 1324.0 | 1282.0 | 689.9 both |
| 1280 | 119.2 | 119.2 | 100 | 100 | 662.6 | 662.6 | 346 both |

* Nav link height stays 42px at every width; no horizontal overflow (scrollWidth equals viewport). 1280 is identical. 390 gains tighter nav row spacing (disclosed visual change, existing 600px breakpoint, no new threshold).
* The baseline 390/1280 numbers come from an instrumented run (ZF_SOFT) that records but does not raise the failing 320 assertion, so the run could proceed; its exit 0 is NOT a baseline pass. Logs: /tmp/g1214-impl-1105-before2 and /tmp/g1214-impl-1105-before2.log.
* Focus ring on a keyboard-focused nav link remains visible and unobscured at 320 and 390 (screenshots /tmp/g1214-impl-1105-after-geom2/nav-focus-320.png and nav-focus-390.png), satisfying critique PC-002 and AC5.

## Validation (P02)

* Existing exact browser check, unmodified, via /home/azureuser/.copilot/session-state/b2a93ce0-8f28-4602-817c-cc41227c89e5/files/run-browser.sh (session wrapper, not committed): process exit 0, 407 PASS lines, `PASS 320x800 summary within one viewport scroll (1592.40625)`, bound 1600 unchanged. Log /tmp/g1214-impl-1105-after-final.log, output /tmp/g1214-impl-1105-after-final. The wrapper holds /tmp/ama-rpi-heavy.lock nonblocking for the whole run, uses read-only gate venv `/tmp/g96-c6-1105a/venvs/api` and Chromium `/tmp/g96-c6-1105a/chromium`, scrubbed env, PYTHONDONTWRITEBYTECODE and an external bytecode prefix.
* Loaded paths asserted before the run (first `__path__` entry of each; the editable installs of the failed checkout appear as a secondary namespace entry and were not first): core, api, agents under /home/azureuser/source/ama-wt/issue-1214-mobile-summary/src/*/src/zava_forward/*; check module /home/azureuser/source/ama-wt/issue-1214-mobile-summary/src/api/checks/case_journey_browser_check.py. The 1592.4 result also proves the candidate CSS was served.
* Original adverse baseline preserved: the unmodified candidate base failed the same check, process exit 1, bottom 1676.40625 (/tmp/g1214-research-1105a.log, /tmp/g1214-research-1105b.log, /tmp/g1214-impl-1105-before.log).
* Existing unit tests tests.test_design_system, test_static_assets, test_case_journey, test_accessibility_baseline, test_content_standard with candidate PYTHONPATH and `-B`: 72 tests, exit 0, API path asserted under the candidate. Log /tmp/g1214-impl-1105-unit.log. No bytecode appeared in the source tree (`git status --ignored` shows only the CSS change).
* Not run, with reason: `python3 tools/rpi-checks.py --changed` (the repository focused-tier command). Its API group creates fresh venvs and pip-installs dependencies, which this task forbade (no installs, reuse existing environment, no tooling changes), so running it would breach constraints. Next action for the coordinator: run it with a new external output directory before publication. No full receipt exists or is claimed; no SQL, image, scanner or cloud operation ran.
* No new regression test: the existing 320x800 assertion is the semantic coverage; a CSS constant test would be trivial.

## Plan Reconciliation

P01-T01, P02-T01 and P02-T03 done. P01-T02 (web-guidelines review of changed lines) and the runner portion of P02-T02 remain open and are recorded as such; P01-T02 is completed in the Review phase.

## Follow-Up Items

* Source-bytecode creation during API discovery (separate tooling investigation).
* Header account control row packing at 320 (about 58px headroom) if later changes need it.

## Correction Cycle 1 (2026-11-05, same task; original sections above preserved)

Reconciliation of the original record without rewriting it:

* Actual remaining margin against the unchanged 1600 bound is 1600 - 1592.40625 = 7.59375px. The "about 58px" header account-row packing figure above is an unmeasured possibility, not current headroom, and is not authorisation for further layout change.
* The original statement that P01-T02 "is completed in the Review phase" was inaccurate: that Review's guidelines refresh was truncated. P01-T02 is now completed by the complete refresh in the correction review (two contiguous fetches of the full source, 2026-11-05). Plan markers are reconciled; P02 stays open for the maintained runner only.
* Original RV-001 to RV-003 and the Residual work outcome stay as recorded; the correction review records dispositions without regrading.

### Maintained focused runner (P02-T02 runner portion)

* Inspected, not executed. `python3 tools/rpi-checks.py --changed --base c6d5a8f3c3a35892322300be27b9747f7b11362d` selection for the committed diff (computed by importing `changed_groups` from tools/rpi-checks.py with bytecode disabled, no execution of any group) is: preflight, project-api, namespace, static, browser, image-api, logo-0600. `.copilot-tracking/` paths are inert; the single CSS path under `src/api/.../web/` selects them because the README states runtime/build inputs select consumer images, and the code adds `logo-0600` for API runtime paths (tools/rpi-checks.py `changed_groups`).
* image-api and logo-0600 build Docker images and use Trivy; the correction brief authorises no images or scanners. The runner has no group-exclusion option, and substituting a homemade subset would not be the maintained command. Therefore the runner is NOT run and no partial receipt exists or is claimed. No missing-dependency failure was provoked or required, so no installation occurred. This is a scope-fit blocker, not a source-bytecode finding (the runner was never started, so the separate bytecode issue was not reached).
* Next action for the coordinator: run the README focused command (`--changed --jobs 3 --base <current origin/main> --out <new path of at most 58 bytes>`) where image and scanner work is authorised, then `--verify-receipt <receipt.json> --required-scope partial --base <current origin/main>`; the expected scope is the seven groups listed above.

### Reproducible browser and unit invocation

Maintained check: `python -m checks.case_journey_browser_check --axe <axe-4.10.3.min.js> --out <dir>` from `src/api`, unmodified. Environment reuse is read-only: gate venv `/tmp/g96-c6-1105a/venvs/api`, Chromium `/tmp/g96-c6-1105a/chromium`, axe `/tmp/g96-c6-1105a/axe-4.10.3.min.js`. Its editable installs point at the failed checkout, so the first `PYTHONPATH` entries must be the candidate and the first-source assertion below must pass before the check starts. The heavy lock is held nonblocking for the whole run.

```bash
S=$(git rev-parse --show-toplevel); G=/tmp/g96-c6-1105a; O=/tmp/g1214-corr1-OUT
mkdir -p $O/home $O/tmp $O/cache $O/bytecode
exec 9>>/tmp/ama-rpi-heavy.lock; flock -n 9 || { echo BUSY; exit 75; }
PP="$G/safety:$S/src/api/src:$S/src/core/src:$S/src/agents/src:$S/src/api:$S/src/api/tests:$S/src/core/tests:$S/src/agents/tests"
run() { env -i PATH="$PATH" HOME=$O/home TMPDIR=$O/tmp LANG=C.UTF-8 XDG_CACHE_HOME=$O/cache \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=$O/bytecode PYTHONNOUSERSITE=1 \
  PLAYWRIGHT_BROWSERS_PATH=$G/chromium ZF_STORE=json ZF_DATA=$O/unused.json PYTHONPATH="$PP" \
  $G/venvs/api/bin/python -B "$@"; }
cd $S/src/api
run -c 'import sys,zava_forward.core as c,zava_forward.api as a,zava_forward.agents as g
for m in (c,a,g): assert m.__path__[0].startswith(sys.argv[1]),m.__path__
' "$S"
run -m checks.case_journey_browser_check --axe $G/axe-4.10.3.min.js --out $O/case-journey; echo "BROWSER_EXIT $?"
run -m unittest -q tests.test_design_system tests.test_static_assets tests.test_case_journey \
  tests.test_accessibility_baseline tests.test_content_standard; echo "UNIT_EXIT $?"
```

Notes: no session wrapper, patching or instrumentation is used; the earlier wrapper's `TemporaryDirectory` patch was redundant with `TMPDIR`. The earlier geometry numbers came from instrumented diagnostic runs and are labelled as such above; only this invocation counts as pass evidence. Results for the frozen head are recorded in the next section.
