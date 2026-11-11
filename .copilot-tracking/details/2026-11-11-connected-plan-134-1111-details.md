<!-- markdownlint-disable-file -->
# Details: Issue 134 connected same-home walk (2026-11-11)

Plan: [plan](../plans/2026-11-11-connected-plan-134-1111-plan.md). Evidence: [research](../research/2026-11-11-connected-plan-134-1111-research.md). Nothing here is admitted or run.

## Factory design

* Import path: `sys.path.insert(0, str(ROOT / "src/core/tests"))` as `home_case_browser_check.py` does (lines 17 to 24).
* Instantiate `test_journey_store.StoreJourney("test_store_journey_reaches_financial_closure_in_order")`, call `setUp()` then `journey()`, read the persisted JSON of its temporary Store (`store.data_path` or `store.data`), call `doCleanups()` only after taking `copy.deepcopy(store.data)` (the Store saves to `live_path`, `live.json`, not to the seed file, so never read the seed path). Return that dict from the harness `data_factory`. The harness writes it as the seed and the server loads it because no `live.json` exists beside it. The separate `audit.jsonl` is not served. A pure test asserts the snapshot holds the journey records (an EPC query event for ZF-1, four technical sign-offs states, a resident decision, a quality handover and an invoice) so an empty or seed-only snapshot fails before any browser starts.
* Do not edit `test_journey_store.py`. If instantiation of the TestCase proves fragile, copy the sequence of Store calls into the check instead and say so in the changes record (a duplicated sequence is allowed only if it keeps the same actors and order).
* Staff in the factory output are those of `test_finance_signoffs.STAFF` plus QI-2; emails are `<code>@example.test` lower-case. They are constructed identities.
* The harness serves with `ZF_PASSWORD=synthetic-check`; the check logs in via the form as in the probe `login()`. The probe `login()` waits for the heading "My cases today" or "Your jobs"; confirm that heading exists for each journey role at P1, else write a local login helper.

## Check structure

* A declared `CHAIN` constant: ordered tuples of (login email, role, screen id, title, expected home text markers). Declared, not enumerated from the menu, so the 14th screen cannot break it.
* A pure function `chain_failures(observed, chain)` returning a list of failure strings: wrong home id, missing selected-home heading, status text differing from `expected_status`, link not targeting `#/case/ZF-1`, reset not returning "No home selected.", and any declared required marker for the step absent from the selected-home evidence (the journey-record markers are required, not optional: an empty journey must fail, not be reported as `gap`). `gap` is reserved for the declared deferrals and for a screen proven by P1 to be unable to render a Store field.
* Same-home carry is tested without a reset in between: select ZF-1 on `asset-board`, follow the in-page menu link to `programme-queue`, assert the destination and the retained `case=ZF-1` in the link `href` and the "Selected home ZF-1" heading. The probe's exact-screen link selector omits `case=`, so the check uses a prefix match `a[href^="#/screens?screen=<id>&case=ZF-1"]`. Reset is exercised once per login at the end of its steps, as its own step.
* Conflict wording: after PM-2 resolves SQ-1 the asset screen shows "Reconciled (recorded by a named person)" (role-screens.js line 132), not "Resolved". The programme proof is the panel heading "Connected view for ZF-1" plus the "Same-home step states" table; the table rows do not themselves name the home.
* A pure function `sibling_failures(text, markers)` returning a failure for every ZF-1 journey marker found on the ZF-2 view (negative control). Markers are distinctive recorded values (query id SQ-1, invoice reference INV-100, named person names such as "Quality Inspector QI-2", design version) and the assertion is scoped to the selected-home evidence region (`.screen-evidence`), never the page, so generic words such as "Accepted" and portfolio panels do not cause false positives or false passes.
* "No stage clears another" and "one home, eight stages" are source statements labelled a design hypothesis; the check reports their presence as text only and claims neither state independence nor eight-stage consistency. A state-change test would be a separate admitted scope.
* A pure function `reportable(observed)` that maps each assertion to `observed`, `gap` or `not-run` and never emits "pass".
* Reuse by import from `specialist_keyboard_browser_check`: `expected_status`, `status_contract_failures`, `focus_failures`, `tab_to`, `wait_status`, `ENTRY`, `MENU`, `HOME`, `RESET`. A signature change in that module breaks this check; the pure-helper test selectors catch it.
* Run-only mutation controls (as the probe does): remove the selected-home heading, switch the home to ZF-2 mid-walk, drop the case link target. Each must be rejected by the same assertion the walk uses.
* Marker strings are taken from the screen render functions at P1 (for example "Source conflict", "Signed off on design version", "Accepted", the invoice reference "INV-100"). Do not guess them: read them from `role-screens.js` and record the line numbers in the changes record.

## Pure-helper test cases (few, focused)

* `chain_failures` rejects a status for the wrong home and accepts the exact `expected_status`.
* `sibling_failures` flags a ZF-1 marker present on the ZF-2 text and passes clean text.
* `reportable` never yields "pass" for any input.
* The declared `CHAIN` lists only screen ids that exist in the roles registry text of `role-screens.js` (static read), so a rename fails the test instead of the browser run.

## Prerequisites for a future run (not touched now)

Throw-away venv outside the checkout, `pip install` of the five `src/<project>` distributions from this worktree, confirm `zava_forward.api.__file__` resolves in the worktree; `playwright install chromium` only if missing; `flock -n /tmp/ama-rpi-heavy.lock`; `ZF_BROWSER_SCRATCH` short absolute path (at most 58 bytes) outside the checkout; `ZF_AXE_JS` only if the pinned file already exists (sha256 `880970c0...bb`), else "axe not run"; private HOME for any future plan, no default `~/.zava-forward` dataset and no private `.env`.

## Evidence wording rules for the implementation record

Constructed-fixture DOM evidence; roles are fixture identities; the status text is not AT output; Asset is a proxy; ZF-1 states are those the Store journey wrote; nothing is user validation; the check passes no AC. Keep original/adverse/witness qualifications from the keyboard probe record intact and link them.
