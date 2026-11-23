---
applyTo: '.copilot-tracking/changes/2026-11-23-issue-2313-live-changes.md'
---
# Plan: issue 2313 PR image build job

Details: [.copilot-tracking/details/2026-11-23-issue-2313-live-details.md](../details/2026-11-23-issue-2313-live-details.md). Research: [.copilot-tracking/research/2026-11-23/issue-2313-what-if-research.md](../research/2026-11-23/issue-2313-what-if-research.md).

## Phases

* [ ] Phase 1: add `.github/workflows/infra-image-build.yml` (PR image build, versioned tag, no push, no login).
* [ ] Phase 2: add `infra/tests/test_infra_image_build.py`; run it, the infra suite, actionlint if installed.
* [ ] Phase 3: record per-criterion table, review, commit.

## Decisions

* Leave `infra-plan.yml` unchanged (criteria 1, 2, 4 already met; hash pinned in the gate matrix).
* Do not add the new file to `tools/rpi-checks.py` WORKFLOWS; mention as a follow-up for the owner's gate.
