# Plan: employee chat skills recheck (#530)

* Research: [research](../../research/2026-11-01/employee-chat-skills-530-recheck-research.md)
* Tier: focused. Local runs are indicative; CI is the evidence. No SQL, no live site, no Azure.

## Phases

* [x] 1. Pip venv, editable core/agents/api.
* [x] 2. Core chat tests, agents chat model tests, API chat panel and widget focus tests.
* [x] 3. ruff check, ruff format --check, mypy for core, agents, api.
* [x] 4. Employee chat browser and pinned axe check.
* [x] 5. Record tracking set and knowledge-base log entry.
* [x] 6. Commit, push, PR with `Refs #530` naming the unmet live criterion.

## Critique (single pass, direct dispositions)

* Risk: claiming closure from local checks. Disposition: `Refs #530`; criterion 8 unmet.
* Risk: duplicating prior verifications. Disposition: record only the delta (fresh run on 51657d30); no source change.
* Verdict: proceed.
