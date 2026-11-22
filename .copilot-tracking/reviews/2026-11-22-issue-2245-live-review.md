# Review: issues 2245 and 2243

One review, executed after implementation. Outcome: conformant for the code scope with open routed items.

## Assessed

* The suspension control is unchanged; only its reported reason and wording changed. Denials other than a suspension still give `activation-not-approved`.
* `expires_at()` fails closed on unset, invalid, naive or non-UTC values; the 2026-11-01 default is kept.
* Targeted tests, mypy and ruff pass as recorded in the changes record. No web files changed.

## Findings routed to later work

1. SUS-1 owner decision (restore or approved removal), then roll the employee image and rerun `probe_chat.py` for "Model calls: 1".
2. Extend `resident_ai.budget.expires_at` via a private SQL path, then rerun `probe_resident.py`.
3. Unexplained first-POST 500: needs readable logs.
4. Python `EXPIRES` in `resident_generated_answer_browser_check.py` still uses the default constant.

## Ranked follow-ups

1 and 2 deliver the demo's key AI proof; 3 is lower value; 4 is cleanup.
