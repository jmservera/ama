# Details: issue #228 simulator and canary pin

Phase 1: in test_procurement_screens.py add ContractorJobPack.test_vulnerability_canaries_never_reach_contractor_view (case and order carry CANARY fields; none appear; notice still shown) and NoRoleSimulator.test_screen_sources_have_no_role_simulator_or_self_approval (both screen blocks free of simulator, impersonation, role assignment, approve/accept calls and POST/PUT).
Phase 2: unittest tests.test_procurement_screens (14 pass), ruff check and format, mypy --strict --cache-dir=/tmp/mypy-228.
