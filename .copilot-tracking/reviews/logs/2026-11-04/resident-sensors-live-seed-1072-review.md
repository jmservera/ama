<!-- markdownlint-disable-file -->
# Review: resident sensors live seed (#1072)

Execution: inline, once, after implementation. Outcome: `conformant-with-open-work` for the documentation change; the issue's acceptance criteria are not met.

* Claims checked against evidence: the walk output, SQL network posture and admin identity, README statements on public access and firewall, and the 2026-10-31 evidence file.
* The 2026-09-30 backfill end and the 24-hour stale rule are source-derived (`sensor_backfill.START`, `DAYS`; the UX specification), not observed live.
* Open work routed to the owner decision: approve the in-VNet run, choose the synthetic window, name the home. A later user-selected `rpi-implement` owns it.
* Human review checkboxes: not completed (owner review pending).
