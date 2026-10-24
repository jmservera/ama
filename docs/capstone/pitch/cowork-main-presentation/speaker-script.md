---
title: Zava Forward Main Presentation Script
description: Timed executive script and interruption cues generated from slides.json
ms.date: 2026-10-24
ms.topic: reference
---

## Timing contract

24 minutes planned narration + 6 minutes discussion = 30 minutes presentation. The separate demo is 10 minutes. S18 is the short close after the demo; its 30 seconds are already in the presentation allocation. Backup slides are not extra scheduled content.

This is a rehearsal script, not an observed delivery or verified timing result.

## S01: More homes ready. No shortcuts on trust.

Planned narration 00:00 to 01:00; 60 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Zava Forward
* Modernise the programme. Prove where AI helps.
* Decision today: a gated validation path, not autonomous delivery.

### Say

My recommendation is to modernise how Zava North Homes moves a home from an identified need to an accepted outcome, and to make AI earn its place inside that process. Not five digital managers making decisions about residents. One accountable programme, with better evidence, less avoidable chasing and clear human authority.

Today I will show the business logic, the architecture behind it and what we have actually learned from building it. Then we will walk one constructed home through the workbench, including an exception. I will distinguish a working technical path from a proven business benefit throughout.

The decision I want is agreement on the next validation gate: named owners, a bounded cost envelope and explicit evidence required before expansion. It is not permission to release works, spend resident funds or operate autonomously. Interrupt me where you need to: the headline survives without the implementation detail.

### Show and deliver

Full-bleed quiet title, Zava green and warm white. One large outcome sentence; no technology logos. Pause after 'one accountable programme'.

### Interruption and return

If asked 'what exactly are you asking us to approve?', answer: a proposed validation path, not a production rollout. B15 contains the gate.

Return: The outcome is accepted progress, not more AI activity.

Evidence: E01, E02, E03

## S02: The constraint is coordinated readiness, not a lack of ambition.

Planned narration 01:00 to 02:15; 75 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* 60,000 homes in the case brief
* Evidence, funding, capacity and resident choice must align
* More starts are not the same as more accepted homes

### Say

The case starts with a 60,000-home association, a small team and a fragmented programme. An energy ambition competes for the same organisational attention as repairs, resident communication, funding and quality assurance.

A home is not ready because it appears near the top of a list. Its evidence must be credible, the right professional must accept the assessment, the resident must retain real choice, and funding and contractor capacity must be aligned. An incomplete handoff simply moves the delay to the next team.

That changes the management question. Instead of asking how many recommendations an agent generated, we ask how many homes reached an accepted handover, how much effort that took and what remained unresolved. Safety reports retain an independent human route; a routine retrofit queue must never become the gatekeeper for urgent help.

The brief's doubling and grant-capture ambitions are the challenge we are testing, not results I can claim today. I am also not presenting the original regulatory wording as a fresh legal update.

### Show and deliver

Three horizontal bands: demand -> coordination constraint -> accepted outcome. Make 60,000 the only large number. Footnote 'Case-study scale; benefits not yet validated'.

### Interruption and return

CEO: 'Why not hire more coordinators?' Use B01: capacity is necessary, but adding people without fixing evidence and handoffs can preserve the same friction.

Return: The bottleneck is a complete, trusted handoff.

Evidence: E01, E02, E12

## S03: One home makes the operating model tangible.

Planned narration 02:15 to 03:30; 75 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Identify need -> assemble evidence -> review readiness -> deliver -> accept
* A conflicting record stops dependent approval, not all useful work
* Illustrative journey, not a resident testimonial

### Say

Imagine one fictional home in that programme. A record suggests it needs retrofit attention, but two sources disagree about its energy evidence. A conventional dashboard might make the inconsistency another amber dot. Here it becomes an owned task: identify the source, retain the conflict and request the relevant review.

The assessment can be prepared without pretending that the missing fact is known. An assistant may explain the evidence or draft a message, but cannot manufacture the observation, infer resident consent or release the work. When the evidence changes, only the reviews that depend on it should need attention again.

After installation, provider completion, independent quality acceptance, resident handover and financial closure remain different events. Closing one must not erase an unresolved defect or complaint.

