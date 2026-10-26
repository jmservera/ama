# Executive review of “Everything but the Software”

## Verdict

**Publish on arXiv after targeted revision; do not wait for the experiment.** The paper is timely, relevant and potentially useful because it connects a traceable failure case to a falsifiable intervention rather than presenting another single-task coding benchmark. However, I would **not post the present version unchanged**.

* **Strongest contribution:** the combination of a traceable case in which artefact-level completion diverges sharply from usable behaviour, plus an experiment that evaluates **retained behaviour and response to unforeseen change**, rather than only immediate feature completion.
* **Biggest weakness:** the manuscript currently presents **three contributions of roughly equal weight**—case study, five-mechanism theory and operating model/experiment—and therefore does not yet have one unmistakable evidential spine.
* **Serious SE review outlook:** in its current form, it would probably receive a **weak reject/revise-and-resubmit judgement** at an ICSE/FSE/EMSE-level review. The main problems would be causal wording, post-hoc mechanism construction, participant-observer bias and an experiment whose current controls do not cleanly identify the effect of consolidation. These are fixable without collecting the experiment results first.

The paper itself already states that the case is exploratory, that the mechanisms are propositions rather than established causal findings, and that the experiment is prospective rather than completed; that restraint is credible and should become even more visible in the title, abstract, RQs and contribution list.

## Direct answers to your two editorial questions

### 1. Do you have to change the central point to the proposed sentence?

**No. Do not make that sentence the paper’s entire central thesis.** It is too narrow and too intervention-led for a paper whose motivating value is the broader mismatch between apparent delivery progress and preserved software capability.

It is, however, an excellent **precise contribution statement**, with one adjustment: avoid wording that makes consolidation sound effective before it has been tested.

### Recommended central positioning

**This paper asks how feature-centric agentic delivery can produce strong artefact-level completion signals while failing to preserve a behaviourally valid and adaptable software system. It contributes a traceable exploratory case, five candidate mechanisms explaining that divergence, and a preregistrable experiment protocol for testing whether scheduled, behaviour-preserving consolidation improves retained behaviour and adaptation to unforeseen change.**

### Recommended contribution statement

**A traceable exploratory case motivating a prospective controlled test of whether scheduled, behaviour-preserving consolidation better retains working behaviour and adaptability during iterative agentic development.**

That creates a clean hierarchy:

1. **Broad question:** when does apparent agentic progress cease to represent software progress?
2. **Empirical contribution:** one unusually well-instrumented case demonstrating the divergence.
3. **Explanatory contribution:** five **candidate** mechanisms.
4. **Prospective contribution:** a controlled consolidation experiment.

### 2. Can you keep the title?

**Keep “Everything but the Software”. It is memorable, relevant and justified by the case.**

I would **not retain “How Coding Agents Accelerate Feature-Driven Decay” unchanged** for a serious SE submission. “How X accelerates Y” ordinarily implies:

* a demonstrated causal mechanism;
* a comparison with a slower or non-agentic baseline; and
* evidence that the agent caused an increased rate of decay.

A single confounded participant-observer case establishes none of those decisively. Explicit disclaimers inside the paper will not fully neutralise a causal claim in the title.

### Smallest defensible adjustment

**Everything but the Software: Feature-Driven Decay in an Agentic Coding Loop. An Exploratory Case Study and Experiment Protocol**

This retains nearly all the title’s character while converting the causal claim into an observational one.

A slightly broader alternative is:

**Everything but the Software: Feature-Driven Decay in Agentic Development. An Exploratory Case Study and Experiment Protocol**

I prefer the first: **“an agentic coding loop” accurately preserves the single-case boundary**.

## Highest-priority substantive issues

### 1. Make one claim govern the entire paper

The paper should follow one chain:

**Observed divergence → candidate mechanisms → testable consolidation hypothesis → controlled protocol**

At present, the feedback-first operating model reads like a fourth contribution. Reduce it to **implications for practice**, or move most of it to an appendix. Otherwise reviewers may reasonably see a case paper, a conceptual framework paper and a protocol paper sharing one introduction.

### 2. Relabel the five mechanisms as candidate mechanisms

“Specification inflation”, “proxy capture”, “learning evaporation”, “process-gate inflation” and “feedback starvation” are useful names. The case can show that the observations are **consistent with** them, but cannot demonstrate that all five causally operated.

For each mechanism, add a compact evidence table:

|  |  |
| --- | --- |
| Element | Required content |
| Definition | Necessary and sufficient characteristics |
| Case indicators | Directly observed evidence |
| Counter-evidence | Negative or inconsistent observations |
| Rival explanations | Other processes producing the same indicators |
| Experimental implication | What result would support or weaken it |

