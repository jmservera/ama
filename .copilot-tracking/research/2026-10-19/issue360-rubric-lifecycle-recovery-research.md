---
title: Issue360 supplemental rubric lifecycle recovery research
description: Bounded same-workstream diagnosis without repeating original RPI evidence
ms.date: 2026-10-19
---

## Brief and Controls

Task 360 / issue360-rg-loop; automatic continuation explicitly authorized on
2026-10-19. Focused convergence for PR416 rubric lifecycle only. No coordinator
implementation, cloud, tenant, private data, hosted inference, push or PR update.
Original research, critique and adverse Review remain byte-exact. Supplemental
research is authorized despite the historical two-cycle stop.

Opening boundary: clean e87967580520f421e6181dff546b478bf5c02f1a,
fresh main634a024d97d2da7168b8a7d5f343ab26e6108cf3 and open PR416 on
fix/demo-private-publisher-360. Verified descendant7e810dc9c9ac520e4e7717b4604dc08fbbc8e311
changes only .github/rubric/scores/latest.json. Authorized fast-forward executed,
preserving source and score. Historical e879 receipt does not cover bot HEAD.

Repository instructions, case studies, KB index/memory, component gate guide
and installed RPI research selected. Inline coupled investigation: no independent
research agent needed. No UI or prompt-authoring change is planned. Existing
gh-aw v0.89.21 compiler, generated-lock/source harness and runtime harness are
selected, not manual lock editing. No interactive checkpoint: caller supplied
scope, authority and stop boundaries.

Questions: what actually caused moved denial; how to distinguish transient
post-push visibility from genuine movement; how to finish at a frozen exact
remote head without repeated score commits or weakening trusted scoring?

## Cycle 1: Wider

C1: .github/workflows/rubric-score.md:209-460 checks lifecycle before checkout,
before recording and at publication; loads trusted gate/prepare/adapter from
base. It records a score using non-force guarded push and publishes to scored
and resulting bot SHA. Source and compiled lock match current origin/main.
Older primary-checkout views are not used.

W1: https://github.com/jmservera/ama/actions/runs/39237980947
(retrieved 2026-10-19), record job118014150315: exact e879 checkout, eligible
preflight, successful guarded push of7e810dc9, NEW_SHA correctly populated,
MOVED empty, record/gate/verify/recheck success, RECORD_HEAD_STATE eligible.
Original fetched record log retained externally:
/tmp/issue360-rubric-original-record.log.

Reflection: output suppression, wrong checkout and failed push do not explain
this run. Need trace the only remaining moved predicate and preserve uncertainty
about the API response, which the original workflow did not log.

## Cycle 1: Deeper

C2: .github/workflows/rubric-score.md:407-420 compares one immediate pulls.get
response with NEW_SHA. Given actual job inputs, the published moved description
necessarily means that response's valid head differed from7e810dc9. The original
response SHA was not logged; stale e879 visibility is a supported mechanism,
not a directly observed value. No genuine concurrent source move is established.

W2: https://github.com/jmservera/ama/commit/7e810dc9c9ac520e4e7717b4604dc08fbbc8e311
(retrieved 2026-10-19): single e879 parent and latest.json-only change.
Live PR retains exactly7e810dc9 and github-actions REQUEST_CHANGES with moved
description. Actual sticky report confirms48/100 against48/100 PASS; the recorded
score and lifecycle verdict are different boundaries. Current status is failure,
not workflow acceptance.

C3: .github/rubric/scripts/test_record_workflow.py:152-182 tests one API
response per publication, including immediate self-commit success and true
movement, but not post-push old-head visibility or integrated push/publication.
Its temporary Git tests cover before/after advertisement movement and deletion.
C4: tools/rpi-checks.py:50-58 excludes rubric workflow from its native matrix.
Explicit rubric regression/compiler/lint/runtime evidence must supplement
all17 groups, not be inferred from their pass.

Reflection: a bounded publication-only consistency wait can retain exact-head
denial. It must accept only the known successful push output after the API
reports that exact head, never reinterpret an old source SHA as final success.

## Cycle 1: Contrarian

Actual new source movement, backward movement, failed push, closed PR, invalid
API response and missing gate output must still deny or remain obsolete.
Retries must be limited to the old scored SHA immediately after this run's
successful bot push; an unrelated SHA is not a visibility lag. Exhaustion
must visibly fail, not accept source equivalence. No score rewrite/inflation,
candidate score trust, force-push or protected main write is justified.

C5: .github/rubric/README.md:132-155 explains GITHUB_TOKEN suppresses recursive
workflows; rubric publishes both SHAs but does not claim other CI ran there.
src/README.md:99-110 requires full gate after any later commit. Finite sequence:
one legitimate scoring/push; fetch final bot head; run full local gate and
independent review there; run retained hosted checks on that same head using
their existing dispatch mechanism, without another source push/rescore.
Persistent rubric publication failure remains a concrete blocker, not grounds
for an empty commit or manual status. Source CI dispatch availability and
exact-head binding require verification before documenting commands.

C6: .github/workflows/src-ci.yml:1-29 has workflow_dispatch; no-base dispatch
selects all four images through infra/scripts/pipeline.py:425-436. Downstream
.github/workflows/infra-plan.yml:22-26 requires a pull_request event, so dispatch
does not execute Azure what-if. Required PR-only/environment checks remain a
separate boundary; no mechanism or permission bypass is inferred.

## Synthesis and Readiness

Research disposition executed; Wider, Deeper and Contrarian completed inline.
Planning Readiness Ready for a bounded consistency repair, focused regressions,
compiler-generated lock and honest finite publication runbook. Preserve exact
score provenance, main baseline comparison, existing push guard and all review/
protection boundaries. No repeat original critique or Review. Source response
was not logged, so exact stale value remains unavailable; reproduce the inferred
mechanism locally and add safe observable head diagnostics.