That is our narrative thread. The demo will return to this same-home pattern rather than jump among unrelated AI tricks. If the current deployed build cannot support a step, I will show its documented contract and label that honestly.

### Show and deliver

Five large journey stations. Use an explicitly fictional identifier such as EXAMPLE-HOME, never a copied resident name/address. Highlight the conflict, then the named review.

### Interruption and return

Resident/customer concern: 'Does no response mean consent?' Answer no, then B06.

Return: The home progresses only when its evidence and decisions are ready.

Evidence: E02, E07, E08

## S04: One programme. One evidence trail. People decide.

Planned narration 03:30 to 05:00; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* People -> controlled workbench -> retained evidence
* Rules keep the boundaries; AI prepares bounded help
* Optional portal assessed; assisted routes stay

### Say

The architecture starts with people, ownership and evidence, not a list of Azure products. The workbench carries commitments and workflow; Azure SQL retains structured state and Blob holds document files. AI prepares permitted evidence for a person's review, never authoritative state or domain approval.

In-use monitoring is the proposed post-retrofit feedback loop. Sensors or a labelled simulator send temperature and humidity through IoT Hub Basic, API validation and SQL; a deterministic signal may request human review. This accepted exercise design is not live transport, diagnosis or measured benefit. A resident's hazard report always uses the independent human safety route.

The resident portal is optional, not rejected. Issue #441 assesses whether self-service status access can reduce avoidable calls and interruptions of staff working time. Portal/workflow comes first using existing case/API authority; any resident-answer assistant is separately gated. Per-message human review remains normative and routine automation is off. Phone, email, visits and accessible assisted routes stay available without detriment.

Source implementation, a design decision and a current live service are different evidence. The portal's local work-in-progress is owner-reported, not inspected delivery or an approved handoff. Test staff and resident effort, access and comprehension before claiming benefit.

### Show and deliver

diagrams/01-the-idea.svg. Three clicks: people; workbench and evidence; bounded-AI strip. Keep the complete static image available; animation is optional.

### Interruption and return

CIO: 'Is this a new system replacing housing management?' B02: a demonstrator of the coordination layer; live integration/replacement is not proven.

Return: The application owns the workflow; people retain the authority.

Evidence: E02, E06, E07, E12, E441

## S05: A faster wrong decision is not progress.

Planned narration 05:00 to 06:30; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Resident choice is explicit
* Professional and financial approvals remain independent
* Unknown, stale or failed evidence never becomes permission

### Say

For this customer, control is part of the value proposition, not a compliance appendix. A faster wrong decision can create more rework, more resident distrust and more organisational exposure.

We therefore distinguish an offer from a commitment, a draft from an approved assessment, an award from grant cash and a provider's completion from independent acceptance. These distinctions exist in the records and API contracts, not just in the colour of a screen.

The assistant can contribute to preparation. It cannot take over resident choice, approve its own work, submit a grant, accept quality or authorise payment. A person reviewing an AI proposal must still have current permission and current source evidence. Accepting a useful paragraph is not accepting the underlying domain action.

Unknown remains a meaningful outcome. If an input is missing or a review becomes stale, the right result can be an owned hold or a request for clarification, not a confident completion message. An urgent hazard goes to its independent human route even if the model is negative or unavailable.

These are testable design boundaries. They are not a claim that every human, legal or professional acceptance gate has already passed.

### Show and deliver

Three large paired labels: draft != approval; offer != commitment; completion != acceptance. Use text and shape signals, not colour alone.

### Interruption and return

Risk leader: 'Can a human rubber-stamp it?' Use B07: meaningful review needs source inspection, competence, time and a challenge route.

Return: We accelerate preparation, not the removal of accountability.

Evidence: E02, E07, E08, E12

## S06: Use AI for uncertainty, not for arithmetic or authority.

Planned narration 06:30 to 08:00; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Rules: explicit policy and repeatable calculation
* Decision model: bounded scoring over supplied candidates
* Generative AI: source-bound explanation and drafting

### Say

There are three different tools here, and treating all three as a chatbot would be an expensive design mistake.

