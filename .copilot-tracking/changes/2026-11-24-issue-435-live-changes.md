# Changes: issue 435 live 2026-11-24

Planned: add `docs/capstone/pitch/tokenomics-model-tier-comparison.md`; link from the pitch README and placement draft; one regression test; research note `capstone-pitch-435-live-2026-11-24.md`; index and log. Tier: focused, no `src` change; rpi-checks not run; hosted CI unobserved (no push). Per-criterion table appended after implementation.

## Implemented

* `docs/capstone/pitch/tokenomics-model-tier-comparison.md` (new), links added in the pitch README and placement draft.
* `tools/test_capstone_pitch_docs.py`: one new test; 6 tests pass; ruff check and format clean.
* `docs/reference/research/capstone-pitch-435-live-2026-11-24.md`, README index row, log entry.
* Tier: focused; no `src` change; rpi-checks not run; hosted CI unobserved (no push). Live Azure and Playwright not used: no criterion needs them.

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Placement decided; deck rebuilt if changed | Proven for the demo (decision 2026-11-13); no deck change, so no rebuild |
| 2 | Mentor confirms meaning | Unproven: needs a mentor statement |
| 3 | Rehearsed in timed route (ticked) | Tick unsupported: computed timing only (99 words, 39.6 s at 150 wpm) |
| 4 | Measured batch authorised, spend authority recorded | Proven for the demo (#432); usage only |
| 5 | Challenged against assessment guide (ticked) | Not re-run this pass |
| 6 | Statements sourced, no price/saving/payback (ticked) | Supported for the new page; labelled USD 0.44 scenario remains per owner decision |
