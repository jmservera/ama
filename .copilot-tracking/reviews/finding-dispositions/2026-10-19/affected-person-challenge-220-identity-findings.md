---
title: "Issue 220 narrow TaskReleaseRecord identity finding disposition"
date: "2026-10-19"
issue: "jmservera/ama#220"
branch: "feat/affected-person-challenge-220"
comparison_base: "d6874f3e"
test_file: "src/api/tests/test_assistant_release.py"
test_file_sha256: "504ee94de7ee745a2059f58eb1a1c8fd824124b9b5c9eac279ecce7427b113b0"
direct_regression_disposition: "corrected"
original_review: "Partial / Not accepted"
original_critique: "Revise"
publication_authorized: false
---

## Scope and verdict

Corrected for the specific coordinator-reported project-api TaskReleaseRecord
identity regression. The test-only repair is justified: it makes synthetic
ownership consistent with the registered coordinator instead of falsifying the
coordinator's identity. No concrete introduced flaw was found in this bounded
diff. This is not a replacement Review, historical UI/evidence disposition,
whole-issue assessment, or acceptance decision.

## Direct source assessment

* Compared the actual test-file diff against `d6874f3e`. It adds
  `TaskReleaseRecord.priority_user`, adds one identity regression method, and
  replaces five forged actor construction sites. Existing test assertions are
  not removed or relaxed.
* `Base.setUp` in `src/api/tests/test_assistants.py:74` replaces the seed's
  staff roster with registered `ROLE-*` synthetic staff, while retaining the
  original case ownership. The previous construction copied a registered
  coordinator but substituted the original case owner's unrelated code.
* `change_provenance._actor` looks up current staff by email and requires a
  named permitted staff role plus exact agreement on email, code, name, role
  and oid. `resident_decisions._actor` delegates to it.
  `resident_decisions.priority_review` checks that identity before yielding to
  `Store.resolve_priority`, including for rejection. Rejecting the forged
  fixture is therefore expected behavior, not evidence that this guard should
  be weakened.
* The helper returns unchanged `self.people[assistants.RC]` and, under the
  store lock, reassigns only synthetic cases sharing ZF-1's original owner to
  that coordinator, including owner name and role, through actual
  `store.save()`. JSON save writes the data; SQL save uses its existing
  transaction/validation path. Neither the staff register nor guard is patched.
  `ai_priority` scopes cases by owner code, so repairing case ownership
  supplies legitimate work without inventing caller authority.
* The inference-off matrix still exercises AI/template sources and
  accept/edit/reject on JSON and SQLite: historical AI accept/edit remain
  denied, while template actions and rejection remain successful. Revoked
  release and changed-route assertions remain; strong-route testing still
  requires initial actionable AI output, subsequent denial, and valid
  rejection. Cached briefing fallback, zero additional calls and recovery
  after release recording remain asserted.
* The new regression mutates each of code/email/name/role/oid independently
  for all three review actions on both stores. It requires the specific
  current-registered-staff `PermissionError`, unchanged serialized in-memory
  data, and subsequent successful rejection by the unchanged valid actor.
  This is 30 invalid identity/action/store combinations. It does not assert
  independent disk/audit equality or concurrency behavior; none is claimed.
* The three directly relevant production files have no diff against the
  comparison base. This correction does not alter production authorization,
  release admission or priority-review behavior.

## Fresh primary evidence and independent checks

Inspected the permitted coordinator directive and the additional identity
section of `manifest.txt` in the allowed session evidence bundle:
`/home/azureuser/.copilot/session-state/bc713866-d9c3-479b-acc9-bb5780f2ebcd/files/issue220-evidence/`.

Independently executed `sha256sum -c` for both `identity-source.sha256` and
`identity-outputs.sha256`; every entry passed. Also recalculated the test-file
hash shown in frontmatter and ran the test-file `git diff --check`, which
passed. Source inspection covered the actual diff, original Base fixture and
the directly relevant current helpers, with narrow save/ownership context.

Read actual raw failure and result sections, not just manifest summaries:

* `release-identity-before.log`: 16 tests, nine errors. The eight
  inference-off positive/rejection subtest errors span both stores; the ninth
  is strong-route rejection. The traceback follows `resolve_priority` through
  `priority_review` into the current actor guard.
* `release-and-challenge.log`: 139 tests, OK, two skips. All 17
  TaskReleaseRecord methods, including the new identity regression, report
  success. The skips are SQLite's inapplicable JSON-file rollback test and
  the existing opt-in browser commitment/reassignment journey.

These are inspected fresh coordinator-produced synthetic test executions,
not independent reruns by this assessor. No tests were rerun here; the
hash-bound outputs and actual diff suffice for this narrow disposition.
No excluded original logs or receipts were accessed or reconstructed.
Tool output exceeded the inline limit on some reads; only the original
permitted files were subsequently read in bounded sections, not the
tool-generated overflow files. Historical UI assets were not assessed.
No cloud, model, private-data, gate or publication operation was performed.

## Unchanged gates and acceptance limits

The coordinator reports the original historical all17 gate attempted all
groups, passed 16, and failed project-api. That original gate failed and is
not reused as a passing receipt; its excluded receipt was not inspected.
The corrected frozen commit and complete exact-head all17 gate remain pending.

The original Review remains **Partial / Not accepted** and original critique
remains **Revise**; neither is changed or repeated here. This disposition
grants no whole-issue, native-SQL-specific, human, legal, RAI, resident or live
acceptance, and no publication authorization.
