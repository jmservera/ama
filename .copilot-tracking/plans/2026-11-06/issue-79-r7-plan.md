---
title: Issue 79 plan, corrective continuation r7
ms.date: 2026-11-06
---

* [ ] Phase 1 (tests first): add regression tests in `test_ranking_publication.py` (verify and publish) and `test_ranking_publication_runner.py` (schedule, publish, verify) for `"2026-11-31"` and malformed types (`null`, number, list, `"20261105"`, empty string); run them and record RED.
* [ ] Phase 2 (smallest fix): `_valid_date` in `ranking_publication`; validate in `publish` before writing and in `verify` before trusting `published_on`; no runner change unless RED shows it is needed.
* [ ] Phase 3: GREEN on the two ranking publication test files; Ruff `--no-cache`, Ruff format check, mypy with external caches.
* [ ] Phase 4: changes record, dedicated Review, state file, one log entry, commit.

Details: [details](../../details/2026-11-06/issue-79-r7-details.md). Research: [research](../../research/2026-11-06/issue-79-r7-research.md).

Critique (single pass, self-run, on the final design before any edit): the fix refuses at the boundary using the existing `PublicationError` for publish and the existing `problems` list for verify, so the runner's existing refusal and reporting paths apply. No silent catch, default date, schema, policy or retention change. A bad record is never counted toward `latest`, so a damaged archive cannot present as current; `publish` refuses with `archive_unverified` and `schedule` shows problems. Risk: a `verify` caller relying on a bad date appearing as latest changes; none exists in the repository (checked by search before the edit). Findings applied directly; none is significant or divergent. Tier: FULL for the eventual gate; this continuation is light only.
