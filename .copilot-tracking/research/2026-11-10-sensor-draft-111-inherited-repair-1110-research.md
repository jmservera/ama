---
title: Issue 111 inherited sensor draft correction research (prospective)
ms.date: 2026-11-10
task_id: 111-sensor-draft-inherited-repair-1110
---

## Disposition and scope

Research executed 2026-11-10T13:43Z (witness `launch`) to 13:44Z (witness `research-open`), against this worktree. Planning Readiness: Ready.

Scope: the ONE inherited correction batch the Root authorized on 2026-11-10 after the dated D2 positive-balance proof (`handoff-111-dated-budget-audit-1336.md`). It fixes only two coupled confirmed defects introduced by the frozen initial candidate `d5e7ac2ef560a09a7035ef55d038b40315313977`: (1) JSON audit failure after a successful primary save, and (2) the configured Core mypy failure in the two new files. It is not a new feature, not a rule approval, not a task activation. Initial, D1 and D2 records and the old UNKNOWN balance statement are preserved unchanged.

## Identities (verified)

| Item | Value |
| --- | --- |
| Branch | `feat/demo-sensor-drafts-111-1110`, clean at start |
| Head | `d5e7ac2ef560a09a7035ef55d038b40315313977`, tree `4436b2b8da73aef9602d058a9800da7458687434` |
| `origin/main` after fetch | `c9e15acbf5c0893358818e562d034d62321ea6d4`; head is not an ancestor of it, main is ahead |
| Main versus my paths | `git diff HEAD...origin/main` touches `server.py`, `store.py`, `sqlstore.py` (other work), not `sensor_review_draft.py` or its core test. No intent conflict for the fix scope; main adoption is not needed and is not performed |
| Witness | `launch` recorded `ok` (seq 1) under `phase111-inherited-repair-evidence-1110`, session `rpi-111-inherited-repair`, actor worker, claimed model `claude-sonnet-5.5` (caller assertions, not attestation) |

## Evidence read (no broad rediscovery)

* D1 report `handoff-111-readonly-diagnostics-1110.md` and Root raw `111-root-json-audit-repro-1110.log`: after an injected audit failure following a successful `save()`, memory has no draft, disk has one (`disk drafts: 1`, `audit lines: 0`); an unrelated save erases it (`memory None disk None`); a retry creates a new draft with a new `created_at` (first-attempt provenance lost).
* Root raw `111-root-core-mypy-1110.log`: mypy 2.4.0, 308 errors in the two new files: 122 `no-untyped-call`, 111 `attr-defined` (all `assertX`/`subTest` on test mixins that do not inherit `TestCase`), 56 `no-untyped-def`, 11 `type-arg`, 3 `union-attr`, 2 `func-returns-value`, 1 each `arg-type`, `no-any-return`, `var-annotated`. Config is `strict = true` in `src/core/pyproject.toml`; existing typed modules that call the untyped Store carry narrow `disallow_untyped_calls = false` override stanzas (for example "Narrow typed sensor boundary calls...").
* Prior independent finding (reviewer `1b06482a`, via the Root comment on issue 111): audit-after-successful-save rollback. Reproduced by D1; not re-diagnosed here.

## Root cause (source-grounded)

`sensor_review_draft._persist` (module lines 215 to 267 at `d5e7ac2ef`): JSON order is `store.save()` then `store.audit(...)`. `Store.save` (`store.py:113-118`) writes a temp file and `os.replace`s it, so a normal return means the case JSON is durably committed. The `except BaseException` then restores `case[CASE_KEY]` for every non-`CommittedReloadError`, including an audit failure after that commit. Memory and disk diverge, the next unrelated `save()` rewrites the whole `self.data` without the draft, and a retry mints a new record. The SQL path audits first (pending audit inside the same transaction) then saves, so a failure before commit rolls both back and a `CommittedReloadError` is already treated as committed. That ordering is unaffected.

The existing contract does distinguish commit status on the JSON store: `save()` returning is the commit point, and `os.replace` is its last statement, so a `save()` that raises has not replaced the live file. No store change is required.

## Constraints and options

* No generic store, SQL schema, importer, adapter, server, UI or permission change. Source paths are the new module and its core test only, plus one narrow `pyproject.toml` mypy override stanza (config precedent above) if typed calls into the untyped Store need it.
* Option A (chosen): track a `committed` flag with `try/finally` rather than a broad `except`; after a JSON commit keep memory, then audit; on audit `OSError` raise a dedicated `DraftAuditError` (a `RuntimeError`) that carries the committed draft view and says the draft is saved but its audit record was not written. Option B: reverse JSON order (audit then save). Rejected: it leaves an audit entry for an uncommitted draft, and the JSON audit is an append-only hash chain that cannot be rolled back. Option C: roll disk back on audit failure. Rejected: it needs a second write that can itself fail and rewrites the store.
* Residual, stated not hidden: an idempotent retry returns the existing draft and does not write the missing audit entry. The raised error is the truthful signal; repairing the audit gap is a later, separately authorized decision.
* Typing: annotate every parameter and return in the module and tests with concrete types; make the test mixin inherit `unittest.TestCase` only under `TYPE_CHECKING` (no `cast`, `Any` casts, `type: ignore` or ignore_errors); narrow `ReviewTaskCandidate | None` with asserts; typed `list[bool]`/`dict[str, object]` where mypy asks.

## Boundaries retained

Exercise-labelled approved-rule boundary, trusted current consent and gate, supplied rule-approval provenance and manual and failure paths are untouched. The draft is not an operational task, priority or safety decision. No rule approval, Legal, safety or resident consent is created; synthetic approvals stay SYNTHETIC TEST ONLY. Whole #111 criteria C1 and C3 stay unmet.

## Budget record (Root-authorized, dated)

Root authorized exactly ONE inherited correction batch on 2026-11-10 after the D2 dated proof: at most three potential historic debits before 2026-11-09 (the PR 871 review with no visible corrective commit, the R2 own-test fix, the PR 1075 source fix `bfa3d6c22`), none after the 2026-11-09 08:00:39Z default-five grant, so the default five leaves a proven minimum of 2 before this batch. The one-time additional five is NOT relied on and no exhaustion is claimed. This batch consumes ONE; the conservative proven minimum afterwards is at least 1, and a second batch requires the Root's explicit selection. No fresh five, no reset, no self-retry.

## Planning Readiness

Ready: root cause, fix shape, files, regressions and typing approach are source-grounded; no human blocker.
