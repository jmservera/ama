# Issue 114 live r2 changes (2026-11-19)

Refs #114. Tier FOCUSED; basis: no source, SQL, infrastructure or deployment change. Files: `docs/reference/research/issue-114-live-r2-2026-11-19.md`, `docs/reference/README.md` (index), `docs/reference/log.md`, and these tracking artifacts. No Azure resource created; nothing to delete.

| Criterion | Ticked | Proven/unproven | Evidence |
| --- | --- | --- | --- |
| Per-year audit and ledger digest verification proven by test before reliance | No | Proven by tests (62 OK, 42.9 s); unproven on the deployed image (digest 5368f4e4..., rev 0000033, unchanged) | docs/reference/research/issue-114-live-r2-2026-11-19.md |
| Measured load, latency, cost | Yes | Not re-run | sql-ledger-live-2026-11-18.md |
| Backup, restore, deletion (DH-005) | Yes | Not re-run | sql-ledger-live-2026-11-18.md |

Validation: unittest command in the note (62 OK); markdown link and diff review; mypy, ruff, web checks and `rpi-checks.py` not applicable (no source or web change).
