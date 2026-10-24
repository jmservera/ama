<!-- markdownlint-disable-file -->

# Implementation Plan: issue444-resident-feedback-preview

| Field | Value |
|-------|-------|
| Date | 2026-10-24 |
| Research | [research](../../research/2026-10-24/issue444-resident-feedback-preview-research.md) |
| Details | [details](../../details/2026-10-24/issue444-resident-feedback-preview-details.md) |
| Critique | [critique](../../reviews/plans/2026-10-24/issue444-resident-feedback-preview-critique.md) (one final-candidate critique, independent) |
| Branch / base | `feat/resident-feedback-preview-444` / `f1e2d830f17558efd868919de1973ea7244a8841` |

## Objective

Start an inspectable, read-only, loopback-only SYNTHETIC resident preview site next to the employee site, with a server-owned fixture identity, default-deny grants and a positive-allowlist projection over the existing case store. Not a live service.

## Phases

* [x] Phase 1: Core boundary `zava_forward/core/resident_preview.py` (grants, projection, safe-start guards) and `synthetic/resident_preview_fixture.py` (disposable dataset and grants builder)
  * Details: Phase 1 in the details file
* [x] Phase 2: API server `zava_forward/api/resident_preview/` (loopback entrypoint, routes, denial of writes, assets) and the one package-data line
* [x] Phase 3: Resident page assets (HTML, CSS with Fluent 2 token names, JS) with keyboard, focus, error and mobile behaviour
* [x] Phase 4: Tests outside the package: core unit tests, HTTP authorization/isolation tests, browser check on the real server; regression of staff tests
* [x] Phase 5: Documentation (api/core READMEs, knowledge-base index and log), start `ama-444-resident` tmux preview, verify HTTP
* [ ] Phase 6: Independent post-implementation Review, commit, local gate, receipt (separate steps recorded in the changes file)

## Acceptance criteria map (issue #444)

| Criterion | Phase |
|---|---|
| Separate resident HTML/assets and read routes under src; staff unchanged | 2, 3 |
| Explicit disposable dataset path; fixture lineage and limits | 1, 2 |
| Loopback only; refuse prod/cloud/non-loopback | 1, 2 |
| Server-owned identity; no password, selector, URL, header | 2 |
| Default-deny grants, next-request expiry/revocation | 1, 2 |
| Two residents, unknown subject, representative valid/wrong-task/expired/revoked | 4 |
| Positive allowlist and canary isolation | 1, 4 |
| Mapped progress; unknown stays unknown | 1 |
| Offers versus confirmed; viewing changes nothing | 1, 4 |
| Unavailable writes denied and visibly unavailable | 2, 3, 4 |
| Banner "Synthetic preview - not a live resident service"; help route | 3 |
| Real HTTP/browser tests; missing store/authority fails safely | 4 |
| RPI artifacts committed; hosted gates | 6 (local gate only; remote closure is the coordinator's) |

## Constraints

* No edits to `server.py`, `auth.py`, `projection.py`, `store.py`; no framework swap; pip only; no `PYTHONPATH=mvp`.
* Shared files touched: `src/api/pyproject.toml` (one package-data line), README/index/log entries.
* No paid AI, Graph, cloud, tunnel, deployment, or Azure mutation. Heavy gates serialize on `/tmp/ama-rpi-heavy.lock` (owned by the gate runner).
* At most two correction cycles after the original Review; unresolved becomes a human blocker.

## Done when

Focused tests pass, the staff `src/api` and `src/core` suites keep passing, the browser check passes on the real preview server, `ama-444-resident` serves the preview on loopback, Review has no open material finding, and the local gate receipt verifies.