First, deterministic rules handle known calculations and controlled state changes: eligibility arithmetic, freshness checks, ownership, permitted transitions and the evidence required before release. They are easier to reproduce and explain than asking a language model to reinterpret the same policy every time.

Second, a decision model such as Decision 1 is a candidate for bounded tasks such as selecting among supplied form candidates or screening evidence support. That is learned scoring, not the rules engine. It must be allowed to abstain, and the candidate set and review cost matter.

Third, generative AI helps where the work is language and synthesis: a cited explanation, an assessment draft or a resident-update draft from permitted facts. It must not invent the missing observation.

A smaller specialised model may improve inference cost or latency, but that is not a measured saving here. We compare the complete task against rules, templates and manual handling, including review, correction, retries and failure. If the simpler route wins, we keep it. AI adoption is not the success measure.

### Show and deliver

diagrams/02-ai-placement.svg. Reveal rules first, then decision model, then generative AI. Say 'learned scoring' explicitly so Decision Models are not confused with decision tables.

### Interruption and return

CFO: 'How much faster and cheaper?' B04 and B05: show the cost equation; no unsupported percentage.

Return: The unit of comparison is an accepted task, not a model token.

Evidence: E04, E05, E09

## S07: We kept the five responsibilities, not five autonomous managers.

Planned narration 08:00 to 09:30; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Prioritisation | assessment | funding | coordination | quality
* Five bounded capabilities in one controlled workflow
* Authority follows the action, not the agent label

### Say

The original request named five agents. We did not discard those business responsibilities: prioritisation, assessment, funding, contractor and resident coordination, and quality are still the capability map.

What we challenged was the assumption that each responsibility should become an autonomous digital manager with its own authority and runtime. Ranking policy, consent, quality acceptance and financial controls should not depend on a persuasive model response. Splitting them into five independent services would also introduce more state synchronisation, retries, failure boundaries and operating overhead before proving the customer value.

The implementation therefore has five bounded assistants sharing one API and a controlled proposal pattern. A deterministic supervisor determines eligible work and records; the assistant prepares an unreviewed output; an authorised person makes the separate decision. Separate queue workers remain a deferred topology, not the explanation of today's assistant runtime.

That is the consultative change: fulfil the purpose of the request while challenging an unsafe or unnecessarily complex implementation. The historical operator evidence includes five real model paths, but ordinary assistant authority and proactive scans were left off after bounded QA. I will not turn that evidence into a claim of five autonomous workers running today.

### Show and deliver

Five equal capability labels above a single workflow rail; one human-decision boundary beneath. Do not draw five AI avatars as decision owners.

### Interruption and return

Sponsor: 'So did you ignore the brief?' B03 maps each requested responsibility to the retained capability and changed autonomy.

Return: We challenged the mechanism, not the customer's outcome.

Evidence: E01, E03, E06, E09

## S08: Measure accepted outcomes, not generated activity.

Planned narration 09:30 to 11:00; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Accepted handovers and time to readiness
* Net coordination effort, including review and rework
* Safety, resident choice and quality are guardrails

### Say

The value case has to survive a comparison with a well-organised workflow that uses no AI. Otherwise we risk attributing the benefit of clearer ownership and cleaner data to the model.

The first comparison asks whether the modernised workflow improves the programme relative to its baseline. The second asks whether adding AI improves the same workflow further. We keep the cohort, task and guardrails comparable, and count preparation, review, correction and burden shifted to other people.

The outcome is accepted handover, not starts. We also need time to readiness, net coordination effort and quality rework, with safety and resident agency treated as constraints rather than metrics to optimise away. Grant application, award, claim and cash remain separate.

The case brief's delivery and grant ambitions are useful hypotheses, not observed benefits. Likewise, the 60,000-home stock is a scale fixture; it is not a claim of 60,000 operational cases in Azure SQL.

A saved hour is capacity until Finance validates how it changes staffing, overtime, contracted effort or delivery. We should not sell it as a cash saving twice. A negative AI result is still a useful result if it prevents an unnecessary operating cost.

### Show and deliver

Two clean comparison brackets: baseline -> modernised workflow; same workflow -> workflow + AI. Put 'accepted task' at the centre and guardrails underneath.

