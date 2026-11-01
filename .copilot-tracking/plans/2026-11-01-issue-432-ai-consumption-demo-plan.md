# Plan: #432 AI consumption metering, demo slice

Date: 2026-11-01. Research: `.copilot-tracking/research/2026-11-01-issue-432-ai-consumption-demo-research.md`.

## Phases

* [ ] 1. Add `src/core/src/zava_forward/core/ai_consumption_demo.py`: constructed SQLite port, scenarios (no price/authority hold; loop/fan-out stop at call limit; synthetic price + authority; completion with tokens; accepted output; report with cost Unknown without billing and synthetic-labelled with billing), `main()` printing JSON.
* [ ] 2. Add `src/core/tests/test_ai_consumption_demo.py` asserting held reasons, exact call stop, Unknown cost, synthetic label, no raw content.
* [ ] 3. Document the command in `src/core/README.md` and log the change in `docs/reference/log.md`.
* [ ] 4. Run focused tests, ruff check, ruff format --check, mypy for `src/core`.
* [ ] 5. Review, commit, push, PR with `Refs #432`.

## Critique (single pass)

Risk: demo fixtures could be read as financial evidence. Disposition: every output carries `synthetic: true` and an evidence label; cost is Unknown without the synthetic bill. Applied directly.
