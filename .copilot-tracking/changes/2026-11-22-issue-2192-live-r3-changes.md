---
title: Issue 2192 changes (round 3)
date: 2026-11-22
---

Tier focused; no src edit. Classification basis: live Azure change limited to the image of one Container App in resource group `ama`, owner-authorised; no Bicep, secret, role or network change left behind (registry readback Disabled, Deny, no rules, exports disabled).

## Changes

* Azure: `ca-resident-demo` revision 0000020 to 0000021, image `zava-resident-demo:2192-0696d9446`, digest `sha256:3066f40840ec84050490c9533e9d4b08f33026f8371a5c94e68fd3ea05d428b7`; only the image differed. Rollback digest `sha256:39348ec9881fd9f04196a4bc839266e7f13a14d0f7e1114373773d5db22e9bc3`.
* Docs: `docs/reference/research/issue-2192-live-r3-2026-11-22.md` and its folder (probe script, raw output, screenshots), `infra/README.md` section, index and log entries.
* Cleanup: no throwaway Azure resource created; the local image tag remains in the local Docker cache only; test resident left unticked (initial state).

## Validation

* Live Playwright: employee state for `ZF-2025-0029` was `consent-withheld`, then `ok` (12 readings) after the resident ticked, then `consent-withheld` after unticking.
* Hosted CI not observed; no push. No tests re-run (no source change).

## Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Plain-language consent text | Proven | `test_content_standard` (round 2); live page text |
| Native checkbox, keyboard, WCAG baseline | Proven (engineering checks and live desktop keyboard run); person-run AT not needed for the demo | `live_probe.json` |
| Withdrawal takes effect, employee view shows withheld | Proven live on revision 0000021 | research note table |
| Audit entry | Proven locally; Azure SQL rows not read (unproven live) | core test; no operator SQL principal |
| Tests | Proven in round 2; not re-run here | no source change |
