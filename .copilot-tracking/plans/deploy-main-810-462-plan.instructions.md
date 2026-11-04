# Plan: deploy main to the two demo apps (2026-11-04)

* [x] Phase 1: build both images locally from `b0080d4e1` (`src/` context).
* [x] Phase 2: open the registry window, push, restore (bare-IP rule removal), read back.
* [x] Phase 3: `az containerapp update` to digests; warm with `/healthz`.
* [x] Phase 4: verify #810 (request tallies) and #462 (Playwright 320px).
* [x] Phase 5: issue comments, infra/README.md, log.md, PR with Refs.

Critique: executed once, no findings changed scope (ops-only, no code change; no Bicep deployment).
