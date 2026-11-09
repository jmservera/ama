<!-- markdownlint-disable-file -->
# Issue 189 C4 optional streaming SDK import critique (2026-11-09)

One critique of the final candidate plan, performed by the author as a read-only self-challenge against the brief's constraints (no separate agent). Not repeated for this task.

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | Non-blocking | Dry-run `--sink stdout` no longer needs the SDK, a relaxation of the previous import-time requirement. | Accepted: the stdout sink sends nothing and needs no SDK; the real `iothub` sink and receiver still require it. |
| 2 | Non-blocking | Catching `ModuleNotFoundError` could mask an unrelated missing module inside `iot_stream`. | Accepted: the catch is narrow, scoped to the single import statement, and maps to a fixed code with no success fallback. |
| 3 | Non-blocking | A new fixed code `IOT_SDK_MISSING` adds an output string. | Accepted: it replaces an uncaught import-time traceback; exit code 2 follows existing `StreamError` handling. |
| 4 | Non-blocking | `pyproject.toml` still lists the SDKs as base dependencies. | Reported, not changed: dependency manifests are out of C4 scope and the brief's contract is boot without them. |
