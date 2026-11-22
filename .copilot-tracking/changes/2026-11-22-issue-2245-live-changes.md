# Changes: issues 2245 and 2243

Status: complete. Refs #2245, #2243. Tier FULL (src changed); `rpi-checks.py --all` not run by this worker, the coordinator owns the gate.

Disclosure: source edits were prototyped before the implement-start witness. They were stashed (`git stash`) while the research, critique, plan, details and this record were written, then restored; the witness itself records the dirty-source qualification.

## Files

* `src/agents/src/zava_forward/agents/chat.py`: `AI_SUSPENDED` outcome.
* `src/api/src/zava_forward/api/server.py`: `chat_admission` and `/api/chat/status` hold wording.
* `src/core/src/zava_forward/core/chat_panel.py`: hold fallback and note.
* `src/api/src/zava_forward/api/resident_demo/assistant.py`, `aoai.py`: `expires_at()` from `ZF_DEMO_EXPIRES_AT`, fail closed.
* `src/api/tests/test_chat_panel.py`, `test_resident_aoai.py`: two regression tests.
* `docs/reference/research/issue-2245-live-2026-11-22.md` and its evidence directory; `docs/reference/README.md` index; `docs/reference/log.md` entry.

## Validation

* mypy clean in `src/api` and `src/agents`; `src/core` has two errors in untouched files (`telemetry.py`, `synthetic/device_provision.py`).
* ruff check and `ruff format --isolated --line-length 100` clean on modified files.
* api `test_resident*` 300, `test_chat*` 159, `test_ai_consumption_api` 40; agents 44; core chat_panel 185. All OK.

## Live changes

* Resident image pushed through `/tmp/acr-push.sh`; registry read back Disabled, Deny, export disabled. `ca-resident-demo` rolled to `--0000022` (digest `sha256:45b517184d47...cff38b`), Healthy. Rollback: `--0000021`, `sha256:3066f4...d428b7`.
* Employee API not rolled. No throwaway resources.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| 2245: which skills and routes call the model, and why none did | Proven (rules-first intents; SUS-1 blocks the rest) |
| 2245: plain statement when answers are rule-based | Proven locally; not live (employee image not rolled) |
| 2245: model-capable question shows "Model calls: 1" live | Unproven: open suspension SUS-1 needs an owner decision |
| 2245: first POST 500 explained | Unproven: not reproduced; Log Analytics denied |
| 2243: expiry from `ZF_DEMO_EXPIRES_AT` with test | Proven |
| 2243: resident image rebuilt and rolled | Proven |
| 2243: resident answers with the model live | Unproven: SQL ledger `expires_at` (probable) refuses; needs an owner-reviewed data change through a private SQL path |

Detail: [issue-2245-live-2026-11-22.md](../../docs/reference/research/issue-2245-live-2026-11-22.md).
