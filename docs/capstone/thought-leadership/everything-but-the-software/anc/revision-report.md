---
title: Everything but the Software - Revision Record
description: Narrative and author-TODO reconciliation, remaining evidence plan and preserved dated review records
ms.date: 2026-11-26
---

## Review-comment cleanup 26 November

At the owner's request, the eight review-comment blocks were removed from
`main.tex` after the author-voice revision. Exact byte comparison confirms
that only those 40 fully commented lines changed. No review markers remain
in the package's TeX files. The revised prose, other inputs and PDFs are
unchanged; no new PDF build is claimed.

The source binding and existing provenance guard now include
`review_annotation_cleanup`. Earlier revision records and hashes below
retain their original scope, including the feedback dispositions.

## Marked author-voice revision 26 November

### Marked passages and reader context

The owner marked eight examples of wording that felt unnatural or assumed
too much project knowledge. Those passages were revised first. The resulting
lessons were written into
[ama-author-voice](../../../../../.github/skills/ama-author-voice/SKILL.md),
then applied across all 71 headed sections in the article and seven active
TeX inputs. Five TeX sources changed. The other three inputs were reviewed
and retained. The selected title and 29 November manuscript date are unchanged.

Work continued from `aa62820383958c4ebfc9f2704eb6b1d026de4dff`, with
owner-staged annotations already present. The original eight comment blocks
were preserved. Some feedback lines lacked TeX comment prefixes; they are
now fully commented so the notes do not render as manuscript prose.

| Marked passage | Applied revision |
| --- | --- |
| Abstract, "rebuild a working demonstrator" | Describes taking an early prototype toward a fuller product. The Introduction explains the supplied retrofit use case and the author's intent to approach production readiness, without asserting that readiness was achieved. |
| Abstract, "the replacement" | Names the new application and the failed action: signing in. |
| Abstract, "realized controls" | Names the longer-session comparison group and explains its remaining room for improvement. The numerical ceiling and unmet target are unchanged. |
| Introduction, "sustained conversation ... preceded autonomous delivery" | Describes weeks spent discussing requirements and recording decisions before asking the coordinator to implement the backlog. |
| Introduction, "though I measured neither gain" | States the author's expectation that clearer requirements would help agents build faster and make fewer mistakes. The case method and Discussion retain the absence of a measured comparison. |
| Introduction, "The paper contributes" | Explains how the investigation moves from earlier studies through the product-development case to a separate coding experiment. |
| Case setting, unexplained internal-assessment disclaimer | Removes the orphan disclaimer and retains the automated scorer's implementation-completeness signal with its evidence cross-reference. Confidentiality and unresolved release linkage remain intact. |
| Discussion, "In my participant account" and "Research assembled a corpus" | Uses first person, refers back to the introduced product, and describes research and role-based agents' actions. The account remains distinct from independently checked task execution. |

### Reusable skill and whole-paper pass

The skill owns the author-voice profile formerly embedded in the
[scientific-writing agent](../../../../../.github/agents/ama-scientific-paper-writer-reviewer.agent.md).
The agent now loads it on demand. Its scientific responsibilities,
frontmatter and approval boundaries are unchanged.

The learned rules concern missing meaning rather than forbidden words:
introduce the object and purpose, name who acted, explain comparison groups
and separate personal expectations from measured benefits. The skill requires
a marked-first pass followed by a full reading and narrative check. Its eight
editing examples are conditional, not replacement strings.

The whole-paper pass introduces the housing-retrofit product before internal
labels, explains the five experiment groups before the predictions, and
defines runs, contracts, follow-up sessions, passing witnesses and complete-frame
comparisons. Headings now describe their contents in ordinary language.
The narrative follows preparation, implementation, blocked use and the narrower
experiment, whose stable retention changed the original interpretation.
Measurement details and historical qualifications remain in their existing
records. Tables and literal prompts retain their scientific roles.

The three blog samples linked in the skill informed voice, not current
technical guidance. Relevant passages were read earlier in this revision;
the second and third retrieved responses were truncated after those passages.
No new literature finding or experiment is asserted.

### Validation and remaining limits

Classification: focused manuscript work, a repository-local prose skill and
directly coupled authoring guards. No application, experiment, infrastructure,
deployment, dependency, security control or repository-gate semantics changed.

All 88 selected authoring tests pass after one correction batch for wording
guards and a source-line wrap. The unchanged native-diagram regeneration test
was excluded because its required Playwright browser was previously found
unavailable; it was not rerun or counted as passed. The first command batch
used the repository root instead of the package directory and was rerun from
the correct directory.

ChkTeX, structural and whitespace checks pass. The structural checker reports
17,578 approximate body words and 1,879 abstract source characters against
the strict limit of fewer than 1,920. Historical baseline `0d5dcb02` remains
unavailable. Ruff reports no findings in the provenance test. The figure
test's existing `I001` and planning test's existing `FURB167` were reproduced
from HEAD; this revision introduces no new Ruff diagnostics.

Exact comparisons preserve seven equations, 176 labels, eleven figure inputs,
three literal prompt inputs, the embedded bibliography and all 61
source-register rows. Numerical sequences match in all 43 table environments;
all 28 instrument/result tabular bodies in the protocol and measurement
inputs are byte-identical. Two active Supplement body digests were refreshed.
Earlier revision bindings and adverse records remain unchanged.

Two PDFLaTeX passes with shell escape disabled produced a separate 75-page
preview. The final compiler log has no warnings, box warnings, missing
characters or unresolved references. Every page has content and in-page
words. Rendered pages 1, 2, 8, 13, 17, 35, 46, 55, 59 and 72 were inspected.
The Supplement begins on page 46 and the source register on page 72.
The preview digest is
`cd2f86c40d030cd466e7021674038d8e0e75a76c4c90bdc66c389759c65455f1`.
`author_context_revision` binds the final sources and preview.
The delivered PDF remains unchanged at
`ff263095ed331c8cdb0d91df7350f4772439b36fc3f986b7baa2612058f21233`;
it is not claimed to match this revision.

Skill frontmatter, name/path agreement, local links and unchanged agent
frontmatter pass. An assisted self-review against the HVE Builder catalog
and rubric found no required corrections. The reviewed skill digest is
`e584ed7199c7aa604c9c1711a34f169c868efad81ff3143a1f28ba27c0b73884`;
the agent digest is
`8c47e7221356e30a94b5fedf46e0c0899854bc7615e9800a7b4ae4bb84f60805`.
There is no root plugin or npm distribution manifest to synchronize, and
the skill ships no scripts. New-session discovery was not independently
exercised. This is a self-review, not an efficacy study or independent review.

Automated prose scoring remains unavailable. A missing PDF-inspector import
was resolved with a task-local installation used only for validation.
No candidate, evaluator, judge, deployment or paid experimental run was
executed. No assistant commit, push or publication ran.

Work execution: Complete for the marked revisions, reusable skill,
whole-document pass and separate preview. Assessment: assisted style/context
review and selected authoring checks complete; the existing browser-dependent
regeneration and baseline lint findings remain unresolved. Human author
acceptance, independent scientific review, hosted CI and publication approval
remain separate and unperformed.

## Unsupported-claim revision 26 November

### Scope and claim dispositions

The owner requested a second whole-paper pass: add a real case or named source
to claims without an example, number or source, or cut them. All 71 headed
sections across the article and seven active inputs were reviewed. Six TeX
sources changed. Definitions, explicit proposals, mathematical consequences
and necessary uncertainty statements retain their distinct roles.

