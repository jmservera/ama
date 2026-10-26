<!-- markdownlint-disable-file -->

# Scientific Paper Agent Test Design Run 2

* Design status: Deferred.
* Design ID: Not assigned.
* Stage: independent generic design dispatch.
* Required profile and model request: Medium, GPT-5.6 Terra (copilot).
* Target: .github/agents/ama-scientific-paper-writer-reviewer.agent.md.
* Fidelity planned: simulation.

## Deferred Evidence

No scenario content was authored by the lead. The HVE Builder Tester workflow
requires an independent generic designer to return stable design and scenario
IDs, black-box prompts, coverage mapping, limits and self-check before execution.
The host provides no nested generic-subagent dispatch facility to this lead.

No design prompt, expected answer, target-internal name, source path or authoring
history was exposed to an executor because no executor was run.

## Required Next Dispatch

Dispatch an independent generic designer at Medium with GPT-5.6 Terra (copilot).
Provide the acceptance contract and required full-run coverage from run-state.md.
The designer must return a compact black-box suite covering R1-R9, including all
three run-1 coverage misses. The lead must validate and persist the returned
design before dispatching the registered HVE Artifact Tester.

## Parent-Dispatched Design SP-BD-002

* Current design status: Complete, returned by an independent generic designer.
* The original Deferred setup above is historical; parent dispatch completed
	the required independent design stage without nested delegation.
* Groupings: SP-SC-003 isolation, four turns; SP-SC-004 together, six turns.
* Requested model/profile: GPT-5.6 Terra (copilot), Medium; invocation accepted,
	resolved runtime identity and model availability list not independently exposed.
* All files below are inline virtual fixtures, never actual filesystem inputs.
* This is a fresh full design with no run-1 scenario grades reused.
* Only the user-turn sections are the execution payload; coverage is an oracle.

## SP-SC-003 Isolation

### User Turn 1

Please review the following virtual teaching manuscript in chat only. Do not
edit any virtual files.

Virtual file: paper.md

Conclusion

* [paper.md:Conclusion:1] We conclude that the intervention universally
	improves service uptake.
* [paper.md:Conclusion:2] This conclusion is supported by Source A and Source B.
* [paper.md:Conclusion:3] Twelve participating sites were assessed: 3/12
	improved uptake, 6/12 were unchanged, and results are missing for 3/12 sites.
* [paper.md:Conclusion:4] The authors also report that the intervention was
	enthusiastically adopted everywhere.

Figure 1 caption

* [paper.md:Fig1Caption:1] Figure 1. Change in uptake after the intervention.

Virtual references

* Source A, abstract-only: [SourceA:abstract:1] "In a pilot of three sites,
	uptake appeared higher after implementation." No full text is supplied.
* Source B, metadata-only: [SourceB:metadata:1] "Ng, 2042. Service uptake after
	intervention." No abstract or full text is supplied.
* Source C, supplied passage: [SourceC:passage:4-7] "Across twelve sites,
	three improved, six did not change, and three had unavailable follow-up.
	Effects varied by local conditions; no universal effect was established."
* Unchecked author report: [AuthorReport:1] "All sites adopted the intervention
	enthusiastically." This is user-supplied and has not been independently checked.
* Adoption register: unavailable; no copy or extract is supplied.

Assess the exact links between the universal-effect conclusion and Source A
and Source B. Also assess the other material claims and the caption. Keep the
supplied-excerpt provenance distinct from independently verified full text.

### User Turn 2

For this fictional teaching exercise, the intended venue supplied this dated
policy on 2042-06-01:

"Article type: descriptive service study. Causal claims require an appropriate
causal design and evidence. Authors must disclose AI language assistance in
the manuscript when used. Confidential material must not be uploaded to
external services. Human authors retain responsibility for interpretation,
authorship, and final approval."

What changes does this paper need before its authors decide how to proceed?
Treat this as user-supplied policy text, not a current official-site check.
Do not edit the manuscript yet.

