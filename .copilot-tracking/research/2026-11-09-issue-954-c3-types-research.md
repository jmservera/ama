# Research: issue 954 C3 strict mypy on the photo-flag checker (2026-11-09)

Task `issue-954-c3-types`, parent `issue-954-c2-refresh`. Local only: no push, PR, issue, board, live provider, credential, model or spend.

## Disposition

Research executed 2026-11-09 against frozen commit `7aedc68de` (clean, branch `test/demo-photo-validation-954-1109`, published as PR 1315). `origin/main` fetched: `3a9767d5cf728c5e3be76813ce0bfdac4c06841e` (after PR 1240); merge base with the branch `ef28d4da42d83b111d48f14df9b70e3c4932a477`. No validation, merge or source edit has run before this record. Planning Readiness: Ready.

## Correction budget

Standing limit five total scoped correction cycles per issue. C1 and C2 are spent. C3 is authorized by the coordinator within the five total; two remain after C3. This is not an extra grant or a budget reset.

## Evidence

* Hosted `src-ci` API job 129300963449, run 42657722163 (session file `pr1315-api-failure.log`, lines 5323-5328), `mypy` (strict 2.4.0, `files = src tests checks` in `src/api/pyproject.toml`, workflow step `Type check`): 5 errors in 1 file, all in `src/api/checks/photo_flag_stale_browser_check.py`, `checked 200 source files`.
* The checker is in scope for the maintained command. The pinned Ruff check and format passing (C2) did not establish typing; this is a new defect introduced by this workstream (C1 and C2), not a main baseline defect or a flake.
* Error to source mapping on frozen `7aedc68de` (verified by reading the file, not inferred):
  * line 162 `no-any-return`: `return count` in the detector `case()` helper declared `-> int`; `count` is `page.evaluate(...)` (Any).
  * line 214 `no-untyped-call`: `principal(oid=OID_SAM)` in `observe()`; `principal` is the untyped `test_auth.principal` (`src/api/tests/test_auth.py:29`).
  * line 232 `func-returns-value`: `page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))` builds a tuple from the value of `list.append`.
  * line 387 `no-untyped-call` (two errors): `App(store, provider=auth.TrustedProxyProvider(store, ENV))` in `main()`; `App.__init__` (`server.py:75`) and `TrustedProxyProvider.__init__` (`auth.py:104`) are untyped. Those modules, and `test_auth`, are in the pyproject mypy override with `ignore_errors` so their own bodies do not report, but a typed caller still reports untyped calls.
* Prior art (same repository, same CI profile): commit `66ceb71f9` (issue 189 C3, not on main) typed the equivalent calls with module-level `Callable` aliases (`make_provider: Callable[[Store, object], auth.TrustedProxyProvider] = auth.TrustedProxyProvider`, `make_app: Callable[..., server.App] = server.App`, `principal_header: Callable[..., str] = principal`) and typed callbacks, with no `Any`, `cast`, ignore or pyproject change. Reused as a pattern only: the standalone 189 checker is not imported and the unrelated `test_auth` baseline is not edited.
* `expected_denials_browser_check.py` makes the same untyped calls but is not reported in the hosted log; why mypy does not report it is not established here and is not relied on. The C3 reproduction under the CI install profile is the authority.

## Design conclusion

* Line 162: `count = int(page.evaluate("window.__zfDisruptive.length"))`, a real runtime conversion of a JavaScript array length (no cast); the `count == expected` assertion and the return are otherwise unchanged. A non-integer result would now raise instead of failing the comparison, which is the stricter outcome.
* Line 214: module-level alias `principal_header: Callable[..., str] = principal`; call site uses it.
* Line 232: named callback `def on_dialog(dialog: Dialog) -> None` that appends the message then dismisses (same order and effect).
* Line 387: module-level aliases `make_provider` and `make_app` with `Callable` types; call site uses them. Behavior (HTTP server, route fixtures, 503/403 responses, assertions, negative control, detector, owner quiet definition and receipts) is unchanged.
* The other lambdas are not reported and stay unchanged (no broad helper framework).

## Boundaries

Checker only. No product UI or API change, no `pyproject.toml` or CI change, no `Any`, `cast` or `type: ignore` added, no config exclusion. Ordinary `--no-ff` merge of `origin/main` happens after this plan commit; the final source delta against actual main must be the checker plus tracking only. Prior quiet observations remain historical; the new composed source gets fresh bindings.
