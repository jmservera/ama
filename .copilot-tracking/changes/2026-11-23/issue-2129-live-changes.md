# Issue 2129 changes (2026-11-23)

Tier: focused. No `src` change, so the full tier does not apply.

## Files

* docs/reference/research/issue-2129-live-2026-11-23.md (new) and its three raw evidence files
* docs/reference/README.md (index row), docs/reference/log.md (entry)

## Validation

* `python3 -m unittest tests.test_chat_isolation` (src/api): 35 tests, OK
* `az containerapp show` env names only: no `CHAT_BREAKGLASS_*` setting, app Running
* Hosted CI: not observed (nothing pushed)

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Break-glass attempts audited, including refusals | Proven (local tests; live refusals 2026-11-18) |
| Audited with purpose | Proven locally |
| Live grant with purpose | Unproven: needs a config change on the shared demo, excluded |
| Policy decided, demo basis | Decided for demo (2026-11-03 disclaimer) |
| Policy decided, production (admin role, notification, retention, content access) | Owner-gated |
| Other administrator access to chat audited | Proven by route review (no such route) |

Overall: #2129 box stays unticked. Use `Refs #2129`.
