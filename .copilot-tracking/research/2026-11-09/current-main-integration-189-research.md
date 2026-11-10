<!-- markdownlint-disable-file -->
# Issue 189 current-main integration research (2026-11-09)

Task `current-main-integration-189`; parent `optional-sdk-189-c4` (C4 evidence head `b933c2f606b394469b53f702824b707e6fc3548d`). Refs #189 only. Research disposition: executed (prospective; read-only inspection, no source change, no merge yet).

## Pinned facts

* Fetched `origin/main` is `3a9767d5cf728c5e3be76813ce0bfdac4c06841e` (`feat(lifecycle): controlled lifecycle integration (#81) (#1240)`), merged 16:50:00Z, 19 hosted checks SUCCESS, issue 81 open. Merge base with this branch is `8d6f029cac004506953f36606862168bbe9d9412` (#1308). Main added `1464b4d85` (#1312 chat-schema SQL selection in `tools/rpi-checks.py`), two rubric score commits and #1240.
* Branch `feat/demo-simulator-control-189-1109`, clean, HEAD `b933c2f60`; published PR 1313 head remains `d381...` (nothing pushed from this lane). Repository-local email `8036360+jmservera@users.noreply.github.com` is set.
* Read-only `git merge-tree --write-tree HEAD origin/main` is clean (exit 0, tree `7f721221a3f3012719fa265833ecdd10a242ee62`). Observation only; no ref or index changed.
* Main's delta since the merge base is 226 files, 6914 insertions. Under `src` it touches only `src/core` (`appointments.py`, `complaints_route.py`, `gates.py`, `procurement.py`, `quality.py`, `resident_decisions.py`, `store.py`, README and tests). It touches no `src/api` file. Under `tools` it touches `rpi-checks.py` (4 lines) and `test_rpi_checks.py` (+48, the 1312 cases).
* This branch's delta against the base touches `src/api` only (13 source/test/check paths, 12 listed in C1-C4 evidence) plus `.copilot-tracking`. There is no file overlap between the two deltas under `src`; `.copilot-tracking` overlap is by name only (main carries its own dated records).

## Composition analysis

* #189 API controls depend on `Store.audit` and core types. #1240 changes `store.py` (17 lines), `quality.py` and gates; the #189 code uses only `store.audit` and the existing `Store` constructor. The diff of `store.py` is read before testing to confirm `audit` is unchanged in signature.
* C4 made `iot_stream` (needs `azure.iot.device`) a lazy import so the SDK-free API base install can boot the server child. The scrubbed-server regression in `tools/test_rpi_checks.py` (`test_api_install_prevents_scrubbed_server_child_writing_source_bytecode`) is the contract; main now adds 1312 cases to that module, which must pass alongside.
* The lifecycle core adds no import of the streaming SDK in `src/core` (grep of the merged tree is part of P4).

## Constraints carried

Historical records untouched: original Functional review and adverse findings, C1 to C4 before/after evidence (C4 before: `ModuleNotFoundError: azure` via `server -> simulator_admin -> live_simulator -> iot_stream`; after: 1 test OK), the older Core/SDK/CI errors, approve 0 on `8ab64519c`, F3 cause UNKNOWN. C1 to C4 are four of five total cycles spent plus a fifth counted in the brief ("C1-C4 spent, ONE of 5 remains"); integration is not a new source correction, grant or reset and consumes no cycle. A new defect or intent ambiguity stops the work with no correction. Owner demo tier: targeted tests, no `rpi-checks --all`, no SQL services, cloud, models, private data, global installs.

## Planning Readiness

Ready. Remaining unknowns are test outcomes, recorded prospectively as P5.
