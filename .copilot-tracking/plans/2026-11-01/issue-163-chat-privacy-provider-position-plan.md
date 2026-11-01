# Plan: issue 163 provider position and DPO decision pack, 2026-11-01

Research: [research](../../research/2026-11-01/issue-163-chat-privacy-provider-position-research.md)

## Phases

* [ ] 1. `chat_privacy.MODEL_PROVIDER_POSITION`: add `documented_terms` (source URL, source date, retrieved date, status `vendor_documentation_not_dpo_accepted`) and keep remaining open items. Extend `test_chat_privacy.py`.
* [ ] 2. DPIA record: replace the provider section and stale open items with the sourced position; add a DPO and Legal decision pack (questions, evidence, blank decision, owner, date). No decision invented, no retention period.
* [ ] 3. Index entry and `log.md` append (docs/reference).
* [ ] 4. Focused validation: core chat tests, ruff check, ruff format --check, mypy for src/core.
* [ ] 5. Review, commit, push, PR with `Refs #163` naming unmet criteria 2 and 5 (acceptance of the provider position needs DPO and Legal).

## Critique (single pass, self)

* Risk: claiming criterion 5 met. Mitigation: label as documented vendor position, DPO acceptance and deployment-type check outstanding; keep Refs.
* Risk: wording that implies a lawful basis. Mitigation: decision pack lists options for the DPO without selecting.
* Verdict: proceed unchanged; no conflict with owner decisions.
