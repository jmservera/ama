<!-- markdownlint-disable-file -->
# Validation evidence: PR 1295 main-provenance selected geometry check (2026-11-09)

Additive record for task `pr-1295-main-provenance-hash-repair`, same consumed C5 repair (fifth of five): no source change, new finding, new cycle, sixth cycle or reset. The original [changes](2026-11-09-pr-1295-main-provenance-hash-repair-changes.md) and [review](../reviews/logs/2026-11-09/pr-1295-main-provenance-hash-repair-review.md) are preserved unchanged.

## Wording correction (additive)

The original records say `test-geometry.mjs` was "not run". Accurate wording: the selected check was attempted and failed with exit 1 because the `excalidraw` CLI was absent (`which excalidraw` failed; preserved as `post-test-geometry.mjs.log` in scratch `/tmp/ama-1295-mp`, with the other adverse pre-logs). It was neither waived nor relabelled. This record supersedes that wording only; the failure log stays.

## Dependency verification before reuse

* The skill [.agents/skills/excalidraw/SKILL.md](../../.agents/skills/excalidraw/SKILL.md) declares `@excalidraw/cli` without a version. The repository tracks no lock for it; the earlier owner validation pinned it in an isolated scratch workspace (`/tmp/ama-pr1295-owner-val-2535257/excal`, recorded in [owner-reconcile changes](2026-11-09/pr-1295-owner-reconcile-changes.md)).
* Reuse verified: `package.json` `^0.3.0`; `package-lock.json` sha256 `a240fdb46d27eed04757374f39985576886721f0ab07bf74ad80408e47e220bb` pins `@excalidraw/cli` 0.3.0 and `playwright-core` 1.63.0; `npm ls` agrees; the lock integrity `sha512-KOKe6TjnxKJBM6M3UXi/7/2lT+rTp94I8MM48tSU1Pq/TsGEbmZgY/tuQwJI8IHCse3oMVvOiC4WSa8zvrpQNg==` equals the registry integrity from `npm pack --dry-run`; installed `dist/main.js` sha256 `9d441629b822d6f6e1eb210228d1cc16e6e1f579b402d85035bde70095c26070`.
* Nothing was installed: no global install, no new version, no framework.

## Selected check and same-head checks

Head `2a132a6c964565a2d1465574f5c99e9fb3a6f092`, tracked tree clean before and after. Scratch `/tmp/ama-1295-gv-1794231087` (uncommitted logs). Environment: scratch `excalidraw` 0.3.0 first on `PATH`, `EXCALIDRAW_BROWSER_PATH=/usr/bin/google-chrome` (Chrome 155.0.8059.39), Node v24.21.0. `test-geometry.mjs` sha256 `a6bdfa70a54a09de397677bd68fa4bac5e96553f918573b6fe6642e1cb892e74`.

| Check | Exit | Result |
| --- | --- | --- |
| `node --test docs/capstone/source/diagrams/architecture/test-geometry.mjs` (selected) | 0 | 4 of 4 pass, including the installed-browser label measurement |
| `node docs/architecture/update-architecture.mjs --check` | 0 | pass |
| `node docs/capstone/source/diagrams/architecture/build-architecture.mjs --check` | 0 | pass |
| `node --test docs/capstone/source/diagrams/architecture/test-architecture.mjs` | 0 | 11 of 11 pass |
| `git diff --check HEAD` | 0 | clean |

The legacy metadata-only proof (property delta only at `customData.evidence[*].sha256`, two hashes per SVG, masked bytes equal, no PNG change) is retained. No 55-slide rerender was run.

## Not applicable or not run

* Capstone `Verify` and `Test-SourceHashes` (`pwsh`): not applicable, because no capstone file references the four changed legacy diagrams and capstone references are unchanged; no PowerShell was installed.
* Full gate, Python tests, private data, Azure, models, cloud: not run. Hosted CI for the exact head and independent exact-head closure remain outstanding; nothing was pushed.
