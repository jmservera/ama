---
title: IoT seed to Quality UI bridge review
task_slug: iot-seed-quality-bridge
date: 2026-11-14
---

## Review (single pass)

Outcome: conformant for the test-only scope; no material findings.

* Determinism: fixed clock and seed; same-seed rows and snapshot digests equal; a different seed differs.
* Parity: home card readings, latest and citation keys equal the AI snapshot source.
* No mutation or network: `sensor_reading`, `cases`, `assistant_tasks` unchanged; provider calls unchanged; `socket.connect` blocked.
* Consent: declined consent withholds values on both surfaces.

## Routed follow-ups

* Add a CO2 channel only if the PRD requires it; the generator, `sensor_view.UNITS` and the card need a separate research and plan.
* Editable installs in the shared env point at a stale checkout; reinstall from the active worktree.
* Human review and hosted CI remain required and unobserved.
