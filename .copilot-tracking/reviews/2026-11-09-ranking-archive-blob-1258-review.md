# Review: ranking archive Blob JSON persistence (c4, Refs #1258)

* Executed once, independent read-only reviewer (code-review agent), on exact head `3b8320ac6` (implementation
  commit; planning head was `514cdfd2a`, merged main `06e3f2f4` at `c626113`). Static review; the reviewer did not
  run tests. Assessed boundary: `git diff 514cdfd2a..3b8320ac6 -- src`.
* Outcome: no Blocking or Significant findings. The critique PC-001..PC-007 dispositions were applied in the code
  (see the changes record). Review is not repeated in this task.

## Findings

| ID | Class | Finding | Routing |
| --- | --- | --- | --- |
| R-1 | Minor | `_publish_blob` would raise an uncaught `ValueError` from the record-name guard if a registry policy version contained characters outside `[A-Za-z0-9._-]`. The only registry version today is `1.0.0`, so it is not reachable now. | Later work: map the guard to `PublicationError`, or validate version at registration. |

## Own evidence (not the reviewer's)

* Targeted tests green: core 134, API wiring 34, digest_blob 27; ruff and mypy clean on touched ranking modules.
* Mock transport only; no emulator, storage account, immutability policy, role grant, Bicep setting or deployment.
  No crash or Azure acceptance; FULL and production criteria of #1258 stay unticked.

## Routed follow-ups

* Final exact-main integration and affected tests after #1292 delivery.
* Container, WORM/immutability, role grant, deployment env var; migration decision for existing folder records.
* R-1 guard.
