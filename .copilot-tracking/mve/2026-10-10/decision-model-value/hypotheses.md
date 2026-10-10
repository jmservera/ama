<!-- markdownlint-disable-file -->
---
title: Decision Model Value - Hypotheses
description: Prioritized falsifiable hypotheses and proposed comparison targets
ms.date: 2026-10-10
---

## Phase 2: Hypothesis Formation

Thresholds inherited from the accepted PRD are unchanged. Additional comparison
targets below are proposed experiment decisions, not approved PRD amendments.
All targets freeze before the held-out run.

| ID / priority | Hypothesis, method and verdict | Rationale / dependency |
| --- | --- | --- |
| H1 / first | We believe Decision 1 can safely select supported candidates in ambiguous evidence. We will test this on 60 held-out families with independent gold dispositions. We will know it meets the quality bar when correct dispositions >=95%, selected accuracy >=98%, answerable coverage >=50%, source binding 100%, and zero critical unsupported selections or prohibited actions occur. Failure of any gate refutes deployable suitability for that task. | Fundamental; H2/H3 cannot justify use of a failing task. |
| H2 / second | We believe Decision 1 can replace generative-agent selection on a narrow task more economically. We will test D versus A on identical frozen candidate/evidence inputs. We will know replacement is justified when D passes H1, the paired family-bootstrap 95% lower bound for accuracy difference D-A is >=-2 percentage points, and cost per correctly resolved item falls >=20% OR p95 machine latency falls >=20%, without human-effort regression. | Proposed non-inferiority/efficiency targets; not an agent replacement claim. Requires H1 and human effort if claiming usable replacement. |
| H3 / second | We believe Decision 1 complements the generative agent by reducing complete-pack human work. We will test H versus A and R in 12 counterbalanced pack blocks. We will know complementarity is supported when H passes all quality gates and median within-pack total active-effort reduction is >=15% versus both A and R, with no critical misses or lower final reviewed quality. | Primary value claim; depends on H1 and real human sessions. |
| H4 / third | We believe semantic selection is more useful on ambiguous than clear structured inputs. We will test the arm-by-input-type interaction, recording accuracy, effort and cost separately. We will know selective placement is supported when at least one semantic arm clears its value gates on ambiguous tasks while rules match its final quality on clear fields at lower cost and no greater human effort. | Placement hypothesis, not a universal superiority claim; exploratory transfer slices remain descriptive. |
| H5 / third | We believe a Decision 1 support screen reduces unsupported agent-draft claims. We will compare H versus A on identical drafted-claim/source pairs and end-to-end packs. We will know screening is supported when H passes the PRD screening/critical gates and critical misses remain zero, while noncritical unsupported claims reaching review fall >=50% relative to A with no >2-point reduction in supported-claim recall. If A has zero such errors, error-reduction benefit is unproven rather than dividing by zero. | Proposed screening target; cannot replace mandatory human review. |

H2 cost and latency comparisons are co-reported; neither alone proves human
benefit. H3 point estimates passing but wide intervals are provisional, not
conclusive evidence. H4/H5 are secondary: no cherry-picking a winning task to
describe the entire system as better.

Every verdict is Pass, Fail or Inconclusive. Missing gold labels, insufficient
denominators, unbooked participants or unavailable measured cost produce
Inconclusive, never an assumed pass.
