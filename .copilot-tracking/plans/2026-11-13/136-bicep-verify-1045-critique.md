# Independent Plan Critique (rubber-duck subagent, one pass)

Verdict: Revise. Findings: (1) offline enforcement for pip build deps / bicep restore; (2) test_public_simulation_startup.py:78 runs Docker when ZF_API_IMAGE set; (3) test_pipeline.py:888 launches API on localhost, needs more than core; (4) editable install/bytecode can write under src/infra; (5) verify copies against commit blobs.

Dispositions (applied directly): (1) pip --no-deps --no-build-isolation, no index access (offline fail is recorded as blocker); bicep build with restore failures recorded, no workaround. (2) unset ZF_API_IMAGE, PATH has no docker use. (3) record test as error/skip if API deps absent; localhost loopback only is tolerated. (4) PYTHONDONTWRITEBYTECODE=1; check git status after and remove untracked egg-info. (5) hash compare to git show blobs.
