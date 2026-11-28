---
title: Capstone Demo and Recovery Runbook
description: Timed panel demo and optional ten-minute walkthrough covering AI evidence, observability, sensors, staff work and resident self-service, with the 2026-11-21 live demo status and explicit readiness limits
ms.date: 2026-11-21
ms.topic: how-to
---

## Outcome And Timing

Show one fictional home, one evidence conflict, one accountable next action
and the boundary between an AI draft and a human decision. Land that outcome
inside two minutes; do not begin with a screen tour or platform inventory.

The [assessment guide](../../reference/method/ama-capstone-assessment-guide.md)
does not allocate a ten-minute demo slot. B3 requires the outcome to land in
under two minutes; its preparation advice also says to rehearse the demo to
under two minutes. B5 requires finishing inside the slot with room for questions.
The [current capstone plan](../README.md#next-work) separately reserves ten
minutes for the demo alongside a 30-minute presentation, whose narration is
24:30 with 5:30 reserve. That is the repository plan, not a confirmed panel allocation.

Use 00:00-01:50 below as the complete panel demo. Continue only if the panel
has confirmed the separate ten-minute slot: prepared navigation ends at 08:00,
leaving 02:00 for questions or one recovery. The extended route includes the
short demo; it is not another ten minutes. Confirm whether any demo must instead
fit inside the presentation slot before the final rehearsal.

Use S22/page 25 to introduce it and S23/page 26 to close. Do not double-count
the presentation's closing 30 seconds. This runbook is the authored demo script;
it does not change the generated deck speaker notes or their source manifest.

This is preparation, not an executed demo or rehearsal. No cloud, identity,
model, resident-data or workflow mutation is authorized by this runbook.
The [live demo status](#live-demo-status-2026-11-21) below records what was
observed on the synthetic demo on 2026-11-21 and what was not verified. It
replaces the five-home target as the description of the live cohort.

## Explain the Requested and Built Autonomy

Use [page 30's matrix and review](../source/review-2026-11-08.md#requested-versus-built-autonomy)
to describe exact brief fidelity. The case already specified L2-L4 and
professional/resident decisions. The current five helpers are evidence
proposals; a request or approved scan can prepare one without advancing the
case. Do not call that a delivered L3 booking or L4 autonomous quality flag.

For the prepared walkthrough, show the three existing help modes:

* Immediate role queue/next action and the rules label in Today's briefing.
* A source-linked proposal on the same case or in Assistant proposals, showing
  reactive/proactive provenance. Do not enable scans or spend a call to prove
  this without separately approved preflight.
* A prepared follow-up through Ask the assistant, with its explicit skill and
  read-only boundary. Selecting a skill does not invoke the proposal task.

If discussing resident access, show only an authorised synthetic site or its
source contract. Explain that website/chat is an added optional route, not
mandatory works consent. An automatic fictional callback search still needs
the resident's explicit confirmation; it is not an operational appointment.
The 8 November review records Decision 1 as historical scoring evidence with
a pending rebuild, not the five-helper engine. Do not describe the document
reader, a deterministic decision rule or generative chat as Decision 1 without
an attested model/task binding on the chosen build.

That review's Quality autonomy statement is also dated. The
[current core contract](../../../src/core/README.md#retained-sensor-readings-for-employees-and-quality-evidence-refs-1288-107)
defines a current, proactive, source-cited model finding as an L4 review flag,
not human acceptance or delivery to a recipient. The
[21 November retained audit](../../reference/research/issue-1288-live-r6-quality-sensor-evidence-2026-11-21.md)
observed readings for two homes but blocked the Quality model at release admission.
Source capability, dated observations and live-ready authority remain distinct.
Refresh the progress and activation snapshot before the final demo.

## Live Demo Status (2026-11-21)

Refs #2203. This section describes the synthetic desktop demo in the Azure
resource group `ama`, under the owner decisions of 2026-11-18 (synthetic data,
desktop only, live Azure authorised, cap USD 700, no drills, no Key Vault
rotation, no production change). Billing reconciliation, DPO and Legal approval
and person-run assistive-technology testing are not needed for the demo. All
homes, readings and residents are fictional.

Observed means seen on the dated run in the
[live evidence note](../../reference/research/issue-2203-runbook-live-2026-11-21.md).
Not verified means the item was not shown in that run. Re-check each Observed
row in the preflight before use: an observation does not stay true by itself.

| Element | Observed (2026-11-21) | Not verified |
| --- | --- | --- |
| Cohort | 20 synthetic homes feed readings. The employee map lists 10 of them with a fresh reading and 10 with none. The ids are in the [184 note](../../reference/research/issue-184-live-demo-sim-consent-mix-2026-11-20.md) | That the 20 ids are the right homes for the story; a run with the 20-home list read back today |
| Cadence | `job-live-simulator` publishes one reading per home every 5 minutes. Executions at 10:15, 10:20 and 10:25 UTC read `Succeeded`. The newest reading was at most 611 seconds old against the 900 second fresh rule | That the cadence holds for the whole demo window; the receiver reads in 30 minute windows, and its recent executions (07:30 to 10:00 UTC on 2026-11-21) all read `Failed` with the cause not verified; [#2201](https://github.com/jmservera/ama/issues/2201) tracks it, so do not call these runs a designed exit |
| Consent mix | 10 homes granted and 10 declined, applied on 2026-11-20 through repository code. Granted `ZF-2025-0031` shows "Recent reading (within 15 minutes)" with 12 readings. Declined `ZF-2025-0148` and a home with no control, `ZF-2025-0331`, read "Readings withheld: monitoring consent is not granted" | The mix as a count today (it was not re-read); real resident consent, which none of this claims. Controls expire on 2026-12-04 |
| Resident checkbox | The deployed resident page (revision `0000015`) has no sensor monitoring checkbox. The checkbox of #2192 is merged to main as #2197 but not deployed, and is proven only against a local store, see the [2192 note](../../reference/research/issue-2192-live-2026-11-21.md) | The checkbox on the live resident app; it needs an image, a sensor-writing SQL principal and a configuration change that nobody has made |
| Chat routing | The resident "Help with your case" panel offers an own-record permission checkbox, a question box and a skill selector, says each answer states whether AI or rules were used, and says chat does not message staff. `ZF_DEMO_ASSISTANT_ENABLED` is `true` on the resident app | A fresh resident answer in this run, its origin label and the employee chat route; use the earlier dated notes only as history |
| Charts | Staff `#/progress` shows six case-flow charts (opened and closed per day and week, backlog trend, journey step, team workload, AI briefing review outcomes). The resident page shows temperature and humidity history charts over 48 readings with a dashed 24 hour forecast labelled an estimate, plus a table alternative | A sensor history chart in the staff Home sensors tab, which shows the latest reading and a 12 row table until PR #2196 (dual-axis chart and map gauges) merges and is deployed; likewise PR #2198 (half the homes with intermittent readings) and PR #2199 (chat routing) are open and not in main or Azure; any chart accuracy claim |
| Operator-triggered AI scope | Source and the 21 November audit: Quality analysis is not run per reading. The [1288 audit](../../reference/research/issue-1288-live-r6-quality-sensor-evidence-2026-11-21.md) read `proactive: false`, `call_allowance: 0` and a refused Quality model at release admission | The scope today: the forecast request timed out at 90 seconds and `rai-metrics` returned 503 once, so no live trigger is claimed and none was made |
| Offline-sensor alert | The overview map has the filter "Show only homes with stale or offline sensors". No live home was stale or offline. A local test run of 21 tests covers "Sensor may be offline" and the switch at 24 hours | A live offline alert; making one would mean stopping the shared simulator for over 24 hours. Use the labelled fixture or the source contract |
| Role proof | The test staff account reads as Retrofit Programme Manager (app role `ZavaForward.ProgrammeManager`, trusted-proxy sign-in), one of the two roles allowed to see indoor readings | Wrong-role denial from a second staff account (only one exists); the Quality Inspector view |
| Hardening | `ZF_CONTAINER_HARDENING` is `off` on the staff app and both live jobs, unset on the resident app and `enforced` on the agents app, which still runs the image from before the 2026-11-20 fix. A throwaway replica of the current image ran healthy under enforcement on 2026-11-21 ([144 receipt](../../reference/research/issue-144-live-hardening-receipt-2026-11-21.md)) | Enforced hardening on the staff or resident app; the fixed images are not on the shared registry. Do not describe the demo apps as hardened |

Two cautions for the room:

* One run at about 10:34 UTC showed "Home sensors are unavailable right now"
  on both tabs while the same data returned normally a few minutes later.
  Open the tab before the audience arrives and keep the withheld and
  unavailable wording ready as a true state, not an error to hide.
* The readings are synthetic and uncalibrated. The staff view says so; say it
  aloud too.

## Demo Operating Mode And Five Homes (Owner-Selected Target, 2026-11-12)

Superseded for the live demo by the
[live demo status](#live-demo-status-2026-11-21) above: the live cohort is 20
homes at one reading every 5 minutes, not five homes at one a minute. The rest
of this section and the table of five homes are kept as the historical
2026-11-12 target and for the cohort regression test; do not read them as the
current live cohort.

Refs #134 and #184. On 2026-11-12 the owner accepted a simplified demo
operating mode. It was a target. Nothing below is implemented, activated or
observed unless the Status column says otherwise, and it grants no model,
deployment or spend authority.

| Element | Status | What the source says today |
| --- | --- | --- |
| Single-instance simulator start and stop, no SQL tickets | OWNER-SELECTED TARGET | Not verified; the earlier ticket-based design is a proposal only |
| Five synthetic demo homes | OWNER-SELECTED TARGET | The simulator reads every open case id and refreshes the list hourly; a control cohort of listed homes exists |
| One new reading every minute | SUPERSEDED | The live simulator publishes every 5 minutes (see the live demo status) |
| Quality AI restricted to the same five homes | SOURCE IMPLEMENTED, LIVE CONFIGURED 2026-11-22 | Source enforces it when `ZF_ASSIST_QUALITY_DEMO_HOMES` lists the five ids; the staff assistants registry shows the effective scope. On 2026-11-21 the live API app had no such variable, so the live scope was unset (see the [issue 2205 note](../../reference/research/issue-2205-live-2026-11-21.md)); on 2026-11-22 revision 0000045 carried the five ids and the registry confirmed it ([live proof](../../reference/research/issue-2205-live-2026-11-22.md)) |
| Deterministic eligibility is separate from paid analysis | OWNER-SELECTED TARGET | Eligibility does not by itself start a model call |
| Analysis is operator-triggered during the presentation, not per reading | OWNER-SELECTED TARGET | Not verified |
| Eight-hour background limit | LATER RECOMMENDATION | Not implemented and not a timer or authority |

Earlier dated statements of the every-open-case scope and the ticket design
remain historical. The observed and blocked histories in the
[cut-over evidence pack](../../architecture/cutover-evidence-pack.md) stand.

### The five homes

Historical 2026-11-12 target list, not the live cohort. Open each case from the Workbench after authorised staff sign-in. The route is
`/app#/case/<id>?tab=sensors`; the dedicated Home sensors tab holds the sensor
panel on the current source. Quality and handover remains the human review
surface. Case ids are fictional constructed records. Open these only on the
chosen build, and follow the preflight below first.

| # | Case id | Archetype | Property type | Stage in the replayed seed | Direct link |
| --- | --- | --- | --- | --- | --- |
| 1 | ZF-2025-0355 | ARC-01 | End terrace | Quality check | [Open ZF-2025-0355](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2025-0355?tab=sensors) |
| 2 | ZF-2025-0382 | ARC-02 | Mid terrace | Quality check | [Open ZF-2025-0382](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2025-0382?tab=sensors) |
| 3 | ZF-2025-0286 | ARC-04 | Bungalow | Quality check | [Open ZF-2025-0286](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2025-0286?tab=sensors) |
| 4 | ZF-2026-0829 | ARC-05 | Mid terrace | Quality check | [Open ZF-2026-0829](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2026-0829?tab=sensors) |
| 5 | ZF-2026-0892 | ARC-06 | Semi-detached | Funding check | [Open ZF-2026-0892](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2026-0892?tab=sensors) |

Provenance and limits:

* The ids come from a local read-only replay of the committed simulation in
  `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator`, run
  with the documented exercise baseline inputs, seed 20260901 and as-of
  2026-10-13 (see the
  [data pack README](../../reference/research/retrofit-synthetic-data/README.md#mvp-operational-coverage-2026-10-13)).
  The replay reproduced the documented 980 cases and 443 open. That count
  match supports the replay; it does not independently verify these five ids.
  The replay read no private stock register, dataset, roster, credential or
  tenant record. Two local runs were byte identical.
* The ids were chosen by a mechanical rule, not by the owner: open, stand-alone
  building, no safety hazard record, at least one damp report in 24 months, not
  paused, on hold or in aftercare, then the lowest id for each of the archetypes
  ARC-01, ARC-02, ARC-04, ARC-05 and ARC-06 (ARC-03 had none). Home 5 is at
  Funding check, the weakest Quality fit, kept to avoid hand curation.
* A local regression, `test_runbook_five_home_cohort_is_reproduced_by_seed_and_as_of`
  in `src/core/tests/test_generated_dataset.py`, reads the table above and
  checks that the seed 20260901, as-of 2026-10-13 build with the tests'
  fictional register contains each id once, open, with no hazard record and
  the stated property type and stage. A seed, generator or table change that
  breaks that match now fails the test. It does not check the archetype rule,
  damp-report history, direct links, sensors, the simulator cohort, AI scope or
  the private deployed store, so the preflight below is unchanged.
* The deployed store is a private seed output. These ids, their open state and
  their sensor readings may differ there. Source selection is not deployed
  acceptance, and it does not show that any sensor exists for a home.
* The origin is the employee host documented in the
  [cut-over evidence pack](../../architecture/cutover-evidence-pack.md) from a
  2026-10-31 observation. This runbook does not claim it is available now.
  Sign-in is required, and an unauthenticated visit lands on sign-in, not the
  case. If the origin is wrong for the chosen build, use the route
  `#/case/<id>?tab=quality` on that build's `/app` page.

Preflight before any live use (record Pass, Fail, Blocked or Not run as above):

* Each historical id you will show exists in the chosen build and is open.
* For the live cohort, the simulator control lists the 20 homes in the live
  demo status and readings for the granted homes are fresh in the chosen
  build's sensor store. Check these five historical ids only if you will show them.
* The effective AI scan scope is evidenced for the homes you will analyse
  before any analysis is triggered (the `quality_scope` block of `GET /api/assistants` shows mode, ids, trigger and per-reading calls); otherwise use route E (see the route table below), not a live trigger.
* Each direct link opens the right case and tab for the signed-in role.
* Current task-specific authority covers any model call; this section grants none.

## Choose The Route Beforehand

| Route | Required evidence | Opening |
| --- | --- | --- |
| E: repository evidence, default | Inspectable source contracts and explicitly dated observations | "This is a repository-evidence walkthrough, not a current live session or fresh model call." |
| L: live exercise | Exact chosen build, identity/role/case denial, SQL persistence, permitted task and effective finite authority all preflighted | "This is the preflighted Azure exercise using constructed data; I will show only the authorized case and actions." |
| U: unavailable | Neither route can support an inspectable explanation | "The demo is unavailable. I will explain the intended control and missing evidence, not simulate a pass." |

Earlier observations do not make route L ready now. The 25 October window
cannot authorize a new run; later narrow exercise scopes do not automatically
cover the demo, roadmap or Fabric. Confirm current task-specific authority.
Do not repair infrastructure, relax
private access or discover a new live feature in front of the audience.

## Executive Hook

These four beats form a complete 1:50 demo. Pre-open the views and use one
fictional home. Read only the quoted lines; action and fallback instructions
are presenter notes. State route E or L before starting the clock.

| Clock | Show | Say |
| --- | --- | --- |
| 00:00-00:25 | Today's briefing, then the selected case and its next owner | "This fictional home needs attention, but priority is not permission to start work. The employee can see the blocker and who owns the next action. The queue is rules-based; AI suggestions are labelled separately." |
| 00:25-00:55 | A prepared document reading beside its synthetic source, or its source contract | "The document says the installer has finished, but independent inspection is not recorded. AI can help surface that gap. The employee checks the source and prepares the next action; the model cannot accept the work." |
| 00:55-01:20 | Same-home journey strip and Home sensors, or their labelled evidence | "The case connects assessment, funding, resident choice, coordination and quality. Sensor readings add evidence and alerts identify something to check. These readings are synthetic, not a diagnosis. Human safety response never waits for AI." |
| 01:20-01:50 | Separately signed-in synthetic resident view, or its source contract; return to the case | "The resident can look up their own information without first contacting an employee. That is a proposed benefit, not measured savings. Here the blocker and next owner are visible. Test whether this reduces total staff effort." |

For route L, show only equivalent pre-arranged, authorized behaviour. Identify
a prepared model output as recorded evidence, with its actual date and source.
For a template or workflow-only answer say: "This is the manual or rules answer,
not a model response." For route E say: "This is the source contract; this step
has not been demonstrated live." An animation or invented answer is never inference.

## Complete The Prepared Flow

Continue from 01:50 only for the confirmed extended slot. Each window includes
navigation and response time; stop at its boundary even if a model is still
waiting. A missing capability takes its fallback within the same window.
Do not spend the question reserve completing more clicks.

### 01:50-02:35 | Prioritise the employee's work

Action: return to Today's briefing and the same case. Point to its recorded
blocker, owner and next action. If a reviewed AI priority proposal exists,
contrast it with the rule-based queue; do not change ranking during the demo.

Say: "The employee starts with work that needs attention, rather than searching
each spreadsheet. The rules explain the current queue. AI may recommend another
priority from permitted evidence, but a suggestion is not a new ranking or an
approval. On this case, I can see what needs checking and the responsible role."

Fallback: show the source-linked queue/proposal contract. Do not manufacture
a rank change or claim that the queue itself is generated by AI.

### 02:35-03:35 | Upload evidence and check the AI reading

Action: on Documents, use Add document with a short, pre-approved synthetic
text fixture, then select Read with AI only if that task is authorized. Upload
and AI reading are separate actions. Compare the returned text with the source
and the case checklist. A text fixture avoids assuming PDF extraction or OCR.

The rehearsal fixture can contain the following, with the selected fictional
reference substituted before approval. This is invented demonstration evidence,
not a report about the retained case:

```text
Synthetic demonstration record. Not operational evidence.
Case: selected fictional case reference.
Installer statement: work is complete.
Independent inspection: not recorded.
Next evidence required: an independent inspection record.
```

Say: "Storing a document does not make it approved evidence. The reader can
summarise this permitted text; I compare its account with the original. Here the
installer statement and the missing inspection are different facts. If the model
misses the gap or adds a claim, I correct the draft or use the manual route.
We do not claim it finds every fact or every possible issue."

Fallback: use an actual dated reading from the same approved fixture, if one
exists. Otherwise show the reader contract and the manual note. A clean file
scan is not evidence acceptance. Do not label this Decision 1 without verified
task/model provenance.

### 03:35-04:25 | Use the assistant to prepare the next action

Action: open Ask the assistant on the case, select the appropriate advisory
skill and use the approved question below. Inspect answer origin and citations.
Do not assume chat can read the uploaded document: only its permitted case
projection and sources are available. Use the document reader for document text.

```text
Using only the sources available to you, explain the unresolved checks,
the responsible roles and the next manual action for this case.
State what you cannot verify. Do not approve work or change a record.
```

Say: "The employee can ask for help in the case context. I check whether this
answer came from a model or from workflow rules, then open the cited source.
A useful suggestion helps prepare a correction or an evidence request. It
does not fix the underlying inspection gap. The task owner still obtains the
evidence and records the decision."

Fallback: show the actual refused, withheld or workflow-only answer and continue
manually. A reversible draft correction may be demonstrated only on the
authorized disposable fixture; do not save a review or send a request merely
to make the screen look complete.

### 04:25-05:15 | Inspect what happened behind the interaction

Action: immediately after the preceding question, open the pre-arranged Azure
monitoring view only if its correlation to that exact interaction was verified
in preflight. Use an existing monitoring button if the chosen build has one;
otherwise switch to the prepared portal tab. Do not promise a button: no
in-app deep link or conversation-to-Azure receipt was established by this review.

With verified correlation, say: "This trace belongs to the interaction we just
ran. It shows the instrumented request, any linked execution and provider call,
elapsed time and recorded failure state. Where settled token usage is available,
we can inspect it. Tracing does not show the model's private reasoning or prove
that its answer is correct."

Point only to spans actually present. Show the actual window, sampling and
missing data. Tokens are not a monetary cost without applicable price and
billing evidence; Unknown is not zero.

Fallback, required until the Azure path is verified: "The source has opt-in,
content-free tracing, but this conversation's Azure trace is not verified.
Here is the instrumentation contract and the protected audit-to-trace join.
I cannot claim that Azure captured the conversation we just had."

The [monitoring runbook](../../../infra/monitoring-runbooks.md#explicit-otlp-instrumentation-2026-11-16)
documents API/proposal/core-provider coverage, not universal chat or resident
coverage. A permitted investigator locates the protected audit trace ID and
filters the authorized collector; business identifiers and conversation text
are not exported. If chat is uninstrumented, a separately verified proposal
trace can illustrate operations, but it is not this conversation's trace.

### 05:15-06:10 | Read sensors and investigate an alert

Action: open Home sensors as Quality Inspector or Retrofit Programme Manager.
Read the displayed temperature, humidity, observation time, freshness and source
classification. Show a pre-existing authorized alert, its reason, owner and next
action. Do not wait for a new reading or start a simulator.

Say: "These values come from retained synthetic readings. Their time and source
matter: outdoor weather-derived data is not an indoor measurement. An alert
such as a stale reading tells the employee what to check and who owns it.
It does not diagnose damp or prove retrofit success. Quality AI can prepare a
source-cited review finding when released; acceptance belongs to the independent
inspector."

If an actual current AI finding exists, compare its cited reading references
with the authorized capture and identify its model/version and unapproved
status. A rule-derived sensor review draft is not a model-generated L4 flag.

Fallback: show missing, stale, withheld or blocked state honestly. If no alert
exists, use a labelled synthetic alert fixture or the source contract, not
a claim that one fired. The live demo status records that no home was offline
on 2026-11-21. The retained 21 November audit blocked the Quality model; it
cannot establish today's cohort or authorize a live trigger.

### 06:10-07:00 | Trace the full retrofit lifecycle

Action: follow the same-home journey strip and relevant records. Use the
following map as narration prompts, not as six new calls. Show actual recorded
stage evidence where it exists; otherwise identify the missing record or show
a labelled source contract. Never fabricate a completed timeline.

| Lifecycle stage | AI contribution to explain or show | Decision retained |
| --- | --- | --- |
| Stock prioritisation | Evidence-based priority proposal alongside deterministic ranking | Authorized human ranking review |
| Assessment | Document reading and assessment-preparation proposal | Competent assessor/coordinator review |
| Funding | Evidence preparation or an actual unapproved application draft | Finance approval and external submission |
| Resident and contractor coordination | Proposed communication, constraints and next actions | Resident choice and authorized booking/communication |
| Quality | Source-cited evidence proposal; eligible proactive findings only when released | Independent inspection and defect/reinspection decision |
| Handover and aftercare | Grounded explanation of recorded status and unresolved checks | Human acceptance, handover and independent safety response |

Say: "This follows the whole lifecycle, not a collection of unrelated screens.
AI has a preparation role at each applicable stage; known rules and human
decisions stay visible. Funding approval is not an award, an offered slot is
not a booking, and contractor completion is not independent acceptance.
We are tracing records and controls, not completing real works in ten minutes.
Any missing stage evidence remains a disclosed gap."

Fallback: use the same-home process blueprint and name unimplemented or
unverified capabilities. Do not call a proposal-only path delivered L3 action.

### 07:00-07:45 | Let the resident answer a routine question

Action: switch to the separately signed-in synthetic resident view. Verify
in advance that it represents the same home; if not, label it a separate
fixture rather than implying a shared case. Show own-record status and document
facts. For an authorized assistant interaction, obtain the explicit record-use
permission and ask: "Where is my retrofit up to?"

Say: "The resident can look up their own status and document information.
A routine answer can avoid an employee lookup; we still need to measure whether
it reduces contacts and total effort. This is a synthetic showcase, not real
resident enrolment. Record use is optional, login is not works consent, and
phone, letters and officer support remain available."

Fallback: show the read-only resident source contract or the rules answer.
Identify answer origin; do not promise a generated reply, live appointments,
document upload through chat or that a safety report was sent.

### 07:45-08:00 | Close on the business test

Return to the owned next action.

Say: "Test whether reviewed next actions take less total effort and residents
avoid routine contacts. This demo does not establish savings."

### 08:00-10:00 | Questions or one recovery

Stop prepared navigation at eight minutes. Restate the question, answer from
the shown evidence and use at most one prepared appendix. If a step failed,
name the failure and the manual route. Do not add a feature, retry inference
or increase scope to consume the reserve.

## Six-Point Rehearsal Acceptance

This is a rehearsal checklist, not a completed result. Record each item as
Pass, Fail, Blocked or Not run, with the build, time and evidence reference.
The planned timings have not been validated by a rehearsal.

| Requested proof | Script window | Evidence needed before claiming it was demonstrated |
| --- | --- | --- |
| AI across the applicable lifecycle stages and document analysis | 02:35-04:25 and 06:10-07:00 | Actual model-origin output, source comparison and task/model provenance per shown example; contracts alone do not prove execution |
| Observability of the conversation just held | 04:25-05:15 | Exact interaction-to-trace correlation and receipt in the authorized Azure view; the staff AI observability view (Assistants, model-call metrics) and its Azure portal link are present from demo API revision 0000161, but the portal view needs a Reader role on Application Insights and Log Analytics; verify the link and the role before the rehearsal, or disclose either as absent |
| Sensor readings and alerts | 05:15-06:10 | Authorized retained readings and an actual alert, or an explicitly labelled fixture; rule alerts and AI findings distinguished |
| Employee prioritisation and issue resolution | 01:50-04:25 | Explainable queue, source-checked assistance and an authorized correction/next action; no claim of a fixed issue while evidence is outstanding |
| Full process | 06:10-07:00 | Same-home stage records or labelled contracts with missing stages disclosed; a completed live lifecycle requires separate proof |
| Resident self-service and potential staff time saved | 07:00-07:45 | Own-record access and a grounded routine answer; observed savings require a separate total-effort/contact comparison |

### Prepare the views, not a new deployment

* Rehearse 1:50 separately, then the eight-minute prepared route. Count clicks
  and waits inside the windows. Cut explanation before using the reserve.
* Pre-open the staff queue, Documents/source comparison, case assistant,
  Home sensors, journey and authorized resident view. Keep portal access in a
  separate clean sharing tab, without exposing tenant identities or raw logs.
* Select one current authorized home with appropriate readings and linked
  resident fixture if available. Prefer a granted home from the 20-home live
  cohort in the live demo status; a different fixture needs explicit demo scope
  and must not silently redefine the cohort.
* Prepare the short text fixture, one expected evidence gap and a manual route.
  A model can miss the gap; retain that failure instead of replacing its answer.
* Verify separate admission and finite call/token/time/spend authority for
  document reading, employee chat, Quality and resident advice. The extended
  script is not permission for four calls or a background scan.
* Record actual model/task/version and source references for any prepared
  output. If none exists, use the source contract, not an invented transcript.
* Verify collector ingestion, sampling and exact interaction correlation before
  attempting the Azure segment. No exporter, collector or UI button is installed
  or activated by this documentation change.
* Keep unavailable states and the accessible manual route ready. Do not use
  colour as the sole explanation of an alert, answer origin or approval state.

## Live Preflight

Record Pass, Fail, Blocked or Not run with the actual time, source/image,
operator, route and safe evidence reference. A written checklist is not a pass.

* Genuine staff sign-in, expected role/case and wrong-role denial, not only a redirect
* Intended SQL state and permitted persistence/restart evidence, without reseeding
* Exact allowed AI task, sources, model/version, finite calls/tokens, expiry,
  processing terms, price/cost scope and current owner authorization
* Independent manual work and human safety routes; no actual emergency test
* Reversible prepared action, disposable fixture where necessary and recovery owner
* Clean sharing profile, no notifications, private identities, endpoints,
  credentials, raw payloads or unapproved generated-data screenshots
* An accessible list/manual explanation and the evidence fallback ready in advance

Do not show invented portal screens. Later resident and employee-chat source
capabilities exist, but an optional resident channel, real enrolment, direct
usability and live acceptance remain separate. Assisted phone, letter and
officer routes stay available; login is not works consent.

## Technology Questions

Keep the demo on one home and an accountable next action, not a platform tour.
Main pages 14-15 explain the built Workbench and existing file/CLI adoption.
The demo is that current-product story, not the future platform. Page 13's
resident map explains the pains and design responses, labelled as hypotheses.
Only closing pages 23-24 propose optional Fabric/Power BI history and richer
semantic/preview ontology context; analytics and context tests are separate.
Use page 31 for rules versus Decision 1 versus generation, page 37 for the
shared API/SQL/Blob decision, page 46 for the source-only IoT route and page 47
for conditional Fabric analytics. The updated sensor route includes the
custom private Event Hub. Synthetic intake is not calibrated diagnosis;
resident hazard reports go directly to the independent human safety service.
Fabric is not a live demo dependency or an approval to copy data.

## Recover Once

| Event | Response | Record |
| --- | --- | --- |
| Sign-in, role or network failure | Stop after one bounded check; switch L to E | Retain the failure; never bypass controls |
| Disabled model, expired authority or timeout | Show unavailable/unknown and continue the manual route | No fresh-inference success or enlarged allowance |
| Wrong or stale draft | Identify the issue, reject the claim and inspect the source | Keep the adverse finding; do not conceal it |
| Sensitive information appears | Stop screen sharing and leave the page | Do not capture it into slides or a transcript |
| Request for an irreversible action | Explain its independent authority and evidence requirement | No sending, approval, release, tenant change or payment |

Restate an interruption in the questioner's terms, answer briefly, then use
one appendix or record an owned follow-up. The deck retains fixed slide-jump
buttons; do not promise dynamic return to the interrupted page. Navigate back
to the actual page deliberately.

## Debrief And Record

For route E say: "We inspected source contracts and dated engineering
evidence. We did not establish a current staff session, fresh inference or
business benefit. Those are the next validation questions."

After a real rehearsal or delivery, record actual route, timings, questions,
failures, inspected behaviour, unmet gates and follow-up owners. Do not write
success statements in advance. Keep private evidence outside this public
package. See the [current pitch notes](../pitch/speaker-script.md) and
[question bank](../pitch/questions-and-answers.md) for the same deck revision.