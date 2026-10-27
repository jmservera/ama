---
title: Supplementary Context and Deferred Research
description: Practitioner framing, contextual repository observations, proposed practices and extensions outside the twelve-trajectory pilot.
ms.date: 2026-10-27
---

## Status and Scope

This companion separates contextual material from the paper's main argument:
inherited state, the AMA case, candidate mechanisms and a prospective
consolidation-package comparison. It contains no experimental results.
The twelve-trajectory pilot has not started. The proposed practices and
extensions below are not validated methods, implemented controls or additions
to its 212-session budget.

This is a contextual source synthesis, not a systematic review. Practitioner
accounts, commercial studies, author recollections and project-authored
claims have different evidential roles. None establishes that the AMA
mechanisms caused its outcome or that consolidation will work.

## Framework and Practitioner Context

### HVE Core

[HVE Core](https://github.com/microsoft/hve-core) describes an opinionated
agentic lifecycle around GitHub Copilot, with Research, Plan, Implement and
Review, dated file-based handovers, human stops and product-side planning
agents. It is not itself the autonomous dispatcher used in the AMA case.
The author's coordinator supplied that delivery loop.

The case account reports plugin snapshot `plugins-v3.3.106`, snapshot commit
`2df5013e29ebfd2ce61bcd0cf021d8c8186482eb`, generated from source commit
`e9af018fe5ffbfbc72321a8bca21fb987359af08`. Those identifiers do not
independently establish the installation date or every session's behaviour.
The Experiment Designer's Minimum Viable Experiment method informed the
proposal; it does not certify the study design or replace registration.

### Additional Empirical Context

The primary [DORA 2024](https://dora.dev/research/2024/dora-report/) and
[DORA 2025](https://dora.dev/research/2025/dora-report/) reports supply industry
background about adoption, delivery and organisational conditions. They are
not mechanism-level evidence for the AMA case.
[Heander et al.](https://arxiv.org/abs/2610.21914) associate baseline
CodeHealth with token cost in an agentic review-and-fix pipeline; batch
fixing left median CodeHealth unchanged. That observational result motivates
measuring cost alongside quality, not a conclusion about scheduled
consolidation or agent-caused decay.

[He et al.](https://arxiv.org/abs/2511.04427) study adoption and repository
quality through a quasi-experimental design. Its interpretation depends on
the authors' design assumptions and differs from a controlled consolidation
intervention. Commercial duplication reports have different samples and
incentives again; they should not be pooled into one effect estimate.

The [METR authors' later update](https://metr.org/blog/2026-02-24-uplift-update/)
qualifies transfer from their early-2025 productivity experiment to newer
tools. Industrial review guidance, including Cohen's *Best Kept Secrets of
Peer Code Review* and
[Google's code-review case study](https://doi.org/10.1145/3183519.3183525),
describes conditions for manageable review, not a universal change-size limit.
Exact book passages were not newly inspected in this revision.

### Craft and Reported Practice

[Karpathy's original post](https://x.com/karpathy/status/1886192184808149383)
illustrates accepting generated code without close review for throwaway
projects. [Willison's vibe engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/)
instead retains professional accountability and stresses testing, planning,
documentation, version control and review. These are contrasting practitioner
positions, not experimental comparisons of decay or the harness.
[Osmani's unfinished final stretch](https://addyo.substack.com/p/the-70-problem-hard-truths-about)
and [Fowler's account](https://martinfowler.com/articles/202508-ai-thoughts.html)
provide further framing rather than controlled effect estimates.

[Beck's augmented-coding essay](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes)
retains concern for code, complexity and tests.
The [Prodacity transcript](https://www.rise8.us/videos/kent-beck-software-engineering-in-the-age-of-ai)
motivates alternating features with consolidation, while
[his mathematicians essay](https://newsletter.kentbeck.com/p/mathematicians-heres-a-way-to-think)
distinguishes visible output from understanding and abstraction.
These accounts motivate the research question; they do not supply a measured
treatment effect.

The [Product Engineers interview with Martin](https://productengineers.com/episodes/season2/why-hardcore-technical-focus-still-matters-big-time-uncle-bob/)
discusses executable feedback and understanding customers.
The [Syntax episode's show notes](https://syntax.fm/show/903/fork-yeah-microsoft-open-sourcing-copilot)
document discussion of simulation tests and testing LLMs, not an exact
stochastic-testing quotation or evidence that deterministic tests are unreliable.
[Thoughtworks](https://www.thoughtworks.com/radar/techniques/complacency-with-ai-generated-code)
warns against complacency; [Sarkar](https://doi.org/10.1145/3649404)
argues for challenge rather than obedience.

[Murphy's bottleneck argument](https://andrewmurphy.io/blog/if-you-thought-the-speed-of-writing-code-was-your-problem-you-have-bigger-problems)
connects code throughput with review queues and work in progress, while
[his craft account](https://andrewmurphy.io/blog/the-five-stages-of-losing-our-craft)
raises learning questions. Goldratt and Cox's *The Goal* is a conceptual
precursor, not direct software-agent evidence.
[Lanzetta's engineering guidance](https://www.linkedin.com/pulse/growing-engineers-hypervelocity-era-mike-lanzetta-qux0c/)
and [orchestra account](https://www.linkedin.com/pulse/hypervelocity-orchestra-mike-lanzetta-p0kvc/)
describe small changes, review and retrospectives.
[Lamanna's account](https://www.linkedin.com/pulse/changing-how-we-build-charles-lamanna-xpitc/)
reports investing agent capacity in reliability and other product outcomes.
These first-party accounts do not isolate consolidation from other changes.

### Informal Conversations

Partner and peer conversations informed the author's thinking, but were not
systematically sampled or independently coded. Their detailed paraphrases
are omitted here pending permission and anonymisation review. They are not
independent corroboration or evidence of prevalence. Neither organisations
nor participants are identified.

## Motivating Experience and External Repository Observations

The full source pins, tracker boundary and claim locators remain in
[the dated repository-observation record](./repository-observations-2026-10-25.json).
These purposively selected observations were added after the AMA analysis.
No external application or reference-parity suite was executed.

### Aithena and Squad

Aithena is the author's book-search project, with PDF ingestion, search and
a browser interface. At the inspected
[source revision](https://github.com/jmservera/aithena/tree/f27aa2e9f949ea76f2a437249e68b52670a22835),
its Squad records describe specialist agents, shared decisions, a work
monitor, pre-task design review and post-failure retrospectives.
[Squad's pinned documentation](https://github.com/bradygaster/squad/blob/481c944596abfa2053e2acd88d765639f994d795/README.md)
describes persistent file-based learning while retaining human leadership.
Designed feedback mechanisms do not establish that each session used them
effectively or that self-improvement was demonstrated.

The dated record distinguishes active preflight tests from fixture-dependent
scenarios skipped in issue jmservera/aithena#1828. It also records the
acknowledgement/failure-contract concern in jmservera/aithena#1804 without
claiming reproduced document loss. Quality gates, releases and substantive
functionality also exist. Of 35 open PRs at retrieval, 34 had a dependency
label; that queue is not an architectural-decay measure. The author's
judgement that maintenance became difficult is retrospective, not a measured
complexity trajectory or controlled framework comparison.

### PhotoCraft

The [pinned PhotoCraft source](https://github.com/storytold/photocraft/tree/5bb853654196eca807212ff8955ba2eb293071ea)
describes an early-alpha, clean-room Rust reimplementation of Photoshop,
not the whole Adobe suite. Its controls include dependency checks,
regression tests, file corpora and visual-inspection guidance.
Its 631-of-631 menu count concerns handler dispatch, not every reference
workflow. The dated assessment's approximately 76% feature breadth and 45%
readiness are project-authored historical estimates, not an independent
application assessment.

At the 25 October 2026, 22:52 UTC tracker boundary, the record reports 2,060
open issues, 212 labelled `bug`, 1,091 open PRs, 49 drafts, 2,604 closed
issues and 3,189 merged PRs. These are tracker states, not unique defects
or a defect rate. Selected reports and corrective PRs concern printing,
save prompts, large PSD files and helper consolidation; none was reproduced
by this revision. A known target still requires inputs, oracles and
tolerances. The records establish neither inevitable decay nor a permanently
human steering role.

## Proposed Feedback-first Practices

These are implications for practitioners to evaluate, not an empirically
validated operating model or new repository rules. One-to-two-week horizons,
three parallel sessions and five acceptance criteria are starting heuristics,
not estimated optima. They never override safety, privacy or required
engineering and human approval gates.

| Practice | Proposed application and boundary | Suggested observation |
| --- | --- | --- |
| Protect a running increment | Exercise a real user journey before replacing a working system | First human use; age of last usable increment |
| Bound batches and horizon | Start small, then adapt horizon and concurrency to task risk | Work in progress; scope versus validated behaviour |
| Hold human checkpoints | Demo, decide what to keep or change, and record the decision | Product-use feedback and decisions, not attendance |
| Make lessons usable | Convert suitable lessons into executable checks or compact, provenance-linked context | Executable lessons; effective read-path size |
| Make gates proportional | Scope checks and records to risk while preserving mandatory gates | Gate time and defects detected per accepted outcome |
| Measure outcomes | Compare scores with journeys and track attributable cost and review effort | Score/demo disagreement; cost per accepted outcome |
| Preserve theory building | Own acceptance examples, inspect domain code and invite challenge | What the owner can predict and explain without the agent |

[Fakhoury et al.'s interactive generation study](https://doi.org/10.1109/TSE.2024.3428972)
motivates making intended behaviour checkable through tests. It does not
evaluate this practice package, scheduled consolidation or cross-feature
retention.

Possible framework-builder additions include paths that exercise running
increments, risk-scaled evidence and executable lessons with context-budget
warnings. These require evaluation; this case does not establish their
benefits or authorise removal of required gates.

## Deferred Research Agenda

* Formal fault-lineage annotation would identify an inherited fault, its first
  contract failure, affected code or rule, and evidence linking distinct
  later failures to reuse. Repetition alone is persistence, not propagation.
  Matched faulty/minimally repaired snapshots require fixed repair rules,
  fresh sessions and a separate resource and analysis amendment.
* Early/late changeability probes would use a withheld core-contract change
  on compatible disposable snapshots, fresh sessions, fixed budgets and no
  feedback returned to the main trajectories. CR1 cannot simply move earlier:
  it requires F9-F10. This extension is outside the pilot.
* Additional suites, independently designed change requests, open-weights
  models and other platforms need separate replication and precision plans.
* Matched-resource human-versus-agent steering, with equal oracle coverage,
  would study a different question from the pilot's scheduled consolidation.
* Human learning and responsibility require separate evidence about
  prediction, explanation and unaided change over time. Lower intervention
  is not inherently better; meaningful participation and valued roles are
  not settled by a code-quality outcome.

No experiment in the paper validates these extensions, the seven practices,
the five candidate mechanisms individually, or a permanent boundary between
human and agent responsibilities.
