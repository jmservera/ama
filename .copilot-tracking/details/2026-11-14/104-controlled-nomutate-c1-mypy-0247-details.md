<!-- markdownlint-disable-file -->
# Details: C1 mypy typing correction

* Add `-> None` to all test and setup methods; typed signatures for `call`, `snapshot`, `assert_unchanged`, `new_audit_actions`, `thread`, `invoke_ready`, `review`, `evidence`.
* Declare `provider`, `baseline`, `baseline_audit`, `cookies`, `steps`, `archive`, `extra` types.
* `cast` for Any returns from JSON; `# type: ignore[no-untyped-call]` limited to `ta.Base.setUp`, `ta.Provider.evidence`, `ta.proposal`, `App(...)` and `ScriptedProvider()`.
