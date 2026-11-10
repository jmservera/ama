<!-- markdownlint-disable-file -->
# Issue 184 IoT demo deployment-readiness metadata slice: details (2026-11-10, Refs #184 #440)

Phase details for [issue-184-cloud-readiness-1110-plan.md](../../plans/2026-11-10/issue-184-cloud-readiness-1110-plan.md). Prospective: nothing below is executed. Research evidence: [issue-184-cloud-readiness-1110-research.md](../../research/2026-11-10/issue-184-cloud-readiness-1110-research.md) Part B (external raw outputs in Root `evidence-184-cloud-readiness-1110/`).

## Phase 1: Resume gate

* Entry: Root states in writing (a) the 108 disposition (merged, or explicit no-KB-change blocked) and (b) that this task may write `docs/reference/README.md` and `docs/reference/log.md`.
* Steps: `git status --short`, `git branch --show-current` (expect `docs/demo-iot-cloud-readiness-184-1110`); `git fetch origin main`; `git diff --name-only HEAD origin/main -- docs/reference/README.md docs/reference/log.md docs/reference/research/iot-sensor-analytics-research-plan.md`; if non-empty, merge `origin/main` into the topic branch (ordinary merge, no rebase or force) only when the owner or Root allows, otherwise stop and report.
* Exit: ownership recorded in state `confirmed_decisions`; anchors re-read.
* Stop conditions: no release; the 108 change edited the #110/#184 README paragraph or the same synthesis section.

## Phase 2: Synthesis subsection (exact content contract)

File `docs/reference/research/iot-sensor-analytics-research-plan.md`, new `###` heading "Current Azure configuration observation (2026-11-10, Refs #184 #440)" at the end of the "Bounded streaming engineering" section. Plain ASCII, `*` bullets, no em dashes, no bold-prefix list items. Required content:

* Scope line: read-only ARM configuration observations of the existing hub, consumer group, demo API app and the two Bicep-declared job names in `ama`, taken 2026-11-10T17:54Z to 17:55Z with five Azure CLI metadata invocations, no retries; no cloud write; not a renewed budget or transport authority.
* Observation table, copying only these values from Research Part B: hub `uksouth`, B1 x 1, Basic, `Active`, `Succeeded`, identity `None`, public network `Disabled`, local auth disabled `true`, 2 partitions, 1 day retention, 0 custom routes, fallback route enabled, 1 private endpoint connection; consumer group `api-consumer` present; API app `Running`, revision `--0000027`, `UserAssigned` identity, digest-pinned image reference, ingress `Http`, `ZF_SENSOR_REVIEW_DRAFTS` not configured; `job-live-simulator` and `job-live-receiver` ARM `ResourceNotFound` (exit 3).
* Interpretation: for the fields both records carry, equal to the 2026-10-29 hub record; the two authored job templates are not deployed under their declared exact names, as their headers state; this says nothing about other or unnamed jobs (including the 2026-11-08 handoff's Manual jobs, historical and unverified); resource existence is not ingestion; is not ingestion; configured digest is not build provenance or runtime proof; no job execution is implied.
* Not claimed or unknown: device registration, certificates, routes to `sensor-readings`, receiver grants, SQL tables, usage, budget (scope ended 2026-10-31 and is not renewed), other jobs including the unnamed Manual jobs of the 2026-11-08 handoff, any Azure acceptance.
* Links: the #440 sensor checkpoint anchor `../../architecture/cutover-evidence-pack.md#sensor-review-wave-actual-main-checkpoint-2026-11-10-refs-440-109-111-184-1288`, `../../../infra/README.md#bounded-existing-hub-exercise-2026-10-29-refs-140-184-137`, and the infra README "Finite demo deployment plan" heading.
* External locators: only the Root session id folder name and file names, no identifiers from Azure.

## Phase 3: Index and log

* README: append 2 to 4 sentences to the existing "For #110/#184" paragraph, linking `./research/iot-sensor-analytics-research-plan.md#current-azure-configuration-observation-2026-11-10-refs-184-440`. State it is a configuration observation only and that #110, #140, #184 and #440 criteria stay open. Do not add a new index row. Append one short clause to the existing per-file row for `iot-sensor-analytics-research-plan.md` (the "In-Use Monitoring Analytics Research Plan" row in the file index, currently line 1009) naming the dated Azure configuration observation, and extend the existing "For #110/#184" paragraph as above.
* Log: one new entry at the end, title `## [2026-11-10] update | IoT demo Azure configuration observation (Refs #184 #440)`, with bullets for what was added, evidence class, query count, what was not observed, and the 108 ordering. Earlier entries are not edited.

## Phase 4: Validation

* Link check: every new relative link resolves and each anchor matches a real heading slug (script or manual grep).
* `git diff --stat` contains only the three KB files plus `.copilot-tracking/` records; no `src/`, `infra/`, `tools/`, tests, workflows.
* Leak scan of the diff and every untracked tracking file for UUID-shaped text, `.azure-devices.net`, `.azurecontainerapps.io`, `.azurecr.io`, `SharedAccess`, `Key=` and full `sha256:` digests (only the abbreviated digest form is allowed).
* Cross-check: Research Part B values equal the external `.out` files, and the Q4/Q5 not-found results and every time and exit code equal the `.err` and `.meta` files; query budget 5 of 8, zero retries.
* Record what did not run: no unit tests, no gate, no hosted CI observation, no re-query of Azure.

## Marker and state obligations for the later stage

* State file `.copilot-tracking/rpi-sessions/2026-11-10/issue-184-cloud-readiness-1110-state.json` is updated before and after each transition; `implement-start` needs a `changes` artifact path and the load_artifacts preflight; no marker is recorded early.
* The same witness log `phase184-cloud-readiness-evidence-1110` is continued, so the qualified partial history (launch, research-open, plan-done) remains visible. A gap between plan-done and implement-start is expected and stated.
