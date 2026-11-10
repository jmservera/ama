# Plan: aftercare integration current-main checkpoint (2026-11-10, Refs #440 #89 #133 #134)

Research: [research](../research/2026-11-10-aftercare-main-440-1110-research.md). Details: [details](../details/2026-11-10-aftercare-main-440-1110-details.md). Critique: [critique](critiques/2026-11-10-aftercare-main-440-1110-plan-critique.md). State: [state](../rpi-sessions/2026-11-10/issue-440-aftercare-main-1110-state.json).

Tier: focused documentation tier (documentation only). No gate, `--changed`, test, install, image, SQL, browser, cloud, model, live or private-data run. Record the classification: documentation and tracking records only; no workflow, dependency, Dockerfile, SQL, deployment or security-control file changes.

## Phases

* [ ] P1 Append one dated section `Aftercare integration current-main checkpoint (2026-11-10, Refs #440 #89 #133 #134 #1401 #1402)` at the end of `docs/architecture/cutover-evidence-pack.md`: identities, direct tree comparison, consumed evidence attribution, requirement trace, boundary review, inherited findings, evidence classes, exclusions, owners and gates, continue/fix/pivot recommendation, process limits. No earlier section is edited.
* [ ] P2 Add one index paragraph to `docs/reference/README.md` next to the Registry wave paragraph, linking the new anchor.
* [ ] P3 Append one entry to `docs/reference/log.md`; no earlier entry is changed.
* [ ] P4 Verify with `git diff` (additions only outside the new files), link and anchor review, ASCII-only and no em dash check, and that no path under `src`, `infra`, `.github`, `tools` or older tracking records changed.

## Decisions carried into implementation

* Attribute every command result to the original author commands on `b7e46b3be`; nothing is re-run on `64c3f9191`.
* Report the source identity proof as a direct tree comparison and keep the `.github` difference explicit.
* Qualify the 77 authored paths against the 98-path two-dot superset.
* Keep #1401 and #1402 OPEN, not waived, not fixed; source-repair authority BLOCKED.
* Recommendation scope: the bounded implemented staff-assisted aftercare surface only.
* No requirement approval, no ticking of #440, #89, #133, #134 criteria, no new issue.