The integrated set may be novel; the underlying phenomena often are not. Developer studies already describe reliance on plans and passing tests as oversight proxies, plus burdensome post-hoc review of broad agent changes.[1](https://hits.microsoft.com/Study/6047863) “Feedback starvation” becomes defensibly distinct only if defined as **insufficient independent, outcome-level feedback despite abundant artefact-level validation**.

### 3. Strengthen the chain of evidence

The manuscript’s traceability is a genuine asset, but a serious review will still ask:

* Which records were contemporaneous and which were reconstructed?
* Who derived the mechanism labels?
* Was any coding independently checked?
* Were AI-generated interpretations treated as data, analysis assistance or both?
* Can a reader trace every major interpretation to repository events, execution evidence or contemporaneous notes?

Add an **observation–interpretation–proposition audit trail**, a reflexivity statement, and ideally a second-coder or peer-debrief pass over the highest-consequence claims. Personal experience alone can systematically diverge from project evidence, which empirical-SE research explicitly warns against.[2](https://www.microsoft.com/en-us/research/publication/belief-evidence-in-empirical-software-engineering/)

### 4. Add a real within-case contrast

The present case is stronger as a chronology than as an explanatory comparison. Compare:

* early versus late feature waves;
* periods with and without operational validation;
* PR cohorts before and after specification/log growth;
* features that remained operational versus those that failed;
* negative cases in which the proposed mechanisms should have appeared but did not.

This would not create causal identification, but it would substantially improve analytical credibility.

### 5. Do not treat volume proxies as decay

PR count, documents, logs and specification growth are useful descriptors, not direct measures of software quality. The paper should explicitly distinguish:

* **production volume**;
* **validation activity**;
* **observable system behaviour**;
* **maintainability/changeability**; and
* **agent or human intervention**.

The striking 183-PR/5-of-5/usability divergence remains compelling, but the argument should rest on behavioural evidence and chronology—not on volume itself.

### 6. Expand the rival-explanation matrix

The current threats section is thoughtful, but reviewers will expect evidence for and against at least:

* environment or deployment drift;
* external service/dependency failures;
* scope expansion;
* inadequate acceptance tests;
* model/tool limitations;
* rate or context limits;
* human overrides and prioritisation;
* specification ambiguity;
* ordinary prototype debt unrelated to agents.

Software reliability is affected by operating environment as well as intrinsic code properties, reinforcing the need to separate repository deterioration from deployment and dependency effects.[3](https://www.microsoft.com/en-us/research/publication/extrinsic-influence-factors-in-software-reliability-a-study-of-200000-windows-machines/)

### 7. Separate evidence, interpretation and prescription

Use explicit labels:

* **Observed in the case**
* **Interpretation**
* **Candidate mechanism**
* **Practice implication**
* **Prospective hypothesis**

This will eliminate much of the perceived overclaiming without making the paper timid.

### 8. Tighten the related work and practitioner material

Retain practitioner sources where they establish contemporary practice, but do not use them as primary support for mechanism novelty or causal claims. Move extended industry examples to an appendix.

The landscape has moved materially:

* *RefactorBench* already evaluates repository-level refactoring agents across 180 tasks from 20 repositories, so agentic refactoring itself is not novel.[4](https://www.microsoft.com/en-us/research/publication/appendix-to-code-reviewing-in-the-trenches-understanding-challenges-best-practices-and-tool-needs/)
* *Building to the Test* reports that coding agents may manipulate or weaken tests when optimising visible test outcomes, directly overlapping proxy capture and hidden-test design concerns.[5](https://www.microsoft.com/en-us/research/publication/when-should-a-software-factory-be-lights-off-benchmarking-code-review-agents-on-bug-detection/)
* *CRBugBench* evaluates review agents on 1,800 human-verified bug tasks and finds larger drops on complex, non-local and proprietary-context changes; this weakens any implication that “review-only” is unexplored, while supporting your concern about independent behavioural feedback.[5](https://www.microsoft.com/en-us/research/publication/when-should-a-software-factory-be-lights-off-benchmarking-code-review-agents-on-bug-detection/)
* *Why AI Agents Still Need You* appeared at ASE 2025, and reproducible repository benchmarks such as *SWE-Sharp-Bench* already exist.[6](https://www.microsoft.com/en-us/research/people/emurphyhill/) [7](https://www.microsoft.com/en-us/research/people/emurphyhill/?lang=ko-kr)

The October 2026 CRBugBench work is extremely recent and appears as an arXiv publication rather than an independently established peer-reviewed result; describe it accordingly.

## Narrow novelty assessment

|  |  |  |
| --- | --- | --- |
| Proposed contribution | Judgement | Recommended claim |
| Five named mechanisms | **Useful synthesis/reframing** | Novel as an integrated candidate model if mappings and boundaries are explicit; do not claim each phenomenon is new. |
| Feedback starvation | **Potentially distinctive reframing** | Defensible if operationally separated from weak testing, missing context and ordinary feedback delay. |
| Scheduled post-feature consolidation harness | **Plausibly novel** | Claim a specific, cadence-based, behaviour-preserving intervention—not first-ever agentic maintenance/refactoring. |
| Feature-only vs consolidation vs review-only | **Plausibly novel configuration** | Novel experimental contrast, but the present review-only arm does not isolate consolidation cleanly. |
| Unforeseen-change performance | **Strong and worthwhile synthesis** | Position as an operational proxy for preserved future options, not as a validated universal measure of maintainability. |
| HIR/IDR adaptation | **Useful operationalisation** | Do not claim new metrics unless definitions, annotation reliability and construct validation are demonstrated. |

**Bottom line:** the novelty is defensible at the **combination and evaluation-design level**, not at the level of discovering technical debt, refactoring, review agents or test gaming.

## Experiment-protocol assessment

### Issues fatal to the intended causal interpretation

1. **Arm C does not isolate consolidation.** A review that cannot act is not equivalent to a non-consolidating corrective process. Any B–C difference could reflect permission to modify code, additional repair, or consolidation.
2. **Fix:** make C a scheduled **review-and-local-repair** arm that may correct detected behavioural defects but is prohibited from structural consolidation. Then B–C better targets consolidation beyond inspection and repair.
3. **Time and compute budgets are part of the treatment.** If B receives extra tokens/time, the estimand is “consolidation plus more resources”. If budgets are equal, state what feature work is displaced.
4. **Fix:** predefine both:
   * an **equal-total-budget estimand**; and
   * a secondary **equal-feature-budget/productivity-cost estimand**.
5. **Future changeability must be the primary behavioural endpoint.** Static complexity, documentation quality or immediate regression survival cannot establish preservation of future options.
6. **Fix:** designate performance on preregistered, unseen change requests—under fixed budgets—as the primary outcome, with accumulated behaviour survival as the key secondary outcome.
7. **The proposed sample is unlikely to support the planned model without simulation.** Bootstrap resampling does not create independent information, and a mixed-effects model with few repository/scenario clusters will be unstable.
8. **Fix:** conduct simulation-based power analysis using plausible baseline success, minimum meaningful effect and scenario/run intraclass correlation. Randomise at the repository–sequence–run level, not at individual change-request level.

### Important refinements

* Preselect one primary hypothesis; apply hierarchical testing or FDR control to secondary hypotheses.
* Keep hidden tests and future changes inaccessible to the acting agent; use independent evaluator credentials and immutable snapshots.
* Pin model/service version where possible; archive prompts, traces, containers, dependencies, tool outputs and failure classifications.
* Repeat stochastic runs; model repository, scenario, feature wave and model version as clustered/random effects where sample size supports it.
* Define HIR/IDR event boundaries, denominator, severity and adjudication rules; report inter-rater agreement.
* Blind comprehension reviewers to arm and outcome; standardise time and permitted tools.
* Predefine stopping, timeout, infrastructure-failure and missing-data rules.
* Measure both **absolute quality** and **quality per token/time/cost**.

## Prioritised revision list

### Must fix before arXiv

1. Replace the causal title clause.
2. Adopt one central narrative and demote the operating model to implications/appendix.
3. Use **candidate mechanisms** consistently.
4. Add an observation–interpretation–proposition audit table.
5. Add within-case contrasts and a rival-explanation matrix.
6. Correct the experiment’s control-arm and budget estimands.
7. Make unforeseen-change performance the primary changeability outcome.
8. Update related work with 2025–2026 refactoring, review-agent, test-gaming and human-intervention research.

### Strongly recommended before arXiv

1. Add independent coding/peer debriefing for consequential qualitative claims.
2. Shorten repetitive motivation and practitioner evidence.
3. Operationally define “decay”, “working behaviour”, “consolidation”, “adaptability”, HIR and IDR.
4. Distinguish chronological evidence from descriptive proxies.
5. Clearly label very recent preprints and first-party industry studies as non-peer-reviewed.
6. Include a one-page protocol summary covering estimand, unit of randomisation, primary endpoint and minimum meaningful effect.

### Can wait for peer-reviewed submission

1. Execute the experiment across multiple repositories and stochastic repetitions.
2. Validate HIR/IDR annotation reliability and construct validity.
3. Add model/provider replication.
4. Release the maximum lawful reproducibility package.
5. Consider separating the fuller feedback-first operating model into a subsequent paper.

## Final publication judgement

**ArXiv:** publish after the targeted revisions above. The case and protocol already justify public scholarly discussion; waiting for results would unnecessarily delay a timely contribution.

**ICSE/FSE/EMSE standard:** not yet competitive as a conventional empirical full paper, but plausibly competitive after sharpening the case methodology and experimental identification. With completed results, the experiment could become the stronger venue paper; without results, the current work is best positioned as an **exploratory case plus preregistrable protocol**, not as evidence that consolidation works or that coding agents causally accelerate decay.
