<!-- markdownlint-disable-file -->
# Research: keyboard probe correction C1 (2026-11-10)

Disposition: executed (source inspection of the existing probe, `index.html`, `style.css`, Root Functional findings). Planning Readiness: Ready.

## Evidence

* Findings (Root `independent-134-keyboard-2016/functional/functional-findings.json`, verdict approve_with_comments, 3 Medium): (1) only entry-link focus visibility is asserted; screen, region and reset booleans are printed only; home and handoff are not measured. (2) `wait_status` checks text only. (3) `REGION` selects only labelled regions, so a lost label or removed region silently shrinks coverage; only the first region is Tab-checked; one negative control on one screen.
* `#workspace-status` is `<p ... role="status" aria-live="polite" aria-atomic="true">` (`index.html` line 40). Global `:focus-visible` gives a 3px outline plus box-shadow (`style.css` line 48).
* Region structure (`role-screens.js` `screenTable`): `div.table-scroll[role=region][aria-label][tabindex=0] > table`. Tables appear only when rows exist, else `p.empty`.
* Prior run (spent, preserved): 38 walks; region reached on resident-choice, hazard-triage, asset-board, programme-queue, technical-queue, safety-lead, data-operator, contractor-job-pack; no region on resident-service-issues, quality-queue, procurement-packages, finance-invoices, finance-funding (legitimately partial; no product tables invented).
* Pins: `src/api/pyproject.toml` and `src/core/pyproject.toml` pin ruff 0.17.1 and mypy 2.4.0; earlier run used 0.17.3 and 2.4.1.
* origin/main `ac962fe6`, three commits ahead of the frozen head; it changes `server.py`, `ops.js`, sensor, `projection.py` and a quality-sensors check, not the screens, `index.html`, `style.css` or this probe. Later movement is checked again at merge time.

## Decisions

* Fix only the probe, its pure-helper tests and register/evidence wording that depends on it. No product change; a stronger assertion that fails on the product is preserved as a failure and gap.
* Boundaries unchanged: fixture roles are not authentication; DOM status is not assistive-technology output; endpoint and handoff markers stay text presence only; no AC or whole-#134 acceptance.