### Interruption and return

CEO: 'Will this double delivery?' B08: not yet evidenced; physical capacity and scope remain constraints.

Return: Better evidence must turn into accepted progress, not a busier dashboard.

Evidence: E02, E10, E07

## S09: Thousands in works and funding per home. Cost the technology separately.

Planned narration 11:00 to 12:30; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Historical benchmark: GBP 6,082 works/home
* Illustrative grant: GBP 3,041/home; GBP 47.4m across 15,600 homes
* Technology exercise: USD 700 October ceiling, not full project TCO

### Say

We did the arithmetic, and the scale matters. The earlier housing-association benchmark is six thousand and eighty-two pounds of works per home. Apply it to our modelled fifteen thousand six hundred homes and the works scenario is ninety-four point nine million pounds. These are national-benchmark planning figures, not surveyed Zava costs or contractor quotations.

If every home and all that cost qualified, a fifty-percent grant share would be three thousand and forty-one pounds per home, below the historical seven-and-a-half-thousand cap: forty-seven point four million pounds across the cohort. That is conditional funding potential, not an allocation or award. Current scheme rules, eligible costs, deadlines and available funding need Finance and funder confirmation.

This is why the documentation matters: link each eligible home and measure to reviewed assessments, cost evidence, the approved application and the evidence required for claims. Reconcile application, award, claim and cash separately. Better records can reduce avoidable returns and clawback exposure; they do not create eligibility or guarantee subsidy. We must measure the improvement.

The technology exercise has an owner-set seven-hundred-dollar October ceiling, not a production quote or full project cost. Execution gates remain and authority expires on 25 October at 16:02 UTC. We still need implementation, integration, hosting, support and human-review costs. The next AI slide restores the inference calculation, without pretending those other costs disappear.

### Show and deliver

Three labelled figures: GBP 6,082 works/home; GBP 3,041 conditional grant/home; USD 700 October exercise ceiling. Beneath, show GBP 94.9m works and GBP 47.4m conditional grant for the 15,600-home scenario. Label historical benchmark, conditional scenario and exercise budget separately; no cross-currency ratio. B09 retains the separate GBP 20,000 exercise package.

### Interruption and return

CFO: 'Is USD 700 the monthly production price?' No. Use B05 and B09; it is the owner-set October exercise forecast ceiling, not a quote or unconditional tranche authority.

Return: We buy evidence in stages; we do not infer a production business case from a demo bill.

Evidence: E02, E05, E11, E21

## S10: The runtime is deliberately simpler than the capability map.

Planned narration 12:30 to 14:00; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Container Apps API + Azure SQL + Blob
* Entra identity; application-enforced scope
* Models return proposals, not authoritative state

### Say

Now we can zoom into the same architecture without changing the story. A staff browser reaches the application through Entra-backed authentication. The API checks the effective staff identity, role, case and permitted fields. Signing in proves an identity, not professional competence or spending delegation.

The Container Apps API hosts the workflow and the five bounded assistants. Azure SQL retains cases, controlled records, proposals and audit. Blob holds document bytes, with references and hashes retained separately. The assistant's context is constrained to what that task is allowed to use.

For a model request, the API captures the relevant evidence, calls the permitted endpoint and validates the result before retaining an unreviewed proposal. The direct Azure OpenAI path does not imply that a Foundry Agent Service is orchestrating the programme. Decision 1 is a separately gated task path, not an assumed always-on service.

Managed identities and private dependencies are part of the design. The diagram is not a fresh network inventory or a claim that every configured control has been accepted in Azure. The latest deployment and sign-in gates remain explicit in the demo preflight.

We can add runtime boundaries when measured load, isolation or reliability requires them. We do not add a microservice merely because a capability has an agent name.

### Show and deliver

diagrams/03-runtime.svg. Build browser/API/SQL first; add identity, models and Blob second. Full-static alternative is mandatory.

### Interruption and return

CTO: 'Where are the queues and five workers?' B10: deferred topology, not the current assistant runtime.

Return: Shared workflow state is controlled centrally; model reasoning is bounded.

Evidence: E06, E07, E09, E13

## S11: Modelled inference: about 44 US cents per home. Full project cost is separate.

