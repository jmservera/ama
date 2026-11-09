<!-- markdownlint-disable-file -->
# Issue 189 C2 browser check phase details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/browser-check-189-c2-plan.md).

## P2 Edit

Add to the check, after `stop`, a helper that waits for the completed response rather than static text:

```python
def wait_for_stop_saved(page: Page) -> None:
    page.locator("#simulator-control-notice").filter(has_text="Stop saved and read back").wait_for()
```

Line 154 onward becomes `stop(page)`, `wait_for_stop_saved(page)`, an assertion that `page.locator("#app dl dd").first.inner_text()` starts with `Stopped.`, then the existing file assertion and axe scan. `stop_state` may use the helper in place of its `saved and read back` wait only if behaviour is identical; otherwise it stays unchanged. No change to `simulator-control.js` or any other file.

## P3 Validation commands (from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`, `ZF_*` unset, owned directory `capture-189-c2-browser`, files named `after<N>`)

* `../../.venv/bin/python -m checks.simulator_control_browser_check --axe /tmp/axe-4.10.3.min.js` ten times, each with own stdout, stderr, exit and cmd; each must print 13 state lines (11 states, two repeated scans) and the pass marker.
* Delayed-Stop probe (critique finding 1): a retained external script routes `**/api/admin/simulator-control/stop` with a 1.5 s delay and runs the old wait (must fail deterministically at the file assertion) and the new wait (must pass).
* Unit modules `test_simulator_admin`, `test_live_control`, `test_entra_authoritative`, `test_auth`, `test_design_system`, `test_content_standard` with `-v` (relevant control and role tests).
* `ruff check` and `ruff format --check` on the check file and `mypy` where configured (`pyproject` located first); `node --check` of the two web scripts.
* Manifest and needs-inventory integrity is checked only if a recipe, workflow or inventory file changes; none is planned, so it is recorded as not applicable with its basis.

## P4 Records

Retain baseline and recapture failed logs; write `hashes.sha256` last, run `sha256sum -c`, record the manifest hash in the changes record. Source-equivalence proof against `bd7a3fb8e`: only the check file differs. Web-guidelines current source was fetched before edits; the change touches no UI markup, so a rule-by-rule review of the check file is recorded as not applicable except the page `simulator-control.js` read for text, state and live-region semantics (`role=status`, `role=alert`).
