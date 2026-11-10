<!-- markdownlint-disable-file -->
# Issue 231 positive coverage plan critique (2026-11-10)

Executed once, by the implementing agent in a separate pass over the final-candidate plan and details (no nested agent was permitted). Reviewed against the brief, the admission report and the research facts. Verdict: approve with the direct applications below. No significant or divergent issue needs a user decision.

## Findings and direct dispositions

1. Negative control weakening: adding `231p` to shared lists could relax the negative branch. Applied: the positive branch is a separate `elif` before the unchanged `else`; `STORY_231` untouched; a temporary external mutation proof is required in P2.
2. Fixture legitimacy: `hazards = []` could be read as clearing a safety gate. Disposition: it is an input with no hazard records, not a runtime release; the code comment and handoff say synthetic input only. No released hazard or gate field is fabricated.
3. Identity inference: sign-off and inspector names must not look like real approvals. Applied: all names are `SYN ...` tokens and the handoff states they are not professional approval.
4. Fake projection risk: no `page.route` is used for positive detail; the before/after `GET` equality uses the real endpoint. Applied.
5. Mutating shared fixtures: `role_screens_fixtures.py` is #233-owned. Applied: private wrapper in the checker, reusing `synthetic_data` and `runpy` of the supplied constructor.
6. Rendered phrase uncertainty: phrases are finalised from the first real render, then fixed; no phrase is loosened to pass.
7. Added tests: the browser run is the check; a separate unit test would only restate the fixture, so none is added. No registered recipe, so no SHA or manifest change; re-verify at P3.
8. Out of scope kept excluded: #130 nomination UI, #111 draft hooks, #233 files, whole-issue, WCAG and assistive-technology acceptance.