Planned narration 14:00 to 15:30; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Planning scenario: USD 0.44 inference/home; USD 6,873 for 15,600 homes
* 20 tasks/home x 13,768 tokens/task x USD 1.60/million
* Dated third-party price assumption; excludes platform, people and delivery

### Say

Here is the calculation we used before. Five real operator runs consumed six thousand eight hundred and eighty-four tokens, averaging one thousand three hundred and seventy-six point eight per run. For planning, we allowed twenty AI tasks per home and made each task ten times that observed size: thirteen thousand seven hundred and sixty-eight tokens.

We priced every token at one dollar sixty per million, the output rate reported by third-party Azure pricing mirrors on 23 October. That gives forty-four US cents of inference per planned home and about six thousand eight hundred and seventy-three dollars across fifteen thousand six hundred homes. Double the workload and it is about eighty-eight cents per home. This is a transparent sensitivity calculation, not a verified deployment price, usage ceiling or measured cost per accepted home.

Compare the scale with the earlier six-thousand-and-eighty-two-pound works benchmark and illustrative three-thousand-and-forty-one-pound grant share. Do not silently equate dollars and pounds. The inference line is small; implementation, integration, hosting, security, support, evaluation and human review still need costing. The seven-hundred-dollar October envelope already includes its AI spend, so we must not count that twice.

For the council, the value is a defensible evidence trail supporting eligible applications and claims, not a promise of automatic subsidy. We still owe measured quality, acceptance, total cost and grant outcomes. Finite tokens are not a money cap; full metering and monetary controls remain requirements to test.

### Show and deliver

Use a large USD 0.44/home with an adjacent 'INFERENCE PLANNING SCENARIO' label. Show the three-factor formula, USD 6,873 cohort total and USD 0.88 doubled-workload sensitivity. Keep dated secondary-source price and exclusions legible. Use diagram 07 only as the separate measurement/control view; it is not a priced forecast. B25 has the exact workings and limitations.

### Interruption and return

CFO: 'Can the bill run away?' Use B25: finite tokens are not money; monetary/per-task/per-request limits remain proposed. B26 covers caching and routing.

Return: Small inference cost is a planning result; accepted value and total project cost still need evidence.

Evidence: E07, E09, E13, E04, E19, E21

## S12: We engineered the learning before scaling the build.

Planned narration 15:30 to 17:00; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Design thinking: understand, explore, test
* HVE: research -> plan -> implement -> review
* Prototype and MVP iterations changed the design

### Say

The technique used to build the solution matters because it explains why the result is more than a literal implementation of the first brief.

We used design-thinking techniques to explore the customer problem and the journeys around it, rather than starting with five model prompts. Role instruments helped challenge the programme from asset, finance, resident, safety, procurement and delivery perspectives. They were research aids, not actual employees and not a substitute for talking to residents or staff.

Prototypes and executable MVP iterations made the assumptions inspectable. The learning was not simply which layout looked better. It exposed ownership confusion, unnecessary complexity, source conflicts and the need for one shared workbench with distinct human decisions.

HVE then provided a disciplined engineering loop: research the evidence, plan a bounded change, implement against explicit acceptance criteria and review the result. Responsible AI, architecture, privacy and supply-chain techniques informed the controls. A review that finds a defect is evidence to act on, not a ceremonial stamp.

The knowledge base compounds that learning across iterations. Decisions, limitations and source dates survive the individual chat session. This is a documented method and artifact story, not a claim of measured developer-productivity uplift.

### Show and deliver

A three-stage learning ribbon: problem discovery -> prototypes/MVP learning -> bounded engineering loops. Show one real design reversal rather than a wall of HVE logos.

### Interruption and return

Panel: 'Were these real user interviews?' B12: distinguish owner feedback, role-instrument desk research and unperformed human validation.

Return: The method made assumptions visible before agents multiplied implementation effort.

Evidence: E14, E15, E03

## S13: From BRD, PRD and ADRs to a reviewable delivery backlog.

Planned narration 17:00 to 18:30; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* BRD + PRD + ADRs -> hierarchical GitHub issues
* 189 board items on 23 October: epics, features, stories and other issues
* Agents implement bounded changes; reviewers retain the gate

