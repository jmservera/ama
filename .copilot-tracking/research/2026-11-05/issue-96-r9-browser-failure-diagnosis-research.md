<!-- markdownlint-disable-file -->
# Research: issue 96 r9 browser-failure diagnosis

Dated 2026-11-05. Refs #96, parent #93. Diagnosis only; no implementation, no gate retry, no receipt claimed. Starting head `38dc133f2251b4d1df6e9035de6f9616300bb523` (clean), main and parent baseline `c6d5a8f3c3a35892322300be27b9747f7b11362d`. The failed receipt `/tmp/g96-c6-1105a/receipt.json` (resume_eligible false) and its logs, snapshot and images are unmodified; nothing was deleted.

## Question 1: baseline or issue 96 regression?

Classification: **baseline failure at unchanged main c6, not caused by issue 96.**

* Failing check: `src/api/checks/case_journey_browser_check.py:1526`, `bottom <= 1600`, measured `.case-summary` bounding-rect bottom at 320x800 after `scrollTo(0,0)`. The bound was added in `6b9e13f98` (#529), not changed here.
* Candidate diff against c6 touches only `src/core` forms, form_review, form_export, their tests and README; `git diff --stat c6d5a8f3c HEAD -- src` lists no `src/api` or web file.
* Baseline execution proof (not source equality alone): a read-only `git archive` of `src/core`, `src/agents`, `src/api` at c6 into `/tmp/g96-diag-main-c6`, run with the existing gate API venv (`/tmp/g96-c6-1105a/venvs/api`, editable installs point at the failed checkout, so module paths were asserted). `run.log` lines 1-3 show every `zava_forward.{core,api,agents}.__path__[0]` under `/tmp/g96-diag-main-c6` (namespace packages; snapshot path listed first) and the assertion passed. Command: `/tmp/g96-diag-run.sh` with `CJ=cj-main-c6`, only the existing exact `checks.case_journey_browser_check --axe <pinned axe> --out ...` under `flock -n` on `/tmp/ama-rpi-heavy.lock` (no holder before or after; `lslocks` empty). Env scrubbed with `env -i`, `PYTHONDONTWRITEBYTECODE=1`, external `PYTHONPYCACHEPREFIX`, `TMPDIR`, HOME, cache.
* Result: exit 1, `AssertionError: 320x800 summary within one viewport scroll (1676.40625)`, identical value to the candidate run (1676.40625). Log `/tmp/g96-diag-out/run2.log`; screenshots dir `/tmp/g96-diag-out/cj-main-c6`. A first attempt (`run.log`) failed only because I pre-created the output directory (`FileExistsError`); it is retained and is not a result.
* The mechanism is rendering, not data: the summary height depends on the web layout and synthetic fixture text; the candidate does not alter either.
* Not a receipt: this is one scoped diagnostic, not a partial or full gate; not the required fresh full run.

Ownership proposal (no issue created or mutated): the failing contract is responsive layout of the case summary at 320px, within the scope of #152 (role workbench information architecture and responsive layout) with the WCAG 2.2 reflow evidence of #151 (both open, read-only view). A web/API lane should decide, under Fluent 2 and the WCAG baseline, whether the layout should be compacted so the summary fits the existing 1600px bound, rather than relaxing the bound, clipping content or skipping the check. Web guidelines skill was not loaded because no web source was inspected or edited. Smallest correction: reduce the 320px case-summary vertical footprint by about 77px (1676.4 to <= 1600) in the original web lane; then a new complete gate against the new main.

## Question 2: source of `__pycache__` in the retained snapshot

Source/log only; no files deleted or modified.

* Retained `/tmp/g96-c6-1105a/checkout/src/{core,agents,api}/src/zava_forward/*/__pycache__` hold `.pyc` files all written within 0.4 s at 10:23:53 on 2026-11-05 (UTC). That is inside the `project-api` `unittest discover` command (`0052-project-api.log` finished 10:34:17; the previous log `0051` ended 10:20:53). No `.pyc` is newer than 10:41, so the browser phase wrote none.
* Cause: during API discovery a test starts a child Python server whose environment is rebuilt from only `PATH`, `HOME`, `LANG` (pattern in `checks/design_system_browser_check.py:244` and `checks/capacity_browser_check.py:821-825`, with `PYTHONPATH` pointing at `<snapshot>/src/*/src`). It therefore loses the outer `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPYCACHEPREFIX`, and imports core, agents and api from the snapshot, writing bytecode beside the sources. I did not identify the single test that launched it; this is inferred from timing, the three affected packages, and the child-environment code, not proven.
* The gate only mitigates later: `tools/rpi-checks.py` lines 2217-2220 write a `sys.dont_write_bytecode = True` `.pth` into the API venv only just before the browser harness, after discovery has run.
* Minimal existing-contract correction (not applied; tooling is not repaired in issue 96): install the same bytecode-policy `.pth` (and `PYTHONPYCACHEPREFIX` equivalent) into the API venv before `project-api` discovery, instead of after it; or make the scrubbed child environments pass `PYTHONDONTWRITEBYTECODE`/`PYTHONPYCACHEPREFIX` through their allow-lists. The first is smaller and stays in `tools/rpi-checks.py`. Route to the gate-tooling lane as a separate RPI.

## Unchanged

Scope, unmet criteria (C1, C5, residual C6, #93 approval) and all earlier outcomes. A fresh complete full run is required after any code or base change.
