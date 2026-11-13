# Details

* `safe_identity(value, limit)`: `type(value) is not str` -> None; len > limit -> None (model) ; value == "offline-extractive; zero model calls" -> kept; regex `[A-Za-z0-9][A-Za-z0-9._:/@+-]*` full match and no `(^|[^A-Za-z0-9])sk-` -> kept; else `unverified-identity`.
* Provider/deployment: `[:120]` then `safe_identity(..., 120)`; `bounded_model` = `safe_identity(v, 512)`.
* Ledger raw comparison `model != reservation["model"]` unchanged (fail-closed).

Critique revisions: `sk-` rejected anywhere (case-insensitive); type check before slice; add `assistants.sanitize_identity(envelope)` applied in `shape_result`, `complete`, `complete_result`; `_settle_meter` passes None for a rewritten model; release check rejects the marker; `ai.py` `evidence` and `out` sanitise model/deployment.
