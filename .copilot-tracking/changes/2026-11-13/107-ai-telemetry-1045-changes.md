# Changes: #107 AI telemetry raw-content exclusion (107-ai-telemetry-1045)

Tracking-only; no `src/` or `docs/` edits. Base `3b05143179f83235c5b4e80e70aad99bdc44d83f`. Refs #107, #159, #108, #104, #891.

## Evidence preserved

* 14 `.copilot-tracking/*/2026-11-13/demo-ai-*` files copied byte-identically from `bdecadacfc61eefaa639e04abe8d0c185f4486f6` (read via `git show`; source worktree not modified). Verified with `sha256sum -c` against hashes of the source worktree files: 14 files, 0 mismatches. The original adverse `6cee25347` BLOCKED record is preserved in them.

## Execution (isolated `/tmp/venv-107-1045`, removed afterwards)

* `pip install --no-build-isolation --no-deps -e src/core -e src/agents`: exit 0 (setuptools and wheel upgraded with `--find-links /home/azureuser/.cache/pip`, exit 0).
* Module origins (all inside this worktree): `zava_forward.core.ai_consumption`, `.assistants`, `.chat_panel` under `.../child-107-ai-telemetry-1045/src/core/src/zava_forward/core/`; `zava_forward.agents` path under `.../src/agents/src/`.
* `python -m unittest -v test_ai_consumption test_chat_panel` from `src/core/tests` (PYTHONPATH unset): Ran 79 tests, OK, 0 skips, producer exit code 0 (status file, not a pipeline).
* Sentinel probe: script [107-ai-telemetry-1045-probe.py](107-ai-telemetry-1045-probe.py), sha256 `d1cbc244e2458db2525eb0973bdfcb1fb57ece632abc0aca87336c97e9bd3832`, producer exit code 0, 43 recorded entries (a mix of scans and assertions), 0 sentinel hits. Ledger cleanliness is partly by construction: ids and proposal ids go through `reference()` hashing and `usage()` drops unknown keys, so this shows allow-listing at those points, not absence of every raw channel.

## Probe result

* Ledger: for all five `REGISTRY` assistants, reserve, complete (usage dict carrying extra sentinel keys), output (sentinel proposal id) and accept. Ledger events and `report()` contain none of the three sentinels. `by_capability` attributes tokens per assistant (5 entries) and per accepted proposal (`tokens_per_accepted_proposal` "120" each); every completed event had nonzero tokens. Raw sentinels as `CallContext` ids are refused with `ValueError` (tested separately).
* Envelopes: `assistants.shape_result` with sentinels in provider text, extra usage keys, extra fields and `meter_id`: envelopes and failure message clean for all five assistants.
* Chat: a model-running turn (`ModelReply` with usage, model called once) and an over-limit turn (model not called, `model_calls=0`): receipts and `chat.*` audit entries clean.
* Sentinel model in `complete` triggers the model-mismatch hold path; the ledger stays clean.

## Residual gaps and findings (not hidden)

* Finding: `shape_result` passes `provider`, `deployment` and `model` through as free strings (provider, deployment, outcome and source truncated to 120 characters; model only rejected above 512 characters by `bounded_model`). Sentinels placed in provider and model DID appear in the envelope in the probe; `deployment` is by code reading only, not probed. They are provider or configuration identity, not a case-content channel, but they are not structurally allow-listed; hardening is a follow-up, no `src/` change made here.
* The chat probe produced no `meter_root` (no authorised price or budget in the synthetic store), so chat ledger events were not exercised; chat is covered at receipt and audit level only.
* Full `Assistants.execute` end-to-end on a SQL store, task-event rows and accepted-proposal review through the real assistant path were not run (budget); only the pure `shape_result` and `Consumption` ledger paths were probed.
* The text-failure path never produced a valid proposal output through `shape_result`, so that function's success path was not scanned.
* RAI criterion of #107 is not addressed here; criterion closure needs human review of these gaps.

## Review corrections applied

* The `meter_id` sentinel only proves 64-hex rejection. The chat scans cover the `consumption` receipt and `chat.*` audit entries only, with no non-empty assertion on the audit list. The `failure text generic` check is weak when a proposal output is produced.
* Claim limit: no sentinel leaks on the paths probed; the #107 criterion is NOT proven closed and the gaps above remain.
