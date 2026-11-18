# Issue 223 live demo details

* Phase 1 commands: `python3 -m zava_forward.agents.review_effectiveness --json` from `src/agents` with `PYTHONPATH=src:../core/src`; unittest for `tests.test_review_effectiveness` and `tests.test_human_review_effectiveness_223`.
* Phase 2: `evidence/2026-11-18/issue-223-live/live_review_proof.py` signs in with Playwright (credentials read at runtime), calls the app routes through in-page fetch with `X-ZF-CSRF: 1`, redacts emails, writes JSON and a screenshot. Synthetic case ZF-2025-0331; one summary record is left reviewed (rejected) in the demo store (synthetic data, ledger-style, not deletable).
* Phase 3: claims are stated per criterion; nothing is ticked on the issue.
* No Azure resource created, so nothing to delete.
