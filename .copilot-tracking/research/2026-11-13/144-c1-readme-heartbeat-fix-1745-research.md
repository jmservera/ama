---
title: "#144 C1 README heartbeat fix research"
ms.date: 2026-11-13
---

## Scope

Fix two Medium and one Low finding of the independent review of `00d6a60b2` (focused tier, local tests only).

## Evidence

* `infra/README.md:1338` row "Worker and job images" still says `serve` refuses to start and that the token source, API post-back and wiring are not built. `runtime.py` (`identity_token`, `ApiResultSink`, `build_runtime`) and `worker.main` implement them; without `ZF_AGENT_RESULT_ROUTE=enabled` (omitted in Bicep) `serve` runs a standby loop that keeps the heartbeat. Live deployed pipeline receipt stays Unmet.
* `infra/README.md:1339` says the 120 s limit is "tested only against the idle cadence and the 40 s provider-call bound".
* `test_worker.py` `test_max_age_covers_...` uses literal 40 and `message().timeout`; the pulse runs once per loop iteration, so the test is a one-call sanity check. Production bounds: `IDLE_SECONDS`, `ERROR_BACKOFF_SECONDS` (worker.py), `HEARTBEAT_MAX_AGE_SECONDS` (runtime.py), message timeout cap `1 <= timeout <= 40` (dispatch.py:87).
* `replace_worker` stops only after an ack, so a redelivery regression hangs.
* Inventory `docs/architecture/cutover-reference-inventory.tsv` is regenerated with `python -m zava_forward.core.synthetic.cutover_audit --write` (cutover-evidence-pack.md:1345).

## Disposition and readiness

Research disposition: executed (reused review evidence plus direct reads). Planning Readiness: Ready.
