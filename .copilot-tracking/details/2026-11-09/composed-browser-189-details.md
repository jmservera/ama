<!-- markdownlint-disable-file -->
# Issue 189 composed browser check details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/composed-browser-189-plan.md).

## P2 Preconditions

* `git status --short` empty; `git rev-parse HEAD`; `git diff 825abaa4c HEAD --stat -- src tools infra` empty; hash `live_simulator.py`, `test_live_simulator.py` and `simulator_control_browser_check.py`.
* `git fetch origin main`; `git diff 3a9767d5c origin/main --stat` (expect only `.github/rubric/scores/latest.json`) and the same diff limited to `src tools infra` (expect empty).
* `sha256sum /tmp/axe-4.10.3.min.js` equals `880970c0...a68bb`.

## P3 Holder check and admission

* One read-only look at the holder (`ps` for the lock owner is informational only), then a single `flock -n 9` admission on `/tmp/ama-rpi-heavy.lock` in the command that also runs P4, so the lock is held for the whole browser process tree and released on exit. No queue, no `flock` wait, no loop. Exit 1 from `flock -n` means BLOCKED-BY-HOLDER: record and stop.

Admission sequence (critique 3): `exec 9>/tmp/ama-rpi-heavy.lock` (opens the existing file, no write), then `flock -n 9`; its exit status is recorded alone as the admission result and contention (1) is the only BLOCKED-BY-HOLDER outcome. FD 9 stays open through P4 (browser and both probes) and is closed after, recording admission and release times.

## P4 Check

Critique 1: every Python and pip call uses `$S/venv/bin/python` explicitly (`python -m pip`), never an activated or global interpreter; record `$S/venv/bin/python -c 'import sys,playwright;print(sys.executable,playwright.__file__)'`.

* Owned scratch `S=$(mktemp -d /tmp/issue189-composed-browser-XXXXXX)`; `python3 -m venv $S/venv`; `pip install` (project only): `-e src/core -e src/agents -e "src/api[dev]"` per the CI profile (pins mypy 2.4.0, ruff 0.17.1) plus `playwright==1.64.0` if not in the extras. No global install, no credentials.
* Run from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`: `python -m checks.simulator_control_browser_check --axe /tmp/axe-4.10.3.min.js`. Playwright launches its installed chromium (`~/.cache/ms-playwright`, existing, unchanged).
* Delayed-Stop: copy the C3 `probe_delayed_stop.py` (coordinator capture directory) to `$S`, run `python -m probe_delayed_stop old` and `new` from `src/api` with the same `PYTHONPATH` extended by `$S`; the old wait uses the pre-C2 wait semantics embedded in the probe and must fail (exit 1), the new must pass (exit 0). The probe edits no repository file. Critique 2: the old-probe exit 1 is the expected negative control only when its stdout reports the control still enabled (`enabled ... = True`) and stderr carries the assertion as in C3 `probe-old.*`; any other failure there is a blocker. Critique 4: the probe duplicates the new wait rather than calling the checker helper, so it is evidence of UI synchronisation, not proof that the helper was exercised. Critique 5: sha256 of the copied probe is compared with the original capture file before execution and kept with the evidence.
* Raw output: cmd, exit, stdout, stderr per command copied into a new coordinator-side `capture-189-composed-browser/` with `hashes.sha256`; the manifest sha256 is recorded. The scratch venv is removed only after evidence is copied; evidence is not cleaned.

## P5 Records

Changes record (commands, exits, counts, hashes, SHAs before and after, tier, boundaries), one original Review (read-only, not repeated), state JSON, records-only commit with the Co-authored-by trailer and the local noreply identity, handoff in the coordinator files directory.
