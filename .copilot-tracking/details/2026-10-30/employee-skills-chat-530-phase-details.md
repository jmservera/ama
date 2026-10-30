<!-- markdownlint-disable-file -->
# RPI Phase Details: employee-skills-chat-530

## Metadata

* Task ID: 530; slug: employee-skills-chat-530; date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/employee-skills-chat-530-plan.md.
* Research: .copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md.

## Phase Index

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Storage acceptance contract | Complete: four JSON/SQLite cases passed |
| P02 | Local evidence and documentation | Partial: heavy gate lock timeout |
| P03 | Review and local commit | Complete; Review Not accepted; local commit only |

<!-- rpi:phase id=P01 -->
## P01: Storage acceptance contract

<!-- rpi:task id=P01-T01 -->
### P01-T01: Two shared regressions

ChatBehaviour already runs against Store, SqlStore and MssqlChatThreads.
Add two methods only, using its make_store/temp lifecycle. Construct ChatIsolation
with explicit synthetic privacy references and a bounded local model callable.
For each registry skill plus general: cite a permitted case stage, require one
call, verify label, citations and selection; reopen through make_store and
assert persisted question/answer/evidence and chat.answer metadata references,
no question/email duplicate in audit, unchanged case and valid audit chain.
Second method: general no-record sources, unavailable-model fallback and foreign
thread denial for each selection without inference. Existing HTTP matrix proves
role projection; do not imply this test alone establishes all authorization.
Close every opened SQL connection through addCleanup. No schema/runtime changes.
Completion: two methods added; four JSON/SQLite cases pass in 1.840 seconds.
The existing MssqlChatThreads inherits both, but actual SQL execution is blocked.

<!-- rpi:phase id=P02 -->
## P02: Local evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Local gates

Focused selector: core test_chatthreads, API test_chat_panel/isolation/fixture roles.
Then run the caller's exact API discovery PYTHONPATH with Python 3.12 from an
environment containing installed src distributions. Use pip only if missing
dependencies fail. Run owning API/core Ruff/format/mypy. No bytecode/cache output
inside source when avoidable. Browser: existing employee_chat_browser_check with
fresh pinned axe 4.10.3, actual loopback server and blocked external browser traffic.
SQL: existing MssqlChatThreads including new shared tests on one newly created
labelled Docker SQL container, random loopback port and ephemeral memory-only
authentication. Never read or reuse configured database/credential files.
Acquire requested heavy lock; no nested acquisition or duplicate waiting gates.
Record precise exits/skips; no skip counts as real SQL/browser evidence.

PC-001 admission protocol: strip inherited ZF_SQL_*, SQL opt-in and cloud/model
configuration from child environments. Generate a unique issue-specific container
name/ownership token and synthetic password in process memory. Launch foreground
`docker run -i` with a bash entrypoint that reads one password line from stdin,
exports it in process memory and execs sqlservr. Feed that line through a pipe;
never use Docker password environment options, arguments, env files or retained
connection-string logs. Retain only sanitized status/counts.
Inspect only the captured container's ID, ownership label, image ID, loopback
dynamic port, 3 GiB memory and 2 CPU bounds (never full environment).
Assert every identity/binding/bound before SQL readiness; bound readiness to
120 seconds, create a unique synthetic database, then enable ZF_TEST_MSSQL only
in a fresh exact-endpoint child environment. Test timeout 600 seconds. On every
exit remove that exact validated container ID and wait for its launch process;
if ownership is uncertain refuse destructive testing and record SQL blocked.
Observed: one focused heavy-lock wait was cancelled before execution to
consolidate the checks; the replacement full local batch used the requested
flock -w 600 and exited 1 with no output after 600 seconds. No container, browser
or full API suite started; no duplicate gate remained. No retry or foreign
resource use. Four lightweight storage cases and eight focused synthetic HTTP
cases pass; API/core Ruff/format/mypy pass. The explicit-file format diagnostic
bypassed the existing format exclusion and showed baseline formatting too; the
configured component commands pass and unrelated formatting was not changed.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Evidence boundaries

Update only src/api/README.md and canonical new RPI artifacts. External outputs
under a new issue-specific scratch directory, not committed. Keep historical
RV-003 unchanged and distinguish new observations from historical acceptance.
Full publication matrix is blocked because it invokes Azure CLI; do not execute
prohibited commands or fabricate a receipt. Live verification remains unmet.
Completion: API guide and changes record reflect exact local evidence and
unresolved gates. No web source file changed, so fresh changed-web review and
visual redesign are not applicable; rules were fetched at research intake.

<!-- rpi:phase id=P03 -->
## P03: Review and handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: Independent Review and commit

One fresh reviewer receives plan/details/critique/research/changes pointers,
baseline SHA and exact changed files plus external validation paths. It writes
only the review artifact. Route findings to later work, do not loop Review.
Reconcile all current markers and state; commit locally with authenticated
noreply identity and required coauthor trailer. No push/PR/merge. Final response
must map proven versus unproven criteria, and preserve external receipt gap.
Completion: independent Review Complete / Not accepted with RV-001 High.
Local implementation/evidence commit aa127630c4cc9565202015880e1997c71f1f7d44
exists with the required coauthor and authenticated noreply author/committer.
No push. The final metadata commit records this completed handoff; it does not
repeat Review or turn missing gates into passes.
