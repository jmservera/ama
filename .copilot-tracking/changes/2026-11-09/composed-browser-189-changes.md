<!-- markdownlint-disable-file -->
# Issue 189 composed browser check changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/composed-browser-189-plan.md). Refs #189 only. Planning commit `6194203d7dc4d022d47beae3fe423f8d972dc962` (tree `464b5c0cb11d610020ab92aacb0a9036f7bd1055`), made before any validation. No source, test, config or schema change.

## Result: planned browser check PASSED (demo-targeted tier, nonqueued, one holder)

Raw evidence outside the repository: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/capture-189-composed-browser/` (runner `run.sh`, per-step `.cmd/.exit/.stdout/.stderr/.start/.end`, `hashes.sha256` 78 entries, `sha256sum -c` all OK, manifest sha256 `2f0275c1743b7af5062b08bb60057e710209d461c569b3aa6a998e6142b03e01`). The manifest was built after the runner finished; `runner.log` is the stdout of the run.

| Step | Exit | Result |
|------|------|--------|
| pre: status, source diff vs `825abaa4c`, axe hash | 0 | clean tracked tree; `src tools infra` diff empty; axe sha256 `880970c0...a68bb` matches the check pin |
| pre: fetch main | 0 | `origin/main` `700bf11e188a9fce05177385019b3d10ba5bb92f`; `3a9767d5c..main` is one file `.github/rubric/scores/latest.json` (4+/4-); `src tools infra` lines 0 |
| admission `flock -n 9` on `/tmp/ama-rpi-heavy.lock` | 0 | admitted at 17:09:28Z, no wait, no queue; FD held through all runs, released 17:10:02Z |
| fresh owned venv `mktemp -d` and `pip install -e src/core -e src/agents -e 'src/api[dev]'` | 0, 0 | playwright 1.64.0, ruff 0.17.1, mypy 2.4.0, azure-iot-device 2.14.0 (declared SDK installed); interpreter proof from the owned venv |
| `python -m checks.simulator_control_browser_check --axe /tmp/axe-4.10.3.min.js` (from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`) | 0 | "Simulator control browser check passed"; 13 distinct states, 13 axe scans, all `violations: []`, 0 "NOT RUN"; stderr one line `http-response POST /api/admin/simulator-control/stop status=503`, identical to the C3 stderr (the intended write-error state) |
| delayed-Stop probe `old` | 1 | expected negative control: `old enabled when wait returned = True`, AssertionError "control still enabled when the wait returned" (the C3 signature) |
| delayed-Stop probe `new` | 0 | `new enabled when wait returned = False`, "new probe passed" |
| post: status, source diff, file hashes | 0 | tracked tree clean, `src tools infra` diff empty, hashes unchanged |

Probe copy sha256 `6c017163...90682` equals the C3 original. The probe duplicates the new wait rather than calling the checker helper; it is evidence of UI synchronisation, not proof that the helper itself was exercised. Pre- and post-run ignored files list is identical (existing caches and egg-info from earlier lanes; the editable install reused them).

## Source and tested identity

* Tested head `6194203d7` (records-only on top of `825abaa4c`); source `src tools infra` equal to `825abaa4c` and to the tested merge `0dea95876` before and after. `live_simulator.py` `5195ff4a...da913`, `test_live_simulator.py` `ccf4cd06...9e78`, checker `b58a105f...5ad21a`, `simulator_admin.py` `ebf939dc...d9293` unchanged.
* Main qualification: historical base `3a9767d5c` versus current `700bf11e1`: rubric data only. No merge or rebase was needed; a merge of current main would change no source tree, so the tested source equals the prospective merged source. Not claimed: hosted CI for any head.

## Boundaries (unchanged, disclosed)

* Five prior C3 browser passes plus this one are evidence, not proof; this run is a single pass on the composed source.
* Source 19 and the 110 Core resident-decision SQL/Azure opt-in skips remain unverified; no actual SQL, cloud, model, private data, global install, credential or live-app activation. Full gate not run (owner demo tier). Web-guidelines review not applicable: no web file changed.
* C1 to C4 spent, one of five remains; no source change, so no correction cycle, no reset.
* The owned scratch venv was removed after evidence was copied; evidence is retained for hash verification.
