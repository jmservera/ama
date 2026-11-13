# Changes: #107 identity-field allow-list readiness (1143)

Refs #107. Tracking-only; no `src/` edits, no venv, no tests run.

## Related plan

[plan](../../plans/2026-11-13/107-identity-allowlist-readiness-1143-plan.md), [critique](../../plans/2026-11-13/107-identity-allowlist-readiness-1143-critique.md)

## History ledger (#107 spent source-correction cycles)

| Source | Finding |
| --- | --- |
| `gh pr list --search 107` | Merged #287, #293, #863, #915, #1095, #1166, #1253, #1255, #1268, #1271, #1281, #1489, #1495; closed duplicate #860. No PR is labelled a review-correction cycle. |
| `gh issue view 107` comments | Status, closure audit (2026-10-31), exact-head review (2026-11-07), process-race and clamp publications. No numeric spent-correction count. |
| `.copilot-tracking` 107 reviews (20+) | "Correction" hits are plan-critique or deviation corrections; not a cycle count. |
| Demo-run ledger | Line 13 records `3417239f72` Conformant-with-findings, identity-field free strings routed. "Final fifth correction spent" (line 14226) is #233, not #107. |

Documented spent count for #107: NOT ESTABLISHED. Not assumed zero; no grant renewed. Earlier history remains unknown.

## Compatibility matrix (static only)

| Field | Current behaviour in `shape_result` | Literal values in existing tests and sources | Risk of allow-list |
| --- | --- | --- | --- |
| provider | exact str, truncated to 120 | trusted-proxy, scripted, local-test-double, azure-openai, password, `offline-extractive; zero model calls` | Spaces/semicolon value is in a paired-report fixture; reachability to `shape_result` unproven |
| deployment | exact str, truncated to 120 | test, capable, d, standard | Low |
| model | `bounded_model`: str up to 512 | test-model, offline-extractive, none, synthetic, m1, m-1, m, live, other-model, model-id, unattested | Release comparison `assistants.py:1704` needs released `serving_model` preserved |

Other exposed path (critique): `ai.py:200` to `ai_consumption.py:772` also uses `bounded_model`.

## Failing-first specification

* `shape_result` with whitespace-free sentinel `sk-SENTINEL0123456789` and a newline-bearing sentinel in each of provider, deployment, model: output has no sentinel; accepted trusted values preserved byte-for-byte.
* Edge cases: non-str, str subclass, missing, lengths 120/121/512/513.
* Same sentinel through the consumption ledger path, including the raw `result.get("model")` passed to `self.consumption.complete(...)` near `assistants.py:1700`, which bypasses `shape_result` (review finding 4).
* Pre-edit gate: producer/caller trace, then existing core/agents/api suites.

## Readiness determination

HELD for any `src/` edit. Reason: the spent source-correction count for #107 is not established and cannot be assumed below the 5-cycle default, so a source correction grant cannot be shown to exist. The failing-first design above is complete and ready for a future owner-authorized, count-established run. Nothing was executed against source.
