# Issue 1837 details (run c), 2026-11-27

Phase 1: in `nomination_browser_check.py`, after `page.remove_listener("request", watch)` and before the second `fixture.action("nomination_review", ...)`, call `page.wait_for_load_state("networkidle")` so the page's background reads, notably the slow `GET /api/assistants` write transaction, finish before the harness writes.

Phase 2: repeat the check three times plus the related unit and axe runs; record outputs under `docs/reference/research/issue-1837-live-2026-11-27-c/`.

Phase 3: live no-write probe, research note, changes record with the per-criterion table.
