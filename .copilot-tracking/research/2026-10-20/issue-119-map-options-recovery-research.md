<!-- markdownlint-disable-file -->

# Task Research: issue-119-map-options-recovery

| Field | Value |
| --- | --- |
| Date | 2026-10-20 |
| Researcher / agent | rpi-research (actual skill invocation in the coordinator-intervention continuation) |
| Status | Complete |
| Research disposition | executed |
| Artifact path | .copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md |

## Process disclosure

An earlier worker pass authored the draft commit 69fa487a, the files named
`issue-119-map-options-*` under `.copilot-tracking/`, and a rubber-duck critique
WITHOUT activating the rpi-research, rpi-plan, rpi-implement or rpi-review
skills. Those artifacts are preserved unchanged as pre-RPI, unverified draft
material and are not an executed RPI loop or an accepted outcome. This recovery
research is the first genuinely skill-driven phase. Its web reads below were
repeated or newly made in this continuation; other draft claims are reused only
where re-verified here and are labelled so.

## Research Brief

* What to research: current, sourced map tile licence, cost and privacy options
  for the existing env-configured map; whether a real screen-reader check of the
  list alternative is possible; verify the draft claims.
* Why it matters: owner direction in #126 comment 6290697705 (research for
  review, retain accessible list, no purchase, no private coordinates on the wire).
* Scope: docs and protocol only; existing code read-only. Non-goals: provider
  selection or approval, purchase, UI redesign, edits to infra runbook, budget,
  form schema or cohort docs.
* Criteria: official source with date; claims not verifiable stated as such.
* Output mode: analysis (comparison of options; no selection). Prepares planning: yes, when Ready.

## Research Parameters

| Field | Value |
| --- | --- |
| Posture | focused (bounded, named sources); provenance: default |
| Explicit limits | no private coordinates in any request; no purchase; no push |
| Edits allowed during research | no (this file is the only write) |
| Evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | repository AMA instructions (docs-only, knowledge-base index and log, regulatory claim dating) | selected |
| Skill | web-design-guidelines and design skills | skipped: no web edit is planned; revisit if plan needs a UI edit |
| Specialist | RPI Researcher | skipped: three small inline lanes |

## User Participation

No interaction: the owner direction and coordinator contract are sufficient.

## Prior Knowledge Gate

* Draft reviewed (unverified): docs/reference/research/ux/map-tile-provider-options.md, wcag-conformance-baseline.md protocol section, ADR 0002 delta, index and log entries.
* Reused after verification: C1, C2, C3, W1, W2.
* Not reused as fact: any vendor price from a secondary summary (W3, W4).

## Research Cycle Log

### Cycle 1

Wider: enumerated provider families (public OSM, Azure Maps, OS Maps API,
MapTiler, self-hosted); Google, Mapbox, HERE, Esri and Stadia remain explicitly
not reviewed (scope and time, not rejection).

Deeper: re-read code and vendor policy pages (evidence below).

Contrarian: sought evidence that weakens the draft. Result: web search summaries
for OS pricing (W3) quote a leisure-scale rate of GBP 0.000525 per 15-tile view
that differs in kind from the draft's premium GBP 0.0331, and the free-allowance
wording is a secondary AI summary. Azure DPA claims (W4) are likewise a secondary
summary that says the DPA applies and Microsoft is typically processor. Neither
is official terms. Both stay unverified and must not be written as established.

Parent synthesis: accepted C1-C4 and W1-W2 as evidence; deferred W3-W4 to owner or
procurement verification; rejected any claim of a recommendation or selection.
No further cycle: remaining gaps need signed-in or JS-rendered vendor pages or
legal review, not more public fetches.

## Evidence Log

| ID | Evidence | Source |
| --- | --- | --- |
| C1 | `tile_config()` reads `ZF_TILE_URL` (https only) and `ZF_TILE_ATTRIBUTION`; development default is public OSM; production without a URL returns no tiles | src/api/src/zava_forward/api/server.py:46-57 |
| C2 | CSP `img-src` follows the tile host | src/api/src/zava_forward/api/server.py:65 |
| C3 | The list alternative is a `details.maplist` with `summary#maplist-h` and a labelled `ul`; Leaflet `tileLayer` uses `referrerPolicy: strict-origin-when-cross-origin` | src/api/src/zava_forward/api/web/app.js:1020-1022, 1041 |
| C4 | The accessibility tests are static string and role checks only | src/api/tests/test_accessibility_baseline.py:65, 71 |
| C5 | No screen reader (nvda, orca, espeak-ng, speech-dispatcher) on PATH and DISPLAY is empty; at-spi2-core library only; so no screen-reader run is possible on this host | shell check 2026-10-20 |
| W1 | OSM tile policy: best-effort, no SLA, may block without notice; visible attribution, valid User-Agent, Referer, cache at least 7 days; no prefetch; ODbL data | https://operations.osmfoundation.org/policies/tiles/ retrieved 2026-10-20 |
| W2 | Azure Maps pricing page: free 5,000 base-map tiles; paid rates render as "$-"; prices are estimates | https://azure.microsoft.com/en-gb/pricing/details/azure-maps/ retrieved 2026-10-20 |
| W3 | OS Premium free-allowance and per-view rates: SECONDARY search summary only; not official text | web search 2026-10-20 (https://osdatahub.os.uk/plans unreadable) |
| W4 | Azure Maps DPA and processor role: SECONDARY search summary only | web search 2026-10-20 |

Draft claims about OS Maps API docs, MapTiler and Azure geography/auth pages were
read in the earlier pass and are not re-read here; they remain draft and
unverified for this recovery.

## Findings Mapped to Questions

* Q1 Options and cost: A is free but policy-limited (W1); B has a free tier and unverified paid rate (W2); C and D prices unverified (W3). No figure is establishable from official pages read.
* Q2 Privacy: a tile request is made by the browser and exposes IP, user agent, app-origin Referer and tile z/x/y (C1, C3); no query text or case data is sent. Processor positions for B, C, D are unverified (W4).
* Q3 Screen reader: not possible here (C5). Static tests do not show announcements (C4). Gate stays unmet; protocol only.
* Q4 UI edit needed: no evidence one is needed (C3 shows the list exists and is labelled).

## Alternatives and Decision State

Comparison only (analysis mode). No option is selected, ranked or recommended.
Decisions belong to the owner after the verification gaps close.

## Open Questions, Risks, Residual Uncertainty

* Actual screen-reader result: unmet human or assistive-technology gate.
* Official paid rates, plan terms, attribution wording, DPA and sub-processor positions for B, C, D.
* Whether a tile area is personal data about residents: DPO question.
* Risk: draft wording that implies shortlist or fallback; already neutralised in the draft per the earlier critique, to be re-checked in plan and review.

## Potential Next Research

Signed-in or JS-rendered vendor pages; legal review of DPAs; human screen-reader run.

## Planning Readiness

Ready for a docs-only plan: re-verify and correct the draft against this
evidence, keep issue criterion 2 explicitly open, add a dated clarification
recording the process defect, and reuse no unverified price as fact.

## Self-check

Brief, parameters, evidence IDs, all three waves, disposition and readiness are
recorded; no source edited; no secret or private coordinate used.

## Linked artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md](.copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md) | This recovery research |
| [.copilot-tracking/research/2026-10-20/issue-119-map-options-research.md](.copilot-tracking/research/2026-10-20/issue-119-map-options-research.md) | Pre-RPI draft, preserved |

## Next Steps

Active parent action: invoke rpi-plan for the recovery plan and its single critique.
