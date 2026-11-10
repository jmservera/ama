# Research: Registry observation parent transition (2026-11-10, Refs #440 #185)

Disposition: executed. Planning Readiness: Ready. Docs only; no runtime, gate, install, browser, SQL or cloud action.

## Facts (read 2026-11-10 after fetch)

* Start: clean `ffb3e4158f866b15510742c978c427e8f308b1f6`, parent `6119b7aa3`.
* `origin/main` is `eff05737e8eaed584f3c269754d45bc5e44d0168`, tree `d486dc8837a7d765438500813feab227d5b574f3`: PR 1396 squash merge on top of `6cc59776666620309fb6b67ad2fdafb343d40998`. It is a descendant of `6cc59776`.
* Between `6cc59776` and `eff05737` only `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md` and `.copilot-tracking` files changed. Subtree ids are identical at both commits: `src` `af889a4f05a2a3f20ea25ff55237fd41a7188c20`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7`, `tools` `432a4e8f7d74f26e88a55dd937c9c6f193016da9`, `.github` `220ca5404c8aeef36da1c27d9ab8833da3d2ca2c`. So the Registry adapter source at the pin is unchanged on fresh main; this proves source identity only, not runtime acceptance on `eff05737`.
* The three docs files at `eff05737` have no diff against the former parent head `6119b7aa3` (squash content equals the parent), so the topic and main differ only by my appended Registry material.
* `git merge-tree` of `origin/main` with the topic: conflicts only in the pack and README (both sides appended at end of file); log merges. No product, test, config or infra conflict.

## Plan basis

Ordinary `--no-ff` merge; resolve the two append-only conflicts keeping main's text and then my Registry section/paragraph after it (both histories preserved). Update only directly dependent wording: the Registry section's declared-dependency sentence and the index and log entry mention that the parent merged as `eff05737`, `6cc59776` stays the historical pin, and fresh main is `eff05737` with equal `src`/`infra`/`tools` ids.

## Boundaries

PR 1395, #109 and #111 integration remain unmerged and excluded; #440 and #185 stay open; no live, credential, provisioning, human or legal approval; bounded offline CONTINUE only. Hosted CI for `eff05737` and independent readiness remain Root's.