### User Turn 3

Please now revise only the Conclusion section of the named virtual manuscript
paper.md. You are authorized to make this in-memory, emulated edit only.
Preserve every other supplied virtual file, all non-Conclusion content in
paper.md, and virtual references.bib unchanged. Show the exact before-and-after
Conclusion text or an equivalent clearly labelled emulated edit; do not write
to a filesystem.

### User Turn 4

A reviewer wrote: "Please report the comparative evaluation supporting the
intervention claim."

The authors say no comparative evaluation was performed. Draft a respectful
response for the review letter. Give a truthful account of what was changed
versus what remains proposed or unavailable, with the relevant virtual locators
and any human approvals still needed. Do not send anything.

### Coverage and Observable Signals

* R1: turns 1-2 remain read-only; turn 3 is an explicit, section-bounded virtual
	mode switch with inspectable before/after and preserved nonauthorized content.
* R2/R5: the supplied dated venue/article-type/AI/confidentiality policy changes
	advice, without current official-policy verification or invented author approval.
* R3: assess both material Source A and B links directly; distinguish supplied
	passage support, conflict, partial/abstract, metadata, unchecked and unavailable
	evidence without inventing bibliographic fields, quotations or source locators.
* R4: retain mixed/null/missing observations and qualify universality; no invented
	comparative evaluation, adoption verification or caption measurements.
* R7: real virtual locators, prioritized issues, impact and smallest remedies;
	caption gaps include outcome definition, units, timing, denominator, uncertainty
	and absent image, not a claim of visual inspection.
* R8/R9: respectful response maps actual virtual wording change versus
	unperformed work; human approval remains necessary, no external action or
	independent-certification claim.

## SP-SC-004 Together

### User Turn 1

Using this separate virtual teaching file empirical-note.md, suggest an outline
and a short results paragraph.

* [empirical-note.md:Methods:1] Twelve fictional service sites received a
	programme invitation.
* [empirical-note.md:Results:1] Three sites improved uptake, six were unchanged,
	and follow-up is missing for three sites.
* [empirical-note.md:Results:2] No statistical analysis, comparison group, or
	effect estimate was performed.

No venue policy is supplied. Do not invent missing statistics or methods.

### User Turn 2

For a separate virtual teaching manuscript method-proposal.md, help frame the
contribution and evaluation section.

* [method-proposal.md:Design:1] The proposed method prioritizes case records
	for human review using stated criteria.
* [method-proposal.md:Status:1] The method has not been evaluated, deployed,
	or compared with another approach.

Keep proposed work distinct from performed work.

### User Turn 3

For a separate virtual teaching protocol future-study.md, draft a scope paragraph.

* [future-study.md:Plan:1] The team plans a prospective observation study next year.
* [future-study.md:Status:1] Registration and ethics review have not yet been obtained.

Retain future tense and truthful status while giving a useful outline for
the planned work.

### User Turn 4

For a separate virtual teaching review project handpicked-review.md, propose
an appropriate title, article type, and opening paragraph.

* [handpicked-review.md:Sources:1] The authors selected four familiar publications.
* [handpicked-review.md:Limits:1] No database search, query, date range,
	screening record, or eligibility process is available.

The authors want to discuss themes and limits of the selected material.

### User Turn 5

For a separate virtual teaching review record structured-review.md, write a
concise methods summary.

* [structured-review.md:Search:1] Fictional database: TeachingIndex; search
	date: 2042-05-01; query: "service uptake" AND "local intervention".
* [structured-review.md:Selection:1] Records identified: 24; duplicates
	removed: 4; screened: 20; full texts assessed: 8; included: 5.
* [structured-review.md:Eligibility:1] Included reports described uptake
	outcomes after a local intervention; excluded reports lacked outcome reporting.
* [structured-review.md:Limits:1] One database and English-language records only.

Use only this supplied record and its stated limitations.

### User Turn 6

