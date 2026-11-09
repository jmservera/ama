# Review: #1288 C2 (2026-11-08, written 20:28Z)

Execution: one author self-review, after implementation. Not independent; the coordinator assesses the exact head.

Outcome: partial. Light SQLite checks pass; the heavy checks are PENDING, so no conformance is claimed.

## Findings

All five findings and the account-summary name have an implementation and a SQLite regression (see the changes artifact). Each regression fails without its fix: same-bucket arrival and context change, uncited and edited output under withdrawal, manual then proactive and proactive then manual, an unsampled declined control, and future/boundary/old/missing readings.

## Web Interface Guidelines

Rules fetched raw 2026-11-08 20:23Z from the vercel-labs command.md.

app.js:188-190 - pass; `aria-label` now contains the visible text. Native summary, no new handlers.
ops.js:49 - pass; plain muted paragraph, no motion or colour-only state. Dates are shown as UTC strings by design.
ops.js:45-56 - pre-existing, not changed: no `font-variant-numeric: tabular-nums` on the table; routed.
Only app.js and ops.js are changed web files. Axe, keyboard and reflow were not run (PENDING).

## Risks and follow-ups (ranked)

1. After #184 merges: resolve the `sensor_consumer.py` overlap semantically, then run the actual integrated SQL and Chromium/axe tests.
2. Heavy checks on the final exact source, including the per-home index query plan.
3. With a five-minute live feed, ready proposals go stale quickly (honest); consider showing the immutable captured evidence as-of.
4. A matching quality release and serving-model attestation, a finite allowance, at most 100 bindings, and a separate admitted live exercise. A fresh deployment needs the consumer `_schema` or `configure` to run so the control index exists; otherwise consent is unknown and readings are withheld.
5. Tabular numerals in the sensor tables.