### Say

Once the problem, journeys and product boundaries were clear enough, we used the BRD, PRD and architecture decisions to generate a large hierarchical GitHub backlog. The historical recollection is around 180 issues, including epics and user stories, not 180 agents or stories alone. We checked the AMA Plan project: on 23 October it has 189 board items, including epics, features, stories and other issues. That is a current project snapshot, not an exact original-generation count and not a claim that every item has been accepted.

The important part is the chain. A business need becomes a requirement. Architecture decisions constrain the implementation. Epics, features and stories organise the work and acceptance conditions. An implementation agent gets a bounded task, not a licence to reinterpret the operating model. Tests, source changes, review findings and pull-request evidence make the work inspectable.

Where work can proceed independently, agents can work on separate topics. Where a decision or dependency blocks it, they must not invent authority to keep a throughput number high. Findings and corrections stay attached to the evidence.

This is the second AI story: AI helped build the solution, using decomposition and feedback rather than an unbounded software factory. More generated code is not the outcome; accepted behaviour is.

### Show and deliver

Use evidence/project-snapshot.png as a project-backed API visual, explicitly not a screenshot of GitHub's website. Preserve the date and status-is-not-acceptance caveat. Add the BRD/PRD/ADR -> issue -> PR -> evidence chain as native PowerPoint text, not a completion chart.

### Interruption and return

CEO: 'Did agents build all of it without people?' B13: bounded implementation and human/independent gates, no unsupported completion or productivity claim.

Return: We scaled reviewable work, not unbounded autonomy.

Evidence: E14, E15, E16, E19, E20

## S14: The most valuable learning was what not to automate.

Planned narration 18:30 to 20:00; 90 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Do not ask a model to enforce known policy
* Do not infer consent, safety or financial authority
* Do not add a service before proving its need

### Say

Three design choices summarise the learning.

First, do not use a generative model to repeat a calculation or enforce an already explicit rule. The variability and review burden add little value. A rules result should be reproducible, and a policy change should be reviewed as a policy change, not drift through a prompt.

Second, do not confuse assistance with delegated authority. A well-written resident message does not prove that the resident consented or even received it. A neat evidence summary does not replace the professional quality judgement. A confident funding draft does not establish eligibility or cash.

Third, do not confuse architectural ambition with a need for more services. Five business responsibilities do not force five separately deployed agents. Sensors can be a useful future evidence source, but a simulated or offline reading is not a live IoT integration, and missing telemetry is not evidence that a home is safe.

These are deliberate trade-offs. We give up the appearance of blanket autonomy in exchange for explainable state, a manual route and a smaller failure surface. The reversal condition is evidence: if a specialised model or independent worker genuinely improves accepted-task economics or isolation, the design can evolve through a new reviewed contract.

### Show and deliver

Three large 'not this / instead this' pairs. Optional link to diagrams/06-sensor-target.svg only if the audience asks about telemetry.

### Interruption and return

Innovation leader: 'Are you being too conservative?' B14: bounded autonomy is a scaling mechanism, not a ban on AI.

Return: We automate effort where it helps, not accountability where it matters.

Evidence: E03, E04, E06, E12

## S15: The next risk is acceptance, not another architecture box.

Planned narration 20:00 to 21:15; 75 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Engineering evidence is necessary, not sufficient
* Human task checks, recovery, privacy and live access remain gates
* Expand only on current, task-bound evidence

### Say

The next phase should not be sold as another feature list. It is an acceptance plan.

We need genuine staff sign-in and role-denial evidence on the selected deployment, task-bound real AI results, durable SQL behaviour and a current cost view. We also need human task and comprehension checks, accessibility evidence, privacy and processing decisions, and recovery work that goes beyond a successful process restart.

The local engineering work gives us useful contracts and negative tests. It does not appoint a professional reviewer, ratify a policy, prove a restore or establish that a resident understands the result. The latest deployment blockers make that distinction particularly important.

The operating model must remain usable if optional inference is disabled, stale or unaffordable. The manual and safety routes must not depend on the demonstration working.