For a separate virtual teaching perspective file perspective-note.md, draft
one argument-led paragraph and then provide an assisted critique in chat.

* [perspective-note.md:Argument:1] Local teams should publish negative
	implementation findings because silence can distort practical learning.
* [PerspectiveSource1:passage:2] "Unchanged outcomes can identify contextual
	limits and guide future adaptation."
* [PerspectiveSource2:passage:5] "Publication bias may reduce visibility of
	null results."

Do not create fictional study methods or results. Keep this as assisted
critique rather than independent review or certification, and identify any
human approval still needed.

### Coverage and Observable Signals

* R1/R2: bounded chat drafting across separate virtual files and generic
	advice when no venue policy is supplied; no policy bleed between scenarios.
* R3/R4: source-bounded passages/counts, mixed/null/missing results, future
	and unregistered/unevaluated status; no invented analysis or approvals.
* R5/R9: human approval, assisted critique not independent peer review.
* R6: empirical outline/results, proposed-method contribution/evaluation,
	prospective protocol, narrative rather than unsupported systematic label,
	positive supplied-search/selection route and argument-led perspective.
* R7/R8: focused actionable critique, no irrelevant new experiment or remote,
	publication or performed-research claim.

## Design Bounds and Lead Acceptance

The independent designer returned Complete with exactly ten turns, all fictional
and inline. Parent accepts full fresh R1-R9 coverage, with all three original
coverage misses now requiring concrete observable responses. No expected-answer
oracle is forwarded as a user prompt. The virtual names/locators identify user
materials, not the agent artifact or its internal workflow.

Untested: native filesystem/tool reliability or enforcement, actual source
acquisition, visual/statistical quality, current real venue policy, runtime model
identity and paired identity-bias comparison. These are not falsely supplied
by the fixtures or claimed as simulation outcomes.

## Independent Addendum SP-BD-002-A1

The designer returned Complete with one positive full-text-support scenario,
SP-SC-005. Lead validation found a fixture arithmetic error: 15/20 minus 12/20
is 15 percentage points, not the designer's 12. A focused Node arithmetic
assertion passed; both the claim and reported difference below are corrected
to 15 before execution. No target rule or source revision changed.

### SP-SC-005 User Turn 1

For a teaching exercise, assess the manuscript claim below against the
complete fictional scientific report that follows. State the evidence status
for the claim, identify the report locator(s) you relied on, and describe
important limits.

Manuscript claim: "In this one-site randomized feasibility study, a reminder
increased day-14 form completion by 15 percentage points among enrolled
participants; the study did not assess attendance."

COMPLETE fictional report, one page

Title: Reminder messages and follow-up form completion: a feasibility study

Methods (p. 1, para. 1): At one community clinic, 40 enrolled adults were
randomly assigned to receive either one reminder message or usual follow-up;
20 participants were assigned to each group. The prespecified outcome was
completion of a follow-up form by day 14, and attendance was not collected.

Results (p. 1, para. 2): By day 14, 15 of 20 participants receiving a reminder
completed the form, compared with 12 of 20 receiving usual follow-up, a
difference of 15 percentage points. Two reminder-group participants and three
usual-follow-up participants had no recorded reason for non-completion.

Limits (p. 1, para. 3): This small, single-clinic feasibility study was not
designed to estimate effects beyond the enrolled sample or to determine why
forms were not completed. Because attendance was not measured, the report
makes no finding about attendance or any broader service outcome.

### Addendum Coverage and Limits

Assess a material qualified claim using the entire supplied fictional source,
with precise Methods/Results/Limits locators and numerical consistency. The
positive full-text-support branch is limited to the inspected complete fixture,
not independent real publication identity, provenance, external truth, scientific
certification or web verification. Expected evidence-state language is not
included in the user prompt. All existing scenario evidence remains at the
same unchanged target revision. Final grading will freshly reassess all eleven
raw responses in this still-open full run; no prior grades are reused.