# Plan: issue #232 server-side cross-home choice queue

* Phase 1: `Store.resident_choice_queue` (role gate, open homes, paged, projected via `detail`), route and `projection.STAFF_GET` entry.
* Phase 2: `resident-choice` screen reads one request instead of N, shows "N of total", unknown on failure (no resident contact, no controls).
* Phase 3: tests (core store, API route, endpoint inventory, node screen tests) and browser check panel scroll fix.
* Critique (single pass): the endpoint must not bypass redaction (applied: reuse `detail`); denied roles must get 403 (applied); failure must read Unknown, not empty (applied). Verdict: proceed.
* Details: [details](../details/2026-11-03-issue-232-choice-queue-projection-details.md)