I would therefore treat expansion as an explicit decision after the evidence is assembled, with a named owner for each unresolved control. We can continue useful independent engineering while a human decision is pending, but we cannot silently convert that pending decision into approval.

### Show and deliver

Three gates: technical reality; human and control acceptance; measured value. All are required. Optional B16 uses diagrams/05-operations.svg.

### Interruption and return

CIO: 'Is it production ready?' B15/B16: no; show exact outstanding gates without an invented readiness percentage.

Return: The release decision follows evidence, not the end of the slide deck.

Evidence: E07, E12, E13, E17

## S16: Fund the next evidence gate, then decide whether to scale.

Planned narration 21:15 to 22:30; 75 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Scope: one connected journey and a paired comparator
* Owners: programme, Finance, technical and control reviewers
* Stop or reverse if quality, control or net value fails

### Say

My proposed next step is a bounded validation tranche, not a commitment to roll out across the entire estate.

The Programme owner defines the journey and what accepted progress means. Finance refreshes the total cost boundary and approves any finite spend. The technical owner establishes deployment and recovery evidence. Named professional, resident-engagement, privacy and safety reviewers own the relevant acceptance decisions; role-agent personas cannot supply those approvals.

Freeze the comparator before running the test. Measure accepted-task quality, total preparation and review time, rework, latency, cost and the guardrails. Retain negative results. If the AI route creates more review work or loses critical evidence, keep the simpler workflow while investigating.

No date or cash commitment is being invented on this slide. The immediate deliverable is an agreed scope, owner and acceptance protocol. A schedule and spend request follow from resolved prerequisites. Expansion is a separate decision after that evidence, with a manual route and a documented reversal condition throughout.

### Show and deliver

One-page decision card: scope / named role owner / evidence / stop condition. No fictional signatures or approved green ticks.

### Interruption and return

CEO: 'When do we get value?' B17: schedule is dependency-led; identify the next evidence deliverable, not an unsupported go-live date.

Return: We are buying a decision-quality result before buying scale.

Evidence: E02, E10, E11, E13

## S17: Now test the story: one home, one exception, one accountable next step.

Planned narration 22:30 to 23:30; 60 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Watch the evidence conflict and its owner
* Watch what AI can draft, and what it cannot approve
* Watch the retained state and next action

### Say

For the next ten minutes, I want you to judge three things. Can we see why the home is blocked? Can we see who can resolve it? And can we distinguish useful AI help from the decision that still belongs to a person?

This is a constructed exercise, not a resident case or a production service. I will state which route passed preflight. If the live route is unavailable, I will use the labelled repository-evidence walkthrough rather than pretend a recording or template is live inference.

Please interrupt on the business decision. If we go deep on infrastructure, I will park the question and use the matching appendix afterwards so that we still reach the exception and the next accountable action. At the end, we return to the same investment decision we started with: what evidence would justify the next controlled step?

### Show and deliver

Three watch-for prompts. Link to the separate demo runbook and a static 'recorded evidence, not live' title card.

### Interruption and return

If asked to try an unprepared action, do not grant roles or mutate a live case. B18 explains the demonstration boundary.

Return: The demo is proof of a bounded behaviour, not permission to operate.

Evidence: E07, E13

## S18: More homes ready, with control intact.

Planned narration 23:30 to 24:00; 30 seconds. Discussion stops the narration clock but consumes the six-minute reserve.

### On-slide copy

* Agree the next validation gate
* Confirm owners, evidence and finite cost boundary
* Scale only what earns trust and measurable value

### Say

The outcome is not five agents. It is a programme that can move more homes toward an accepted result without losing the resident, the evidence or the accountable decision-maker.

We have a credible architecture and real engineering learning. We still owe the human, operational and value evidence. My recommendation is to agree the bounded validation gate, confirm its owners and cost boundary, and make the scale decision from the result. That is how we turn AI ambition into a service we can defend.

### Show and deliver

Return to the opening visual. Show the decision in one sentence; no new diagram or new number.

### Interruption and return

Restate any requested change in the customer's language, name which assumption changes and record the decision as pending unless explicitly made.

Return: More accepted progress. No shortcuts on trust.

Evidence: E02, E10, E13
