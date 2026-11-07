---
title: Issue 80 r13 changes, owned installed environment and schema download browser run
description: Original change record for the first installed-environment run of the prepared schema download browser check; no tracked source changed
ms.date: 2026-11-06
---

* Plan: [plan](../plans/2026-11-06-excel-transition-80-r13-installed-browser-run-plan.md). Prospective Research, Plan, Details and the one independent critique were committed as 472ae7dab833aead1357454656084be0c4b289ac (tree 00337a250d32a2f8145499482560f4fe0e551458) before any environment preparation. That is the execution HEAD; it differs from a6bc5af2 only by the three r13 prospective records.
* Tracked source, harness and check changes: none. Only new r13 records are added. All evidence is under `/mnt/ama-gates/e80-r13-r67-1106/`.

## Environment (owned, external, pip)

* Interpreter `/mnt/ama-gates/e80-r13-r67-1106/venv/bin/python`, Python 3.12.3, new venv. Initial import of aiohttp failed (ModuleNotFoundError; `logs/import-initial.out`), which justified installing.
* Pinned hash manifest `src/api/requirements.txt` installed with `pip --require-hashes` (exit 0); `playwright==1.64.0` installed (exit 0); `pip check` reported no broken requirements. No uv, no global upgrades.
* Candidate distributions zava-forward-core, -agents, -api 0.1.0 were built as wheels from a `git archive` of the execution HEAD, outside the checkout, and installed with `--no-deps`. Wheel build attempt a1 with `--no-build-isolation` failed (no setuptools in the venv; logs preserved); attempt a2 with build isolation succeeded. Wheel sha256: core a805e580..., agents f12f47e9..., api e3479417.... This deviates from the guides' editable wording to avoid writing egg-info or build directories into the checkout.
* Import provenance, parent: `logs/provenance-a3.json` (exit 0). `zava_forward.api.server`, `zava_forward.api.auth`, `zava_forward.core.forms` and `zava_forward.core.store` resolve inside the venv site-packages with bytes identical to the checkout files. Attempts a1 and a2 failed because my script named non-existent modules (`zava_forward.api.forms`, `zava_forward.api.form_export`); they are preserved and the script was corrected only in its module list. PYTHONPATH and other PYTHON variables were cleared for the parent.
* Limitation stated: the harness child server still runs with a `PYTHONPATH` to the checkout `src/{core,agents,api}/src` (reviewed harness behaviour), so the server code under test is the checkout source; byte identity of installed and checkout modules above shows the parent and the child run the same bytes.
* Browser: existing Chromium revision 1248 in `~/.cache/ms-playwright`, no browser install. Tool caches, TMPDIR, XDG and `ZF_BROWSER_SCRATCH` external; `PYTHONDONTWRITEBYTECODE=1`.

## Browser run

* Admission: memory available 5761424 kB, `/mnt` 129 GB free, root disk 100% full (1.9 GB free; nothing written there beyond this record), no lock holder (`fuser` empty).
* `run.py` took `/tmp/ama-rpi-heavy.lock` with `LOCK_EX|LOCK_NB`, called unmodified `tools/rpi-checks.py` `worker_limit(1)` (returned 1), and ran from `src/api` with stdin `/dev/null`: `PYTHONDONTWRITEBYTECODE=1 $R/venv/bin/python -m checks.schema_download_browser_check`. Started 14:17:02, ended about 14:17:07, lock released at exit.
* Result: exit 0; 21 PASS lines; final line `COMPLETE: catalogue download (authorized, keyboard) and denials checked; no axe scan here`; stderr empty. Observed: the Retrofit Programme Manager reaches the link by Tab, activates by Enter, downloads `form-schemas.csv` with the catalogue header and one row naming the synthetic schema; support and grants have no working affordance and the direct export returns 403, not an attachment, with no catalogue content. Hashes: stdout f04a30af..., exit 9a271f2a....
* Post-run: no owned server process; scratch directory empty; ignored-inclusive status empty before and after (0 lines); HEAD unchanged; hashes of the check, harness and `role-screens.js` identical before and after; `git diff --stat a6bc5af2 -- src` empty.

## Not performed or not claimed

* No FULL, SQL, container, scanner or model call. No axe scan in this check; no WCAG, assistive technology, Fluent, concurrency, every-list, owner threshold, main or live acceptance. This is the author's local observation, not independent acceptance. FULL on the final frozen head needs a new admission.
