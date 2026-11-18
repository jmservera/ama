# Details: issue 114 live evidence

* Phase 1: scripts live_load.py (five sessions, two writers, 60 s warm-up, 1800 s window) and drill.py (erase, restored, cleanup steps run as throwaway Container Apps jobs). Result files hold no credentials.
* Phase 2: note `docs/reference/research/sql-ledger-live-2026-11-18.md`. Criteria C1 to C3 each marked proven or unproven with the reason.
* Phase 3: index row and log entry.
* Phase 4: validation is link and diff review plus python compile of the two scripts and ruff format check on them.
