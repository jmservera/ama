---
title: Capstone Demo and Recovery Runbook
description: Current v2 same-home story, under-two-minute hook, ten-minute route, owner-selected five-home demo target and honest live/evidence preflight
ms.date: 2026-11-12
ms.topic: how-to
---

## Outcome And Timing

Show one fictional home, one evidence conflict, one accountable next action
and the boundary between an AI draft and a human decision. Land that outcome
inside two minutes; do not begin with a screen tour or platform inventory.

The current full route is ten minutes, separate from the 30-minute
presentation: eight minutes prepared flow and two for questions or recovery.
Use S22/page 25 to introduce it and S23/page 26 to close. The closing
30 seconds already belong to the presentation narration allocation.

This is preparation, not an executed demo or rehearsal. No cloud, identity,
model, resident-data or workflow mutation is authorized by this runbook.

## Explain the Requested and Built Autonomy

Use [page 30's matrix and review](../source/review-2026-11-08.md#requested-versus-built-autonomy)
to describe exact brief fidelity. The case already specified L2-L4 and
professional/resident decisions. The current five helpers are evidence
proposals; a request or approved scan can prepare one without advancing the
case. Do not call that a delivered L3 booking or L4 autonomous quality flag.

For the prepared walkthrough, show the three existing help modes rather than
adding features to the ten-minute route:

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
Decision 1 is historical scoring evidence with a pending current rebuild,
not the current five-helper engine. Refresh the progress and activation
snapshot before the final demo.

## Demo Operating Mode And Five Homes (Owner-Selected Target, 2026-11-12)

Refs #134 and #184. On 2026-11-12 the owner accepted a simplified demo
operating mode. It is a target. Nothing below is implemented, activated or
observed unless the Status column says otherwise, and it grants no model,
deployment or spend authority.

| Element | Status | What the source says today |
| --- | --- | --- |
| Single-instance simulator start and stop, no SQL tickets | OWNER-SELECTED TARGET | Not verified; the earlier ticket-based design is a proposal only |
| Five synthetic demo homes | OWNER-SELECTED TARGET | The simulator reads every open case id and refreshes the list hourly; a control cohort of listed homes exists |
| One new reading every minute | OWNER-SELECTED TARGET | Not verified against the current simulator cadence |
| Quality AI restricted to the same five homes | OWNER-SELECTED TARGET | Supersedes the earlier every-open-case scan scope as the selected target; the current source scope is unchanged and unverified |
| Deterministic eligibility is separate from paid analysis | OWNER-SELECTED TARGET | Eligibility does not by itself start a model call |
| Analysis is operator-triggered during the presentation, not per reading | OWNER-SELECTED TARGET | Not verified |
| Eight-hour background limit | LATER RECOMMENDATION | Not implemented and not a timer or authority |

Earlier dated statements of the every-open-case scope and the ticket design
remain historical. The observed and blocked histories in the
[cut-over evidence pack](../../architecture/cutover-evidence-pack.md) stand.

### The five homes

Open each case from the Workbench after authorised staff sign-in. The route is
`/app#/case/<id>?tab=quality`; the Quality and handover tab holds the sensor
panel. Case ids are fictional constructed records. Open these only on the
chosen build, and follow the preflight below first.

| # | Case id | Archetype | Property type | Stage in the replayed seed | Direct link |
| --- | --- | --- | --- | --- | --- |
| 1 | ZF-2025-0355 | ARC-01 | End terrace | Quality check | [Open ZF-2025-0355](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2025-0355?tab=quality) |
| 2 | ZF-2025-0382 | ARC-02 | Mid terrace | Quality check | [Open ZF-2025-0382](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2025-0382?tab=quality) |
| 3 | ZF-2025-0286 | ARC-04 | Bungalow | Quality check | [Open ZF-2025-0286](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2025-0286?tab=quality) |
| 4 | ZF-2026-0829 | ARC-05 | Mid terrace | Quality check | [Open ZF-2026-0829](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2026-0829?tab=quality) |
| 5 | ZF-2026-0892 | ARC-06 | Semi-detached | Funding check | [Open ZF-2026-0892](https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io/app#/case/ZF-2026-0892?tab=quality) |

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

* Each of the five ids exists in the chosen build and is open.
* The simulator control cohort lists exactly these five homes, and readings
  for each exist in the chosen build's sensor store.
* The effective AI scan scope is evidenced as these five homes only before
  any analysis is triggered; otherwise use route E (see the route table below), not a live trigger.
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

| Clock | Point | Evidence route |
| --- | --- | --- |
| 00:00-00:30 | "A home can be high priority and still not be ready." | State fictional scope; show the same-home blueprint on page 13 |
| 00:30-01:10 | "Conflicting evidence has an owner; unknown is not silently resolved." | Trace the source/version and dependent-review boundary, not a private case record |
| 01:10-01:45 | "AI can draft. It cannot grant consent, release work or approve funding." | Show the controlled draft/review flow on page 20 and the retained human decisions |
| 01:45-02:00 | "The result is an owned next action, not an automatic green status." | Name what is observed, what is proposed and what still needs acceptance |

For route L, show only the equivalent pre-arranged, authorized behaviour.
An animation or a prepared response is never presented as live inference.

## Complete The Prepared Flow

| Clock | Focus | Boundary |
| --- | --- | --- |
| 02:00-03:00 | Evidence conflict and current versions | Do not merge unknown identities or invent stock-to-case links |
| 03:00-04:20 | Unreviewed proposal | At most the separately approved single task/call; otherwise show the contract |
| 04:20-05:20 | Inspect cited evidence and usage | Citation presence is not semantic truth; missing usage is unknown, not zero |
| 05:20-06:25 | Independent decisions | No irreversible consent, work release, sending, grant submission or payment |
| 06:25-07:15 | Owned unresolved next step | State whether any state changed; do not imply completion |
| 07:15-08:00 | Debrief actual evidence | No current live, housing-outcome or savings claim from repository inspection |
| 08:00-10:00 | One question or one recovery | Stop prepared navigation at eight minutes; do not add unprepared features |

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