Work began from clean commit `c953b07b5c48f506d51b0548ef35177fa28c481e`.
The case and experiment pins remain
`29c6b512f5e68733bb2cc1882343db39f5eb2cad` and
`d097a10b090baefadf995ecd910eb96c324f0234`. The earlier
[claim-to-example map](#claim-to-example-and-evidence-map) retains the inspected
case-log and report passages. The table below records this stricter pass;
source support is limited to the specified claim and passage.

| Manuscript locator | Disposition | Evidence and verification limit |
| --- | --- | --- |
| Introduction, Cunningham paragraph | Retained the named WyCash account; cut the unsupported visible/hidden-debt taxonomy and generic maintenance opener. | Existing Cunningham citation. No new debt measurement or literature finding is asserted. |
| Introduction, PhotoCraft and SWE-Maintain | Retained the reported project and benchmark results; cut the inference that agentic development compresses schedules and makes maintenance more pressing. | Existing cited results do not establish that schedule effect. |
| Introduction, discovery chronology | Replaced the claim that preparation made hasty prompting hard to blame with the recorded sequence of discovery and delivery. | Case evidence index, author-review context and retained coordinator recovery. Preparation does not rule out rival explanations. |
| Introduction and Background 2.3 | Replaced broad instruction-inheritance and maintenance claims with this experiment's repository/handover arrangement and named recommendations. | Protocol design; Nigh's "What works in practice" recommends runnable commands and explicit boundaries. Anthropic's "Compaction" and "Structured note-taking" describe context curation. Targeted relevant passages were inspected; this is practitioner guidance, not an efficacy estimate. |
| Case narrative and constructs | Added case-index locators and named the author's approval responsibilities; removed repeated claims about the importance of complete workflows. | Case evidence index, `author_review_context.discovery_and_handoffs`, O1, O2 and O5. The participant account remains separate from independently executed journeys. |
| Case contrast table and Supplement A.2 | Replaced causal wording about task framing with changed conditions whose effects were not isolated. Replaced unverified version changes with recorded model-selector changes. | Case evidence index, historical coordinator recovery and instruction versions. Actual backend identities remain unavailable. |
| Supplement A.2, counter-evidence | Attributed healthy-revision reports to coordinator summaries and MVP use to the participant; retained human approval boundaries. | Case evidence index, adverse-outcome summary at turn 1022, O1 and coordinator instructions. Neither report supplies a verified paired sign-in trace. |
| Discussion 8.2, "What worked" | Cut the uncorroborated durations "in days" and "in a day", and the exact claim of rejecting five agents. Retained the concrete consent, professional-judgement and prototype examples. | Author review and case-index discovery/handoff entries support revisions and prototypes, not measured speed benefits. No human-only comparison exists. |
| Discussion 8.4 | Gave Darwin and SkillOpt their own existing citations instead of leaving Ng's citation to appear to support all three. | Existing named procedures; no source replacement or bibliography addition. |
| Discussion 8.5 | Replaced a causal explanation of low loss with the endpoint's rollback/protected-test scope; tied unequal preservation burden to GPT's CR1 prerequisites. | Protocol, resource/information boundaries and CR1 prerequisite table. The policy's causal effect was not separately tested. |
| Discussion 8.5, follow-up | Cut speculative benefits of full RPI and the unsupported prediction of substantially higher token needs. Retained discovery-disabled status and an explicitly proposed comparison subject to resource approval. | Runtime-boundary record and reported model/arm cells. No follow-up efficacy or spending estimate is claimed. |
| Discussion, case follow-up | Cut the unevaluated squash-diff recommendation; retained archive/restore and approval requirements as conditions on any later retention change. | Explicit proposal and repository evidence-retention boundary, not an experimental result. |
| Supplement A.3.4 | Replaced "checks caught bounded defects" with the specific size-limit correction and its interrupted gate. | Previously inspected PR 445. The interrupted gate did not pass; elapsed gate and review effort were not measured. |
| Supplement economics and deferred measures | Cut nonlinear-cost speculation and the claim that rate definitions would prevent rewarding failure or discouraging judgement. | The assumed cost model, equations and intervention exclusions remain intact; their behavioural effects were not evaluated. |
| Methods and Supplement A.12 | Replaced broad repeatability and cost-free preparation claims with evaluator/source boundaries and the judge-call formula's scope. Cut the generic claim that multiple judges expose disagreement where no between-model comparison ran. | R05 evaluator inventory and the completed judging record. Preparation cost was not measured; development-model overlap and the earlier 313-trajectory judging frame remain explicit. |

The two newly rechecked public recommendations are
[Nigh's agent-instruction article](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
and [Anthropic's context-engineering article](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents),
retrieved on 26 November 2026. Initial responses were truncated; a subsequent
targeted retrieval included Anthropic's compaction and note-taking passages.
Only those relevant passages support the added recommendations. This was not
an exhaustive external-citation audit.

### Checks and concurrent delivery

Classification: focused manuscript work and directly coupled source-binding
tests. No study design, experimental scoring, application, infrastructure,
deployment, security control or repository-gate semantics changed.

All 88 selected authoring tests pass. The one excluded test is
`test_given_native_exporter_when_run_then_exports_without_rewriting_sources`;
its earlier execution failed because Playwright browser build 1194 was absent.
It was not rerun or counted as passed. Diagram sources and exports are
unchanged. Ruff, ChkTeX, structural and whitespace checks pass. The structural
checker reports 17,213 approximate body words and 1,823 abstract source
characters against the strict limit of fewer than 1,920. Its historical
comparison against `0d5dcb02` remains unavailable.

Exact comparisons with the intake preserve seven equations, 176 labels,
eleven figure inputs, three literal prompt inputs, 61 source-register rows
and the embedded bibliography. Numerical sequences in all 43 table
environments are unchanged; the result tables in the protocol and measurement
input are byte-identical. Scientific results, unknowns, billing holds and
dependence limits retain their existing meaning. Three changed active
Supplement body digests were refreshed, with earlier revision records kept.

Two PDFLaTeX passes with shell escape disabled produced a separate 75-page
preview. The final compiler log has no warnings, box warnings, missing
characters or unresolved references. Every page has content, and extracted
words remain within page bounds. Rendered pages 1, 2, 6, 35, 36, 47, 49, 59
and 72 were inspected. The Supplement starts on page 46 and the source
register on page 72. The preview digest is
`21a14331918ef957a9f26354cabfab674466bbd65ca5878a74bd344912d0514b`.

During validation, another process committed most of the prose and a changed
delivered PDF in `25463dd58d4aa3fbb3737f4ccee194cc21edae35`. The owner
explicitly approved retaining that work and finishing the remaining sources,
bindings and evidence records. The intake PDF digest was
`3cd7f5c5db89b757128f5468e064241980c807060ce0de5558ffe96b365e948c`;
the retained PDF is
`ff263095ed331c8cdb0d91df7350f4772439b36fc3f986b7baa2612058f21233`.
This build did not overwrite either delivered file. The retained PDF's
equivalence to the final sources is not asserted; use the separate preview
for this revision. `unsupported_claims_revision` binds the final sources and
preview while preserving the previous delivery records.

Automated prose scoring remains unavailable because the installed detector
could not be found. No candidate, evaluator, judge, deployment or paid
experimental run was executed. No assistant commit, push or publication ran.

Work execution: Complete for the authorized manuscript, records and separate
preview. Assessment: scoped claim grounding and selected authoring checks
complete; native-diagram regeneration remains blocked. This assisted pass is
not independent scientific review. Human approval, applicable hosted checks
and publication acceptance remain separate and unperformed.

## Concrete-example revision 25 November

### Scope and applied changes

The owner requested a review of the whole whitepaper for generic claims,
with real examples replacing vague explanations. The approved outputs were
all eight active TeX sources, existing revision records and a separate PDF
preview. The owner subsequently approved the directly coupled source-binding
test update. Work continued on `docs/remove-paper-results-switch` from
`4538851406ef3945aa71c98dc202d926a3b618df`; no commit, push or submission ran.

The review covered 71 section, subsection and subsubsection headings, including
starred sections, across the article and seven active inputs. Changes name
the observed task or inspected procedure instead of adding unsupported
performance claims. Repeated summaries were shortened where the example
already explained the point. The selected title and 29 November 2026
manuscript date remain unchanged.

Classification: focused manuscript work with directly coupled source bindings
and one existing authoring-test update. No application, experimental scoring,
dependency manifest, infrastructure, deployment, security control or repository
gate semantics changed.

### Claim-to-example and evidence map

Case passages use the retained source pin
`29c6b512f5e68733bb2cc1882343db39f5eb2cad`. Experiment passages use the
[final report](https://github.com/jmservera/ama-thought-mve/blob/d097a10b090baefadf995ecd910eb96c324f0234/results/pilot-estimation/report.md)
at `d097a10b090baefadf995ecd910eb96c324f0234`, with the existing
[numerical snapshot](./study-results-2026-11-15.json) and
[case evidence index](./case-evidence-matrix.json).
Full-text support below means the inspected passage supports the stated
example; it does not mean every source or external claim was audited.

| Manuscript locator | Concrete replacement | Inspected source and locator | Evidence state and limit |
| --- | --- | --- | --- |
| Abstract; Sections 3.1 and 4.2 | Inability to sign in, followed by the difference between app-role assignment and an internal staff binding; the recorded error is "no staff record with this oid". | Case account and historical knowledge-base log, lines 1912-1916 at the case pin. | Full-text support for the recorded distinction; no paired release-linked sign-in execution was recovered. |
| Introduction | Before another chat-app feature, start the server, create a chat, send a message and check its response. | [Anthropic harness article](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), "Getting up to speed". | Full-text support for the described startup check; no estimate of its effect on this case. |
| Sections 3.2 and 4.1 | Photo/GPS provenance, professional assessment, structured-invoice, capacity and sensor what-ifs; the journey-atlas handoff to requirements. | Historical log, lines 334-381 and 468-477; [PR 71](https://github.com/jmservera/ama/pull/71), requirements and approval disposition. | Full-text support for recorded discovery and handoff; role answers remain exercise hypotheses. |
| Section 3.2 and opening of Section 4 | "My cases today", case cards, call logs, manual paths and separately recorded resident decisions; a material handover change requiring fresh acceptance. | Historical log, lines 1202-1213; [PR 32](https://github.com/jmservera/ama/pull/32), prototype simplicity review; retained prototype review RV-001, re-acceptance after handover. | Full-text support for recorded affordances and review findings; fresh acceptance was a proposed remedy, not a completed staff usability study. |
| Sections 3.3 and 4.4 | "build all new in src, but migrate what's needed first"; later, "provide a running website as soon as possible". | Case evidence index, retained coordinator user-message turns 66 and 1147. | Full-text support for owner steering; the messages do not establish deployment completion or actual historical worker identities. |
| Section 5 and Supplement A.3 | Requirement handoffs, missing staff bindings, the file-size-limit correction and requests for a running site replace abstract mechanism indicators. | Case records above; [PR 445](https://github.com/jmservera/ama/pull/445), per-artifact size override and interrupted full gate. | Full-text support for the records. PR 445 did not pass that interrupted gate; mechanisms remain hypotheses, not measured causes. |
| Sections 7.2-7.4 and 8.4; Supplement, "Additional endpoint and resource statistics" | Consent/hold precedence, contractor-field redaction, ranking consistency and regional handoff; `READ_METHODS`, `view.rank_cases()` and `NotAllowed`; known versus newly added writes through read-only views. | Final report, GPT F9 ranking and read-only test incompatibility; Gemini `privacy:3` and regional/handoff extension accounts. | Full-text support for report examples. The records do not identify the treatment action that caused a cell difference. |
| Sections 7.9 and 7.11; Supplement, "Detailed post-collection ratings and calibration" | Different CR1 preservation burdens and a terminal `ValidationError` without a later recovery action explain endpoint and calibration limits. | Existing CR1 prerequisite table; final report, calibration disagreement on `ranking:3`. | Full-text support for the recorded distinction; the two GPT CR1 outcomes and incomplete calibration remain unresolved. |
| Background Section 2.3 and engineering-rationale paragraph | SkillOpt retains validation-selected edits and rejected-edit feedback; AgentRx checks trace evidence against schema and policy; one Kiro bug fix expands to four stories and sixteen criteria. | [SkillOpt](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/), "How SkillOpt works"; [AgentRx](https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/), guarded diagnosis; [Böckeler's trial](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), Kiro example. | Full-text support for inspected procedures and trial details; external retrieval was targeted and partly truncated, not an exhaustive literature audit. |
| Supplement opening and "Illustrative economics and sensitivity" | The existing cost-model example explains the assumed implementation premium beside the measured ten-feature spending. | Existing illustrative economics, equation definitions and figure inputs. | Illustrative assumption, not fitted evidence or measured currency savings. |
| Supplement A.9 | Eighteen GPT F9 permission-request sessions are concrete annotation candidates. | Final report, execution/tool account; existing Supplement task and accounting record. | Full-text support for requests and unchanged-source records; received help, HIR and IDR are not inferred. |
| Supplement A.1 and A.11-A.16 | Source-specific qualifications, nonzero Sonnet lint despite report generation, zero retained loss without acquiring ranking, citation-ID anchoring and the limits of note word counts. | Retained literature qualifications, final report, numerical snapshot and literal prompt records. | Full-text support for the stated examples and instrument rules; counts and generated reports do not establish usability or review quality. |

### Validation and preview-only delivery

The structural checker passes. The abstract has 1,823 normalized source
characters against its strict limit of fewer than 1,920. The approximate
main-body count is 17,428 words under the existing checker definition.
Its historical comparison against `0d5dcb02` is unavailable.

Exact comparisons with the intake commit preserve all seven displayed
equations, 176 labels, eleven figure inputs, three literal prompt inputs,
61 source-register bindings and the embedded bibliography. Numerical
sequences in every table are unchanged. The reusable bibliography,
experimental snapshot, diagram sources and figure exports are untouched.

The initial 89-test authoring run found stale source bindings, the earlier
record's PDF digest mismatch and a missing Playwright build 1194 browser.
The authorized test update reads the new revision binding while retaining
the historical chain and evidence checks. The subsequent focused selection
passes all 88 tests; native-diagram regeneration was not selected because
its required browser remains unavailable. Ruff passes for the modified
test, and ChkTeX and the whitespace check pass.

Two PDFLaTeX passes with shell escape disabled produced the separate
75-page preview. The final compiler log has no warnings, box warnings,
missing characters or unresolved references. Every page has content and
all extracted words are within page bounds. Rendered pages 1, 4, 8, 9, 13,
28, 36, 46, 69 and 72 were inspected; the Supplement starts on page 46 and
the source register on page 72.

The preview SHA-256 is
`8e3110d7438b213bb6a7cf1d2831e984fca546f071be4708a43e90fb1ae1a421`.
The unchanged delivered PDF remains
`03695df517d118e6e6bbf8e022c4126e83806cd28db3e35aae434346d22c7a8b`.
The older cleanup record's different PDF digest is preserved as history,
not silently replaced. `generic_claims_revision` records the current source
and preview bindings; four active Supplement body digests were refreshed.
The preview and compiler evidence are in this session's files directory;
they were not published or copied over the delivered PDF.

Automated prose scoring is unavailable because the installed detector could
not be found. No new candidate, evaluator, judge, deployment or paid run was
executed. The 315 trajectories, conditional interval, original unmet target,
two CR1 unknowns, 55 billing holds, unregistered amendments and dependence
limits retain their existing meaning.

Work execution: Complete for the authorized prose, records and preview.
Assessment: scoped example grounding and selected authoring checks complete;
native-diagram regeneration is blocked. Independent scientific review,
human approval, applicable hosted checks and publication acceptance remain
separate and were not performed in this revision.

## Publication revision and disposition 24 November

The owner authorized repairs against the completed experiment and excluded
another experimental round. A deeper study will address the remaining
measurement and identification questions. The revision preserves original
scores, thresholds, intervals, literal prompts and prior adverse findings.
New tables are post-collection descriptions of existing public exports.

Classification: focused document/package work with directly coupled
authoring guards and data bindings. No application, experimental scoring,
execution, dependency manifest, infrastructure, deployment, security control
or repository gate semantics changed. The owner selected the current branch
despite its separate presentation PR. Unrelated agent-file work was left
untouched.

### Publication checklist

| No. | Review item | Applied disposition | Remaining action or limit |
| --- | --- | --- | --- |
| 1 | Dependence and uncertainty | Preserve the original estimator and intervals; state their independence assumptions in methods, abstract and conclusion. | Service/epoch dependence is unmeasured. Intervals support conditional exploratory interpretation. |
| 2 | Amendments and outcome access | Retain sixteen source epochs and distinguish decision/commit dates from collection and inspection times. | Complete outcome-access chronology remains unavailable in the public final-study exports. |
| 3 | Ten-point threshold and ceiling | Add the realized 96.9629% D mean and 3.0371-point maximum gain against those controls. | Original target remains unmet; a future outcome/target pair needs calibration before collection. |
| 4 | PF1 retained F/P reporting | Reconcile all 6,300 rows: complete risk and observation flags, 630 empty-risk rows, one persistent episode. | Rich observed-subset reporting for future incomplete histories remains deferred. |
| 5 | Rollback and test protection | Explain that rejected increments were reset and accepted tests protected. | Retained loss cannot describe every failed edit or an unchecked maintenance policy. |
| 6 | PF2 CR1 prerequisites and graded outcomes | Add all fifteen F9/F10 prerequisite cross-tabulations from existing exports. | Strata are post-treatment; complete graded new-contract/prior-pass decomposition remains deferred. |
| 7 | Two CR1 test errors | Preserve unknown status and allocation bounds. | Existing summary exports do not settle the causes; no rerun is used. |
| 8 | F8/F9 immutable-test mechanism | Keep the source report's inspection and identify interaction with the harness's accepted-file policy. | No separately randomized mechanism or general model-ranking claim. |
| 9 | PF3 cost completeness | Tabulate held attempts by all fifteen model/arm cells and retain settled-subset denominators. | 55 charges remain held. All-allocation, quality-matched efficiency and long-horizon payback remain unidentified. |
| 10 | O1-O5 case evidence | Recover source-located steering, repeated scheduling and adverse assistant reports; preserve participant-observer status and null release/journey pairs. | Complete HIR/IDR annotations, denominators and underlying outcome receipts remain unavailable. Case mechanisms remain hypotheses. |
| 11 | Historical runtime identifiers | Recover the committed Sonnet worker selector, tmux/RPI prescriptions and later script chronology. | Prescribed selectors do not verify execution. Historical CLI, reviewer and backend identities remain unavailable in the inspected records. |
| 12 | Consequential citations | Inspect the full SEC Order 34-70694 (Paragraphs 1, 12-17), SEC release 2013-222 and Borg et al. (2026) PDFs supplied by the owner; inspect full text of retained open web articles; remove 14 non-essential citations that had only abstract, excerpt, HTTP 403 or unverified third-party upload access. | Classic print books and papers cited for conceptual background were not re-audited page by page; no independent replication of cited studies' raw data is claimed. |
| 13 | Metric fidelity and stopping | Keep structural measures as treatment-target proxies and retain the Ruff suppression caveat and unmet lint target. | No new suppression audit or inferred reason for session termination. |
| 14 | Judging completeness | Keep the frozen 313/315 study frame and four unjudged endpoint packets. | No new judging; its dependence and missing-scenario limits remain. |
| 15 | Human calibration | Retain the incomplete, AI-assisted author spot-check and context denominators. | Independent reliability is unestablished; a later instrument needs separate calibration. |
| 16 | Abstract and conclusions | Lead with completed exploratory findings and measurement lessons; add ceiling, protection and conditional-inference limits. | No causal, broad model-population, hybrid-efficacy or payback claim. |
| 17 | Stale source binding | Add a new publication revision binding and preserve previous source/PDF records. | The final binding applies only to its named files. |
| 18 | Authoring checks | Narrow the case-voice guard, align wording checks and add a table/snapshot consistency check. 74 of 75 authoring checks pass. | Native diagram rendering rejects five arm feature labels for text overflow on this host. Existing committed figure/source bindings pass; regeneration remains unresolved. |
| 19 | Source/PDF consistency | Rebuild one PDF with the additive Supplement from the revised source. | Final pagination, digest and actual checks are recorded with delivery. Earlier page counts remain date-scoped. |
| 20 | Deposit manifest and registration | Publish GitHub release `results-exploratory-s1-v1` at `d097a10b` with a 216-file sanitized archive, SHA-256 sidecar and manifest (excluding `.copilot-tracking/` and `suite.json:sec.endpointdlp`); preserve `v4`/`v6`/`v7` and OSF `ywsrv`/`xcpt4` without creating a post-collection OSF deposit. | OSF registration metadata remains owner-confirmed rather than API-verified (HTTP 401); raw workspaces and private mappings remain off-Git. |
| 21 | Human clearance and approval | Record manager approval, the 14 November AICC receipt, the owner-reported manager confirmation of a 14-day no-objection window maturing 29 November 2026, and both authors' sign-off (Juan Manuel Servera Bondroit and owner-reported explicit sign-off from Isabel Cabezas Martin). | Written CELA policy was not independently inspected, 29 November 2026 has not yet elapsed, and the authors must confirm the 14 November submission and final sign-off cover this exact 24 November draft, subtitle and recovered excerpts. |
| 22 | arXiv source and metadata | Add canonical policy links and instructions for the 22 required compilation inputs, metadata, licensing and generated-PDF inspection. | Actual submission, endorsement if required, license choice and arXiv compilation remain pending. |
| 23 | Completed-research framing | Foreground the executed 315-trajectory study and its measurement contribution; update the subtitle to *An Exploratory Case Study and Experiment* per owner selection. | Confirm coauthor sign-off covers the updated subtitle on the exact submission PDF. |
| 24 | Independent final review | Separate local authoring checks from scientific assessment and approval. | Independent human scientific/statistical review and applicable exact-head/hosted review remain outstanding. |

### Evidence checked for the new reporting

The immutable experiment source remains
`d097a10b090baefadf995ecd910eb96c324f0234`. The four inspected exports
are `results/pilot-estimation/runs.csv`, `retention.csv`, `episodes.csv`
and `attempts.csv`. Their full hashes, derivation rules and cell counts are
in the [publication evidence snapshot](./publication-evidence-2026-11-24.json).
The original chart-input snapshot remains byte-for-byte unchanged.
An offline consistency check compared every new cell with those CSVs:
all four hashes, the retention counts, thirty prerequisite subgroups,
fifteen held-attempt cells and the realized-control ceiling matched.
This operation tabulated retained public records without executing
candidates, evaluators or judges.

The original seven equations and published uncertainty calculations are
unchanged. The publication revision also replaces staged contrast
sentences with direct statements where their scientific meaning can be
preserved. Qualifications concerning missingness, causal scope and approval
remain. The installed prose detector was unavailable; no automated style
score is claimed.

The citation verification pass on 25 November inspected the owner-supplied full
texts of SEC Exchange Act Release No. 34-70694 (18 pages, Paragraphs 1 and
12-17), SEC Press Release 2013-222, and Borg et al.'s *Echoes of AI* (78 pages,
Abstract and Sections 1, 2.2 and 4), confirming the 2005 Power Peg code move,
the July 2012 deployment omitted on one of eight SMARS servers, more than four
million executions from 212 customer orders, the loss exceeding USD 460
million, and Borg et al.'s late-2024 two-phase design (observational Phase 1,
randomized Phase 2 with no significant maintainability difference). Ten open
web/standards references were also inspected in full text, while 14
non-essential references that had only abstract, brief-excerpt, HTTP 403 or
third-party caption access (`beamnxw2026memorytalk`, `philia2026ngmoroney`,
`orosz2025beck`, `martin2026productengineers`, `besker2018cripples`,
`bird2014extrinsic`, `microsoft2026autosaddler`, `openai2026harness`,
`laban2025lost`, `beck2025augmented`, `beck2026mathematicians`, `beck2018tcr`,
`eldridge2016pilot`, and `gamma1995patterns`) were removed from both
bibliography files.

### Historical coordinator evidence

The owner authorized read-only historical VM investigation. The
[case evidence index](./case-evidence-matrix.json) now retains a bounded
recovery record with exact session/turn, date and committed-source locators.
The article and deferred-measures Supplement summarize it without publishing
host details, raw transcripts or private configuration.

The coordinator selection contains 1,198 retained rows from 15 to 24 October:
1,066 start with `[Scheduled prompt #` and 132 do not. The latter have not
been exhaustively classified as manually authored corrective help. The
record supports examples of migration and product steering, resource/gate
decisions and requests for functional/refactoring checkpoints. It also
preserves assistant reports of unresolved sign-in/readiness and checkpoint
failures. Underlying execution receipts and paired release-linked user
observations were not recovered. These row counts supply no HIR/IDR rate.

Committed instructions prescribe tmux/worktree issue sessions, qualified
RPI workers and recurring checks. The 21 October instruction version selects
`claude-sonnet-5.5` for workers and continuations, leaving the coordinator
Automatic and reviewer selection unchanged. Actual launches, historical
CLI/reviewer identities and backend builds remain unverified. The
versioned coordinator shell/Python scripts first appear on 22 November in
the inspected history; attributing them to the October case would be
unsupported.

The inspected experiment-kit checkout on that VM is an older copy without
the final pilot-estimation state at its expected location. It cannot settle
the completed study's two CR1 unknowns or 55 billing holds. Historical case
steering and the separate experiment's owner attestation retain their own
evidence boundaries. The investigation used stored records and Git sources;
no live resumed agent, model call, deployment or new experimental round ran.

### Publication validation and delivery

The rebuilt [paper](../main.pdf) has 73 pages, with its additive Supplement
starting on page 45 and the source register on page 71.
`publication_readiness_revision` in the
[integration record](./supplement-integration.json) binds all eight TeX
sources, the case/publication evidence snapshots, reusable bibliography and
the delivered PDF. Previous revisions and their original hashes remain
unchanged. The active Supplement body hashes were refreshed separately.

Checks performed:

* The structural checker passes: approximately 16,520 main-body words,
  1,802 abstract source characters, 80 cited/embedded entries and 91
  reusable bibliography entries. The optional `0d5dcb02` historical
  comparison remains unavailable.
* Two-pass PDFLaTeX with shell escape disabled succeeds. The final compiler
  log contains no warnings, box warnings or unresolved references.
  All 73 pages contain content, with no words outside page bounds or
  unresolved-reference markers.
* The complete package authoring suite runs 75 checks: 74 pass. All source,
  literal-prompt, active-Supplement, empirical-chart and committed-diagram
  bindings pass. The added reporting check preserves unknown CR1
  denominators, undefined empty-stratum rates and the held-attempt cells.
* The remaining failure is the unmodified native diagram exporter:
  five `arm-*-feature-label` elements exceed their containers during
  regeneration. The original missing-browser failure was resolved for
  validation with the official Chromium 141.0.7390.37 archive, Playwright
  build 1194, in a task-local cache. The automatic installer stalled after
  download and was stopped; the downloaded archive passed CRC verification
  and was extracted locally. This exposed the rendering failure. No
  diagram source, committed export, lockfile or exporter was changed.
* The clean compilation archive contains exactly eight TeX sources,
  eleven PNGs and three literal prompts (22 files, 7,219,690 uncompressed
  bytes). It excludes generated PDFs and private/raw histories. An isolated
  extraction compiles twice to 73 pages; extracted text matches the
  delivered PDF on every page. The integration record retains its digest.
  Ancillary evidence remains in the repository source package.
* The original chart-input snapshot, empirical figures and literal prompts
  remain byte-for-byte unchanged. No candidate, evaluator or judge was
  executed for these authoring checks.

Work status: the scoped scientific/prose revision, sanitized GitHub deposit
release (`results-exploratory-s1-v1`) and PDF delivery are complete; native
diagram regeneration remains unresolved. The remaining study gaps are
disclosed limits and inputs to a deeper study. Both authors' sign-off is
owner-reported; before upload, confirm that sign-off and the 14 November AICC
submission cover this exact 24 November draft, updated subtitle and newly
recovered excerpts, wait through the owner-reported 29 November 2026 CELA
no-objection date, and complete arXiv metadata, license and generated-PDF
inspection. Independent scientific review is recommended; local assisted
assessment supplies no human peer review or certification.
Applicable repository exact-head review and hosted checks have not run for
these uncommitted changes. Nothing was committed, pushed or submitted.

### Preserved earlier revision summaries

The 16 November source-only revision applies a plain-language pass to the
article and every active TeX input. Its scope and validation are recorded
below; the existing PDF is excluded from delivery.
The later abstract edit keeps the author's revised opening paragraph and
recasts the study description as a sequence: agents work through features,
then a separate isolated evaluator runs tests hidden from them.

The preceding v23 revision rewrites selected paper prose for direct, readable
language. It preserves the findings, study design, formulas, tables, figures
and source evidence, and records the rebuilt paper in a new binding.

The latest 15 November narrative revision connects the interrupted workflow,
hypotheses, exploratory findings and future-study learning. It records the
author's answers and distinguishes applied editorial changes from pending
VM evidence, source verification and final approval. The dated v21 and earlier
records below retain their original wording, including superseded approval
dates and validation counts.

The earlier 15 November readability revision centralizes exact provenance in
one end register, adds local result explanations and shortens repeated prose
without changing observations or expanding the 70-page delivery. The v20
and earlier source, review and delivery records below remain historical.

The 15 November final-results update incorporates the completed source-bound
315-trajectory dataset and adds human-readable direction and uncertainty cues
to the empirical and economics graphics. Earlier reviews, source pins,
incomplete-data states and validation records below remain historical.

The 14 November critique and falsifiability revision applies the external
review of hypothesis refutability: it separates the short-horizon decay
premise (P1) from the consolidation remedy (P2 coverage threshold
$\Delta_*=10$ percentage points; P3 CR1 adaptability and cost payback) and
the structural manipulation check, surfaces the per-model coverage split in
the abstract, main results and conclusion, and adds a 30-to-40-cycle
factorial follow-up design (`sec:futureexperiment`). It preserves all
existing numerical tables and earlier dated records.

The 14 November finalization follow-up records the exact Coach assessment,
original-source checks, active participant-name audit, allowlisted historical VM
metadata and the owner's approval/deposit decisions. It retains the existing
estimator, original outcomes, source-access limits and earlier adverse records.

The later 14 November report refresh records owner-attested coverage and
exploratory companion estimates from the changed local/online report. It
preserves the strict automated primary gate, two partial trajectories,
readability improvements and all earlier dated source and delivery records.

The 14 November readability revision reorganises the article around its
findings, separates the wide result tables and retains detailed statistics
and provenance in the existing Supplement. It changes no experimental
observations, scoring or protocol. Dated records below retain their original
wording and validation outcomes.

The 13 November study-results revision integrates the completed 315-trajectory
five-arm exploratory S1 experiment, 14 implementation epochs, 630-endpoint
workflow replay, 1,252-call blinded `gpt-6-luna` judging, 90-row human
calibration spot-check and 5,357-journal SDK intervention audit from
`results/WHITEPAPER_REPORT.md`, enabling `\resultstrue` while preserving all
earlier method, measurement and historical records.
The 9 November supplementary judging account adds prospective methods for
a separate post-collection instrument. It preserves original endpoints,
running sources, results TODOs and all earlier revision evidence.
The 8 November measurement clarification supplements the execution and
coauthorship record and corrects the earlier Ruff safeguard claim. It
changes no running experiment or recorded outcomes.
The 8 November execution and coauthorship record supersedes earlier
then-current implementation and pre-collection status. It does not
overwrite historical scientific findings or certify current execution.
The 5 November recovery/source check, 2 November allocation record and
1 November disposition retain their original evidence and limits. The sections
from Scope and Outcome through Title Assessment retain the original
24 October report, and the 25 October addendum remains historical. Their
earlier word counts, TODO locations and protocol choices are unchanged.

## Scientific author-voice revision 24 November

The owner requested a full review and rewrite for a scientific audience,
using the completed experiment and the voice in the supplied blog examples.
All 70 active sections were read, including the seven TeX inputs and back
matter. The two inactive historical inputs were excluded.

The three English blog posts were retrieved as style samples only. Their
practical motivation, direct explanations and candid trade-offs informed the
rewrite; their dated technical guidance supplied no scientific evidence.
The pinned experiment report at `d097a10b` was retrieved through GitHub REST,
and its SHA-256 matched `e4680e66ba6791c7a23bd484954767bc7d580f881db939cf4fb113d28af10f15`.
No private dataset or new model outcome was collected.

The abstract and opening were rewritten. Interpretive passages distinguish
acquisition, retained behaviour and extension failure, with the case account
in first person and experimental findings stated descriptively. The summary
table no longer labels the across-arm coverage range as Arm A alone,
claims no consistent CR1 saving and does not treat structural cleanup as
validation of an untested hybrid. Stable short-horizon retention remains
evidence against the expected decay pattern under these conditions.

Classification: focused editorial work with a directly coupled source-binding
test update. It changes no experimental data, scoring, execution, dependencies
of the application or publication authority. `scientific_voice_revision`
records the new sources and prior active-content digests; every older revision
binding remains unchanged.

Preservation checks compare the pre-edit source with the revision: all seven
equations, numerical values in 40 table environments, citation keys, labels,
three literal prompt references, the embedded bibliography and all 61 source
register rows are unchanged. Two CR1 outcomes, 55 billing holds, the
313-trajectory judging snapshot, dependence assumptions and clearance/source
TODOs remain unresolved. The 47-of-more-than-180 issue count in the opening
is attributed to the participant's account, not independently verified.

The installed humanizer and scientific-critical-thinking skills guided the
edit; the existing Scientific Agent Skills citation remains. The prose
detector was unavailable in the installed plugin/skill locations, so no
automated prose score is claimed. This is an assisted editorial review,
not independent scientific review or arXiv readiness certification.

Structural checks pass: the approximate body count is 16,152 words and the
abstract has 1,880 source characters, below the 1,920-character limit.
Of 74 authoring tests, 73 pass. The native figure-export test fails because
the expected Playwright Chromium headless shell is absent. No figure source
or asset changed; fresh exporter validation remains unperformed.

Two pdfLaTeX passes produced a separate 70-page PDF without unresolved
references or box warnings. All pages were checked for blank content and
out-of-page words; pages 1, 2, 22, 35, 45 and 68 were visually inspected.
The Supplement starts on page 45 and the source register on page 68.
The validation PDF SHA-256 is
`358554c5de5377fee258e44df10574c1393d92c59e2bdf595b2aaf2db8d2cfd1`.
The repository's existing PDF is unchanged. No new hosted CI or independent
exact-head review has run for this uncommitted revision.

## Copy Review Recommendations 16 November

The owner approved all five findings from the read-only copy review of
`main.tex` and its seven active imports. The edits affect the article,
`anc/experiment-protocol.tex` and `anc/measurement-provenance.tex`.

| Original finding | Applied change | Evidence and limit |
| --- | --- | --- |
| "Nobody has tested whether that works" claimed absence of research beyond the study's scope. | "This study did not test that procedure." | Narrows the claim without asserting a new literature search. |
| Historical reporting instructions preceded their status explanation. | Identify the earlier risk-set definitions and reporting requirements before presenting them. | The instructions and the inspected analyzer's narrower export remain distinct; no reporting gap is resolved by editing. |
| "Owner" left supplied registration/runtime information unattributed. | Use the participant-observer's existing first-person voice and identify the repository-maintainer role in the execution account. | The 8 November execution record retains the owner's supplied registration and runtime account. Metadata remains independently unverified; execution/data collection remains Cabezas Martin's role. Literal provenance status fields are unchanged. |
| "Every intervention ... [has] not been independently verified" had ambiguous negation. | State explicitly that out-of-band intervention coverage and private manifest contents have not been independently verified. | Preserves the distinction between published bindings and independent verification; no private manifest was inspected. |
| "Review wins on Gemini" overstated the descriptive comparison. | "Higher observed Gemini CR1 success under review." | Keeps the recorded counts, intervals and exploratory interpretation. |

Classification: focused editorial work with directly coupled source-digest
guard maintenance. The existing tests retain their coverage;
no application, dependency, security control or publication-gate semantics
changed. `copy_review_revision` adds all eight current source hashes.
The active Supplement content digest is refreshed, with its preceding value
retained in `prior_active_content_sha256`. All dated historical revision
bindings remain unchanged.

Direct comparison with intake commit
`1088d68f2e0b8870b3c17c22b2935b7944bc5075` preserves seven displayed
equations, 252 inline-math spans, all 94 citation commands in order,
172 labels, ten input commands including literal prompts, 36 full-line
comments and the numeric-literal sequence. Bibliography and PDF bytes are
unchanged. No new empirical claim, number, citation or actor role is inferred
from the copywriting rules.

Structural checks pass, including the unchanged 1,910-character abstract.
The first 74-test run found a stale active Supplement content digest after
the wording edit, alongside the existing diagram-export failure. After the
digest correction, 73 of 74 tests pass; the unchanged native diagram exporter
cannot import `esbuild`. Historical comparison with the checker's optional
`0d5dcb02` baseline is unavailable, separately from the direct intake
comparison above. No TeX compiler is available on PATH; no new PDF or
rendered-layout review is claimed.

Copy delivery checks pass for source-grounded wording, retained author voice,
scientific qualifications and absence of Unicode em/en dashes in the eight
active TeX files. UI, asset, motion and interaction checks do not apply.
Independent exact-head review and hosted checks are tracked in PR #1825;
local source checks do not establish scientific, author, employer or venue
approval.

## Conservative Prose Follow-Up 16 November

The owner requested a scientific-prose pass that included the imported TeX
sections and authorized inclusion of the existing staged abstract edits.
The article and all seven active inputs were checked. Since the prose
already needed little editing, further changes are limited to four wording
adjustments in the article and one sentence in the Supplement introduction.
Technical uses of terms such as harness, journey and end-to-end are retained,
as are uncertainty, attribution and first-person case narration.
The inactive inputs are unchanged.

Classification: focused editorial work with directly coupled source-digest
and authoring-test maintenance. The existing guard checks the new revision's
eight source hashes; its coverage is unchanged. Earlier bindings and review
outcomes remain historical. No executable application, dependency, security
control or publication-gate semantics changed.

Comparison with the intake source, including the owner's abstract edits,
preserves 35 complete table/longtable blocks, seven displayed equations,
252 inline-math spans, all 94 citation commands in order, 172 labels, three
literal-input commands, 36 full-line comments and all 2,731 numeric tokens.
The bibliography and reusable BibTeX file are unchanged. Expanded source
length falls from 33,426 to 33,422 whitespace-delimited words. Each input
stays within the requested length limit. Character checks find no unintended
invisible characters, mixed-script confusables, nonstandard spaces or trailing
line whitespace.

Structural checks pass, including the 1,910-character abstract and all
94 cited bibliography keys. The package run passes 73 of 74 tests.
The native diagram-export test fails because Node cannot import `esbuild`;
that failure was present before this pass and no diagram changed. A stale
source digest caused a second intake failure after the staged abstract edit;
the new binding resolves it while preserving the previous record.
No TeX compiler is available on PATH, so no new compilation or rendered-layout
check was performed. The existing PDF's bytes are unchanged.

Independent review of `a5080d83df569c9e2510dc0ddff83a6a9b126b3f`
found one issue: the inherited abstract said complexity was below ten, while
the methods set a target of at most ten and the results say no functions
exceeded ten. The abstract is corrected to at most ten. No observed values
changed. This finding and the original review outcome are retained here;
the final exact-head assessment and hosted checks are tracked in PR #1825.
After the correction, structural checks and all 28 measurement-provenance
tests pass. The unrelated diagram-export failure was not rerun.
The next review, of `2bb6342d6bf2a81acb8bbb0524b4a19de787c666`,
found a stale manuscript hash after the sentence changed between validation
and commit. With owner permission, the validated wording is restored and
the affected checks are rerun before publication. That review did not
reproduce the claimed test pass for the intervening source.

`prose_polish_revision` binds the eight current sources and unchanged PDF.
This editorial pass does not establish independent scientific peer review,
hosted CI success or final approval.
Earlier validation and review statements below apply to their named revisions.

## Human Readability Revision 16 November

### Scope and Changes

The owner requested clearer explanations, varied sentence length and common
language for computer scientists and data scientists using LLMs and agents
in the SDLC. The full current article and its seven active ancillary TeX
inputs were read, covering 70 sections and subsections. No active section
was omitted. The inactive `extended-background.tex` and `compact-appendix.tex`
remain unchanged.

The edit explains a repository trajectory and test contract before relying
on them, distinguishes implementing features from preserving and extending
them, and defines risk sets and the primary estimand in plain language.
The bootstrap description explains resampling, while the judging account
explains why ordinal scores and missing-outcome bounds need care.
Long qualifications are split into specific statements. Repetitive contrasts
are reduced while preserving consequential uncertainty and approval limits.
The participant-observer retains first-person narration.

The abstract's study description now explains the measurement setup before
giving its results. Agents saw the feature specifications, while the scoring
tests remained outside their workspaces. After each development step, a
separate evaluator ran the tests in an isolated container and counted passed
contracts. The paragraph then follows the runs through consolidation and
change-request results. The author's revised first abstract paragraph was
left unchanged. No study methods, outcomes or analysis changed.

There is no new source verification, equation audit, experimental analysis,
scoring, registration or protocol amendment. The owner separately authorized
maintenance of the directly related content tests and binding. Exact-wording
expectations now match the revised explanations; existing scientific guards
and data comparisons remain active.

### Validation and Source-Only Delivery

Classification: focused editorial revision with directly coupled authoring-test
and digest maintenance. No application, dependency manifest, infrastructure,
deployment, security control or repository gate semantics changed.

* The structural checker passes: 94 cited keys and 94 embedded bibliography
  entries resolve; the abstract has 1,916 source characters, below 1,920.
  The historical comparison object remains unavailable.
* Direct comparison with the intake source preserves all 40 table
  environments, seven displayed equations, three literal prompts, citation
  sequences, bibliography, labels, 61 source-register bindings and author
  comments/TODOs. Figures, chart inputs and inactive inputs are unchanged.
* The package suite passes 73 of 74 tests. The native diagram-export test
  fails because its required Playwright browser is unavailable. No figure
  changed, and no export success or full-suite pass is claimed.
* A separate external Tectonic build produces a 73-page PDF. The Supplement
  starts on page 46; the source register starts on page 70. All pages contain
  text within page bounds, and no unresolved-reference markers were found.
  Rendered pages 1, 15, 21, 36, 46, 51 and 73 were inspected in the earlier
  readability build; the follow-up build confirms the updated abstract on
  page 1. The inherited `inputenc` warning remains; no overfull or underfull
  boxes were reported.
* The existing `main.pdf` was already dirty at intake and subsequently
  changed outside this revision's external build. The owner confirmed
  source-only continuation with that PDF left uncommitted. No claim is
  made that its bytes were preserved. `human_readability_revision` binds
  the current sources and separate validation PDF; every historical
  source/PDF binding remains unchanged.

Work execution: Complete for the authorized source revision and focused
checks; browser-export validation remains unavailable. Assessment:
editorial review complete within the active source package, without
independent scientific peer review or fresh claim-by-claim verification.
Independent exact-head review, applicable hosted CI, author/employer approval
and venue acceptance remain separate requirements.

## Direct Style Revision 15 November

### Scope and Applied Changes

The owner requested a direct-prose revision of the paper. The abstract now
states the motivating case, study conditions and findings in shorter
sentences. The case account, consolidation discussion and conclusion replace
selected formulaic contrasts with direct statements. The practical section
gives readers a concrete recommendation: measure consolidation cost against
retained behaviour and success on a new requirement.

The edit preserves first-person narration for the participant-observer,
all reported results and their uncertainty, the study design, equations,
tables, figures, citations and source registers. It adds no experiment,
analysis, scoring or model call. The original `author_voice_revision`
binding remains unchanged; `style_revision` records the new source and PDF.

### Validation and Delivery

Classification: focused editorial revision.

* The Tectonic build produced a 72-page PDF. The Supplement starts on page 45,
  and the source and digest register starts on page 70.
* Rendered pages 1, 11, 35-37, 45 and 70 were inspected. Extracted PDF text
  contains the revised abstract, case heading, practical recommendation and
  conclusion.
* The manuscript structural checker passed. The package suite ran 74 tests:
  73 passed, and the native diagram-export test could not launch because its
  Playwright browser was unavailable. The `style_revision` binding records the
  final source/PDF digests and keeps the prior author-voice binding unchanged.
* The Tectonic log contains the inherited `inputenc` warning for its UTF-8
  engine. No overfull or underfull box warnings were found.
* No experiment, model call, source retrieval or publication action occurred.
  Independent exact-head review, hosted CI, author approval, employer
  clearance and venue acceptance remain separate.

Work execution: Complete for the authorized editorial revision. Assessment:
scoped editorial review complete; this does not certify the scientific
claims or constitute independent peer review.

## Narrative, Learning and TODO Reconciliation 15 November

### Authorized Scope and Scientific Boundary

The owner authorized applying the present revision and deferred VM evidence
access. The AMA Presentation Communications Strategist supplied bounded
read-only narrative suggestions. The applied arc is interrupted usable
workflow, explicit conjecture, an experiment that did not reproduce the
expected decay, and clearer questions for a separate future study.
The title, results, scoring, estimator, registration, literal prompts and
historical/adverse records remain unchanged. The article reports completed
exploratory research, not a newly frozen protocol or a completed RPI comparison.

Detailed theory mapping, the unchanged assumed cost equation/figure/table,
numerical follow-up candidates, the untested hybrid and historical resource
arithmetic moved into the existing additive Supplement. The main account
explains why acquisition, retention and adaptation answer different questions.
Attributed author reflections do not establish that longer tasks will decay,
that RPI prevents decay or that review alone explains any effect.

### Current Author TODO Disposition

The intake found eight active author-action items, plus three conditional
plotting comments. Six author-action comments and the three historical plot
comments remain after two editorial dispositions. Comment presence alone is
not the release checklist; the unresolved obligations below still apply.

| Intake item | Answer or action applied now | Remaining evidence or approval |
| --- | --- | --- |
| Submission date | Preserved the draft date and date TODO; arXiv is the author's chosen target. | Set the real date only for the authorized submission candidate; freshly check applicable arXiv policy, category, disclosure and source-bundle requirements. |
| Manager/CELA clearance | Corrected the earlier 27 October account using the supplied AICC acknowledgement: receipt 14 November 2026, starting its stated fourteen-day review period. The author expects a response by 29 November. No private submission identifier or correspondence was added. | Final-version scope and applicable clearance remain pending. Receipt, silence and an expected date are not approval. Retain the owner's reported manager approval as reported, not independently verified. |
| Historical runtime identifiers | Narrowed the TODO to missing historical case CLI/reviewer/build records. | Inspect retained VM evidence read-only when access is supplied. Current installations cannot reconstruct unlogged history; mark unavailable identifiers explicitly. |
| Acknowledgements/review | Removed unsupported generic acknowledgements. The author reports only the coauthor's review. | Do not imply additional reviewers or both authors' approval of this exact revision. Obtain final exact-version approval separately. |
| Material source/claim verification | Narrowed the TODO to consequential gaps in the existing source register. The author reports reading most cited papers. | Record exact passages supporting material claims; preserve abstract-only, partial, metadata-only and unavailable states. Reading most papers is not a recorded claim audit or independent replication. |
| Selected provenance permission | Recorded authorization for the selected existing excerpts, subject to required clearance; replaced the generic permission TODO with a scoped dated disposition. | Historical/raw records and newly released excerpts require confidentiality review. Permission does not waive clearance or authorize upload. |
| Deposit and registration correspondence | Retained the selected experiment GitHub deposit and historical v4/v6/v7 distinctions. | Bind approved released files and hashes in a final manifest; verify accessible registration/archive correspondence without retroactive registration claims. |
| Statistical chronology/dependence | Inspected public scheduling implementation and export limits; clarified asynchronous execution. | Reconcile actual timing, scheduling overlap, amendments and outcome access, then obtain a dated dependence justification. Any additional sensitivity analysis needs explicit post-collection status and authorization; no estimator was replaced. |

The three `PF` comments remain in the inactive historical plotting branch:

| Historical plot item | Current disposition |
| --- | --- |
| PF1: F/P checkpoint vectors, eligibility and missingness | The current chart explains P checkpoints, but is not a complete F/P acquisition/loss risk-set reconstruction. Do not equate plotted means with all requested vectors. |
| PF2: CR1 vectors, prerequisites, assistance and all-attempt costs | Current CR1 tables exist; two outcomes and 55 attempts' billing remain unresolved. The chart is not a complete prerequisite/assistance/cost reconciliation. |
| PF3: final coverage and attributable delivery credits | The scatter uses the fully billed subset, not a complete quality-matched cost frontier or measured long-horizon payback. |

The twelve owner-TODO occurrences in the retained original
[hypotheses](./mve-feature-consolidation-harness/hypotheses.md),
[design](./mve-feature-consolidation-harness/experiment-design.md) and
[plan](./mve-feature-consolidation-harness/mve-plan.md) are historical proposal
questions, not current approvals. They are preserved rather than completed
after observing outcomes. Earlier checklists and false-results instructions
retain their original dated scope; the current manuscript has results enabled.

### Evidence Inspected in This Revision

| Claim and manuscript locator | Inspected source and genuine locator | Evidence status and limit |
| --- | --- | --- |
| Model/arm allocation; experiment Design and estimands, Supplement Scheduling evidence | Public experiment source at `d097a10b090baefadf995ecd910eb96c324f0234`, `harness/study.py:286-323` | Full source support: model order shuffled within replicate, then arms within model. Not actual start order. |
| Asynchronous dispatch; same sections | Same pin, `harness/study.py:2141-2180` | Full source support: worker pool fills eligible work and defers routes under backoff. Scheduling groups are not synchronized execution batches. |
| Public chronology limits; Supplement Scheduling evidence | Same pin, `results/pilot-estimation/runs.csv`, `attempts.csv`, `provenance.json` | Direct export inspection: 315 runs, 63 model/replicate groups each A-E; 5,372 attempts across sixteen sources; no attempt start/finish timestamp columns. Parallelism history records ten then eight. No wall-clock independence inference. |
| Clearance timing; author TODO | Author-supplied AICC acknowledgement and correction | Supplied record inspected for receipt date; final clearance and its scope unverified. Expectation of a 29 November response is author-supplied, not a policy guarantee. |
| Surprise, task scale and full-RPI hypothesis; Discussion and Conclusion | Author answers in this revision | Participant interpretation, not experimental evidence. More complex tasks, review-component comparisons and larger spending remain unapproved follow-up candidates. |

### Remaining Work in Dependency Order

1. When VM access is supplied, inspect only approved retained records: missing
   historical identifiers, per-attempt starts/durations and controller/source
   transitions. Reconcile them against amendments and outcome-access records.
   Record missingness rather than starting sessions to recreate history.
2. Resolve the dependence justification with the actual allocation/overlap
   evidence and statistical review. Preserve the published estimator and
   label any newly authorized sensitivity analysis as post-collection.
3. Reconcile CR1 unknowns, held billing, judging-frame completeness and human
   calibration where original evidence permits. No rerun, paid call, changed
   score or unknown-to-success conversion is authorized by this editorial task.
   Close PF1-PF3 only to the extent actual inputs support their full scope.
4. Complete consequential claim/source checks from the existing register,
   retaining partial/abstract-only limits. Known examples include the cited
   Knight Capital order versus inspected SEC release and technical-debt
   productivity's inspected institutional abstract versus unavailable full
   methods. Do not silently substitute sources.
5. After applicable clearance and both authors' exact-version approval,
   reconcile the approved deposit manifest and registration archives; verify
   current arXiv rules and source-bundle compilation, set the submission date,
   and obtain any required independent scientific and exact-head review.
   No upload or submission is part of this revision.
6. Design the future experiment for a later paper only after a separate brief,
   resource approval and protocol review. Justify task scale, independent units,
   acquisition/retention/adaptation endpoints, full-RPI and component contrasts,
   missingness, uncertainty and cost-matching before collection. Existing
   30-40-cycle and factorial suggestions are candidates, not a frozen design.

### Validation and Delivery

Classification: focused editorial and non-gate authoring-tool/test changes.
No experiment execution, scoring, data, infrastructure, deployment, dependency
manifest, security control or gate semantics changed. The full application
gate is not the relevant check for this slice.

* The single rebuilt PDF has 72 pages, Supplement page 45 and the source
  register on pages 70-72. The main route reaches the Supplement three pages
  earlier than v21; moving detail does not imply reducing the total length.
* Direct baseline comparison against `1172b5a6637e8e12d51b8f9836292959aabcef44`
  preserves all 34 original table data bodies, seven displayed equations,
  three literal prompts and 61 identifier/value pairs. Empirical snapshot,
  chart sources, figures and editable diagrams are unchanged. Existing
  historical manifest entries remain intact; a new binding records v22.
* Structural checks pass: approximately 15,701 main-body words, 1,594 abstract
  source characters, 94 cited/embedded bibliography entries and 105 reusable
  BibTeX entries. Historical baseline `0d5dcb02` remains unavailable.
* The body counter now stops at the first unnumbered back-matter section or
  bibliography, not only an Acknowledgements heading. Removing unsupported
  acknowledgements exposed that coupled bug; one regression covers all three
  boundaries. Relocated-content tests now inspect the appropriate active input.
* The 73-test run passed 72 tests. Native diagram re-export failed before
  browser launch because the required Playwright executable was absent.
  The host platform was unsupported by that pinned browser installer; a
  task-local fallback download did not finish and was stopped. No diagram
  was changed, and the missing check is not reported as passed.
* Tectonic 0.17.0 compiled with the resolved official bundle endpoint; only
  the inherited `inputenc` warning remains. All pages are nonblank, text is
  in bounds and extracted text contains no unresolved `??` references.
  Selected rendered pages 1, 35, 36, 45, 51, 52 and 68 were inspected.
* Hosted CI and independent exact-head review were not performed. Employer,
  author and venue approval are separate. No VM access, experiment, paid
  judging, registration change or external submission occurred.

Work execution: Complete for the authorized editorial revision and TODO
disposition; remaining evidence work is deferred explicitly. Assessment:
assisted narrative/source review, not independent human peer review or
scientific, statistical, employer or venue certification. Browser re-export
validation remains unavailable.

## Author Voice Follow-Up 15 November

The owner asked for direct first-person singular when the paper describes his
case actions and reflections. The narrative now uses I/my for that account,
identifies the author as participant-observer in the methods, and retains
named author attribution in metadata and formal contributions. The future-study
passage now states the bounded design that was evaluated and the questions and
design work a follow-up can address. No results, study design or protocol
changed.

### Validation and Delivery

Classification: focused editorial and authoring-test update. The active source
and PDF hashes are recorded in the new `author_voice_revision` binding; the
preceding `narrative_learning_revision` entry remains unchanged.

* The PDF has 71 pages, the Supplement starts on page 45, and the source
  register occupies pages 69-71. Pages 1, 8, 34, 36, 45 and 69-71 were
  rendered and inspected.
* `python3 -B anc/check_paper.py` passes structural checks. The 74-test
  authoring run passed 73 tests; the native diagram-export test could not
  launch because the required Playwright browser was unavailable.
* Two-pass pdfLaTeX compilation succeeded. The log contains two ignored
  infinite-glue-shrinkage diagnostics at `main.tex:1988`. PDF text extraction
  confirms the revised passages and successful reference resolution.
* Independent exact-head review, hosted CI, final author approval, employer
  clearance and venue acceptance remain separate and unperformed.

Work execution: Complete for the authorized author-voice and limitation
wording revision. Assessment: scoped editorial review complete; this does not
certify the paper's scientific claims or constitute independent peer review.

## Provenance and Readability 15 November

### Scope and Applied Findings

The owner requested a readability review and authorized revision of the white
paper, specifically moving repeated SHA digests into an end table and reducing
reader backtracking without adding length. The revision uses the current
article, active Supplement inputs and retained package evidence. No external
source was newly retrieved or independently revalidated. The existing topic
branch and open PR 1790 continue the same paper workstream; no remote write
was performed.

* Full identifiers interrupted Data Availability, execution history, judging,
  attestation and prompt explanations. Table 35 (`tab:source-register`) now
  contains each of the original 61 identifiers once, with a linked R01-R61
  record, object type, purpose and historical/final scope. The 19 SHA-256
  digests remain distinct from the 42 Git commit/tree/blob IDs. No source pin
  or digest value changed.
* Result letters and checkpoints required backtracking. Tables 10-13 now have
  a local arm key; the design and result prose explain S1, final feature
  checkpoint P10, regional-access extension CR1, acquisition/retention and
  sampling intervals versus bounds for unknown outcomes. Complexity and the
  deferred intervention-demand rate have local plain-language explanations.
* Repeated comparisons and revision chronology obscured the argument. The
  introduction, conclusion, Data Availability and AI-assistance account are
  shorter; all detailed data tables, original disclosures, literal prompts,
  prior reviews and author TODOs remain in their existing records. The
  allowance comparison explicitly names Arm A as D's comparator.
* Follow-up wording implied more certainty than the task supports. The
  longer-horizon design is presented as a proposal, with an assumed economic
  model and unmeasured long-run cost slope. The hybrid/practice package remains
  untested; safety, privacy, approval and publication gates remain explicit.

The preserved final-results source and prior checks retain their original
evidence status. This editorial pass establishes source/number preservation
and local presentation checks, not new empirical support or a measured gain
in reader comprehension.

### Validation and Delivery

The focused tier applies to editorial TeX, non-gate authoring tests, bindings
and documentation. The tests follow relocated identifiers and add unique-
register/local-context checks; experimental scoring, estimator, dependencies,
security controls and required publication-gate semantics are unchanged.

* All 72 authoring tests pass. The initial full-suite run found one obsolete
  phrase assertion about D's allowance; it now checks the explicit Arm A
  wording, and the exact test and full suite pass. A dangling editorial
  transition was also corrected and rechecked before the final build.
* Baseline comparison at `c3d08d0631151ce022d073f6d10ffc1d6504b1ba`
  preserves all 61 unique identifiers, 1,454 fields across 34 existing tables,
  seven displayed equations, three literal prompt files and every author TODO.
  All historical binding entries are unchanged; prior active Supplement
  digests are retained in the new revision entry.
* The structural checker passes: 1,836 abstract source characters, 94 cited/
  embedded entries, 105 reusable bibliography entries and approximately 16,737
  introduction-through-conclusion words. Historical baseline `0d5dcb02`
  remains unavailable; these counts are not outcomes or readability scores.
* Tectonic builds one 70-page PDF: Supplement page 48, final source register
  pages 68-70. The preceding v20 Supplement began on page 51. All 30,868
  extracted words are within page bounds, no page is blank and all 61 register
  destinations resolve. There are no errors, undefined references, overfull
  or underfull boxes; the inherited `inputenc` notice remains.
* Selected pages 1, 2, 4, 28, 29, 31, 37, 38, 40, 48, 53 and 68-70 were
  inspected directly or were pixel-identical to inspected candidate renders.
  Figure files and raw chart inputs are unchanged. The installed PDF matches
  the final external build in
  `/tmp/ama-paper-readability-20261115-final-AN4no9/`.
* The `provenance_readability_revision` in
  [supplement-integration.json](./supplement-integration.json) binds the final
  PDF, sources, register and reviewed pages. Earlier candidates and revision
  records remain intact; no cleanup was authorized or performed.

Local requested revision is complete. Assessment is a scoped assisted
readability and preservation review; scientific evidence limitations,
unregistered amendments, two CR1 unknowns, 55 billing holds, the incomplete
judging/calibration frame and author decisions remain unchanged. Human,
employer/venue approval, hosted CI and independent exact-head review are not
established. No paid run, VM change, experiment, scoring, registration,
commit, push or external publication occurred.

## Final Results and Chart Interpretation 15 November

### Source and Scope

The owner supplied the final experiment report and its pilot/judging folders,
reporting that the researcher executed the completed recoveries. The source
pin is `d097a10b090baefadf995ecd910eb96c324f0234` in
`jmservera/ama-thought-mve`. The inspected online report identifies that commit;
the committed report SHA-256 is
`e4680e66ba6791c7a23bd484954767bc7d580f881db939cf4fb113d28af10f15`.
The final execution pin is `5481fd8a47aa0bad660e7c0ab68f7fcfeea4137f` and
study-state binding is
`7992b0e21cbacde39b48bb6223d5b663b7013630b265ae64a37223414ab05e4a`.
These source/metadata checks do not independently rerun or certify the study.
Researcher execution and operational separation retain the authorship and
institutional-independence limits in the manuscript.

| Claim and manuscript locator | Inspected evidence | Support and limit |
| --- | --- | --- |
| Completed frame; execution and collection sections | Committed report, summary, run and attempt exports | Artifact support: 315 completed trajectories, 5,355 measured steps, 5,372 attempts, sixteen source epochs, accepted retention panel and owner-attested unassisted coverage. Out-of-band intervention is not independently verified. |
| Final coverage and CR1 outcomes; main tables and Supplement | Committed summary, retained snapshot and contrast exports | Coverage/structural/CR1 table values match the retained snapshot. All four coverage comparisons now have estimates; two unadjudicated CR1 errors remain unknown, not zero or failed outcomes. Estimates remain exploratory. |
| Billing; resource table and ledger | Committed attempt export and report | 5,317 fully billed attempts, 62,299.75904 settled credits, 38 retry holds and 17 recovery holds. The 55 holds retain 19,200 reserved credits; the 783.16186 lower bound is not a settled total. |
| Judging and calibration; post-collection assessment | Existing committed judging outputs | The earlier 313/315 snapshot retains 630 scheduled/626 evaluable packets and 1,252 calls. Completing development did not complete those four unavailable judging packets. Calibration remains in progress and AI-assisted, not independent reliability evidence. |
| Empirical charts; Figures 9 and 10 | 3,150 committed cycle rows and source-bound JSON | All 150 cell-by-cycle means for each of the two plotted metrics reproduce within retained precision. Static range clipping and the Arms A-D denominator were corrected. No candidate code or judge was rerun. |

### Human Reading Cues

The user requested an explicit better/worse direction and additional reading
clues. Figures and captions now state:

* Higher pass rates mean more specified contracts satisfied; lower hotspot
  percentages mean fewer complex functions, not proof of correctness.
* Each trajectory line is a 21-run mean without uncertainty bands. The upper
  axis is zoomed, and expanding contract sets can lower coverage without
  showing loss of previously acquired behaviour.
* Positive contrasts favour the first named arm. Intervals including zero
  leave the direction uncertain; +10 points is the primary practical benchmark,
  not a significance threshold.
* More CR1 passes are preferable, but retention obligations depend on prior
  feature completeness. Grey outcomes remain unknown.
* Up/left in the cost panel means more coverage/less spending. Upper-left is
  preferable only at comparable delivered behaviour; coverage uses every run
  while costs use fully billed subsets. Cheap failure is not efficiency.
* The economics graphic is an assumed model. Higher net A-B favours B;
  fewer break-even cycles mean earlier payback, and larger k/delta delays it.
  The null case, invented parameters and observed step means remain distinct.

The triggered hybrid policy is explicitly a proposed follow-up, not an
evaluated combination or a measured cost advantage. An Excalidraw delegate
updated the native economics labels and matching authoring text through the
existing exporter; equations, values and other diagram files were preserved.

### Validation and Delivery

The focused tier applies: reporting, figures, non-gate export tooling, related
authoring tests and bindings changed. No experiment engine, scoring rule,
dependency, security control or publication-gate semantics changed.

* All 70 authoring tests pass. The initial full-suite run had one stale exact-
  phrase assertion; the test now checks the actual explicit exploratory-study
  declaration, and the same check and full suite pass afterward.
* The structural checker passes: 1,836-character abstract, 94 cited/embedded
  entries, 105 reusable bibliography entries and approximately 17,010 main-body
  words. Historical baseline `0d5dcb02` remains unavailable.
* Browser geometry checks confirm fourteen direction/reading cues fit without
  text overlap. All plotted cycle values lie within their axes. Native source,
  export, full-raster, frozen-prompt and current/historical bindings pass.
* Tectonic produces one 70-page PDF, Supplement page 51, with zero errors,
  unresolved references, overfull or underfull boxes. All 31,103 extracted words
  have in-page bounds and no page is blank. Final rendered pages 28, 32, 36,
  51, 69 and 70 were inspected; earlier candidate opening and conclusion pages
  were also inspected. Only the inherited `inputenc` notice remains.
* PDF SHA-256 is
  `a31b7e8968a175ac5ac8ac8816e55ca860d5b1032f2697be93cc57a86391781b`.
  The separate `chart_interpretation_revision` in
  [supplement-integration.json](./supplement-integration.json) preserves the
  pre-annotation `final_results_revision` and every earlier revision. Working
  build/inspection files remain external.

Local work is complete. Scientific assessment remains source-bound and
exploratory; author, employer and venue approval, remaining original-source
access limits, hosted CI and independent exact-head review are not established
by these checks. No new data collection, paid candidate/judge call, VM change,
registration, commit, push or external publication occurred in this update.

## Critique and Falsifiability Revision 14 November

### Applied Critique and Prediction Verdicts

The user-supplied review observed that the ten-feature S1 study neither
confirmed the initial conjecture nor could formally falsify an elastic
"can carry ... unless" phrasing, and recommended stating explicit testable
predictions with thresholds, labelling each verdict honestly, naming the
per-model split alongside the $+1.19$-point pooled B-D coverage estimate,
and designing a deeper follow-up experiment.

| Critique item | Manuscript change | Locator |
| --- | --- | --- |
| Replace elastic "can carry ... unless" phrasing with falsifiable predictions and explicit verdicts | Separated the conjecture into P1 (short-horizon decay premise), P2 (primary B-D coverage gain $\Delta_*\geq10$ percentage points), P3 (CR1 adaptability and credit payback) and a structural manipulation check, keeping pre-specified $\Delta_*=10$ distinct from post-collection evaluation structure | `main.tex` Abstract, Section 1 (`sec:intro`), Section 9 (`sec:conclusion`); `anc/experiment-protocol.tex` Table 15 (`tab:predictionverdicts`) |
| Surface per-model heterogeneity next to the pooled $+1.19$ pp B-D figure | Reported GPT 6.1 Sol $+3.15$ pp ($[0.00,+6.30]$, F9 ranking acquisition 12/21 vs 6/21) alongside Sonnet 5.5 $+0.26$ pp ($[-0.15,+0.75]$) and Gemini 4 Argon $+0.15$ pp ($[-0.15,+0.52]$), whose intervals span zero | `main.tex` Abstract, Section 1, Section 9; `anc/experiment-protocol.tex` Section 7.9 (`sec:resultscorrectness`) |
| Propose a future experiment with sufficient depth for conclusive results | Added Section 8.5 (`sec:futureexperiment`): $N=30$--$40$ sequential cycles on a $3\text{k}$--$10\text{k}$ NLOC brownfield service repository spanning $N_{\mathrm{BE}}=\lceil 1+2k/\delta\rceil$, $K\geq4$ branch-isolated Latin-square change requests at $P_{10}..P_{40}$, a $2\times2$ factorial crossing refactoring and invariant review plus test mutability, and preregistered block-level falsification rules | `main.tex` Section 8.5 (`sec:futureexperiment`) |

### Unblocking the Two Quarantined Trajectories

Read-only inspection of `/home/jmservera/source/ama-thought-mve` (`harness/study.py`,
`harness/prepare_estimation_recovery.py`, `harness/pilot_analysis.py`) and
allowlisted metadata in `ama-thought-mve-fallback-recovery/.study/pilot-estimation/state.json`
identifies why `primary_estimates_available` is `false` and what is required
to finish the two incomplete trajectories before the active study deadline
(`1795318710.65`, `2026-11-22T03:38:30Z`):

1. **Exact state of the two quarantined cells:**
   * `pilot-estimation-gemini-4-argon-E-15` (`completed_steps = 10` of 21,
     checkpoint `f06-feature` at Git HEAD `763a9a36eb7191d023601c35fcfa049e1c1894b5`)
     stopped on `pilot-estimation-gemini-4-argon-E-15-f06-feature-1`
     (`status = infra_failed`, `failure_kind = transport`, `failure_stage = session_send`,
     `accounting = unknown`, 300 reserved credits in `quarantine_hold`,
     `supervision.action = quarantine_cell`). Eleven steps remain
     (`f06-feature` through `f10-repair` plus `cr1-change`).
   * `pilot-estimation-gpt-6.1-sol-C-20` (`completed_steps = 18` of 21,
     checkpoint `f10-feature` at Git HEAD `81e23369f6125314bab89ac52361b44da8339f60`)
     stopped on `pilot-estimation-gpt-6.1-sol-C-20-f10-feature-1`
     (`status = recovery_interrupted`, `credits_status = recovery_hold`,
     300 reserved credits) under incident `FALLBACK_RECOVERY_STATE_SHA256`
     (`kind = fallback_metadata_quarantine`). Three steps remain
     (`f10-feature`, `f10-review`, `cr1-change`).
2. **Code gates preventing in-place replay:**
   * `StudyController.go()` (`harness/study.py` line 2096) skips cells with
     `status == "quarantined"`, and `new_attempt()` (line 1819) raises
     `StudyError("Quarantined cell cannot replay an unresolved request")`.
   * `validate_supervisor_state()` (`harness/study.py` lines 572--575)
     requires `cell["status"] == "quarantined"` whenever a ledger entry has
     `status == "quarantine_hold"`, and `validate_recovery_state()`
     (lines 1084--1096) requires `cell["status"] == "quarantined"` and
     `cell["attempts"][-1] in quarantine_only` for `fallback_metadata_quarantine`.
3. **Controlled recovery path to complete the 315/315 frame:**
   * Never mutate `ama-thought-mve-fallback-recovery` in place; preserve
     stopped state `fb39a46fc36f33f62f3286fd517b63bb09787e9c7bcd7d276c4a362f256f2de1`
     as the immutable 13--14 November baseline.
   * Add a fifteenth disclosed recovery transition in `harness/study.py` and
     `harness/prepare_estimation_recovery.py` keyed to `fb39a46f...` that
     copies `.study/pilot-estimation` into a new working directory, keeps
     the two 300-credit unknown-charge holds permanently in `recovery_hold`
     (so unknown usage is never zero-imputed), resets both cells from
     `"quarantined"` to `"partial"` at their verified checkpoint HEADs
     (`763a9a36...` and `81e23369...`), and authorises fresh retry
     reservations for the remaining 14 steps (11 in `gemini-4-argon-E-15`
     and 3 in `gpt-6.1-sol-C-20`).
   * Run `study.py` to finish only those 14 steps, update
     `intervention-coverage/v1` to attest all 315 completed trajectories,
     and re-export `results/pilot-estimation/`. That flips
     `primary_unassisted_frame_complete` and `primary_estimates_available`
     to `true`, completing all five-arm H1 coverage contrasts (`B-D`,
     `B-A`, `B-C`, `E-B`). Note that two already-completed trajectories
     (`pilot-estimation-gpt-6.1-sol-B-08` and `C-14`) have `cr_success = null`
     because their CR1 hidden-test runs ended with non-binary collection
     outcomes (`agent_returned`); those are genuine task outcomes and must
     not be rerun, so GPT CR1 contrasts will rightly remain identification
     bounds even after all 315 trajectories complete.
   * Replay the four newly completed endpoint packets ($P_{10}$ and CR1 for
     `gemini-4-argon-E-15` and `gpt-6.1-sol-C-20`) through `judging/execute.py`
     and run 8 `gpt-6-luna` calls ($4\text{ packets}\times2\text{ repeats}$)
     to complete all 630/630 packets while preserving the existing 1,252
     Assessment v3 ratings.

### Validation

* All 67 authoring tests pass, including the new falsifiability and
  future-design regression test.
* All 1,378 existing numerical and protocol table fields match the prior
  v18/v17 sources; the new 4-row `tab:predictionverdicts` table is additive.
* The structural checker passes: 1,811-character abstract ($<1,920$), 94
  cited/embedded entries, 105 BibTeX entries, and approximately 15,979
  main-body words.
* Tectonic compiles a single 66-page PDF (Supplement starting on page 47)
  with zero errors, zero unresolved references, zero overfull boxes and no
  blank pages; the inherited `inputenc` warning remains. Rendered pages
  1, 2, 3, 32, 35, 36, 47, 65 and 66 were visually inspected. Current PDF
  SHA-256 is `6b00bc227ccd56b89c352d1cea57871a85fd55aa6bf000eb75385b0a64a45977`,
  bound under `falsifiability_revision` in
  [supplement-integration.json](./supplement-integration.json).

## Finalization Follow-up 14 November

### Scope and Six Dispositions

The owner requested the exact Data Science and Engineering Coach, RPI original-
source research, a partner/customer/coworker-name review, approval-status handling,
historical version-retrieval advice and the experiment GitHub repository as the
deposit. The owner confirmed local write permission and then authorized read-only
SSH metadata access in the named last-execution and v3 judging working copies.
The staged v17 paper remains intact; new changes continue on
`docs/whitepaper-study-results`.

| Item | Completed work | Remaining author action or limit |
| --- | --- | --- |
| Statistical TODO | Exact Coach assessment and parent verification identify independent model/arm whole-trajectory resampling, 63 five-arm groups and public run/source joins. The Supplement now distinguishes public linkage from private timing and valid dependence assumptions. | Approve a dated dependence justification and actual amendment/outcome-access chronology; any sensitivity analysis is separately post-collection, not a silent replacement. |
| Original sources | Wider inventory, Deeper original-passage checks and Contrarian scope/consistency checks completed. The source register below identifies actual originals and verification coverage. | Author-confirm the assisted checks and keep remaining abstract-only/full-text limitations explicit. |
| Participant names | Active source/PDF participant contexts and six native SVG text exports reviewed; no additional identified case partner, customer or coworker was found beyond the two authors. No private contacts, cohort paths or VM details were added to the paper. | Credited publication authors/public speakers remain named. Future extracts, historical/private files and complete Git history require their own publication-scope review. |
| Manager/CELA status | Owner reports manager approval and a draft sent to CELA on 27 October with no objection. The TODO now records those facts rather than generic absence of all approval. | No approval record, final-version scope or no-response policy was inspected. The earlier draft predates the empirical additions; confirm that the applicable process covers the current draft. |
| Historical metadata | Read-only VM retrieval found all attempt starts/durations/IDs/source commits and matching v3 source/config bindings. No restart or new session was needed. | Controller intervals do not prove provider-service independence. Unlogged historical case/reviewer/backend IDs remain unavailable until retained records expose them. |
| Deposit | Experiment GitHub repository selected. Published v4/v6/v7 protocol archives and checksum assets confirmed by release metadata. | Complete an immutable-version release manifest, verify exact registered-archive correspondence/file hashes and approve the sanitized publication scope. No remote publication occurred. |

The exact Coach's first invocation stopped on a parent-imposed read-only-file
restriction. The retry permitted only its mandatory session-state write and
completed the assessment. All four scientific skills were loaded; SymPy execution
was unavailable, and the reported arithmetic used standard-library checks rather
than a new symbolic certification. This is assisted assessment, not independent
human scientific review.

### Original Source Register

Coverage is targeted to retained claims, not all 94 cited works or raw-data
replication. Original manuscript versions remain distinguished from publication
metadata. No citation was silently replaced by a different source.

| Source | Inspected original and locator | Support and limit |
| --- | --- | --- |
| SWE-Maintain | [arXiv v1](https://arxiv.org/html/2610.14768v1), Sections 4.1-4.2, Tables 2-3; Table 3 `S4.T3` | Full-text support for retained counts/contrasts, including selected 619-event TR `-1.1 [-3.8,+1.6]` and ER `+2.7 [-0.5,+6.1]`; selected cohorts remain outcome-dependent. |
| AGENTS.md evaluation | [arXiv v3](https://arxiv.org/html/2602.11988v3), Section 4.2, Tables 2-3, Appendix B | Full-text support for reported cost/success contrasts and table `p=0.038`; percentage-formatted prose and relative introduction wording are not imported as different absolute effects. |
| Context-file evolution | [arXiv v4](https://arxiv.org/html/2510.21413v4), Section 4.3/Table 2 | Full-text support for 169 commits and 242 overlapping category assignments; counts do not establish net growth, intent or performance. |
| Agent READMEs | [arXiv v2](https://arxiv.org/html/2511.12884v2), Sections 4.2.2-4.2.3 | Full-text support for 100 post-adoption commits, 139 assignments and 78/32/19/10 displayed labels; not a causal context-file effect. |
| Agentic PR decisions | [arXiv v1](https://arxiv.org/html/2605.22534v1), Sections 3-6/Tables 1-3 | Full-text support for 9,799 reviewed/717 manual PRs; 35.7% uses 353 rejections, 15.4% uses 364 merges. |
| AIDev | [arXiv v1](https://arxiv.org/html/2602.09185v1), Section 1/Table 1 | Full-text support for 932,791 PRs/five agents/116,211 repositories; dataset cutoff 1 August 2025, not accepted user outcomes. |
| Multi-turn conversation | [arXiv v1](https://arxiv.org/html/2505.06120v1), Abstract, Section 6.1/Table 1, Figure 1 and Section 9 | Retained 39% relative drop supported by abstract/results; v1 Figure 1 says 35%. The inconsistency is retained explicitly, not silently reconciled or generalized to coding repositories. |
| Code Red | [arXiv v1](https://arxiv.org/html/2203.04374v1), Sections 4.2, 5.2/Table 3 and 5.4 | Full-text support for 39 proprietary codebases and reported 124% longer issue Time-in-Development; vendor association, proxy and observational limits confirmed. |
| Knight Capital | [SEC release 2013-222](https://www.sec.gov/newsroom/press-releases/2013-222), technological missteps paragraph | Primary-page corroboration for orders, loss and 2005/2012 code/deployment facts. Original order PDF still unavailable; release is not silently substituted for the cited order. |
| Expert judgment | [Anthropic primary page](https://www.anthropic.com/research/agents-judgment-calls), Study design, Results and Limitations | Primary-page support for 61 recruited/50 agent users/86% match across four decisions; strengthened preferences, one task/model and subgroup differences retained. |
| Building to the Test | [arXiv v1](https://arxiv.org/html/2606.28430v1), Sections 2-4/Table 1 | Full-text support for seven of twelve assigned oracle-in-the-loop runs with dead/absent library dispositions; task-specific, not general prevalence. |
| CLI adoption | [arXiv v1](https://arxiv.org/html/2607.01418v1), Sections 5.1 and 6 | Full-text support for modeled approximately 24% merged-PR lift; self-selection, time-varying confounds and proxy scope retained. Original link added to both bibliography forms. |
| Technical-debt productivity | [Chalmers institutional record](https://research.chalmers.se/en/publication/46d5f3e9-bfac-47f8-bd9d-d1cced552753), Abstract; DOI `10.1145/3194164.3194178` | Abstract supports 43 surveyed developers/16 follow-up practitioners/23% self-reported wasted time. ACM PDF returns 403 and legacy Oslo link redirects to NVA; full-method verification remains unavailable. |
| Echoes of AI | DOI [publisher page](https://link.springer.com/article/10.1007/s10664-026-10889-1), secondary abstract metadata | Abstract/metadata support for observational phase 1 and randomized phase 2 with no significant downstream differences. Publisher article/PDF redirects to identity infrastructure; exact late-2024 qualifier remains unverified in this pass. |
| SlopCodeBench | [arXiv v2 record](https://arxiv.org/abs/2603.24755v2) | Identity/abstract verified; no numerical SlopCodeBench effect is retained in the current manuscript. Conference status not established. |
| METR | [arXiv v2 record](https://arxiv.org/abs/2507.09089v2) | Original identity located, metadata-only verification; no numerical METR effect is retained. No new effect size or citation was imported from this lookup. |

### Retained Metadata and Access Boundaries

The author-named execution working copy retains the study state with SHA-256
`fb39a46fc36f33f62f3286fd517b63bb09787e9c7bcd7d276c4a362f256f2de1`.
All 5,357 attempts have numeric starts and controller durations, IDs and source
commits. The state has 315 trajectory records and selects 21 replicates per model/arm at
source `a9d76bb6dbb118c43315fb2a13b7bcdb732d946d`. No separate finished/ended or
boot/launch IDs were present in the inspected attempt objects. This is metadata
coverage, not independently measured model-service overlap.

The v3 instrument freeze uses that same state hash, judging source
`c10e6d6f62785a5028406a9963acdd499f6bd6b6` and config digest
`efb0516ec2f2b28ff3cb7880baf42398e16867e65830abe5eb82babd9958dfec`, frozen
`2026-11-13T16:00:17.959379+00:00`. The judge config declares `gpt-6-luna`,
two repeats and `sdk1.0.28-cli1.0.105-judge3`; human-calibration completion is
still false. File-byte digests are separately retained in the delivery binding:
config `5da1116ec0b34750f3094ffd79cce4b4fe61a8814ca555f053f0b37e1e33ce37`,
freeze `514fa31dbe1c6c182cc733675ead8cddc85c5d90fa8a33c53329688f181932ab`.

Only allowlisted metadata was read. No credentials, prompts, raw packets,
private specimen mappings or private datasets were inspected or printed. The
first broad metadata command completed after a timeout; a quoting-failed aggregate
was stopped and repaired with a stdin-fed query. Neither failure was recorded
as missing historical evidence. No VM or experiment state was modified.

### Validation and Remaining Gates

The focused tier applies: source reporting, related authoring tests and metadata
bindings changed; experimental observations, estimators, dependencies, security
controls and publication-gate semantics did not.

* All 66 authoring tests pass, including three new finalization regressions.
* All 1,378 existing table fields are unchanged against the staged v17 sources.
* The structural checker passes: 94 cited/embedded entries, 105 reusable entries,
  1,904-character abstract and approximately 14,582 main-body words. Historical
  baseline `0d5dcb02` remains unavailable.
* The single 64-page PDF retains Supplement page 45. All 28,323 extracted words
  have in-page bounds and no pages are blank. Rendered pages 24, 36, 37, 42,
  45, 53, 54, 61, 62, 63 and 64 were inspected, including the preserved
  fourteen-epoch table and both B/C prompt displays.
* Tectonic reports no errors, unresolved references or overfull/underfull boxes;
  the inherited `inputenc` notice remains. Current PDF SHA-256 is
  `3d8a48e26f0f889edb691acdd1904f6283c2853109b3b15fb4adb23055809100`.
  The new `finalization_revision` in
  [supplement-integration.json](./supplement-integration.json) preserves v17
  and earlier bindings. Build/review files remain external.

Local research, metadata retrieval, scoped name review and supported source
changes are complete. Statistical dependence/adoption and amendment decisions,
remaining original-access limits, final author/CELA/venue clearance and final
deposit-manifest approval remain unresolved. Hosted CI and independent exact-head
review were not run. No new estimator, experiment, paid candidate/judge session,
registration, VM restart or mutation, commit, push or external publication is claimed.

## Attested Report Refresh 14 November

### Scope and Source Pins

The owner requested updating the paper from the changed local
`/home/jmservera/source/ama-thought-mve/results/WHITEPAPER_REPORT.md` and its
online GitHub `main` file. Work continues on `docs/whitepaper-study-results`;
the staged v16 candidate was preserved. The experiment repository remained
read-only, and no new candidate or judge calls, private-data inspection,
protocol amendment, registration, commit, push or publication occurred.

The inspected experiment head is `bd75c1c2104d001d62f9fb2bb4feab438b86f763`.
The report's latest file-changing commit is
`fa34bb91a74e47d5e2cb12430c01a873540e1ef2`; its local and online Git blob is
`f416316985c8dca20ad8955fe3c596db995c6276`, and its SHA-256 is
`ffde7266c3379446b5cdcc8fa695ee387c99a8a6c31fbd227b62291fd33c200c`.
The report frontmatter still dates itself 13 November; this refresh is
identified by the inspected commits and 14 November retrieval, not by
silently changing the source date. The new
`results/pilot-estimation-judging/extracted-contrasts.json` has Git blob
`f1aef11e7094ca284c25594459aecb180212c9cb` and schema
`extracted-complete-pair-and-judging-contrasts/v1`.

### Evidence and Applied Interpretation

| Claim and manuscript locator | Inspected source | Evidence state and limit |
| --- | --- | --- |
| Current report identity; Data availability | Local Git identities and report SHA-256; online GitHub file/API | Metadata-only identity check; matching blobs do not independently validate the study. |
| Owner-attested unassisted coverage for 313 completed trajectories; collection ledger and Supplement execution record | `results/pilot-estimation/provenance.json`, `runs.csv`, updated report | Full-text/artifact support for the operator account: `owner-attested`, 313 covered, zero assisted, timestamp `2026-11-14T02:48:20.351742+00:00`. Recorded manifest SHA-256 `66b098851800522d9d5117177aac34525cb1e9a17c0c4bd7d924d512c1ea6b06` and study-state SHA-256 `fb39a46fc36f33f62f3286fd517b63bb09787e9c7bcd7d276c4a362f256f2de1` are supplied provenance, not an independent inspection of the private manifest or out-of-band activity. |
| Whole-study primary remains unavailable, while complete B-D/B-A comparisons have intervals; coverage results and Supplement contrasts | Updated report, companion extraction, retained `runs.csv` and `harness/analyze.py` | Full-text/artifact support. Both pooled coverage points and 10,000-draw, seed-2027 bootstrap intervals were reconstructed to reported precision. Complete pair means complete compared arms, not paired resampling or retrospective preregistration. |
| Model-specific CR1 uncertainty and pooled missing-outcome bounds; Supplement CR1 tables | Companion extraction, retained Boolean outcomes and `success_difference` helper | Seven complete-cell points and conservative binomial intervals reproduced. Unknown outcomes remain bounds, not zero or Boolean failures. Per-comparison coverage is distinct from family-wide coverage. |
| Judge point contrasts, allocation bounds and abstention counts; main judge table and Supplement partial-frame tables | Companion extraction and retained `results/pilot-estimation-judging/summary.json` | 128 comparisons checked. Judge intervals are transcribed from the pinned companion, not independently regenerated or rescored. Observed-scenario means change the estimand; bounds over wholly missing trajectories do not identify unrated dimensions within observed trajectories. |

One rounded-summary precision limit remains: the companion's degenerate
CR1 B-D recovery bound is `-0.0113`, whereas reconstruction from the
published rounded trajectory means yields approximately `-0.0112434`.
Its two endpoints account for the only differences exceeding half a unit
in the fourth decimal (maximum about `0.0000566` score points). The source
precision is retained, not treated as exact raw-rating reconstruction;
this does not change the reported interpretation. That degenerate bound
is not substituted for the observed-scenario bootstrap interval.

The report's claims that NA counts resolve all ambiguity or that positive
finite-allocation bounds prove a general effect are not adopted. The
manuscript explains the conditional quantity instead. Prior corrections
to structural-target compliance and D's time/credit allowance remain.
Historical reviews, hashes, calibration limitations, unregistered amendments,
the fourteen execution epochs and the unchanged economic sensitivity
model are preserved.

### Validation and Delivery

The focused tier applies: this changes scientific reporting, related
authoring checks and documentation, not experimental observations,
oracles, dependencies, security controls or publication-gate semantics.

* All 63 paper authoring tests pass, including three new report-refresh
  regressions. Source/PDF, prompt and native figure bindings pass.
* Exact transcription checks match 241 new numerical, missing-value and
  abstention fields to the pinned companion. All 886 prior v16 fields in
  twelve results tables remain unchanged; new pooled CR1 bounds are additive.
* The structural checker passes with 94 cited/embedded entries, 105 reusable
  BibTeX entries, a 1,904-character abstract and approximately 14,520 main-body
  words. Historical baseline `0d5dcb02` remains unavailable.
* Tectonic produces one 64-page PDF, Supplement page 45. The actual log has
  no errors, unresolved references or overfull/underfull boxes; the inherited
  `inputenc` compatibility notice remains. All 64 pages are nonblank and
  all 27,844 extracted words have in-page bounds. Rendered pages 1, 30, 34,
  45, 55, 56, 58, 59 and 63 were inspected for readable, intact content.
* The new `attested_report_revision` in
  [supplement-integration.json](./supplement-integration.json) binds the
  current sources and PDF, preserving v16 and earlier records. PDF SHA-256
  is `6928c5920f5b4607d92f750c204c49cd422fecbe70953f108c16d1e9d2f99b44`.
  Build logs and review images remain outside the repository in
  `/tmp/ama-paper-report-refresh-20261114-4KyGId/`.

Work execution is complete for this local refresh. Evidence assessment is
source-bound and exploratory, not independent human scientific review.
The automated whole-study primary remains unavailable because of two
partial trajectories; billing, scheduling dependence and scenario
abstention remain limits. Hosted CI and independent exact-head review
were not run, and author/employer/publication approval is not claimed.

## Readability and Interpretation 14 November

### Scope and Disposition

The owner authorised applying the preceding coherence/readability review
on the existing `docs/whitepaper-study-results` branch. The results-intake
candidate was already staged; that staging was left intact. The outputs
are the article, its existing Supplement, the single PDF, directly related
authoring checks and package/knowledge-base pointers. No experiment source,
dataset, judge run, budget or registration was changed.

| Review concern | Applied revision |
| --- | --- |
| Conclusions buried in numerical repetition | Abstract and conclusion state stable retention, selective benefits, additional costs and task-specific scope before supporting detail. |
| Structural-target claims contradict the table | Gemini's low baseline metrics are distinguished from meeting every target; Sonnet B's nonzero lint remains visible. Session stopping reasons and review follow-through are not inferred from cell means. |
| Proposed and completed judging mixed together | Active methods describe the performed assessment; the 9 November proposal is explicitly historical, with its source pin retained. |
| Retention, completeness and CR1 appear interchangeable | The results explain never-acquired ranking, treatment-dependent CR1 retention obligations and the workflow/hidden-test coverage difference. Missing-outcome bounds are distinguished from confidence intervals. |
| Wide tables require tiny type | Coverage/CR1 and structure/resources are split into larger-type tables. Additional distributions, size measures, ratings, calibration and the execution ledger remain in the Supplement. |
| Provenance overwhelms interpretation | Runtime rosters, hold categories, exact precision and recovery/source details move out of the findings narrative while preserving source records and the original dataset frame. |
| Hypothetical economics precede measured spending | The cost discussion begins with settled observations and their incomplete-billing limits; the original equation and all sensitivity cells are unchanged. D's allowance is correctly described as 50% more time and twice the credits. |

### Evidence and Validation

This is an editorial revision of the previously supplied results, not a
fresh execution or independent scientific assessment. The source remains
the 13 November handoff pinned in the prior section. A direct comparison
against the staged v15 sources passed 618 field/denominator/source-ledger
checks, including exact-fraction checks of CR1 identification bounds.
All fifteen model-arm cells, reported rating means, calibration values
and fourteen execution sources are retained across the split tables.

The validation tier is focused: presentation, interpretation and existing
authoring-test expectations changed; application behaviour, experimental
oracles, security controls, dependency manifests and publication-gate
semantics did not. The root virtual environment was initially absent;
`uv venv .venv --python python3` restored the local standard-library runner
without changing dependency manifests.

* All 60 package authoring tests pass, including numerical planning,
  prompt/figure bindings, completed-method wording, table allocation and
  explicit structural-target shortfalls.
* The structural checker passes with 94 cited/embedded entries, 105 reusable
  entries and a 1,826-character abstract. Approximate main-body length is
  14,251 words, versus the v15 record's 16,349. The checker's unrelated
  historical baseline `0d5dcb02` remains unavailable.
* Tectonic produces one 60-page PDF, Supplement page 44, with no errors,
  unresolved references or overfull/underfull boxes. The inherited
  `inputenc` compatibility notice remains. All-page extracted text bounds
  and nonblank-page checks pass. Selected rendered pages were inspected;
  final table-flow corrections and the intact B/C prompt page were rechecked.
* The original v15 delivery binding is preserved in
  [supplement-integration.json](./supplement-integration.json), alongside
  the new `readability_revision`. Final PDF SHA-256 is
  `5f2bf7f61a76adcd8a0384dc768c13990cbfdcdc9b2c9c7f8c13c41504b2e9df`.
  Compiler logs and rendered working files remain in external build directories.

Work execution is complete for this local editorial scope. Formal primary
estimates remain unavailable, assistance coverage and billing remain
incomplete, and calibration remains an author/AI-triaged spot-check.
Hosted CI and independent exact-head review were not run. No commit, push,
external publication or scientific/employer approval is claimed.

## Study Results and Post-Collection Judging 13 November

### Scope, Source Pins and Mandatory Guardrails

The owner requested adding the completed study results from
`/home/jmservera/source/ama-thought-mve/results/WHITEPAPER_REPORT.md` and
`https://github.com/jmservera/ama-thought-mve/blob/main/results/WHITEPAPER_REPORT.md`
to the whitepaper. In `jmservera/ama-thought-mve`, the squash-merged `main`
commit is `7943e40347862e76e3bc04490040ad5904487c86` and the local branch head
is `8591630c556f9f87c952f5d44ca7ce58b2bf1a83`; both resolve to the identical
Git tree `cb542312d8bde5d26bc716f2c8f7a5e8eaef7037`. The report
`results/WHITEPAPER_REPORT.md` has Git blob
`3e44ae10547b6376864089e605e946f74a378d56` and SHA-256
`2180679ce9fe18d77e3107ed5cdc01edd32749a4a15114bf23f647c516d83af4`.

Every table and summary statistic in `WHITEPAPER_REPORT.md` was cross-checked
against the committed artifacts in `results/pilot-estimation/` (`report.md`,
`runs.csv`, `series.csv`, `attempts.csv`, `intervals.csv`, `provenance.json`,
`hypotheses.tex`, `trajectories.tex`) and `results/pilot-estimation-judging/`
(`README.md`, `summary.json`, `report.csv`,
`human-calibration/human-vs-ai-comparison.json`,
`intervention-log-audit-summary.json`) using exact rational arithmetic and
the four scientific methodology skills (`sympy`, `statistical-analysis`,
`scientific-critical-thinking`, `experimental-design`).

| Claim / manuscript locator | Inspected source locator | Evidence state and limit |
| --- | --- | --- |
| 313/315 completed trajectories, 5,341/5,355 measured steps across 5,357 attempts and 14 source commits ending at `a9d76bb6`; Section 7.8 and Table 18 | `results/WHITEPAPER_REPORT.md`; `results/pilot-estimation/runs.csv`, `attempts.csv`, `provenance.json` | Full-text and artifact support; 14 implementation epochs and recovery scheduling remain confounded with time, arm and model |
| Two transport-quarantined runs (`gemini-4-argon-E-15` at 10/21 steps, `gpt-6.1-sol-C-20` at 18/21) and withheld primary intervals (`primary_estimates_available = false`); Section 7.8 | `results/pilot-estimation/report.md`, `runs.csv`, `provenance.json` | Full-text support; no external `intervention-coverage/v1` operator attestation supplied, so formal bootstrap CIs remain `unavailable` |
| 5,303 complete-billing attempts (`62,052.6069` settled credits) and 54 incomplete-billing holds (`18,900.0` reserved, `783.16186` partial lower bound); Section 7.8 | `results/WHITEPAPER_REPORT.md`; `results/pilot-estimation/attempts.csv` | Full-text and ledger support; missing charges are never zero and AI credits are not converted to currency |
| P10 coverage, open regressions (1 across 313 endpoints), loss cycles, pooled within-cell SD (3.1119 pts, df 298) and CR1 identification bounds; Section 7.9 and Table 9 | `results/WHITEPAPER_REPORT.md`; `results/pilot-estimation/runs.csv`, `series.csv`, `intervals.csv` | Full-text and exact-rational verification; 87 records (98 test outcomes) reclassified by `analysis-adjudications/v1`, with two `gpt-6.1-sol` CR1 runs remaining unadjudicated `null` |
| Three model-specific mechanisms (Sonnet 5.5 F10 edge case; GPT 6.1 Sol F8 test-immutability self-lock; Gemini 4 Argon F8 view-blocklist trap where Arm C 16/21 beat Arm B 8/21); Section 7.9 and Discussion | `results/WHITEPAPER_REPORT.md`; `results/pilot-estimation/runs.csv`, `series.csv`; `intervention-log-audit-summary.json` | Full-text support for observed outcomes and journal counts; mechanism explanations remain exploratory within S1 |
| P10 structural metrics (0.00% functions > 10 CCN in all 63 Arm B runs; 92%-100% lint reduction on Sonnet 5.5 and GPT 6.1 Sol), NLOC, Markdown words, settled delivery/CR1 credits and minutes, and per-cycle consolidation spend `k` (5.82, 12.59, 12.04 credits); Section 7.10, Table 10 and Section 8.1 | `results/WHITEPAPER_REPORT.md`; `results/pilot-estimation/series.csv`, `runs.csv`, `attempts.csv` | Full-text and exact cell verification; Arm B roughly doubled delivery credits (1.84x-2.25x vs A) without lowering 10-feature or CR1 spend |
| 12-workflow replay across 3,457 commits (630 packets, 626 evaluable, 0 witnessed losses) and blinded `gpt-6-luna` Assessment v3 (`1,252/1,252` calls, `418.635894` settled credits after v1/v2 halts); Section 7.11, Tables 11-12 and Supplement Section A.9 | `results/WHITEPAPER_REPORT.md`; `results/pilot-estimation-judging/README.md`, `summary.json`, `report.csv` | Full-text and JSON verification; post-collection exploratory instrument, `gpt-6-luna` shares a provider family with `gpt-6.1-sol`, and workflow scenarios did not exercise CR1 view-mutation surfaces |
| Human calibration spot-check `S01..S08` (90 rows, 79 scorable, 16 contexts, 94.3%-98.7% raw exact agreement, 0 diffs >= 2) and 5,357-journal SDK audit (0 interactive RPCs, 99.83% `isolated_exec`, 36 permission-halt sessions); Section 7.11 and Table 13 | `results/WHITEPAPER_REPORT.md`; `human-calibration/human-vs-ai-comparison.json`; `intervention-log-audit-summary.json` | Full-text support; reviewer `jmservera` recorded `review_status = in_progress` under `human-calibration-guidance/v3` with disclosed AI-assisted failure/mismatch triage |

### Validation and Delivery Binding

* `python3 -B -m unittest discover -s anc -p 'test_*.py' -v`: **58 tests PASS**,
  including the new study-results and guardrail regression checks.
* `python3 -B anc/check_paper.py`: **PASS**, 94 cited/embedded entries,
  105 reusable BibTeX entries, 1,871-character abstract (limit < 1,920) and
  approximately 16,349 main-body words.
* `tectonic main.tex --keep-logs --keep-intermediates --untrusted`: compiles
  the single **56-page** PDF (`main.pdf`, SHA-256
  `ab687b49b89a696ba83f00a668d018fec32ffd5d7d132e2d5c5aaa076ca9e354`), with
  empirical results in Sections 7.8-7.11 (pages 26-30), the 14-epoch table in
  Data availability (page 37) and the additive Supplement starting on page 46.
  The TeX log has zero errors, zero unresolved references and zero overfull or
  underfull boxes; only the inherited `inputenc` compatibility warning remains.
  The active source/PDF bindings are recorded under `study_results_revision` in
  [supplement-integration.json](./supplement-integration.json), preserving all
  earlier revision records.

## Supplementary Blind Judging 9 November

### Scope, Assistance and Source

The owner requested checking the blind post-run judging enhancement, adding
it to the paper and obtaining a Data Science and Engineering Coach analysis.
The clean current main `ad679b96` supplied the independent topic branch
`docs/blind-post-run-judging`. Outputs are the existing article, additive
Supplement, single PDF, source/evidence record, related index/log and focused
authoring regressions. No experiment code, private data, running study,
registration, visibility or paid judging action is included.

The supplied branch resolved to
[`b7973e200a6edbb1d19355badae3b7e03a066b09`](https://github.com/jmservera/ama-thought-mve/tree/b7973e200a6edbb1d19355badae3b7e03a066b09).
The [judging README](https://github.com/jmservera/ama-thought-mve/blob/b7973e200a6edbb1d19355badae3b7e03a066b09/judging/README.md)
was inspected in full; its Git blob is
`6cc0c236e4ca093198d38909dceb80f850196faa`.
This is a separate enhancement source, not evidence of a collection-source
change from `e71037d9` or of completed judging.

The user supplied the installed Data Science and Engineering Coach definition.
The launchable agent list lacked that exact agent; a separate general-purpose
context was instructed to use the supplied definition and its experiment/
evaluation guidance for a read-only assessment, without impersonating the
named specialist or changing customer/Coach state. Scientific-critical-
thinking, experimental-design, statistical-analysis and SymPy informed the
scoped measurement/design assessment. The existing `kassis2026skills`
reference is retained: current arXiv metadata was checked on 9 November
(same five authors/year; latest version v2, no published DOI shown).
The citation records assistance, not evidence for the study outcomes.

### Claims and Evidence States

| Claim / manuscript locator | Inspected source locator | Evidence state and limit |
| --- | --- | --- |
| Separate supplementary exploratory assessment; main post-run subsection | Judging README, Purpose and status; Paper-ready methods text | Full-text support for the proposal; no completed assessment or preregistration verified |
| Fixed panel, eligible P checkpoints and post-CR1; Supplement Table 16 | Judging README, Workflow panel; Snapshots and temporal interpretation | Full-text specification support; no candidate execution or private checkpoint history inspected |
| Witnessed risk-set loss, undefined empty/missing density; Supplement Equation 7 | Judging README, What is measured; Snapshots and temporal interpretation | Full-text support for the described measure, distinct from hidden-contract H2; algebra/boundary checks are not outcome analysis |
| Four ordinal dimensions, abstention and evidence citations | Judging README, What is measured; Generic command adapter contract | Full-text rubric/contract support; judge accuracy, calibration and real-user usability remain unverified |
| Anonymised packets and residual blinding limitations | Judging README, Blinding and evidence controls; Validation and human calibration | Full-text design support; no proof that actual packets or reviewers were blinded |
| Full allocated-frame, equal-model contrasts and nested observations | Judging README, Report and handoff | Full-text reporting-contract support; no intervals, formal verdicts or scheduling-block resolution supplied |
| Separate costs, operator permission and hash-bound resume | Judging README, Freeze and prepare; Run the blinded judge | Full-text operator-contract support; no calls, billing or hard provider cap verified |

The text uses prospective methods rather than copying the README's
illustrative performed-methods paragraph. Final fulfilment, acquisition,
endpoint loss and API-task ratings stay distinct. Treatment-dependent
acquisition makes loss density conditional on the witnessed set: it cannot
alone rank arms. Whole trajectories remain the experimental units; judges,
repetitions, scenarios and snapshots are repeated measurements.
Implementation epochs and scheduling/service dependence retain their
existing unresolved scope rather than being silently corrected.

### Coach-Guided Source Assessment

The separate context inspected the pinned judging implementation, example
configuration, test sources and relevant public isolation/transport contracts.
It verified the supplied README Git-blob binding. This was static source
review: no judging tests, reference/candidate execution, models, real
packets, calibration or billing were run or inspected.

| Priority / concern | Pinned implementation locator | Disposition in the paper |
| --- | --- | --- |
| Important: earlier witnesses/retention labels can anchor endpoint ratings; local evidence IDs repeat across checkpoints | `judging/judge.py:363-374,441-447,471-480`; `judging/copilot-judge.mjs:118-121`; `judging/scenarios.py:61-65` | Disclose historical context and nominal citation validation; endpoint-only packets or namespaced IDs require a separately versioned instrument, not an alleged current fix |
| Important: treatment-dependent acquisition and missing earlier history change witnessed risk sets | `judging/judge.py:246-255,682-689` | Require final fulfilment, acquisition classifications, risk counts and missingness with conditional loss density |
| Important: post-CR1 loss uses any earlier eligible P witness, not only P10 | `judging/judge.py:363-365`; `judging/scenarios.py:26-47`; `judging/tests/test_judge.py:108-126` | Distinguish endpoint loss from incremental CR1-induced loss; explain maxima of nine/eleven prior-witness scenarios |
| Important: no scheduling-block/epoch fields in report rows | `judging/judge.py:291-308,322-323,379-381,694-710` | Require private trajectory/source/epoch/block linkage; retain descriptive and unresolved dependence limits |
| Important: pooled ordinal means/ranges conflate between-judge and repeat variability | `judging/judge.py:659-681`; `judging/config.example.json:11-14` | Require judge-specific ledger inspection and blinded human calibration; no reliability or equal-interval claim |
| Important: hashes/admission checks cannot prove prospective choices or full-frame affordability | `judging/judge.py:319-323,396-405,565-572,589-609` | Record exposure/choices and separate calibration costs; budget exhaustion can leave contrasts unavailable |

Source-verified strengths include full allocated-cell checks, no last-successful
endpoint substitution, undefined empty/missing risk-set density, exact recorded
commit/runtime-asset replay, read-only/no-network evaluation and tool-free
guarded judging transport. Evidence locators: `judging/judge.py:136-164,291-308,336-341,673-710`,
`harness/isolation.py:251-267`, `judging/copilot-judge.mjs:24-49,105-144`.
These are implementation-contract findings, not adversarial integrity,
deployed-environment, scientific or accuracy certification. Actual anchoring,
mis-citation, calibration and dependence remain untested.

### Validation and Remaining Decisions

The owner's later technical-flow request extends this same paper workstream.
The flow labelled "Main experiment" in the supplied explanation depicts
stopped-archive post-run replay/judging; the one labelled "Judging" depicts
tool-enabled development. The added subsection and original paired figure
use the corrected names. They separate host-side Python/JavaScript model
transport from isolated candidate execution, including writable development
state versus read-only replay inputs, fresh processes versus retained files/
Git, and collected failures versus unavailable isolation/collection.
Exact source-support and final figure/PDF validation are recorded with this
continuation rather than claiming the earlier judging-only build covered it.

The Coach-guided follow-up checked the supplied sources at `b7973e20` and
compared relevant contracts at running source `e71037d9`.
The source evidence corrects one supplied control claim: the entire
container is not capability-free. Four capabilities are re-added for
the protected supervisor; the UID/GID 1001 candidate child has cleared
effective/permitted/inheritable capabilities and no-new-privileges.
Development persistence is validated state replay, not a persistent
container or writable host checkout. Committed regular content crosses
feature/CR checkpoints with canonical host history; candidate process
reset does not reset host/model conversation context.

| Technical claim | Inspected source locator at `b7973e20` | Evidence state / limit |
| --- | --- | --- |
| Stopped-archive recorded-HEAD replay, read-only snapshot/evaluator | `judging/judge.py:203-222,258-272`; `harness/isolation.py:265-267` | Source support; no real archive or image qualification inspected |
| Bounded evidence, host adapters, no-tool judge and report | `judging/judge.py:167-195,218-220,485-523,598-605,646-755`; `judging/copilot-judge.mjs:24-49,118-125` | Source support; no provider sessions or actual packets executed |
| Host bridge, fresh development commands and logical state replay | `harness/isolated_runtime.py:275-301,487-494,556-574`; `harness/isolation.py:447-467`; `harness/isolation_helper.py:529-572` | Source support; no persistent host writable mount or candidate process continuity implied |
| Committed checkpoint imports and separate scheduled validation/measurement | `harness/isolated_runtime.py:335-384,427-451`; `CONTRIBUTOR.md:335-349` | Source support; agent-requested tests remain distinct from controller-scheduled checks |
| No-network/root/resource controls, constrained supervisor and unprivileged candidate | `harness/isolation.py:251-267`; `harness/isolation_helper.py:25-33,282-297,337-360` | Conflict with whole-container zero-capability claim; corrected, not newly enforced |
| Isolation/collection unavailable versus ordinary candidate failure | `judging/judge.py:351-356`; `judging/scenarios.py:298-308` | Source-supported classification, not verified outcomes |

The running source has corresponding network/root/resource/mount controls
at `harness/isolation.py:198-214`, development replay at `333-345` and
host routing at `harness/isolated_runtime.py:249-332,486-622`.
The transport/runtime guard files match between the two source pins, but
the isolation files do not wholly match: linked/special-file output
rejection recovery is a later enhancement and is not attributed to the
running source. There is no judging directory at `e71037d9`.
Neither comparison verifies the deployed image/runtime or all three
archived implementation epochs.

SymPy 1.14.0 checked the new fraction's zero-loss, total-loss and one-of-four
boundaries (0, 1 and 1/4) on a valid positive denominator. Empty or unavailable
risk-set endpoints are excluded by definition, not imputed as zero.
The two-endpoint session expression is dimensionally a count; the conditional
example 2 x 315 x 1 x 3 = 1,890 is arithmetic, not observed judging activity,
an actual configuration or an independent sample size.

The initial judging-only 56-test suite and structural checker covered the added prospective-method,
source binding, risk-set, ordinal-rating, aggregation and cost boundaries.
Structural results retain 94 cited/105 reusable references and a
1,806-character abstract. Approximate main-body words are 11,506 using the
existing method; historical comparison `0d5dcb02` remains unavailable.
These checks validate paper invariants, not the external judging pipeline.

Tectonic 0.17.0 compiled that initial single **47-page** PDF, Supplement page **37**,
main judging subsection page **21**, instrument detail pages **44-46**.
The actual compiler log has no errors, unresolved references or overfull/
underfull boxes; the inherited `inputenc` warning remains.
All-page text bounds, 183 internal destinations, 51 outline entries and
absence of blank pages pass. Changed pages 21/29/44-46, the intact B/C
examples on 46/47 and an all-page layout proof were rendered and inspected.
The optional pdfLaTeX-specific log-marker check was not claimed under
Tectonic. Final PDF SHA-256 is
`93f3b405fc0a9118787619be514d5c58eea1e99154bd4fdb5edc97bf050fb75b`.
Build intermediates, visual proof and the exact scoped source assessment
remain external session working files; lasting findings and provenance
are preserved here and publication evidence belongs in the PR.

The complete technical-flow continuation passes **57 authoring tests**,
including six-figure native byte-identical re-export and current source/PDF
bindings. Structural checks retain 94 cited/105 reusable references and
the 1,806-character abstract; approximate main-body words are now 11,943.
Historical comparison remains unavailable. The complete PDF has **49 pages**,
Supplement **39**, execution-boundary text **17-18**, paired Figure 6 **19**,
judging methods **21**, detailed rules **46-48**, and the intact C prompt **49**.
All-page text bounds, 184 internal destinations, 52 outline entries and
absence of blank pages pass. Changed pages, the original paired diagram,
B/C prompt pages and an all-page layout proof were inspected.
The actual Tectonic log retains only the inherited `inputenc` warning,
with no errors, unresolved references or overfull/underfull boxes.
Final PDF SHA-256 is
`6847840ddbf3d49abc27ab52b626fad57728ebccb592c7e83c13bd11734abdb6`.
The source/editable/SVG/PNG diagram bindings are in
[diagram-exports.json](../diagram-exports.json); the current source/PDF
bindings are in the `runtime_flow_revision` of
[supplement-integration.json](./supplement-integration.json).
The earlier judging-only binding and validation outcome remain historical,
not the complete candidate's receipt.

Author/operator decisions remain: actual archive/source epochs and availability;
freeze timing and prior outcome exposure; chosen judge models/adapters,
repetitions and separate authorised budget; blinded human-calibration sample,
agreement/disagreements and reviewers; residual blinding; and any justified
block-aware inference outside the descriptive instrument. The source/PDF
bindings are refreshed in [supplement-integration.json](./supplement-integration.json),
preserving the historical 8 November bindings.
Component checks, independent exact-head review and publication evidence are
recorded separately below and in the PR. None supplies scientific, human,
ethics, venue or employer publication approval.

## Measurement Provenance Clarification 8 November

### Scope, Assistance and Source

The owner explicitly requested paper explanations, tables and relevant example
prompts after the read-only measurement audit. Work continues directly on
`docs/capstone-autonomy-story`, from clean `836093cf`, with PR #1283 open.
The authorized outputs are the existing paper/source record and additive
Supplement, plus directly related documentation and focused authoring tests.
The slides and the running experiment are not revised in this scope.

The active public source is
[`e71037d961cb80fc5c659437796de7736820f6c9`](https://github.com/jmservera/ama-thought-mve/tree/e71037d961cb80fc5c659437796de7736820f6c9).
The default `baf58b4f` inspected during the audit contains it; the supplied
execution has no tag. The source files below were inspected directly.
No private run records, hidden oracle bodies or paid model calls were used.
This is implementation-source verification, not verification of collected
outcomes or actual per-session tool/provider conditions.

Copilot-assisted clarification used scientific-critical-thinking, the
scientific-writing reference, existing tests and PDF tooling. The existing
`kassis2026skills` citation and prior metadata-verification limit are retained;
the manuscript records the actual added assistance. No new algebra/design
audit, venue policy check or claim of independent human peer review is made.

### Claims, Locators and Evidence States

| Claim / paper locator | Inspected active source | Evidence state and limit |
| --- | --- | --- |
| No separate numerical AI judge; Outcomes and retained-contract loss | `harness/measure.py:342-374`, `harness/pilot_analysis.py:53-154`, `harness/runner.py:387-433` | Full-text/source support for the described code path, not proof of every private execution |
| Functional coverage is hidden-contract pass fraction, not line/branch coverage | `harness/measure.py:205-320`, `harness/pilot_analysis.py:157-307` and public panel/config metadata | Source support for scoring and completeness rules; no hidden test contents or outcome data inspected |
| Complexity/duplication/lint/size are structural proxies; field table in additive Supplement | `skeleton/tools/metrics_core.py:126-292`, `skeleton/tools/quality.py:8-39` | Source support for actual fields, scales, backend settings and lack of a general quality/maintainability-index score |
| Earlier Ruff suppression safeguard is false; final Measures paragraph | `skeleton/tools/metrics_core.py:217-250,255-292` | Conflict: actual call has `--isolated`, not `--ignore-noqa`, and no suppression count; corrected, not fixed in the running kit |
| AI credits/tokens/time are recorded resource observations, not AI scores | `harness/analyze.py:74-184`, `harness/runner.py:222-263` | Source support for parsing and observations; full all-attempt cost needs the journal and complete usage, neither newly inspected |
| B/C text is treatment instruction, not a scoring rubric; Active prompt examples | Both `harness/prompts/*-step.prompt.md` templates, `harness/runner.py:51-69,222-263,387-433` | Exact template bytes retained and SHA/Git-blob checked; actual private `prompt.md` and full provider/system context not inspected |
| Conservative loss/CR1 reporting remains narrower than the planned specification | `harness/pilot_analysis.py:53-154,157-307` and failure-attribution module | Source support for conservative unavailable summaries and composite CR1; richer graded/stratified exports remain gaps |

The main table distinguishes outcomes, structural proxies, resource observations
and explicit annotation/integrity records. The Supplement gives raw field names,
units, denominators, backend/pin and missingness limits. Empty denominators
remain undefined; zero complexity summaries on an empty function set are
described as source-emitted sentinels, not a valid measured mean/share.

The active prompt snapshots are:

* [B](./consolidation-active-e71037d9.prompt.txt): 1,471 bytes, SHA-256
  `1ee3da712fcb787a7843d1270aabf61b55abb7c8b7df2534d4adc078b0241494`,
  Git blob `fe00defa94b65eeb319e24256e425942247e0a14`.
* [C](./review-only-active-e71037d9.prompt.txt): 719 bytes, SHA-256
  `06a8dfcaee30ab52c243c771844619cf08f23854ef866f1bfde5277362391725`,
  Git blob `706d15d3c7e1615d58c0902a050b0e80d163e929`.

All retained bytes include the Markdown heading/comment. The PDF explains how
the runner strips these and substitutes the 900-second budget as `15 minutes`.
The current C source's `optional placebo` heading is retained, but the paper
continues to classify it as information-bearing review. The old frozen v4
prompt and its checksum remain unchanged. Matching measurement-module/C-prompt
blobs across the three disclosed epochs do not make all data or execution
conditions uniform.

### Validation and Assessment Boundary

The 50-test authoring suite and structural checker pass: 94 cited entries,
105 reusable entries and a 1,806-character abstract. The approximate main-body
count is 11,156 using the existing method (tables included; abstract,
bibliography and appendices excluded); historical baseline `0d5dcb02` is
unavailable, so no before/after comparison is claimed.
Six focused documentation regressions guard template byte
bindings, active Supplement includes, field names and instrument classification,
the Ruff limitation, and the distinction between AI review and outcome scoring.
They validate authoring invariants, not experimental correctness or efficacy.

Tectonic 0.17.0 compiled the single 45-page PDF, Supplement page 37. Its log has
no TeX errors, unresolved references or overfull/underfull boxes; the inherited
`inputenc` compatibility warning remains. The optional checker still expects
a pdfLaTeX marker and is not used as evidence of Tectonic failure.
All-page word bounds, 180 internal named destinations and 49 outline
destinations pass; no blank pages or invalid internal targets were found.
Tables 7/15, explanation pages and both prompt listings were rendered and
inspected, along with an all-page layout proof. The final short C example is
kept intact on page 45. The complete B/C display text matches after NFKC/
whitespace normalization and exclusion of page-number footers; that check
does not claim byte identity of PDF text. The retained source templates are
separately byte/hash-bound as specified above.

Final PDF SHA-256:
`58287cefefb4d0b10b6db6bac086a23c329597fe356211a88cda3ac144fea52f`.
Current source, normalized additive-body and literal-input bindings are in
[supplement-integration.json](./supplement-integration.json); earlier
authorship/historical bindings are preserved. The external component build
is under this session's `files/paper-measurement-2026-11-08/`. Independent
exact-head review and a fresh focused local publication gate remain separate
steps; their outcomes/receipts are retained in PR #1283 rather than making
component checks stand in for approval.

The existing title, coauthors, case claims, original/adverse reviews, historical
figures, source epochs, pending result TODOs and false results switch are
preserved. No experiment code/configuration, results, OSF registration or
amendment, repository visibility or slides are changed. The inspection cannot
certify scientific, human, employer, ethics or venue approval.

## Execution, Registration and Coauthorship 8 November

### Authorized Scope and Assistance

Mode: scoped revision and existing local tests/build, not a new study-design
or research audit. After an explicit owner override, authoring moved to the
existing `/home/jmservera/source/ama` branch `docs/capstone-autonomy-story`.
Its checked starting HEAD was `d3edf91039872e8e6d8548ea0387d371cca34ac7`,
including `80fc5ba8`'s author-affiliation change. Both original and child
paper packages were clean and byte-identical before editing. No child edits
had been made or transferred; `/tmp/ama-study-authorship-1108` remains
untouched. No branch switch, stash, commit, remote write or parent
slide/index/log edit belongs to this revision.

The named inputs were the package README, manuscript, current `review.md`,
relevant revision dispositions, active TeX inputs and existing local tooling,
plus the supplied exact-commit public `pilot-estimation.json` and narrow
public README/CONTRIBUTOR passages. The scientific-writing reference was
read; capstone Section D was kept separate from generic scholarly criteria.
No target venue or current employer publication policy was inspected.
No private experimental data, study launch or actual outcome analysis was
requested or performed.

Copilot-assisted revision used the scientific-critical-thinking skill for
bias/source qualification, not a new equation or design audit. The existing
`kassis2026skills` citation, DOI `10.48550/arXiv.2609.00065` without a
version suffix, and earlier four-skill disclosure are retained. The parent
supplied a latest-v2 arXiv metadata check; its simplified page did not verify
the full author list. No new author-list verification is claimed.
The manuscript adds the actual 8 November assistance scope.

### Authorship and Current Registration

The owner explicitly selected **COAUTHOR** and confirmed that Isabel
Cabezas Martin agrees to the credit and stated affiliation, **Software
Engineer, Frontier Company at Microsoft**. The author list/PDF metadata
and contribution statement add her, preserving Juan Manuel Servera
Bondroit's current name and **Senior Partner Solution Architect,
Microsoft EMEA, Zurich** affiliation. No location, email, ORCID,
credential, manuscript review or final-author approval is inferred.

Servera Bondroit conceived the study, designed methodology, defined
evaluation criteria, analysed the historical case and wrote the manuscript.
Experimental analysis remains a responsibility as collection proceeds.
Cabezas Martin conducts ongoing execution/data collection independently
under the predefined exploratory protocol and disclosed amendments.
Operational separation is intended to minimise potential experimenter bias;
both authors remain Microsoft employees. It supplies neither institutional
independence nor independent scientific review/analysis, and does not
demonstrate elimination of bias. Views/competing interests are plural.
Employer external-publication clearance and final-author approval are separate.

The owner confirms **registered base** `https://osf.io/xcpt4`, dated
**7 November 2026**. The supplied displayed time is `Nov 7, 2026 4:46 PM`,
with no timezone; the manuscript uses the date only. Access evidence
supplied for this task reports an app shell on the public page and HTTP 401
from `https://api.osf.io/v2/registrations/xcpt4/`. Registration/date are
owner-confirmed, not independently verified OSF metadata. No approval,
embargo, DOI or prospective timing for all observations is inferred.

Current execution includes **disclosed unregistered amendments** for short
calibration, parallel execution and VM restarts. The public source describes
the changed path as unregistered; its false/null amendment-registration
fields do not mean there is no registered base. Neither public source
disclosure nor an older freeze makes this a homogeneous preregistered
confirmatory dataset. No new OSF amendment is asserted or created.

### Implementation Epochs and Evidence States

Active source: `jmservera/ama-thought-mve` commit
`e71037d961cb80fc5c659437796de7736820f6c9`, tree
`e7ec1561d4ecee921e7c9eba3711a1ab7e9f4058`, **no tag**.
Profile: `protocol/pilot-estimation.json`, analysis design
`model-stratified-v2-five-arm`, suite `s1-retrofit`, exploratory
pilot-estimation, `formal_hypotheses=[]`. Owner-supplied runtime selection:
GPT 6.1 Sol / Claude Sonnet 5.5 / Gemini 4 Argon, medium effort, A–E,
21 replicates per model/arm despite file default 12, F1–F10 plus CR1,
seed 2027. Planned trajectories are `3*5*21=315`; completed trajectories
and an independent observed n were not supplied.

| Epoch | Exact execution source | Public commit time supplied as checked metadata | Owner-reported completed steps as of 8 November |
| --- | --- | --- | ---: |
| E1, pinned CLI fix | `99a1ed170d7c71acb428b52e0e24be8856cc3ea3` | `2026-11-07T22:12:45Z` | 651 |
| E2, source-bound estimation recovery | `3c2ce89b00fe583c1f0715e8ccd3510419d5e734` | `2026-11-08T08:36:43Z` | 227 |
| E3, failed-request charging fix | `e71037d961cb80fc5c659437796de7736820f6c9` | `2026-11-08T13:01:01Z` | 369 |

Total **1,247 completed steps**, including possible measured nonpasses.
These are owner-reported progress, not inspected private data, independent
replicates or completed trajectories. Commit times are not collection times.
Preserve each step's actual source epoch, failures, unknowns and model/arm/time
assignments. Temporal/arm/model confounding limits pooling evolving-source
data. No post-hoc sensitivity analysis/result is invented.

| Claim and manuscript locator | Source and inspected locator | Evidence state and limit |
| --- | --- | --- |
| Coauthor identity, affiliation and roles; title block, Author contributions and Competing interests | Explicit owner instructions for this revision | **User-supplied unchecked**, owner-confirmed credit agreement; not a manuscript approval or credential check |
| Registered base/date; Section 7.1 (PDF p. 15) and Data availability (pp. 27–28) | Owner confirmation of OSF xcpt4 and supplied page/API access results | **User-supplied unchecked** confirmation; OSF metadata **Unavailable** to independent verification in this task |
| Declared current design/default/models/features; Section 7.1 and Data availability | Retained `pilot-estimation-e71037d9.json`, `study`/`runtime`/`analysis`/`registration` objects; exact public commit identity supplied | **Full-text support** for inspected declared fields, not saved runtime identity or actual execution |
| Unregistered short calibration/parallel/restart path; Section 7.1 and Data availability | Read-only `gh api` at `e71037d9`, README lines 9–17, 129–154, and CONTRIBUTOR lines 1–17, 74–81 | **Full-text support** for the disclosed changes; historical readiness prose is not evidence of current operational approval |
| Current SHA/tree and epoch commit times; Data availability and this table | Public commit metadata supplied as previously verified by the parent task | **Metadata-only**, supplied prior check, not re-queried here; times identify commits rather than run events |
| Selected n21, ongoing collection and 651/227/369 steps; abstract, Section 7.1 and Data availability | Owner-supplied runtime choice and progress account as of 8 November | **User-supplied unchecked**; no dataset, trajectory completion, cost reconciliation or efficacy result inspected |

The retained protocol input is
`/home/jmservera/.copilot/session-state/a94bf42c-3cbc-40ed-936a-62702b3fce6f/files/paper-study-update-2026-11-08/pilot-estimation-e71037d9.json`.
Pinned source locators:
[protocol](https://github.com/jmservera/ama-thought-mve/blob/e71037d961cb80fc5c659437796de7736820f6c9/protocol/pilot-estimation.json),
[README](https://github.com/jmservera/ama-thought-mve/blob/e71037d961cb80fc5c659437796de7736820f6c9/README.md),
[CONTRIBUTOR](https://github.com/jmservera/ama-thought-mve/blob/e71037d961cb80fc5c659437796de7736820f6c9/CONTRIBUTOR.md).
Read-only source retrieval checked the relevant passages, not the entire
execution implementation, release image or study data.

### Applied Changes and Preservation

Updated the abstract, protocol/current execution, conclusion, author list
and metadata, contributions, plural views/competing interests, data
availability and assistance disclosure. The existing Supplement receives
only cross-reference/provenance corrections, without a parallel supplement
or duplicated case narrative. The retained v6 design/measurement diagrams
are unchanged and labelled historical in captions; no new diagram is needed.

Historical v4/v6/v7 records, registered materials, original adverse reviews,
case data, numerical observations, frozen consolidation prompt and
`\resultsfalse` remain. Power/resource tables, thresholds, planned analyses,
budgets and economic assumptions were not recalculated or silently revised.
Earlier source-inspection reporting/inference gaps remain explicit, without
pretending to re-audit their active implementation or backdating a remedy.

### Local Validation and Delivery

All new compiler intermediates/logs, caches and inspection PNGs are in
the external run:
`/home/jmservera/.copilot/session-state/a94bf42c-3cbc-40ed-936a-62702b3fce6f/files/paper-study-update-2026-11-08/paper-build/authorship-revision-GQAxhZ`.
Only the verified `main.pdf` was copied into the paper package after
confirming that the original delivery had no conflicting tracked or staged
edit and still matched the starting child delivery.

* `python3 -B -m unittest discover -s anc -p 'test_*.py' -q`: **44 tests
  pass**, no test failures/errors. These are existing authoring/planning
  regressions, including all 39 historical resource cells and five native
  diagram source/export bindings, not executed-study validation.
* `python3 -B anc/check_paper.py`: **PASS**, 94 cited/embedded entries,
  105 reusable entries, 1,806 abstract source characters, unique resolved
  labels and a false results switch. Approximate body words: 10,487.
  The configured historical baseline `0d5dcb02` remains **UNAVAILABLE**;
  no baseline reduction is claimed.
* Tectonic **0.17.0**, `--untrusted --keep-logs --keep-intermediates` with
  an external output directory and task-local HOME/XDG caches: **exit 0**.
  Actual final log: **0 TeX errors**, **0 unresolved references/rerun
  warnings**, **0 overfull boxes**, **0 underfull boxes**. One inherited
  warning remains: `Package inputenc Warning: inputenc package ignored
  with utf8 based engines.` No pdfLaTeX output-marker check is claimed.
  The normal automatic rerun completed; `main.log` and
  `tectonic-console.txt` are retained in the run's `compiler/` directory.
* PyMuPDF **2.0**: **40 pages**, one additive Supplement starting at
  **page 35** (Appendix A). All-page word bounds checked 17,370 extracted
  words at a 0.5-point boundary tolerance: **0 out-of-page words**, **0
  blank extracted pages**. **174 named internal links**, **254 destination
  page bindings** and **47 outline destinations** resolve within the
  document, with **0 invalid destinations**. The 83 external URI
  annotations were enumerated, not live-access validated.
* Full 125-dpi renders inspected on pages **1–3, 8–9, 15–22, 25–28,
  35–37 and 40** (21 pages), covering changed authorship, status, historical
  figure/table labels, conclusion, disclosure, availability and Supplement
  corrections. All 40 pages were also inspected in layout proofs.
  Renders/proofs remain in `inspection/`; no scientific figure was changed.
  An optional Pillow contact-sheet attempt failed to import `PIL`.
  No dependency was installed; the existing PyMuPDF renderer then produced
  the inspected all-page layout proofs successfully.
* Source comparison confirms unchanged equation bodies, bibliography,
  `review.md`, original adverse review, case data/evidence index, native
  diagrams and literal frozen prompt. Active normalized Supplement digests
  are refreshed with prior digests retained; current source/PDF digests are
  in `supplement-integration.json`.
* Checked delivered PDF SHA-256:
  `1a39c104c7e6ae0bb2075cceffe54b3ed8cdb037effe8d6efa223f3b84a47cda`.
  PDF metadata lists **Juan Manuel Servera Bondroit; Isabel Cabezas Martin**.
  Title and current Juan Manuel affiliation were preserved.
* Scoped `git diff --check` passes. Pre-existing ignored checkout compiler
  remnants were observed and left untouched (the `main.log`/`main.aux`
  timestamps precede this task; historical `supplement.*` remnants also
  remain). They were not this revision's outputs. No dirty-input exclusion,
  stash or commit was used. The child worktree has **no task changes**.

There is **no blocking component validation**. Exact-head independent
assessment, the focused repository publication gate, hosted checks and
human publication/author approvals were not run or inferred; the parent
owns those steps and its slide/index/log synchronization.

Work execution: **Complete** for the scoped revision and local validation.
Assessment: evidence-bounded assisted revision with owner-confirmed
registration/runtime/progress facts and independently unavailable OSF
metadata, not independent review, statistical certification, scientific
acceptance or publication approval. No new experimental result,
experiment-source/configuration or registration change, or actual model run.

## Recovery and Scientific Alignment 5 November

Work execution covers the owner-authorized recovery and bounded source
corrections. Assessment is an independent agent-assisted scientific
consistency review plus parent numerical/authoring checks, not independent
human peer review, statistical certification or collection approval.
Validation and publication are recorded separately below.

### Recovery and Current Source

Closed PR #1206 without deleting its branch. PR #746 already contained the
four scientific skills, reviewer and prior manuscript changes, with exact
tree/blob equality verified. The current-main paper package was identical
to the parent of `3ef395b8`. Replayed only that final amendment with
`--no-commit` on fresh topic `docs/paper-scientific-reconciliation`,
based on `c6d5a8f3`. The actual replay was conflict-free; the new log record
was appended after all existing main history.

The [original scientific review](../../../../../.copilot-tracking/reviews/2026-11-05-paper-scientific-reconciliation.json)
is retained unchanged, including its three major findings, one minor
finding and adverse assessment. It inspected the active article and TeX
inputs, disclosure, allocation figures' text and current kit source.
It did not re-audit the case or systematically verify external citations.

The review inspected current public MVE default
`5ab24be4556876500a40e56201f6efc3930cc8b8`, a manifest-only child of
`7de2f0d42955c62b52906747de480df2b3f1e0ca`, which the published
`protocol-frozen-v6` tag identifies as execution source. Current source
contains A/B/C/D/E and the immutable selector. The existing local checkout
at `1fee4535` and its `origin/main` at `03c50856` were stale, and were
neither updated nor used as current implementation evidence.
Release/tag identity and source bodies were checked; release attachments,
the complete fingerprint, runtime image and declared harness/SDK/canary
test totals were not independently reproduced.

### Findings and Dispositions

| Finding | Source correction | Scientific boundary |
| --- | --- | --- |
| EBTS-SCI-01, major | Replaced current A/B/C-only assertions with the dated full-SHA v6 implementation account in protocol, disclosure, availability, current README and design-figure source. Kept historical v4 and 2 November inspections. | Implemented source is not executed study evidence, scientific approval or a completed prospective record. |
| EBTS-SCI-02, major | Marked observed-subset loss/missing bounds and graded/prerequisite CR1 panels as prospective reporting requirements. Added the inspected analyzer's conservative unavailable-result rule and explicit uncertainty in prior acquisition/risk membership. | Author must separately authorize implementation or prospectively amend reporting before collection. No kit or estimand was silently changed. |
| EBTS-SCI-03, major | Described independent arm/model draws as the implemented candidate and made the required scientific choice explicit. Added the inspected primary-frame availability rule without accepting or replacing it silently. | OPEN before collection: justify scheduling-only blocks with independent inference, or approve block-aware inference and aligned variance/planning, bound to exact source and prospective recording. A scheduling label establishes neither pairing nor independence. |
| EBTS-SCI-04, minor | Corrected the Introduction to make matched-ceiling B-D primary and extra-allowance B-A secondary. | Equal ceilings do not ensure equal realized spending or isolate refactoring. |

The review's source-body probes used synthetic in-memory inputs only,
including schedule balance, immutable selection, admission, missingness and
independent-arm resampling. They did not instantiate the launcher, create
or resume a saved study, invoke providers or establish inferential coverage.
The parent did not repeat the delegated external-kit source investigation.

Other explicit pre-collection decisions remain allocation/rationale,
primary-frame eligibility, additional CR1 reporting and E's external
semantic adjudication. Full-allocation affordability requires a dated
researcher forecast/approval; the current launcher's attempt/aggregate
admission and nonempty calibration note do not establish that forecast.
Public configuration values and unknown-usage holds are declarations, not
reconciled bills or proof of remaining spending authority.
The inspected manifest has a null registration date,
`prospective_osf_update_recorded=false` and `collection_authorized=false`.
No date, authorization or OSF state is invented here.

### Numerical and Authoring Checks

The recovered candidate passed all 34 existing authoring tests. Nine new
stdlib regressions independently derive all 39 resource cells from the arm
schedules and CR1, verify all three conditional sample-size rows, nine
economic cells and discrete payback, and check matched ceilings/allocation
labels. All 43 passed before the source reconciliation. A further regression
now protects the current source pins and explicit reporting/inference gates.

An isolated pip environment supplied Python 3.12.3, SymPy 1.14.0 and
mpmath 1.3.0. The final isolated `runpy.run_path` invocation passed after
direct script invocations failed to import SymPy; the failed attempts are
not reported as passes. Exact symbolic checks reproduce
`2*sigma**2/(M*n)` under independent balanced cells and
`delta*N*(N-1)/2-k*N` for cumulative cost. A covariance-aware illustration
reduces to the independent expression only under the corresponding zero-
covariance/common-variance assumptions; it selects no actual dependence model.
Conditional normal planning reproduces 12/21/33 per cell for assumed SDs
15/20/25 and 131 for SD 50.

| n per model per arm | Hypothetical normal power at assumed SD 25 |
| --- | ---: |
| 12 | 0.3964384390 |
| 21 | 0.6122026489 |
| 33 | 0.8035274845 |

These are pre-data sensitivities, not observed power, actual variance,
bootstrap-coverage validation or scientific acceptance. The actual
300,000-credit envelope and 270,000 admission ceiling are unchanged.
No study, calibration, paid model call, private dataset, Azure, freeze,
registration or visibility action was performed.

### Final Local Validation

* `python3 -B anc/check_paper.py` passes with 94 matching cited/embedded
  entries, 105 reusable entries, a false results switch and a 1,719-character
  abstract. The approximate body count is 9,999; its configured historical
  baseline is unavailable, so no baseline reduction is claimed.
* `python3 -B -m unittest discover -s anc -p 'test_*.py' -q` passes all
  44 tests, including the ten new planning/source-fidelity regressions.
  These numerical and authoring checks are not scientific acceptance.
* The native figure authoring script and offline exporter complete. All five
  source/export bindings pass; only the two revised conceptual figures change.
  The design footer identifies v6's five-arm implementation, and the
  measurement figure marks additional retention/CR1 reporting as planned.
  Both revised diagrams were visually inspected.
* `./tools/update-pdf.sh` completes with Tectonic. The delivered PDF has
  38 pages and one Supplement beginning on page 33. All-page extracted text
  bounds and internal destinations pass; revised power/resource pages 19
  and 21 were rendered and inspected. No TeX error, unresolved reference or
  overfull box was found. One inherited `inputenc` compatibility warning
  remains. No pdfLaTeX-specific output-marker pass or accessibility
  acceptance is claimed.
* Checked PDF SHA-256:
  `6f822964e6031d9f14c05c8a94b3f26353af440e8e6851e5441082a1ff827dc4`.
  The original review copy matches its independently written JSON at
  `e4107b4847b1918f4f1b91d46ab56f3dd62a328d50a64a726d0001ab273fbc63`.
  New review links and heading fragments resolve; tracked/untracked
  whitespace checks pass.
* The focused repository gate, independent exact-head correction assessment
  and hosted checks follow the committed candidate. Their receipts and
  verdicts are publication evidence to be recorded with the replacement PR,
  not passes inferred by this pre-commit record. Collection and scientific
  approval remain separately blocked by the decisions above.

## Prospective Allocation Revision 2 November

Work execution is complete for the requested manuscript allocation revision
and compiled PDF. Assessment consists of scoped assisted numerical, structural
and rendering checks, not independent scientific review or collection approval.
The title, three selected models, A/B/C/D/E proposal, false results switch,
original v4 prompt and historical disclosures remain unchanged.

### Selection and Power

The [protocol](./experiment-protocol.tex) now offers 12 (default), 21 or 33
independent repository trajectories per model per arm. The researcher records
the choice and rationale, assumed SD, power/precision trade-off, date and
source-bound saved configuration before study collection. The selected
allocation is immutable on resume. Outcome-driven resizing, additions,
replacements and automatic budget-driven sample reductions are prohibited.
Features, tests and agent sessions are not independent replicates.

Python's standard-library NormalDist reproduces the existing approximation
for three equally weighted models, a ten-percentage-point B-D contrast,
two-sided alpha .05 and target power .80:

| Assumed within-cell SD, percentage points | Unrounded planning minimum | Ceiling per model per arm |
| ----------------------------------------: | --------------------------: | -------------------------: |
|                                       15 |                11.77331960 |                        12 |
|                                       20 |                20.93034596 |                        21 |
|                                       25 |                32.70366556 |                        33 |

These are conditional planning assumptions, not measured variances or
interchangeable guarantees. With SD 25 and n=12, the same normal model gives
approximately 0.396438 power, not .80. This is a hypothetical sensitivity
calculation, not observed power. Worst-case bounded-score SD 50 requires 131
per cell under that approximation, outside the offered choices. Scheduling
blocks still need reconciliation with the independent-trajectory planning
variance and within-model/arm bootstrap before the new freeze.

### Schedules and Resource Audit

Read-only inspection of the earlier
[candidate protocol](https://github.com/jmservera/ama-thought-mve/blob/7c3802d1f010bb03e9005e89b51abf730c15b776/protocol/pilot-estimation.json)
and its README confirms the proposed arm schedules, 45-minute/300-credit
CR1 in every arm, excluded calibration without CR1, and aggregate controls.
Its fixed-33 allocation is an earlier proposal, not the selection adopted here.

For each study trajectory, A/D have eleven sessions and B/C/E twenty-one.
A has 5.75 maximum hours and 3,300 nominal credits; B/C/D/E have 8.25 hours
and 6,300 credits. Multiplying each arm by three models and selected n gives
`15*n` trajectories, `255*n` sessions, `116.25*n` maximum hours and
`85500*n` nominal session credits. Exact Fraction arithmetic independently
reproduces these coefficients.

Calibration retains one ten-feature trajectory per model per arm, no CR1:
15 trajectories, 240 sessions, 105 hours and 81,000 nominal credits.
The protocol table now presents all three choices, with the default column
bold. All 39 numerical cells match the independent calculation. Default 12
gives 180 study trajectories, 3,060 study sessions, 3,300 sessions including
calibration, 1,500 maximum hours including calibration and 1,107,000 summed
nominal credits. The package README presents all three summary scenarios too.
The two allocation-bearing figures and their authoring script now show the
selectable allocation, default 180 study trajectories, shared CR1 selection
and A/B/C-only implementation boundary. Native SVG/PNG exports and their
source/export hashes were refreshed; historical figures remain in Git.

Nominal session sums do not enlarge the actual 300,000-credit aggregate
envelope or 270,000-credit local admission ceiling. The inspected older
candidate records 21.79019 known prior credits and a distinct 1,200-credit
unknown-usage hold; those are historical ledger entries, not newly reconciled
billing or free headroom. The manuscript preserves prior spending,
unknown-usage holds, all-attempt accounting and full-selected-allocation
affordability/deadline gates. Infeasibility halts collection; it does not
silently change n. A different allocation needs a separately authorized
prospective amendment and new saved study. An interrupted or unaffordable
study remains incomplete at its original selected allocation.

### Implementation and Evidence Limits

The owner supplies the current MVE capability: `--replicates` accepts
12/21/33, defaults to 12 and preserves an immutable saved selection, but
only A/B/C are implemented. The paper retains all five arms, so D/E
implementation and qualification remain required before its primary B-D
study can run. This revision corrects the earlier five-arm implementation
wording without deleting its dated record.

Read-only inspection found the public default at `03c50856`, the earlier
five-arm proposal at `7c3802d1`, and the local default checkout at `1fee4535`.
These inspected versions do not source-bind the newer selector update;
its capability remains owner-supplied, not independently exercised or
certified by this paper revision. The earlier candidate's runtime claims
are not treated as evidence that the owner's current A/B/C implementation
includes D/E. No MVE source, saved study or dataset was modified or used.
No study, smoke, calibration, model session, OSF action or freeze change
was launched. These changes are not part of the published v4 freeze.

### Focused Validation

* All 34 existing paper-authoring tests pass. Active Supplement hashes and
  the literal frozen prompt remain unchanged. The two revised native figures
  pass overflow checks and all nine figure/integration tests; their refreshed
  SVG/PNG bindings pass, and both exports were visually inspected.
* The structural checker passes with 94 cited entries, 105 reusable entries,
  a 1,707-character normalized abstract and a false results switch. The
  historical body-word baseline is unavailable, not reconstructed.
* Independent arithmetic checks pass for every resource-table cell and the
  three sample-size rows. No measured variance or study result is inferred.
* Tectonic compiles the 38-page PDF; the Supplement starts on page 33.
  Direct log/PDF checks find no TeX errors, unresolved references, overfull
  boxes, blank extracted pages or out-of-page words. The power and resource
  table pages 19 and 20 were rendered and visually inspected. One inherited
  inputenc compatibility warning remains. No pdfLaTeX-specific output-marker
  check is represented as passing under Tectonic.
* The required focused repository gate was attempted with `--changed`, an
  explicit base and external output after fetching `origin/main` at
  `a56df549`. It stopped with `Candidate has tracked modifications or
  untracked inputs`. No gate test groups ran or passing receipt was produced.
  No commit, stash, exclusion, branch change or remote write bypassed that
  precondition.

Remaining alignment gates are a source-bound selector update and D/E
implementation, resolution of scheduling-block dependence, a new exact-source
review/freeze and prospective OSF amendment, full-allocation affordability
and deadline evidence, collection authorization, and the clean-candidate
repository gate. No independent review, hosted approval or publication
readiness is claimed.

## Author Review Disposition 1 November

The nine points in the [author's review](../review.md) were applied to the
[manuscript](../main.tex), its active TeX inputs and editable figures.
The [integrated PDF](../main.pdf) has 37 pages; its Supplement starts on
page 32. The title is unchanged. The review document itself is unchanged.
This is an assisted editorial and mathematical review, with no experiment
collection, kit amendment, independent peer review or publication approval.

### Review Points

| Point | Disposition and remaining boundary |
|-------|------------------------------------|
| 1 | Replaced the merge-count-led premise with research, iterative BRD/PRD/ADR work, Design Thinking challenge, disposable prototypes, backlog generation and coordinated delivery. Renewed participant feedback and refactoring are part of the account. Preparation was intended to improve speed and quality; no human-only comparator establishes that effect. |
| 2 | Replaced visible statements about absent experiment results with author TODOs for checked results and PF1-PF3. The results switch remains false and the design remains prospective. |
| 3 | Removed programme-specific framing from the opening, referred readers to the evolving repository and retained the planned temporary embargo. Source pins and deposit/approval duties remain explicit. |
| 4 | Rephrased all six quoted examples and additional repeated contrastive disclaimers. Necessary distinctions about causal identification, missing data and treatment scope remain. Figure wording was revised in the same direction. |
| 5 | Abstracted the fictional customer into a synthetic multi-role service workflow. The methodology and handoffs now carry the case description. Actual bibliographic titles and provenance remain intact. |
| 6 | Replaced calendar-led case narration with phases and approximate durations. Dates in source filenames, bibliography and freeze/deposit metadata retain their provenance function. |
| 7 | Rewrote section 3.6 around workflow preservation, context transfer, completion evidence and renewed outcome feedback. Historical O1-O5 records and missing execution identifiers remain in the evidence index. |
| 8 | Replaced the project ledger with a phase table and focused contrasts, removed the log-volume plot from the article, and removed count-based mechanism/conclusion claims. Retained chart inputs and historical measurements were not deleted. The owner-supplied export supports the handoff sequence. |
| 9 | Used SymPy, statistical-analysis, scientific-critical-thinking and experimental-design to review all active equations and quantitative definitions. Clarified estimand/estimator, units, risk denominators, missingness, integer break-even and deferred-rate domains. Scheduling-block dependence remains a pre-freeze analysis decision. |

### Evidence Refresh

Targeted local history and log reads, together with fetched PR bodies,
support the process reconstruction:

* [PR #32](https://github.com/jmservera/ama/pull/32), local integration
  `e60adcd7`, links critiques of disposable prototypes to simplicity requirements.
* [PR #71](https://github.com/jmservera/ama/pull/71), local integration
  `9ef7e40f`, links desk-research journeys to revised requirements and architecture.
* [PR #461](https://github.com/jmservera/ama/pull/461), local integration
  `d783b63a`, records later recurring stabilization with qualified local evidence.
* The knowledge-base log records repeated what-if challenges, owner steering
  and requirements reconciliation after some backlog scope had appeared.

These are selected workflow anchors, not an exhaustive audit of every issue,
conversation or deployed release. The participant supplies the fuller steering
and feedback account. Initial bulk issue creation was not replayed; later PR
history does not by itself date restored deployed usability.

The [project export](./project-insights-2026-11-01.csv) preserves all supplied
32 daily rows and the Open, Completed and Not planned columns, with LF line
endings. The checksum identifies this repository copy; original-download
bytes were not accessible in the remote workspace. Around the
handoff, Open rises from 12 to 143 while Completed remains one. The final
supplied row is 129/86/7. These describe administrative states. The CSV omits
year, export time, timezone, filter settings and status definitions; its year
is inferred from the owner's discussion. The insights-page retrieval returned
HTTP 404, so the supplied export is the chart evidence used here.
Its SHA-256 is
`dfb9fe875bda546f545b625a594d2ce4a04ca2586f7140f285fd9b76de558489`.
The [evidence index](./case-evidence-matrix.json) adds these sources alongside
the unchanged historical observations and null execution links.

### Equation and Design Audit

Exact checks used Python 3.11.15 and SymPy 1.14.0 in an external isolated
environment. Normal quantiles came from the standard-library NormalDist.
The statistical and design skills guided review of the experimental unit,
dependence, weighting, controls, missingness and interpretation. No observed
outcomes were available for distributional diagnostics or effect estimation.

| Formula or definition | Verified result and interpretation |
|-----------------------|------------------------------------|
| Retained-contract loss and density | The count sums failures only over observed eligible prior-pass contracts; density divides by the observed set. It is checkpoint prevalence. An empty observed set is undefined. With missing count M, the full-risk loss count is bounded by L and L+M. Acquisition, recurrence and recovery remain separate. |
| Primary B-D contrast | The estimator equally weights the three within-model differences. For balanced independent cells with common variance, its planning variance is 2 sigma-squared / (3 n-cell). The displayed estimator is now distinguished from its estimand. |
| Normal sample-size approximation | SD 25 points, a 10-point target, alpha .05, power .80 and three models give 33 per cell, 99 per arm and 495 total. SD 15/20/50 gives 12/21/131 per cell. These are conditional planning calculations, not guaranteed power for bounded scores or the bootstrap. |
| Historical binary-interval illustration | The earlier lower limits -0.77639320 and -0.03650752 are reproduced by Bonferroni combination of two 97.5% Clopper-Pearson intervals for hypothetical all-success versus all-failure samples of two and six. Pooling heterogeneous model cells needs a different justification. The illustration was removed from the main protocol; per-model counts and component assumptions remain. |
| Cost accumulation and break-even | Symbolic summation of delta(t-1)-k agrees with delta N(N-1)/2-kN. For positive k and delta, the first nonnegative difference occurs at ceil(1+2k/delta). The examples give 11 and 201 cycles; delta zero yields no payback for positive k. All nine sensitivity-table entries agree. Parameters remain unestimated. |
| HIR and IDR | Both are cycle-incidence proportions over positive attempted-cycle denominators, with separate supplied-help and demand indicators. Complete annotation is required; incomplete records leave the full-run rate unknown. Zero attempts is undefined. These measures remain deferred. |
| Cost per accepted outcome | Attribution, period and accepted-outcome counting must be declared. Zero accepted outcomes leaves the ratio undefined; report expenditure and count separately. |
| Resource arithmetic | Study allowances total 8,415 sessions and 3,836.25 hours; excluded calibration adds 240 sessions, 105 hours and 81,000 credits. Combined allowances are 8,655 sessions, 3,941.25 hours and 2,902,500 nominal credits. The existing aggregate envelope is unchanged and affordability remains a gate. |

The first verification probe assigned calibration an erroneous 99,000-credit
allowance. Deriving it by arm gives 81,000; the corrected probe passes and
confirms the manuscript's existing combined total. No expenditure was inferred.

The substantive unresolved analysis point is agreement between model/replicate
scheduling blocks and independent within-arm bootstrap resampling. The paper
now requires source-bound review to justify independence or adopt a
block-preserving analysis and corresponding variance before the new freeze
and prospective registration. No companion-kit code or allocation was changed.
The single suite, fixed change request, selected models and bundled treatment
also limit generalisation and mechanism identification.

### Current Validation

* All 34 existing authoring tests pass, including the nine figure/integration tests.
* Native sources and SVG/PNG exports remain bound by hashes and raster dimensions.
  The original frozen prompt is unchanged. Prior supplement content hashes are retained.
* Structural checks pass: 94 cited bibliography entries, 105 reusable entries,
  balanced TeX, resolved labels and a false results switch. The abstract is
  1,724 normalized source characters; approximate body count is 9,048 words.
* Tectonic produces the 37-page PDF. Direct checks find no TeX errors,
  unresolved references, overfull boxes, blank pages or out-of-page text.
  One inherited inputenc compatibility warning remains explicitly reported.
* The optional check_paper log mode fails its pdfLaTeX-specific output-marker
  test under Tectonic. Direct compiler/PDF checks are the evidence above;
  this failure is not relabelled as a passing command.
* The old protocol_checks document mode targets a superseded four-run,
  eight-feature proposal and was not used to certify the five-arm candidate.
* The historical body-word comparison is unavailable because its baseline
  object is absent. No verified baseline percentage reduction is asserted.
* The focused repository gate first required its explicit base argument.
  After fetching main, the retry against `origin/main` at `2dc91854` stopped
  at preflight: tracked modifications or untracked inputs are present.
  No gate test groups ran and no passing receipt was produced. A clean,
  committed candidate is required for the later source-bound gate; no
  commit, stash, exclusion or other bypass was used here.

No historical cloud exports, private datasets, paid model calls, experiment
trajectories, repository-visibility changes, OSF actions, commits or pushes
were performed. Collection, independent review and publication gates remain
separate from these local authoring checks.

## Scope and Outcome

All edits are inside docs/capstone/thought-leadership/. The starting working
tree was clean. `git worktree list` showed this checkout and two separate
worktrees; the agent-process check found no other agent using this checkout.
The branch was left unchanged. No loop, issue, pull request, commit, push,
stash, rebase or branch switch was performed.

The package matched the expected layout in everything-but-the-software/.
Additional files were existing ignored LaTeX outputs and endpoint-DLP
sidecars, which were not treated as source. The sidecars were not edited.

The revised paper is not submission-ready: registration, historical model
provenance, author checks and publication permissions remain unresolved.
No experiment was run. The results switch remains false.

## Changes by Phase

| Phase | Outcome |
| --- | --- |
| 0 | Listed the package, checked Git/worktree safety and compiler availability, counted the original body and listed its author TODOs. pdfLaTeX was available; texcount and rg were not. |
| 1 | Replaced experience-report framing, defined the case and unit of analysis, added the participant-observer design and MVP contrast, and disclosed Microsoft 365 Copilot-assisted coding. |
| 2 | Fetched all nine requested sources and SWE-CI. Added matched bibliography entries, ordered both files by key, and bounded novelty to a controlled test of an already practised intervention. |
| 3 | Softened causal attribution, added the six requested rivals and bounded the MVP/loop contrast. The migration row cites issue #196, verified in pinned ADR 0006. |
| 4 | Set four first-pass runs per arm and eight features, retained five main-study runs, corrected fixed/random effects, verdicts, failure handling, end state, fairness, registration wording and threats. Updated the protocol and added its pre-run divergence log. |
| 5 | Found the Sonnet 5.5 worker selector and its introduction in PR #420 on 21 October, Automatic coordinator selection and the separate deployed assistant model. Kept unsupported version and instruction-date TODOs. Expanded the AI-use disclosure without claiming every historical source had been rechecked. |
| 6, optional | Added pinned Git line-churn measurement, its saved output, a paper table and the artefact/source ratio. Reported literal merges separately from a squash-integration heuristic. No lizard dependency was installed. |
| 7, optional | Not attempted. A 15% body cut would require broader editorial changes; the Monday checklist and main title remain. |
| 8 | Added the v3 README section, compiled twice, ran structural and protocol checks, and checked Markdown diagnostics. Removed temporary compiler files after recording the results; retained the revised PDF. |

## Reference Verification

All URLs below were opened with the web-fetch tool on 24 October 2026.
Verification concerns metadata and the stated passages, not independent
replication or an exhaustive assessment of each source's validity.

| Key | Verified metadata and relevant evidence |
| --- | --- |
| waseem2025vibe | Muhammad Waseem, Aakash Ahmad, Kai-Kristian Kemell, Jussi Rasku, Sami Lahti, Kalle Makela and Pekka Abrahamsson; *Vibe Coding in Practice: Flow, Technical Debt, and Guidelines for Sustainable Use*; 2025. Both abstract and full text retrieved. The full text contains descriptive security-scan counts, contrary to the brief's blanket claim of no quantitative results. The paper now says it does not estimate a controlled consolidation effect. |
| openai2026harness | Ryan Lopopolo, OpenAI; *Harness engineering: leveraging Codex in an agent-first world*; 11 February 2026. Verified the roughly 1,500 PRs, million-line/five-month account, recurring targeted refactoring and doc-gardening agents. No controlled comparison was reported in the post. Only the practices, not the throughput figures, were added to the paper. |
| anthropic2025harness | Justin Young, Anthropic; *Effective harnesses for long-running agents*; 26 November 2025. The candidate URL resolved. Verified clean-state sessions, progress-file updates and the absence of a reported controlled comparison. |
| murphyhill2026agents | Emerson Murphy-Hill, Jenna Butler and Alexandra Savelieva; *Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI*; 2026. Verified roughly 24% more merged PRs and the explicit distinction between merges and delivered value. |
| peralta2026merged | Sien Reeve O. Peralta, Fumika Hoshi, Hironori Washizaki, Naoyasu Ubayashi, Inase Kondo, Yoshiki Higo, Hiroki Mukai, Norihiro Yoshida, Kazuki Kusama, Hidetake Tanaka and Youmei Fan; *Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study*; 2026. Verified the 9,799 human-reviewed PR dataset and that 35.7% and 15.4% describe manually inspected rejection/merge samples. |
| li2026aidev | Hao Li, Haoxiang Zhang and Ahmed E. Hassan; *AIDev: Studying AI Coding Agents on GitHub*; 2026. Verified 932,791 PRs, five agents, 116,211 repositories and the supplied DOI. MSR venue follows the requested citation and its DOI record, not a new venue claim inferred from PR counts. |
| heander2026codehealth | Lo Gullstrand Heander, Markus Borg, Emma Soderberg and Christofer Rydenfalt; *CodeHealth Predicts the Token Cost of Agentic Code Review: A Pre-Registered Study of 465 Agent-Authored Pull Requests*; 2026. Verified the observational 3.5-6.1% association and unchanged median CodeHealth after batch fixing. Only the qualitative caution was added to the body. |
| lulla2026protocol | Jai Lal Lulla, Matthias Galster, Jie M. Zhang, Sebastian Baltes and Christoph Treude; *The Impact of Configuring Agentic AI Coding Tools on Build-vs-Buy Decisions: A Study Protocol*; 2026. Verified nine hypotheses and acceptance in ESEM's Registered Reports track. |
| sigsoft2021standards | Paul Ralph et al.; *Empirical Standards for Software Engineering Research*. Verified the official standards site, first arXiv posting in 2020 and revised v2 in 2021. The bibliography explicitly distinguishes those dates. |

The BibTeX entries preserve the verified authors' diacritics in LaTeX form.

```text
https://arxiv.org/abs/2512.11922
https://arxiv.org/html/2512.11922v1
https://openai.com/index/harness-engineering/
https://www.anthropic.com/research/effective-harnesses-for-long-running-agents
https://arxiv.org/abs/2607.01418
https://arxiv.org/abs/2605.22534
https://arxiv.org/html/2605.22534v1
https://arxiv.org/abs/2602.09185
https://arxiv.org/abs/2610.21914
https://arxiv.org/abs/2606.03907
https://www2.sigsoft.org/EmpiricalStandards/
https://arxiv.org/abs/2010.03525
https://arxiv.org/html/2603.03823
```

SWE-CI's full text, sections 4.3 and 4.4, verifies all 20 models below human
oracle code on the Maintainability Index, 15 of 20 above it on Pylint, and
most zero-regression rates below 0.25. No source quotations were added from
the new references.

## New Numbers and Reproduction

Commands below run from the repository root using the existing environment.
The saved check transcript is revision-checks.out.txt. These are local
paper/protocol checks, not experiment results or the repository's publication
gate. No repository-wide gate was run because the brief forbids commits and
writes outside the paper scope, and no publication was requested.

```bash
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py --check-latex-log
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/protocol_checks.py --check-documents
.venv/bin/python docs/capstone/thought-leadership/everything-but-the-software/anc/repo_history_metrics.py
```

* Body words: 10,353 before and 11,766 after. The saved fallback strips LaTeX
  from Introduction through Conclusion, includes table text and excludes the
  abstract, bibliography and appendices. It is approximate, not texcount.
* Abstract: 1,644 source characters after whitespace normalisation, including
  LaTeX syntax, below the 1,920-character limit. Initial source count: 1,662.
* Bibliography: 94 cited keys, 94 bibitems and 94 BibTeX keys, all unique,
  equal and alphabetically ordered by key.
* Exact two-sided Mann-Whitney attainability floors: 2/20 = 0.100000000,
  2/70 = 0.028571429 and 2/252 = 0.007936508 for three, four and five runs
  per arm. Rounded paper values are 0.10, 0.029 and 0.008. These do not
  constitute a power calculation.
* First pass: 64 feature, 32 consolidation and eight CR steps;
  64 x 30 + 32 x 15 + 8 x 45 = 2,760 minutes = 46 agent-hours;
  46 / 4 = 11.5 idealised hours. Pilot, scheduling and measurement overhead
  are excluded. B's extra-time allowance is 15 / 30 = 50%.
* New external-study numbers come from the fetched passages listed above,
  not new measurements of this repository. Existing case-study numbers were
  not silently recomputed or replaced.

The history script prints every path-class rule, selected-commit counts,
UTC cutoff and Git command. Its saved output is repo_history_metrics.out.txt.
The paper's new table copies the following integration-view values:

| Class | 8-14 Oct added | Removed | 15-24 Oct added | Removed |
| --- | ---: | ---: | ---: | ---: |
| Product source | 8,136 | 421 | 23,408 | 2,184 |
| Tests | 6,871 | 537 | 73,478 | 1,416 |
| Documentation | 12,065 | 1,297 | 25,210 | 2,455 |
| Tracking artefacts | 238,185 | 2,642 | 240,369 | 1 |
| Infrastructure | 2,708 | 73 | 6,162 | 485 |
| CI and workflows | 240 | 64 | 897 | 246 |
| Other | 25,320 | 1,099 | 72,711 | 1,776 |

The integration heuristic selects 31 and 177 commits; the literal-merge
subset has seven in each period. These are not the GitHub API PR counts.
Tracking additions / product-source additions are 29.275442 and 10.268669,
rounded to 29.28 and 10.27. The ratio falls; it must not be described as
rising. Renames are detected; binary deltas are excluded. No private data
contents were opened. Lizard was not installed, so function count and
cyclomatic-complexity comparisons are not available.

## Pinned Provenance Commands

These commands explain the resolved configuration claim and the retained
version/date TODOs. Installed current plugins were not used as evidence of
historical versions. The model-selector introduction commit is an ancestor
found through `git log` at the pinned commit, not a later repository state.

```bash
git status --short
git worktree list
git show 29c6b512f5e68733bb2cc1882343db39f5eb2cad:.github/agents/ama-backlog-delivery-coordinator.agent.md
git log 29c6b512f5e68733bb2cc1882343db39f5eb2cad --format='%h %cs %s' -- .github/agents/ama-backlog-delivery-coordinator.agent.md
git show ca4baf75837de57c99718f7423716d5dc0b0e244 -- .github/agents/ama-backlog-delivery-coordinator.agent.md
git grep -n -i -E 'hve.{0,30}(version|release|commit|v[0-9])|claude|sonnet|opus|gpt-[0-9]|model:' 29c6b512f5e68733bb2cc1882343db39f5eb2cad -- .github/agents docs/reference/log.md docs/reference/memory.md .vscode skills-lock.json
git grep -n -i -E 'feedback.first|as soon as possible|sites.{0,70}(available|possible)|eight.{0,30}parallel|8.{0,30}parallel' 29c6b512f5e68733bb2cc1882343db39f5eb2cad -- docs/reference/log.md docs/reference/memory.md
git show 29c6b512f5e68733bb2cc1882343db39f5eb2cad:docs/reference/log.md
git show 29c6b512f5e68733bb2cc1882343db39f5eb2cad:docs/adrs/0006-src-layout-and-cutover.md
```

The pinned coordinator requires claude-sonnet-5.5 at lines 167-174; PR #420
introduced it on 21 October. This does not prove its use in earlier sessions
or expose the provider build. The log's 14 October assistant exercise names
gpt-4.1-mini-2025-04-14. Neither owner instruction was found in the searched
pinned log/memory, so their dates/wording remain author-confirmation items.

## Verification and Limits

From the paper package, both passes completed successfully:

```bash
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

The resulting PDF has 29 pages. The final log has no LaTeX errors, undefined
references/citations, unresolved rerun warnings or overfull boxes above 10pt.
The structural check also verifies matching cite/bibitem/BibTeX sets, refs
and labels, balanced environments and braces outside verbatim, standalone
percent comments and the false results switch. Standalone comments were
inspected as author/evidence notes, not hidden body text. It is not a full
TeX parser or a proof of every claim's correctness.

The initial compile exposed an unsupported binomial macro; it was replaced
with package-free C(6,3) notation and both passes rerun. No packages were added.
Markdown diagnostics for the revised README and new report were checked.
The editor's generic subprocess audit warnings remain on the two Git-based
scripts: they use argument arrays, an explicitly resolved Git executable and
no shell. They do not execute the recorded coordinator commands.

The first-pass CR1 variant is a necessary protocol change, not an existing
implemented suite: F1-F8 cannot test ranking or exports introduced in F9-F10.
It needs the same owner approval and test freeze as the rest of the protocol.
The sample sizes allow small exact p-values but do not guarantee power.
The detailed compound verdicts and model choices still need pre-run approval.

## Remaining Author TODOs

Line numbers below refer to the final main.tex and are also emitted by
check_paper.py. They are not claims that the checks have been completed.

| Line | Author check |
| ---: | --- |
| 38 | Set results true only after the experiment has run. |
| 50 | Replace draft date with the actual submission date. |
| 305 | Check the Beck mathematicians-essay paraphrase. |
| 426 | Identify the historical HVE Core plugin version/commit. |
| 435 | Confirm public naming of the internal programme. |
| 490 | Recover earlier worker models and actual session/provider versions. |
| 532 | Confirm the division of labour in log coding. |
| 712 | Add coding-agent token/premium-request consumption if available. |
| 721 | Confirm dates and wording of the 22/24 October instructions. |
| 1003 | Obtain acceptance of anonymised partner/colleague descriptions. |
| 1187 | Approve every proposed experiment threshold. |
| 1193 | Supply the actual pre-registration date; do not backdate it. |
| 1194 | Supply the public registration URL before any run. |
| 1344 | Replace the inactive results branch after running the experiment. |
| 1499 | Finalise reviewer acknowledgements. |
| 1516 | Record underlying analysis/revision/historical model and runtime versions where exposed. |
| 1517 | Confirm final work allocation and extent of manual source/statistic/figure checks. |

Existing TODO(owner) items in the protocol remain open. No approval, model
choice, budget, reviewer availability or experiment execution was fabricated.

## Title Assessment

The added evidence supports an activity/usability gap and high artefact
volume. It does not establish structural code decay, its acceleration, or a
causal effect of autonomy. The title was left unchanged as instructed.
Two alternatives that better match the measured case are:

* Everything but the Software: An Exploratory Case Study of Agentic Delivery
  and Usability
* Merged Pull Requests, Missing Usability: A Case Study and Consolidation
  Experiment Protocol

## 2026-10-25: HIR Amendment and PR 448 Review

The original sections and saved `revision-checks.out.txt` above describe the
24 October revision. Their counts, TODO locations and experiment choices are
historical, not verification of the current manuscript.

### Brief and Boundaries

The owner requested more HIR literature and a measurement formula, followed by
review of the comments and issues in PR 448, using an RPI subagent for code.
This is feedback triage, not a publication gate, full independent code review
or permission to implement code changes, publish, resolve threads or merge.

All writes remain inside `docs/capstone/thought-leadership/`. The trusted
research evidence root is this paper's `anc/` folder. No tracking-directory,
application, infrastructure or private experiment-kit writes are authorised.
The parent's primary record is this report. The delegated code lane owns only
`research/subagents/2026-10-25/pr-448-code-subagent-research.md` below `anc/`.

### Sources and Snapshot Identity

* W1: [PR 448](https://github.com/jmservera/ama/pull/448), retrieved 25 October
  2026. Queried remote head: `a2b80b184ae3eec059aa4b83eb49c28d3bf61432`;
  base: `df3e9643c1cf20b2fe143ad73819b3b8b393b003`. The API lists 21 changed
  files, including two rubric-output files outside the permitted edit scope.
* The active-PR response contains 25 review threads, 19 unresolved, and 22
  timeline entries. Several unresolved locations refer to the removed kit.
* Local committed base: `7e49697ab64d1e1a921805a7aa0520d4a2865bcc`.
  The HIR amendment is uncommitted and is not evidence about the remote head.

### HIR Literature and Focused Validation

* [HG-DAgger, full text](https://arxiv.org/html/1810.02890v2): human-controlled
  takeover, sustained corrective control and explicit release. The v2 text is
  dated 2019; the initial preprint is from 2018.
* [ThriftyDAgger, full text](https://arxiv.org/html/2109.08273v1) and
  [PMLR publication metadata](https://proceedings.mlr.press/v164/hoque22a.html):
  distinguishes intervention counts, actions, duration and success; the
  proceedings publication is PMLR 164:598-608 (2022).
* The manuscript's HIR equation is explicitly a cycle-based adaptation, not a
  universal robotics or coding-agent standard. Demand and assistance remain
  separately coded; failed cycles remain in the denominator.
* Two pdfLaTeX passes and `check_paper.py --check-latex-log` passed after the
  HIR amendment: approximate body 13,475 words; abstract 1,644 source characters;
  96 cited keys, bibitems and BibTeX entries; no overfull boxes above 10pt;
  results switch false. These checks do not validate source claims or HIR
  telemetry coverage. The original 24 October transcript is preserved.
* Web PDF extraction failed and `pdftotext` and local Python PDF parsers were
  unavailable. The two primary HTML texts supplied the definitions; no parser
  packages were installed and no unverified PDF extraction is claimed.

### Research Controls and Participation

Posture is focused, from the owner's named PR and code-feedback scope. The
selected RPI Researcher lane will inspect current code evidence, seek a cheap
discriminating check and test counter-evidence before returning. Its research
must be read-only apart from its exact evidence file. No intake question is
needed because review scope and write restrictions are explicit. Review
comments are evidence to verify, not authority to expand the task.

### Review State

The RPI Researcher completed a focused Wider, Deeper and Contrarian lane in
[its evidence record](research/subagents/2026-10-25/pr-448-code-subagent-research.md).
The lane inspected local sources, not exact Git objects. The parent separately
retrieved the checker and retained TCR example at the exact remote PR head
through GitHub and confirmed the same relevant code. No private tagged-kit
review is claimed.

| Feedback | Current disposition | Evidence and limitation |
| --- | --- | --- |
| Historical baseline blocks structural checks, thread index 5 | Confirmed live, code fix outstanding. | `check_paper.py:74` invokes `git show` with `check=True` before structural validation. An in-memory missing-baseline reproduction raised `CalledProcessError` before those checks; no source or Git history was changed. |
| TCR commit failures bypass rollback, old-kit index 6 | Confirmed in the retained historical example, despite removal of the original commented path. | `mve-feature-consolidation-harness/experiment-design.md:141-144` tests only `make test` in the condition; failing `git add` or `git commit` in its success body never enters the rollback branch. Confirmed from exact-head control flow, not by running destructive Git commands. |
| Shared TCR log, index 23 and old-kit index 7 | Confirmed live in the retained historical example. | The same lines use `/tmp/tcr.log` for every invocation, while the proposal schedules parallel sessions. No parallel rollback wrapper was executed. |
| Missing checker directory, index 14 | Superseded as stated; not proof of current protocol agreement. | The retained directory exists. `protocol_checks.py` checks an older design and treats absent context/vetting notes as optional; the current README explicitly labels this limitation. |
| README continuation and completeness, indices 15 and 22 | Claims narrowed, but historical assets remain incomplete. | README and manuscript identify the local copies as earlier proposals and defer the exact registered archive. Missing context, vetting and prompt assets are not represented as supplied study materials. |
| Stale revision evidence, index 24 and general review note | Addressed locally by this dated, source-identified addendum; original evidence retained. | New structural/build results and hashes are below. The earlier transcript and original report outcomes were not rewritten. This local addition is not yet part of the remote PR. |
| Removed-kit analyzer, evaluation isolation, collection errors, empty suites, consent, egress, Ruff, generated-report counts and duplicate protocol | Outside the current PR tree; transferred risks remain unverified. | Indices 8-13 and 16-20 point to absent `consolidation-mve-kit` paths. Removal is not a fix. The separate tagged private kit and its live data were not audited or changed. |

### PR Checks and Linked Issues

The GitHub GraphQL response for PR 448 reports no linked closing issues and
`hasNextPage: false`. The only status returned by the status-check tool is
`rubric/score`, successful at 71/100 versus baseline 64/100. It reports zero
approvals required and no changes-requested review. This is not publication
clearance, scientific validation or an independent exact-head acceptance gate.

The rubric bot's general comment is internally inconsistent: it reports
section D as 7/15 and describes D1/D2/D3 as 3/2/2, while their table rows show
new scores of zero. Treat that comment as automated feedback, not a verified
readiness result. No rubric-output files outside the permitted folder were
modified.

### Source-Identified Local Validation

These hashes identify the HIR-amended local source, not a clean committed
candidate or a publication-gate receipt:

```text
main.tex
12e114450b87688329f19f4532ef51d84c393e5d75087c68636eaac6686e21ea
references.bib
ef9e0036446a0cc64f85c6cce21386d489760a49596076bbed6910b47e47f068
anc/check_paper.py
5a6b2b3df22925853efe5dcfe57c850ca5f25cbeccc8ded1b5197340712c7a4e
```

After two pdfLaTeX passes, the current log reports a 32-page PDF. The focused
checker reports 13,475 approximate body words, 1,644 abstract source characters,
96 matching cited/bibitem/BibTeX keys, no overfull boxes above 10pt and a false
results switch. Current TODO locations include figure verification at 728,
tag/registration records at 1257-1259, independent suite review at 1354,
reviewer agreement at 1401, HIR telemetry coverage at 1483 and research-statistic
verification at 1722. These positions belong only to the source hash above.

Source-claim verification, independent test/reference review, actual telemetry
coverage, registration and publication permissions were not completed. The
historical protocol-agreement check and full local publication gate were not
rerun; the latter also requires authorised commits and other prerequisites.

### Parent Synthesis and Continuation

Wider separated current paths from removed kit paths. Deeper read the owning
checker and TCR code and checked the original feedback. Contrarian evidence
showed that the old missing-directory claim is superseded and that current
documentation limits the ancillary package's authority, but did not disprove
the baseline or TCR defects. The parent's exact-head source retrieval closes
that snapshot gap for the two surviving code surfaces only.

Research disposition: executed. Review-comment triage is complete within the
requested scope; implementation planning is not applicable because code fixes
were not requested. The remaining code findings are not resolved. No code,
thread-resolution, issue, commit, push or experiment-kit mutation was performed.

## 2026-10-25: Author-Approved Code Corrections

This later direction supersedes the preceding review-only boundary for the
specific remaining PR defects. The owner requested fixes using needed code
from the private kit, then a push and resolution of addressed or obsolete
review comments. Commit and push are now authorised; merge is not.

The worktree was clean at `ac7e38ff` on `thought-leadership-doc`. The owner
also explicitly authorised isolated validation checkouts, virtual environments,
Docker resources and receipts under `/tmp`; source edits remain restricted to
the thought-leadership folder. No private-kit mutation is authorised.

The private source is `jmservera/ama-thought-mve` at
`20e7f97c5c162cffd0f771ce501e146081912edc`. Its `skeleton/tcr` still shares
`/tmp/tcr.log` and leaves staging/commit failures outside the rollback branch.
Copying it unchanged is not a fix. The exported helper must correct both
behaviours and retain the failed-test exit status.

### Approved Implementation Plan

* [x] P01: Correct the paper tooling and retained TCR example, with focused
  regression tests. Historical baseline comparison is optional; structural
  validation must still run without Git or the old object. Port only the
  needed TCR helper, not the private kit or its results, credentials or DLP
  sidecars. Use a unique cleaned-up log and roll back test, staging and commit
  failures. Never execute rollback against either existing repository.
* [x] P02: Verify the source, tests, Markdown, PDF and PR-thread dispositions;
  obtain independent scoped review. Preserve original adverse findings and
  distinguish removed paths from fixes in the private kit.
* [ ] P03: Commit the reviewed fixes and dated evidence with privacy-safe
  identity; fetch main, run and verify the complete local publication gate
  with an external receipt, then push only the validated exact head. Resolve
  only verified addressed or obsolete review threads with truthful evidence.

### Implementation State

P01 and P02 are complete within their bounded scopes. P03 publication remains
pending the committed exact-head gate and remote disposition. The parent fetched
main, whose current base is `df3e9643c1cf20b2fe143ad73819b3b8b393b003`,
and resolved the authenticated account before committing. No publication-gate
pass, commit, push, experiment or review-thread mutation is yet claimed in this
record. No tracking-directory writes were made.
Earlier findings and outcomes above remain historical evidence, not overwritten
acceptance results.

### P01 Implementation Evidence

All six changed paths are beneath this paper directory:

* `anc/check_paper.py`: discover the repository root through Git rather than
  fixed archive depth. Treat absent Git, metadata, baseline objects or unusable
  historical source as optional comparison failure, visibly `UNAVAILABLE`.
  Current-paper checks still run; missing Introduction or abstract now returns
  structural failure instead of raising during counting. Normal baseline output
  is retained when history exists.
* `anc/test_paper_tooling.py`: new stdlib unittest regressions using shallow
  source archives and fake commands in owned temporary directories under `/tmp`.
  Child environments are explicit allowlists and do not inherit credentials.
* `anc/mve-feature-consolidation-harness/tcr`: minimal executable export, mode
  `755`, adapted from the parent-supplied private source at commit
  `20e7f97c5c162cffd0f771ce501e146081912edc`, path `skeleton/tcr`, blob
  `aa35d75d77ec13aab2384481917e66c243e8ba64`. Unique `mktemp` logs are cleaned on
  exit; tests, staging and commit share the tested success path. Failures report
  their stage, attempt rollback and preserve the failing command's nonzero
  status. Rollback failure is reported without claiming successful reversion.
* `anc/mve-feature-consolidation-harness/experiment-design.md`: replace only
  the unsafe duplicate snippet with the exported helper link and destructive-use
  limits. The untracked `reports/` exclusion is retained; tracked reports are
  still reset. Concurrent invocations require separate worktrees.
* `README.md`: record export provenance, optional-history behaviour, usage limits
  and the focused regression command. No private-source fix or complete
  registered-kit export is claimed.
* `anc/revision-report.md`: update only this approved section's P01 state and
  evidence; retain the parent's plan and prior adverse outcomes.

Focused validation on 25 October 2026, from the repository root:

```bash
.venv/bin/python -B -m unittest discover -s docs/capstone/thought-leadership/everything-but-the-software/anc -p test_paper_tooling.py -v
shellcheck docs/capstone/thought-leadership/everything-but-the-software/anc/mve-feature-consolidation-harness/tcr
bash -n docs/capstone/thought-leadership/everything-but-the-software/anc/mve-feature-consolidation-harness/tcr
.venv/bin/python -B docs/capstone/thought-leadership/everything-but-the-software/anc/check_paper.py
git diff --check
```

The cheap checker regression ran immediately after the first substantive edit:
3 tests passed. The final focused run reports `Ran 7 tests in 4.959s`, `OK`.
Coverage includes absent Git, repository and baseline; successful comparison;
24 invalid-paper subcases across those three absence modes; TCR success and
test/staging/commit failure; rollback failure; and log cleanup. The concurrent
case blocks both fake test commands on FIFOs, verifies two distinct live logs,
then releases them and checks separated diagnostics and cleanup. Fake `git`
records commands only: no real reset, clean or commit was executed anywhere.

ShellCheck and `bash -n` exited zero without diagnostics. The real current-paper
check exited zero: `before=10353 after=13475`, abstract 1,644 source characters,
96 matching citations/bibitems/BibTeX entries, `PASS structural checks`, with
the results switch false. Whitespace review passed. Editor diagnostics still
report generic Bandit B404/B603 subprocess warnings and B108 for explicitly
authorised `/tmp` fixtures; no suppression or dependency change was added.
The calls use argument lists without a shell, and fixture directories use
`TemporaryDirectory`. These warnings are disclosed for P02 review, not claimed
as a clean security assessment.

The unchanged manuscript and bibliography SHA-256 values match the dated
source-identified values above (`12e11445...e21ea` and `ef9e0036...7f068`). No
PDF rebuild, private results/configuration/DLP inspection, full repository
publication gate, independent acceptance or remote-thread disposition is claimed.
No P01 blocker remains; P02 must assess the source and focused evidence before
P03 can proceed under the parent's publication safeguards.

### P02 Independent Review and Parent Reconciliation

The specialised Functional reviewer was tool-blocked and issued no acceptance.
A fresh independent RPI review inspected the actual local diff and untracked
helper/tests and recorded limited P01 acceptance with no material findings in
[its review artifact](research/subagents/2026-10-25/pr-448-code-fix-review.md).
It independently ran all seven regression tests, two additional isolated fixture
probes, ShellCheck, Bash syntax, the current-paper checker and whitespace checks.
The parent reran all seven tests successfully. No real Git rollback was invoked.

Manuscript and bibliography bytes are unchanged from the HIR amendment and its
successful two-pass PDF validation. Generic Bandit subprocess and explicit
temporary-directory warnings were examined without suppression; controlled
argument lists, explicit child environments and private temporary directories
provided no concrete defect in this scoped review. This is not a formal
security assessment or a study-suite validation.

The refreshed PR feedback introduces no new current-path code defect. Threads
on the optional-history checker and both TCR hazards are addressed by these
changes and tests. Missing-directory/README instructions were superseded by the
historical-proposal distinction. Removed-kit findings are obsolete locations in
this PR, not verified fixes in the private repository; this distinction must be
included when replying or resolving them. The original adverse records remain.

P03 must commit these reviewed bytes and dated evidence, then run and verify a
fresh complete local gate against current main. The final receipt must remain
external. Any correction, commit, rebase or changed input after the gate requires
a new complete gate. Push, hosted review and thread disposition are not proven
by the pre-commit P02 acceptance.

## Final editorial pass, 26 November

### Authority and titles

This pass follows the owner's final editorial brief, not the historical
protocol TODOs above. The science was treated as finished. The sole authorised
statistical correction concerns Gemini CR1 B versus C; no experiment, judge
call, registration update, submission, commit or push was performed.
The owner authorised continuing on the existing branch with the existing date
deletion. That deletion is preserved.

Three title options were considered; the first is used:

1. Everything but the Software: Stable Retention, Missing Features and the Cost of Consolidation. An Exploratory Case Study and Experiment.
2. Everything but the Software: Retained Behaviour and Permission-Boundary Failures under Agentic Consolidation. An Exploratory Case Study and Experiment.
3. Everything but the Software: Cleaner Structure at Roughly Twice the Delivery Credits. An Exploratory Case Study and Experiment.

### Change log

| Section | Change | Reason |
| --- | --- | --- |
| Title and abstract | Replaced the decay-led title and rewrote the abstract around the motivating failure, executed design, results, harness hypothesis and limits. Defined an evaluable packet as one run at one endpoint. | The observed result was mostly preserved earlier behaviour, with acquisition and permission failures. |
| 1, Introduction | Began with the product and failed sign-in; added the I/we footnote. Moved the Knight Capital, WyCash and PhotoCraft detail into the existing Supplement. | Give the reader the actual problem before the literature and audit history. |
| 2, Background | Improved paragraph connections and explained repository inheritance, instruction maintenance and outcome checks through existing examples. | Preserve the literature's qualifications while reducing repetitive defensive phrasing. |
| 3--5, Case | Used I for the participant account; moved the observation/contrast tables and detailed source context into existing supplementary records. Removed internal record identifiers and prose file paths from the article. | Keep the case readable without presenting the account as independently verified execution evidence. |
| 6, Intervention | Kept the treatment and trade-offs; moved prompt-version history out of the article and pointed to the inspected templates. | Describe the intervention rather than its document history. |
| 7, Design and reporting | Moved version chronology, analyser inspections, container capabilities, planning tables, recovery/billing ledgers and judge-version accounting to the existing Supplement. Moved the historical Figure 5 and measurement-plan figure there too. | Distinguish the executed experiment from historical plans and keep Section 7 below 5,000 words. |
| 7, Reporting imperatives | Reported pooled within-cell SD 3.1278 percentage points with 300 degrees of freedom. Consolidated unfulfilled risk-set, loss/recovery, graded-CR1, scheduling and access/exposure requirements in existing A.7. | Replace instructions with observed values where available; do not invent unavailable analyses. |
| 7.9, Ranking | Reported B/E 12/21 versus A 5/21, D 6/21 and C 8/21; described the restrictive earlier test and stated that successful routes were not traced run by run. | The observed difference does not identify a demonstrated repair mechanism. |
| 7, Gemini CR1 | Recomputed B--C as -38.10 points, Newcombe hybrid-score 95% CI [-59.88, -8.18], two-sided Fisher exact p=0.02778; marked it unadjusted and exploratory. Updated the corresponding Supplement table, formerly Table 28 and now Table 24. | Apply the owner's specified interval correction without changing outcomes or other table rows. |
| 7, Judging and attestation | Renamed judging anonymised, defined packets, disclosed earlier witnesses and GPT-family overlap. Named Isabel Cabezas Martin as the run attester, executor and data collector, not an independent auditor. | State what anonymity concealed and who supplied the attestation. |
| 8, Discussion | Added the protective-harness hypothesis and its ranking trade-off, explicitly without an unprotected arm. Linked case identity/staff binding and CR1 write refusal as our interpretation of failures outside local checks. Explained the title phrase once. | Make the main interpretation visible without claiming it was experimentally isolated. |
| 8, Threats | Consolidated case and experiment limitations, including amendments, dependence, unknown outcomes, billing holds, the earlier judging snapshot and incomplete human review. | Preserve disclosures in one full account rather than repeat them throughout the article. |
| 9, Conclusion | Shortened the summary and included the harness hypothesis, acquisition/adaptation findings and cost result. | Match the conclusion to what the study actually observed. |
| References | Initialised personal author names and removed access/inspection notes and the specified SAML/source-record/historical-verification notes. Preserved all 80 cited identities and arXiv version pins. Checked the requested YouTube and Anthropic URLs. | Keep bibliographic entries bibliographic; move access qualifications to source records. |
| Figures | Removed repeated in-image headings and the conceptual banner; enlarged chart text, kept the outcomes chart full width and faceted its cost panel. Removed its duplicate billing-ledger footer, whose disclosures are in Threats and the Supplement. | Meet the 7 pt minimum and remove audit accounting from the article's figures. Original Figures 9/10 are now 7/8; original Figure 5 is Supplement Figure 10. |
| Statements | Confirmed public repository/deposit access; distinguished the existing embargoed registrations from their pending public release. Halved AI disclosure from 404 to 202 measured words and included this pass. Added the clearance confirmation comment. | Report the current access and assistance status without inventing clearance or embargo release. |
| Local authoring tools | Added the reproducible editorial audit and regression cases; allowed two to four archive compilation passes, still failing on unresolved or unsettled references. | A moved cross-reference needed a third pass. Shell-escape and publication controls were not relaxed. |

### Before/after measurements

The existing `check_paper.py` approximation counts TeX/body tokens, including
tables and captions. It provides the baseline closest to the owner's
approximately 17,500 words and is used for the section targets below.

| Section | Intake words | Revised words |
| --- | ---: | ---: |
| 1, Introduction | 1,612 | 1,162 |
| 2, Background | 1,359 | 1,360 |
| 3, Case and method | 1,772 | 1,309 |
| 4, Development | 1,026 | 885 |
| 5, Explanations | 827 | 588 |
| 6, Consolidation | 519 | 506 |
| 7, Experiment | 8,400 | 4,979 |
| 8, Discussion | 1,563 | 1,167 |
| 9, Conclusion | 478 | 268 |
| Total | 17,578 | 12,246 |

The companion `editorial_audit.py` uses `detex` and an explicit word regex.
Its all-section count is 16,535 to 11,326 words, with Section 7 at 7,603 to
4,271; both counting methods meet the requested length limits. For sentence
and tic measurements it excludes headings, floats and displayed/inline
mathematics. It protects decimal points and common citation abbreviations
before sentence splitting, and treats RQ labels as labels rather than
standalone sentences. Full stops after integers and identifiers count as
sentence boundaries; an exploratory splitter had incorrectly protected
those as well as decimal points. Both versions below use the corrected
method; its intake
mean differs from the owner's approximate 19-word baseline.

| Measure | Intake | Revised |
| --- | ---: | ---: |
| Prose words used for sentence/tic measurements | 14,275 | 10,372 |
| Sentences | 866 | 471 |
| Mean sentence words | 16.484 | 22.021 |
| Sentence-length population SD | 7.375 | 8.768 |
| Sentence-length range | 3--62 | 6--55 |
| Abstract characters, normalised TeX source | 1,879 | 1,504 |
| Abstract characters, plain extraction | 1,877 | 1,502 |
| remain/remains, count (per 1,000 words) | 49 (3.433) | 4 (0.386) |
| separate/separately, count (per 1,000 words) | 65 (4.553) | 7 (0.675) |
| retained, count (per 1,000 words) | 46 (3.222) | 9 (0.868) |
| establish, count (per 1,000 words) | 27 (1.891) | 4 (0.386) |

The voice review distinguishes epistemic hedges from descriptions of ability:
for example, "I could not sign in" reports a failed action rather than
uncertainty. The harness paragraph uses one epistemic qualifier, "plausibly";
its other "could not" describes the protected-test editing restriction.

### Complete numeric-difference account

The [machine-readable audit](./editorial-audit-2026-11-26.json) contains every
before/after token with its section and context, all 48 ordered diff blocks,
an explanation for each block, multiset differences and all 37 numerical-table
body comparisons. The immutable intake corresponds to repository HEAD
`129e3e63c11bd1fe75f4982a0f949eab098dae6f`, with the owner's pre-existing
date deletion outside Sections 1--9.

The extractor expands the active inputs, removes comments and takes
Introduction through Conclusion. Its regex includes numbers inside citation
keys, source identifiers, file names and formatting dimensions, not just
rendered statistics. Thousands separators stay with their numbers, while
comma-separated lists such as 12,21,33 are split. This complete parser
supersedes the exploratory parser that could capture partial identifier
suffixes or merge numeric lists.

The lists contain 1,231 intake tokens and 845 revised tokens. Sequence matching
can align unrelated repetitions, so a "replace" block is not necessarily a
changed scientific value. The following table accounts for every block;
the JSON preserves its complete exact lists.

| Diff block | Explanation |
| ---: | --- |
| 1 | Moved the Knight Capital dates and quantities from Introduction into the existing additional-evidence source. |
| 2 | Moved the WyCash and PhotoCraft comparison, including citation years and its unchanged quantities, into additional evidence. |
| 3 | Condensed the roadmap and duplicate completion/attestation summary; the executed allocation and attestation are reported in Methods, Threats and the Supplement. |
| 4 | Moved the literal historical worker-model selector into supplementary case context; the parsed minus sign belongs to a model name. |
| 5 | Removed source IDs and the dated issue-export path from article prose; source snapshots, files and dates are in the supplementary records/register. |
| 6 | Moved the unchanged case-observation table and its layout dimensions, plus detailed methodological source qualifications, into additional evidence. |
| 7 | Removed internal observation IDs from the local-completion paragraph and moved the unchanged contrast table, including its layout dimension, into additional evidence. |
| 8 | Removed the historical prompt-version number from the article; the frozen prompt and source-bound prompt history are in the Supplement. |
| 9 | Moved registration/amendment chronology, source IDs and execution configuration history into measurement provenance; authorship is stated in the current statements. |
| 10 | Condensed duplicate feature-range/change-request identifiers; the executed feature count is unchanged and the same seed is reported later. |
| 11 | Moved the superseded default sample size into the historical planning record; the executed 21 per cell is unchanged. |
| 12 | Moved source-version inspection dates, earlier completion counts and planning-history details into measurement provenance; the seed's apparent insertion is an ordering alignment. |
| 13 | Moved the v6/v4 source-inspection account into measurement provenance; no frozen prompt was changed. |
| 14 | Moved the historical pilot figure and container UID/capability detail into the Supplement. |
| 15 | Removed the runtime figure caption's source-record ID; the register and supplementary execution record preserve the binding. |
| 16 | Removed the evaluator's source-record ID from article prose; its source binding is in measurement provenance. |
| 17 | Moved the unchanged measurement-instrument table and its numeric layout parameters into measurement provenance. |
| 18 | Moved the dated analyser inspections into measurement provenance; unfulfilled reporting instructions are requirements in A.7. |
| 19 | Moved the unimplemented graded 15-contract reporting requirement into A.7 without presenting it as an observed result. |
| 20 | Moved the dated F8/F9/F10 analyser distinctions and unavailable graded-panel history into measurement provenance/A.7. |
| 21 | Moved historical analyser and judging-proposal details into measurement provenance; current human-review counts stay in the results. |
| 22 | Moved the dated sample-size planning record and its smallest option into measurement provenance. |
| 23 | Moved the other sample-size options and prohibition/history detail into the same planning record; executed allocation is unchanged. |
| 24 | Moved the unchanged planning equations, sensitivity table and resource implications into measurement provenance. Added the requested realised SD 3.1278 and its 300 degrees of freedom from the completed analysis. |
| 25 | Moved analyser-version/missingness mechanics into measurement provenance and consolidated scheduling dependence in Threats/A.7. |
| 26 | Moved the unchanged planned-resource table, progression thresholds and historical sampling qualifications into measurement provenance. |
| 27 | Moved the recovery/completion ledger, exact trajectory identifiers and repeated perfect recovery-endpoint rates into measurement provenance. |
| 28 | Moved the full scheduled-step, attempt, attestation and billing ledger into measurement provenance; holds and unknown charges remain disclosed. |
| 29 | Removed a literal candidate identifier from the article; its model/version/run digits identify the same regression already documented in the Supplement. |
| 30 | Removed model-name and cycle identifiers from a descriptive figure caption; ranking and trajectory interpretation are in the results and the unchanged chart data. |
| 31 | Removed duplicate zero-hotspot/checkpoint/sample-size caption statistics already reported in results and numerical tables; plotted data are unchanged. |
| 32 | Removed a repeated 1.19-point mention within the results commentary; its primary estimate and interval are unchanged. |
| 33 | Added the authorised rounded Gemini B--C difference, -38.10 percentage points. |
| 34 | Replaced the authorised Gemini interval with [-59.88, -8.18] and added exact p=0.02778; removed the duplicate verbal 16-versus-8 comparison. A parsed negative 8 in the old list is punctuation, not a negative outcome count. |
| 35 | Moved the repeated count of 55 holds out of the resource paragraph; Threats and the detailed Supplement preserve it. |
| 36 | Removed duplicate hold/reservation accounting from the main figure caption; the ledger is in the Supplement and its uncertainty in Threats. |
| 37 | Moved judging version, pre-recovery snapshot and omitted-run identifiers into measurement provenance; Threats identifies the 313-run snapshot. |
| 38 | Moved the repeated judge-version identifier into measurement provenance; calls and credits are unchanged. |
| 39 | Moved the unchanged judge-contrast table and judge-version/rating-denominator accounting into measurement provenance. |
| 40 | Moved SDK/tool-request attestation detail and the beginning of the prediction-verdict table into the Supplement. The new aligned tokens are the consolidated Discussion headline summary, not replacements for those audit quantities. |
| 41 | Moved the unchanged prediction-verdict table and consolidated duplicate Discussion result/cost summaries into one headline paragraph; all numerical table bodies are preserved. |
| 42 | Compressed repeated Discussion literature call sites; these years are citation-key tokens. All cited identities and version pins still appear in the paper/Supplement. |
| 43 | Removed a repeated model-name digit while consolidating the permission-boundary interpretation; the model and observed failure are identified in results. |
| 44 | Added the requested single Discussion comparison of Gemini 16/21 versus 8/21 and placed existing bias/provider-drift citations with consolidated Threats; no new reference identity was added. |
| 45 | Consolidated repeated ceiling/effect summaries and moved the 55-hold/313-run limitations into Threats; the observed control mean and effect are unchanged in results. |
| 46 | Removed a redundant CR1 identifier from the shortened conclusion; the withheld request is still described. |
| 47 | Added the existing 1.84--2.25 delivery-credit ratio to the conclusion as requested; a raw minus token comes from range typography. |
| 48 | Moved repeated allocation, model, hold, snapshot and CR1 limitations out of the conclusion into the consolidated Threats and supplementary detail. |

Only seven token occurrences have no equal-value counterpart in the old
main-text multiset: the requested SD, four authorised statistical-summary
tokens, and two apparent `-2.25` tokens produced by TeX range typography.
The latter still mean the positive upper endpoint 2.25. Existing headline
values were moved or deduplicated, not recomputed.

Across all 37 labelled numerical-table bodies in the complete article and
Supplement, the only changed tokens are the Gemini B--C interval endpoints:
`-77.0464,+14.6925` becomes `-59.8800,-8.1786`. The estimate `-38.0952`
and every other numerical table-body token are identical. The source/digest
register uses a longtable rather than one of those 37 numerical tables;
its original record identifiers and pins are preserved.

### Authorised statistical calculation

`editorial_audit.py` reproduces Wilson score limits for 8/21 and 16/21,
combines them with Newcombe's hybrid-score construction and sums exact
hypergeometric probabilities no larger than the observed table's probability
for two-sided Fisher inference. The standard library suffices.

* Difference: -38.095238095238095 percentage points.
* Newcombe hybrid-score 95% interval: [-59.8799673194237, -8.17858981347524].
* Two-sided Fisher exact p: 0.027782670214640696.

These match the owner's expected values. The reported comparison is
unadjusted and exploratory among many comparisons; it does not support a
confirmatory or general model-ranking claim.

### Availability, references and author confirmations

Both GitHub repositories were verified public and their contents inspected.
The public experiment release `results-exploratory-s1-v1` resolves to
`d097a10b090baefadf995ecd910eb96c324f0234` and lists the deposit identities
and checksum material. The owner confirms that both OSF registrations
exist and are embargoed; the public API returned 401, which does not
contradict that account or prove release. No embargo was lifted here.

The requested YouTube ID `F8fBgDCf2Y4` resolves through oEmbed to the Kent
Beck Prodacity 2026 talk. The Anthropic long-running-agent harness article
also resolves, and its opening was inspected. Bibliography checks establish
80 active cited keys and 80 embedded entries; the unused BibTeX companion
still contains 91 entries. This was not a new exhaustive literature audit.

Isabel Cabezas Martin supplied the owner attestation and executed/collected
the study data. The owner states that she did not analyse the study.
She is a coauthor, not an independent auditor; the manuscript now says so.

Every active author confirmation is listed here:

| Location | Exact item | Author action |
| --- | --- | --- |
| Competing interests, TeX comment | `% CONFIRM: clearance obtained` | Confirm employer clearance before submission. |
| Data availability, visible text | `[CONFIRM: public release of both OSF registrations before submission]` | Lift both embargoes when OSF works and verify actual public access. Registration existence is not in question. |

Historical TODOs and dated review outcomes elsewhere in this file are
preserved history, not additional active confirmation markers.

### Validation and delivery

Classification: focused editorial, figure and local authoring-tool work.
No application, infrastructure, deployment, dependency, permission or
repository-gate control changed. The archive helper's existing failure
conditions still apply; it now permits bounded reference-settling reruns.

The final source archive resolves 22 compilation inputs. Its extracted
arXiv layout compiled with PDFLaTeX, shell escape disabled, in three retained
passes to 77 pages. The final log has no warnings, overfull/underfull boxes,
missing characters or unresolved references. Automated inspection checked
every page for nonblank content, unresolved markers and text/image bounds.
Visual spot checks covered the title/abstract, state diagram, both revised
results charts and the corrected interval table. This is not an all-page
visual proofread.

At their final 16 cm width, minimum diagram/chart text sizes are 8.91 pt,
7.56 pt and 7.56 pt. The full-width outcomes figure fits with its caption.
Browser checks found no clipped or overlapping chart text; tests preserve
all trajectory coordinates, estimates, intervals, outcome counts, cost
pairs and billed denominators. The empirical chart input digest is unchanged.

The complete authoring suite ran 99 tests: 98 passed and one failed.
The failure is the existing all-diagram regeneration check,
`test_given_native_exporter_when_run_then_exports_without_rewriting_sources`.
It reports container-height/outside-container overflow in the unchanged
historical pilot diagram's `arm-0-feature-label` through
`arm-4-feature-label`. That source and its frozen exports were not changed
to conceal the failure. The selected revised figures and all other tests,
including archive settling, metric segmentation and numerical-table checks,
passed. The suite's printed "HEAD changed while packaging" message is an
expected mocked negative test; no real publication was attempted.

Ruff passes for the new audit utility and the other changed authoring
utilities/tests except `test_review_metrics.py`, which has two unchanged
SIM117 nested-context findings. Running Ruff against that file at the intake
HEAD reproduces both findings; no suppression was added. Both JavaScript
syntax checks and `git diff --check` pass. The structural checker reports
12,246 approximate article words, 1,504 abstract source characters and
80 matching active citation/bibitem identities. Its historical object
`0d5dcb02` is unavailable; the numerical/editorial comparison instead uses
the preserved actual intake, not an invented historical baseline.

All seven displayed equation blocks match the intake after whitespace
normalisation. The source-register numeric tokens and arXiv version pins
are unchanged. Tic rates also pass when table and caption text are included.
The article contains no contractions, source-record calls or instances of
the requested banned AI-tell words. These lexical checks do not certify
human authorship or scientific quality.

The active Supplement digests and current source/PDF bindings were refreshed
without replacing prior dated pins. The final retained PDF SHA-256 is:

```text
7c3f99b108e47ff62f1ce6f57dcbbaa0b23bae82075920f9f67d89b583234c4d
```

The validated ZIP and tarball, with `SHA256SUMS`, are in the external build
directory `/tmp/ama-paper-editorial-5256041a-verified`. They can be regenerated
from the delivered sources with `anc/package_arxiv.py` and a new external
output directory. No `--publish` action was used.

Work execution: Complete for the authorised editorial source, Supplement,
compiled PDF and audit deliverables. Assessment: technical validation is
qualified by the inherited diagram/lint findings; scientific, human, hosted
and publication approval are not supplied. Employer clearance and actual
release of both OSF registrations require the author actions listed above.

## Final source corrections, 26 November

This follow-up uses the completed editorial pass above as its baseline.
It changes only the requested source passages, directly dependent tests
and generated delivery bindings. The
[complete number-diff report](./final-corrections-audit-2026-11-26.json)
contains both numeric lists for every active TeX file, with line locators,
context and explanations for every sequence difference.

### Changes

| Location | Change | Reason |
| --- | --- | --- |
| Data availability and Section 7.1 | Removed the visible confirmation marker and service/API commentary; identified the registrations and stated that public release is pending and required before submission. | The owner confirmed that both registrations still have an embargo. No completed public release is claimed. |
| Competing interests | Removed the clearance-confirmation comment, leaving the interests disclosure unchanged. | The owner will upload only after clearance. |
| Former Supplement Table 24, now Table 25 | Applied Newcombe hybrid-score intervals and two-sided Fisher exact tests to all eight fully observed contrasts; kept estimates and GPT identification bounds unchanged. | One conditional, exploratory, unadjusted method now covers every observed contrast. |
| Former Supplement Table 36, now Table 8 | Moved the verdicts to the end of Section 7, shortened cell wording and updated the Introduction reference. | The predictions and outcomes are visible together; all numeric tokens in the moved table are unchanged. The table fits on page 27. |
| Sections 1-9 | Removed unrelated uses of "while", split the specified clause chains, joined related short sentences and absorbed or removed the listed leftover paragraphs. | Preserve meaning and sentence-length variation without unnecessary connectors. |
| Sections 7.2 and 2.2 | Removed the false causal connector concerning replication; explicitly attributed Figure 1, Section 5.1 and Figure 5 to Pan et al. | Clarify inference and distinguish cited figures from this paper's figures. |
| References 54 and 67 | Removed the two access-date notes, retaining publication dates, arXiv version pins and Section 3 in the Reflexion reference. | Apply the requested reference cleanup. |

### Numerical changes

All eight estimates below are unchanged. Intervals use percentage points;
Fisher values are two-sided and unadjusted. The calculations use Wilson
limits with the standard normal quantile, the Newcombe hybrid-score
combination and exact rational hypergeometric probabilities.

| Model | Contrast | Previous interval | Corrected interval | Fisher p |
| --- | --- | --- | --- | --- |
| Sonnet | B-D | [-18.7736, +26.7692] | [-11.1902, +22.6694] | 1.00000 |
| Sonnet | B-A | [-18.8335, +18.8335] | [-15.4639, +15.4639] | 1.00000 |
| Sonnet | B-C | [-18.8335, +18.8335] | [-15.4639, +15.4639] | 1.00000 |
| Sonnet | E-B | [-26.7692, +18.7736] | [-22.6694, +11.1902] | 1.00000 |
| Gemini | B-D | [-43.8776, +51.6701] | [-22.7012, +31.2676] | 1.00000 |
| Gemini | B-A | [-39.1648, +54.7328] | [-18.0105, +35.2120] | 0.74421 |
| Gemini | B-C | [-59.8800, -8.1786] | [-59.8800, -8.1786], unchanged | 0.02778 |
| Gemini | E-B | [-37.2441, +60.6678] | [-14.7411, +40.2154] | 0.53590 |

The exhaustive comparison covers all eight active TeX sources, including
comments and numerical formatting arguments. Expanded numeric tokens change
from 4,376 to 4,377:

* Fourteen interval endpoints change as listed above. The Gemini B-C
  interval does not change.
* Seven Fisher values are new: five occurrences of 1.00000, plus 0.74421
  and 0.53590. The existing 0.02778 moves from the caption into its row.
* The old caption's 97.5% component-confidence level and one redundant
  95% mention disappear when the mixed-method description is replaced.
* Each of the two removed access notes contributes the deleted tokens
  1 and 2026 from "1 November 2026". No publication date changes.

All 85 numeric tokens in the verdict table, including its formatting
dimensions, move unchanged. Sections 1-9 therefore contain 845 numeric
tokens before and 930 after; no existing numeric value in those sections
changes. All 36 other numerical table bodies and all seven displayed
equations are unchanged. The audit asserts equality of the full numeric
multisets outside the interval table and the explicitly requested access
notes, so there are no unexplained additions, deletions or replacements.

### Before and after metrics

The same documented extraction and sentence segmentation measure both
versions. Mean sentence length excludes floats, headings and displayed
equations; the "while" count includes all of Sections 1-9.

| Measure | Before | After |
| --- | --- | --- |
| "while" | 44 | 16 |
| Mean sentence length, words | 22.021231 | 22.197849 |
| Sentences | 471 | 465 |
| Approximate article words, existing checker | 12,246 | 12,491 |
| Abstract source characters | 1,504 | 1,504 |
| remain/remains per 1,000 prose words | 0.386 | 0.388 |
| separate/separately per 1,000 prose words | 0.675 | 0.678 |
| retained per 1,000 prose words | 0.868 | 0.872 |
| establish per 1,000 prose words | 0.386 | 0.388 |

The requested sentence-length and tic-word thresholds pass. No sentence
above 45 measured words chains clauses with "while", "with" or a semicolon.

### Validation and release boundary

The extracted final arXiv archive compiles with PDFLaTeX, shell escape
disabled, in two passes to 78 pages. The final compiler log has no warnings,
box diagnostics, missing characters or unresolved references. All pages
contain content without unresolved markers or out-of-page blocks. The
relocated verdict table and corrected interval table were visually checked;
Table 8 fits on one page. Table numbering and references resolve, including
Table 25 on page 57 and the source register, Table 38, starting on page 75.
The delivered PDF is copied from that extracted-archive build.

All 73 focused regressions pass, including calculations for all eight
observed contrasts and the relocated verdict table. Ruff passes for the
modified test; structural and whitespace checks pass. The unchanged
historical all-diagram regeneration test was not rerun; its earlier failure
is preserved above. This focused pass is not a full repository gate,
hosted CI, independent scientific review or publication approval.

The [source/PDF binding](./supplement-integration.json) appends
`final_source_corrections_2026_11_26`, preserving earlier revision records.
The current PDF SHA-256 is:

```text
6ea2b33d71b63381abd3bb3ea63f786756628a07824060de98056516eaebd499
```

The validated archives are in
`/tmp/ama-paper-final-corrections-5256041a-verified`. No publication command,
commit, push, arXiv submission or OSF change was performed.

Work execution: Complete for the source corrections and technical validation.
Assessment: Public release of both OSF registrations is still pending and
blocks submission; author clearance and final approval are human actions.

## Final arXiv release pass, 26 November

Both OSF registrations (`https://osf.io/ywsrv/overview` and `https://osf.io/xcpt4`)
were checked through the unauthenticated OSF v2 registration API on
26 November 2026 and returned HTTP 200 with `public: true` and `embargoed: false`.
The owner also confirmed employer clearance and coauthor approval.

### Targeted changes applied

* Data availability, second paragraph: replaced the pending-release sentence
  with "Both registrations are public." Verified that no `[CONFIRM`, `TODO` or
  `pending` string appears in Data availability.
* Supplement A.20.1: removed "Its metadata was not independently verified
  (Data availability)."
* Supplement A.20.17: replaced the HTTP 401 access-failure sentence with
  "Both registrations are now publicly accessible."
* Supplement A.20.12: replaced "The independent researcher completed" with
  "Isabel Cabezas Martin completed", and scoped URL break rules around
  `pilot-estimation-gpt-6.1-sol-C-20` and
  `pilot-estimation-gemini-4-argon-E-15` so line breaks occur only at hyphens.
* Supplement A.20.16: added "Table 36 lists the measurements in the active kit
  and how each is produced." directly under the heading via `\ref{tab:measurementprovenance}`.
* Section 7.8: merged the three one-sentence paragraphs on trajectory
  completion, outcome completeness and billing holds into a single paragraph
  without altering their wording.
* Title-page date: unchanged (renders as November 26, 2026).

### Validation

All 37 numerical table bodies, all displayed equations, all citations, the
bibliography and all main-text numbers are unchanged. The extracted arXiv
archive compiles with PDFLaTeX (`-no-shell-escape`) in two passes to 78 pages
with zero warnings, box diagnostics, missing characters or unresolved
references. The current PDF SHA-256 recorded in
[supplement-integration.json](./supplement-integration.json) under
`final_arxiv_release_pass_2026_11_26` is:

```text
33f89fa43397e3954d95dace508313ff07ee2a0c22e36f52b0b7d50dbd1c017f
```

The validated submission archives are in `/tmp/ama-paper-final-pass-2-5256041a`.
No commit, push or external upload was performed.
