# Research: classify heldout_aoai.py in the call-site inventory (435 C1, 2058)

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* `src/api/tests/test_ai_call_site_inventory.py` `call_sites()` walks `src/*/src/**/*.py` and flags a file that contains a `chat/completions`, `/openai/deployments` or `/responses?api-version` string constant, or an SDK import or name. `heldout_aoai.py` contains `/openai/deployments/{deployment}/chat/completions` in an f-string (and the plain constant fragment), so it is detected as `agents/src/zava_forward/agents/heldout_aoai.py`. This is the only difference reported by the failing hosted test.
* `INVENTORY` maps a file to `(join status, note)`. Statuses in use: `ledger`, `own-accounting`, `counts-only-sink`.
* `test_ledger_status_follows_the_admission_calls_in_source` requires `status == "ledger"` exactly when the file calls `*consumption.reserve` or `*consumption.dispatch_check`. `heldout_aoai.py` makes no such call (it imports no ledger), so `ledger` would fail; any other status passes.
* `test_ledger_call_is_inside_the_admission_and_completion_path` and `LedgerJoinBehaviourTest` only inspect `core/.../ai.py`; they are unaffected.
* `heldout_aoai.py` is an opt-in adapter that builds the `Call` for `heldout_batch.run_batch`. The runner (`heldout_batch.py` lines 242-317) reserves worst-case tokens and cost per call from an owner authorization with a USD 5.00 hard cap and 50-call limit and charges the worst case on any malformed usage. That is run-local accounting, not the core consumption ledger; the adapter has no ledger, price register or authority. This matches the `own-accounting` definition used for `resident_demo/aoai.py`.
* `counts-only-sink` does not fit: the runner reserves and closes per-call token and cost accounting, not optional counts.
* The cutover pack (`docs/architecture/cutover-evidence-pack.md`) cites the test by name and a historical test count (6); it is a dated observation and is not changed.

## Selected approach

Add one `INVENTORY` entry `own-accounting` for `agents/src/zava_forward/agents/heldout_aoai.py` with a note stating: per-call worst-case reserve and close by `heldout_batch.run_batch` under owner authorization, no core ledger join, opt-in, no network at construction, no live call without explicit flags. No source change to the adapter is required.

## Not selected

* `ledger`: would assert an admission path the source does not have (test would fail, claim would be false).
* Wiring the adapter into the core ledger: out of scope for a CI fix; needs owner approval.
