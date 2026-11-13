# Critique: #107 identity-field allow-list readiness (1143)

Independent `rubber-duck` critique, executed once. Verdict: Revise.

1. Blocking: a charset pattern is not an allow-list (`sk-SENTINEL...` passes). Disposition: accepted; plan now requires explicit allow-list and a whitespace-free sentinel test.
2. Blocking: raw model also reaches consumption via `ai.py:200` and `ai_consumption.py:772`. Disposition: accepted; plan records the boundary decision and both consumers.
3. Non-blocking: passing suites cannot prove non-reachability. Disposition: accepted; plan requires producer/caller trace.
4. Non-blocking: `pick()` accepts exact str only, so non-str become None. Disposition: accepted; edge-case tests added. Source line verified by critic at `assistants.py:107`.

Count conclusion confirmed: spent #107 source-correction count NOT ESTABLISHED, not zero; HELD follows.
