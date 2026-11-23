# Research: issue 1258 new angle (2026-11-23)

Earlier workers (origin/main commits referencing #1258: #1858, #2007, #2078, #2104, #2178, #2296 and others) covered mocked syscall order, strace order, mutation of the parent-sync loop, mount-id boundaries, symlinked and read-only parents, and a live app revision check.

Gap: `test_separate_processes_publish_one_truthful_record` races four real processes only into an existing archive folder. No test races real processes on first publication into a missing nested archive, where `os.makedirs` creates ancestors concurrently and each writer must still confirm through the ancestor syncs.

Angle: one real-process test, no mocks, in `src/core/tests/test_ranking_publication.py`. Test-only, FOCUSED tier.
